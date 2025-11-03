**Tryhackme: Wonderland**

**Enumeration:**

**Rustscan:**

l started enumeration with **rustscan** and found two open
port **22**(**http**) and **80**(**ssh**).

<img src="./media/media/image1.png"
style="width:6.5in;height:3.57083in" />

**Nmap:**

After **rustscan** l go with **nmap** for found ports version.

<img src="./media/media/image2.png"
style="width:3.60031in;height:0.55005in" />

<img src="./media/media/image3.png"
style="width:6.5in;height:0.99444in" />

There were no known vulnerabilities in the versions of the two services.

I decided to check the HTTP service. The webpage showed the phrase
*“Follow the White Rabbit”* and one photo.

<img src="./media/media/image4.png"
style="width:6.5in;height:1.03125in" />

<img src="./media/media/image5.png"
style="width:6.1422in;height:5.27546in" />

l decided to check **source code** but l can’t find anything.

<img src="./media/media/image6.png"
style="width:6.5in;height:2.77986in" />

After check source code l decided check photos **metadata** with
**steghide**. I run **steghide extract -sf white_rabbit_1.jpg**. The
tool prompted for a **passphrase**.I pressed **Enter** to submit an
empty passphrase and observed that the file had no passphrase set and we
found **hint.txt**.Let’s check **hint.txt**.

<img src="./media/media/image7.png"
style="width:3.35029in;height:0.70839in" />

<img src="./media/media/image8.png"
style="width:3.14194in;height:0.56672in" />

Maybe this “*follow the r a b b i t*” is real hint l we must don’t
forget this message.

**Dirsearch:**

Let’s check directorys with **dirsearch**.

<img src="./media/media/image9.png"
style="width:6.5in;height:2.2125in" />

We have important two directory **/poem** and **/r**.l check first
**/poem** directory.We see just poem.

<img src="./media/media/image10.png"
style="width:6.5in;height:3.55139in" />

l check again source code l again we found nothing after l go to check
**/r** directory.

<img src="./media/media/image11.png"
style="width:6.5in;height:2.53542in" />

We see “*Keep Going*” and “*Would you tell me, please, which way I ought
to go from here?*”

Okay go again directory search.

<img src="./media/media/image12.png"
style="width:6.5in;height:1.11597in" />

We found **/r/a** directory and **/r/a** again say keep going maybe we
must check **/r/a/b/b/i/t** directory because l remember **hint.txt**
say follow the **r a b b i t.** l check **/r/a/b/b/i/t** directory yes
we found it.

<img src="./media/media/image13.png"
style="width:6.5in;height:3.56597in" />

Again message and photo l check this photo **metadata** maybe again some
secret things but it wants passphrase.

After this l decided check source code and l found **user** and
**pass**.

<img src="./media/media/image14.jpeg"
style="width:6.5in;height:2.64931in" />

l use this **user** and **pass** for the connect **ssh**.

<img src="./media/media/image15.png"
style="width:5.60882in;height:4.30871in" />

When l look file found **root.txt** but l didn’t have permission to
read.

<img src="./media/media/image16.png"
style="width:5.05044in;height:2.3002in" />

We see **walrus_and_the_carpenter.py.**l check this python file and we
see python code about **poem** and we see **random** library.

<img src="./media/media/image17.png"
style="width:6.26721in;height:4.30871in" />

<img src="./media/media/image18.png"
style="width:5.50048in;height:4.29204in" />

After this l use **sudo -l** command for look user privileges.

<img src="./media/media/image19.png"
style="width:6.5in;height:1.03403in" />

The target script runs as the user **rabbit**. Python searches the
script’s directory before the standard library when importing modules,
so a local **random.py** will shadow the builtin. I created a local
**random.py** containing **import os; os.system("/bin/bash");** when
**walrus_and_the_carpenter.py** imported random, the code executed and
spawned a Bash shell running with Rabbit’s privileges.

<img src="./media/media/image20.png"
style="width:2.93333in;height:0.54167in" />

<img src="./media/media/image21.png"
style="width:6.5in;height:2.81389in" />

<img src="./media/media/image22.png"
style="width:6.18333in;height:0.525in" />

After we got rabbit shell l check **/home/rabbit** and l see
**teaParty** file.

<img src="./media/media/image23.png"
style="width:5.41667in;height:2.05833in" />

l upload this file my own linux and use strings command for read
human-readable strings in file.

<img src="./media/media/image24.png"
style="width:4.72917in;height:0.6875in" />

<img src="./media/media/image25.png"
style="width:6.5in;height:0.83611in" />

<img src="./media/media/image31.png"
style="width:6.5in;height:4.63333in" />

l found **/bin/echo -n ‘Probably by ‘ && date –date=’next hour’-R**.This is same thing with when we use alice user to go rabbit user.l
create date file and write **bash script**,**permission** and **export**
**path**)

<img src="./media/media/image32.png"
style="width:5.60417in;height:1.10417in" />

<img src="./media/media/image33.png"
style="width:6.5in;height:2.7125in" />

<img src="./media/media/image34.png"
style="width:6.5in;height:1.02361in" />

Okay when we run **teaParty** file we must get **hatter** user shell.

<img src="./media/media/image35.png"
style="width:4.09375in;height:1.15625in" />

Yes we get **habbit** user shell.

I examined the **/home/hatter** directory and found a file containing
the hatter user's password. I then executed **su hatter** and entered
the discovered password to obtain a full login shell with hatter's
privileges.

<img src="./media/media/image36.png"
style="width:5.0625in;height:1.75in" />

<img src="./media/media/image37.png"
style="width:4.86389in;height:0.58333in" />

<img src="./media/media/image38.png"
style="width:3.22528in;height:0.68339in" />

l search suid binaries with **find / -perm -4000 -type f 2\>/dev/null**
but l can’t find any useful vector.l decided check capabilities with
**getcap -r / 2\>/dev/null** and l found **perl** capabilities.

<img src="./media/media/image39.png"
style="width:4.27537in;height:3.09193in" />

<img src="./media/media/image40.png"
style="width:3.09193in;height:0.85007in" />

We can use this **perl** capabilities for privileges escalation.l go to
[gtfobins](https://gtfobins.github.io/) and find **perl capabilities**.We can use this for privileges
escalation.

<img src="./media/media/image41.png"
style="width:6.5in;height:1.98056in" />

<img src="./media/media/image42.png"
style="width:6.5in;height:1.63056in" />

We use **/usr/bin/perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec
"/bin/sh";'** command we get **root** user and found **user** and
**root** flag.

<img src="./media/media/image43.png"
style="width:6.5in;height:2.62986in" />
