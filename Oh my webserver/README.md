**Tryhackme: Oh My Webserver**

**Enumeration:**

**Rustscan:**

l start with rustscan first for find ports and l found
22(ssh),**80(http)** ports.

<img src="./media/media/image1.png"
style="width:4.80042in;height:1.01676in" />

<img src="./media/media/image2.png"
style="width:2.87525in;height:0.55838in" />

**Nmap:**

After rustscan use nmap for check ports version.

<img src="./media/media/image3.png"
style="width:6.49236in;height:4.21181in" />

**Searchsploit:**

When I searched for the HTTP port version in Searchsploit, I found
**Path Traversal** and **RCE** in **Apache HTTP server
2.4.49**.<img src="./media/media/image4.png"
style="width:6.49236in;height:0.65909in" />

**Metasploit:**

l want use **metasploit** for exploit this vulnerability.We search this
vulnerability in metasploit and we found it .After we found exploit use
**exploit/multi/http/apache_normalize_path_rce** and set options.

<img src="./media/media/image5.png"
style="width:6.5in;height:2.31042in" />

<img src="./media/media/image6.png" style="width:6.5in;height:3in" />

<img src="./media/media/image7.png"
style="width:5.7255in;height:1.09176in" />

Run and get **meterpreter**.

<img src="./media/media/image8.png"
style="width:6.5in;height:1.80208in" />

We use shell command to get shell.

<img src="./media/media/image9.png"
style="width:4.50039in;height:1.06676in" />

I used this command(**python3 -c 'import pty; pty.spawn("/bin/bash")'**)
to get a fully interactive shell so that the username, hostname, and
current directory appear properly in the prompt.

<img src="./media/media/image10.png"
style="width:3.46697in;height:0.38337in" />

l look **/home** directory found the user flag but l can’t find
anything.

<img src="./media/media/image11.png"
style="width:3.59861in;height:1.18194in" />

l use python server for upload linpeas target machine for privileges
escalation.<img src="./media/media/image12.png"
style="width:4.72708in;height:2.68194in" />

l use wget but machine haven’t **wget** after this l use **curl**.

<img src="./media/media/image13.png"
style="width:4.75in;height:0.40139in" />

<img src="./media/media/image14.png"
style="width:6.01528in;height:0.89375in" />

Give permission **linpeas.sh** and run it.

<img src="./media/media/image15.png"
style="width:6.5in;height:4.46944in" />

l found **/usr/bin/python3.7 = cap_setuid+ep** we can use this for
privileges escalation.

<img src="./media/media/image16.png"
style="width:3.13194in;height:0.43056in" />

l go gtfobins for privileges escalations with **python3.7
capabilitites**.

<img src="./media/media/image17.png"
style="width:6.49306in;height:1.84722in" />

l use **python3.7 -c 'import os; os.setuid(0); os.system("/bin/sh")'**
command and we got root and user flag.

<img src="./media/media/image18.png"
style="width:6.02083in;height:0.91667in" />

<img src="./media/media/image19.png"
style="width:6.5in;height:2.32639in" />

We get user flag but we can’t get **root.txt**.l check **/etc/hosts**
and found **172.17.0.2** ip.

<img src="./media/media/image20.png"
style="width:4.53889in;height:1.61736in" />

We have same ip in this machine.**172.17.0.2** is container we must
check **172.17.0.1** ip l use nmap but this machine haven’t nmap and l
built **port-scanner.py** with **ChatGPT** and l upload this port
scanner in target machine and run it we see **5986** port.

<img src="./media/media/image21.png"
style="width:3.30417in;height:1.23472in" />

l use google for searching **5986** port exploit and l found
**CVE-2021-38647** vulnerability.

<img src="./media/media/image22.png"
style="width:6.5in;height:3.86528in" />

<img src="./media/media/image23.png"
style="width:6.5in;height:4.02569in" />

Again l copy **CVE-2021-38647.py** and run first **id** command work it.

<img src="./media/media/image24.png"
style="width:3.37361in;height:0.48681in" />

<img src="./media/media/image25.png"
style="width:3.64375in;height:0.47847in" />

After this l try to get **/root/root.txt** and we got root flag.

<img src="./media/media/image26.png"
style="width:4.8in;height:0.55625in" />
