#!/usr/bin/env python3
"""
portscanner_safe.py
Threaded TCP "connect" port scanner (safe for CTF / lab use).
- Resolves the target once to avoid socket.gaierror floods.
- Uses a worker pool (queue + threads) instead of creating 65k threads.
- Optional banner grab (-b / --banner).
- Can scan specific ports, ranges, or all ports (use "all").
Usage examples:
  python3 portscanner_safe.py 10.201.28.171 all -t 300 -w 0.8 -b
  python3 portscanner_safe.py example.com 1-1024 -t 150
  python3 portscanner_safe.py 127.0.0.1 22,80,443
"""
import argparse
import socket
import threading
import queue
import time
import sys

DEFAULT_THREADS = 200
DEFAULT_TIMEOUT = 0.8
COMMON_PORTS = [
    21,22,23,25,53,80,110,111,135,139,143,161,389,443,445,465,587,
    636,993,995,1433,1521,1723,2049,2082,2083,2086,2087,2222,2375,3306,
    3389,3690,4444,5000,5432,5900,5985,5986,6000,6379,8000,8008,8080,8443,9001,10000
]

def parse_ports(spec, do_all=False):
    if do_all:
        return list(range(1, 65536))
    if not spec:
        return COMMON_PORTS[:]
    spec = spec.strip()
    ports = set()
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a,b = part.split('-',1)
            ports.update(range(int(a), int(b)+1))
        else:
            ports.add(int(part))
    return sorted(p for p in ports if 1 <= p <= 65535)

def worker(target_ip, q, timeout, do_banner, results, lock, progress, stop_event):
    while not stop_event.is_set():
        try:
            port = q.get_nowait()
        except queue.Empty:
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            err = s.connect_ex((target_ip, port))
            if err == 0:
                banner = ""
                if do_banner:
                    try:
                        s.settimeout(0.7)
                        # send small probe, some services respond
                        try:
                            s.sendall(b"\r\n")
                        except Exception:
                            pass
                        time.sleep(0.12)
                        banner = s.recv(1024).decode(errors='ignore').strip()
                    except Exception:
                        banner = ""
                with lock:
                    results.append((port, banner))
            s.close()
        except KeyboardInterrupt:
            stop_event.set()
            break
        except Exception:
            # ignore other socket errors per port
            pass
        finally:
            with lock:
                progress[0] += 1
            q.task_done()

def print_progress(total, progress, results):
    done = progress[0]
    pct = (done/total)*100 if total else 0
    sys.stdout.write(f"\rScanned {done}/{total} ports ({pct:.1f}%). Open: {len(results)}")
    sys.stdout.flush()

def resolve_target(target):
    try:
        # Try numeric IP first (fast)
        socket.inet_aton(target)
        return target
    except Exception:
        pass
    # otherwise resolve hostname
    try:
        infos = socket.getaddrinfo(target, None, family=socket.AF_INET, type=socket.SOCK_STREAM)
        if not infos:
            raise socket.gaierror
        return infos[0][4][0]
    except socket.gaierror:
        raise

def main():
    parser = argparse.ArgumentParser(description="Threaded TCP connect port scanner (CTF/lab use only)")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("ports", nargs="?", help="Ports: e.g. 1-1024, 22,80 or 'all' for 1-65535 (or omit for common ports)")
    parser.add_argument("-t","--threads", type=int, default=DEFAULT_THREADS, help=f"Worker threads (default {DEFAULT_THREADS})")
    parser.add_argument("-w","--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"Connect timeout seconds (default {DEFAULT_TIMEOUT})")
    parser.add_argument("-b","--banner", action="store_true", help="Attempt to grab small banner from open ports")
    args = parser.parse_args()

    do_all = False
    if args.ports and args.ports.strip().lower() == "all":
        do_all = True

    try:
        target_ip = resolve_target(args.target.strip())
    except Exception:
        print(f"ERROR: Cannot resolve target '{args.target}'. Check the hostname/IP and DNS.", file=sys.stderr)
        return

    ports = parse_ports(args.ports, do_all)
    if not ports:
        print("No valid ports to scan.", file=sys.stderr)
        return

    q = queue.Queue()
    for p in ports:
        q.put(p)

    results = []
    lock = threading.Lock()
    progress = [0]
    stop_event = threading.Event()
    workers = max(1, min(args.threads, len(ports)))
    threads = []

    start_time = time.time()
    for _ in range(workers):
        t = threading.Thread(target=worker, args=(target_ip, q, args.timeout, args.banner, results, lock, progress, stop_event), daemon=True)
        t.start()
        threads.append(t)

    try:
        last_print = 0
        total = len(ports)
        while any(t.is_alive() for t in threads):
            with lock:
                if time.time() - last_print >= 0.5:
                    print_progress(total, progress, results)
                    last_print = time.time()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping workers...")
        stop_event.set()

    q.join()
    end_time = time.time()
    print_progress(len(ports), progress, results)
    print("\n")
    print(f"Scan completed in {end_time - start_time:.2f} seconds.")
    if results:
        results.sort()
        print("Open ports:")
        for port, banner in results:
            if banner:
                print(f"  {port}\t{banner}")
            else:
                print(f"  {port}")
    else:
        print("No open ports found (with the given timeout).")

if __name__ == "__main__":
    main()
