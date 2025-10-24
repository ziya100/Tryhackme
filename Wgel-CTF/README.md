**Tryhackme: Wgel Ctf**

**Enumeration:**

**Rustscan:**

First one l start with rustscan for check port:

<img src="./media/media/image1.png"
style="width:3.18361in;height:0.35003in" />

We have 2 open port(22,80):

<img src="./media/media/image2.png"
style="width:2.80024in;height:0.60005in" />

**Nmap:**

Lets check ports version with nmap:

<img src="./media/media/image3.png"
style="width:4.52539in;height:0.38337in" />

<img src="./media/media/image4.png"
style="width:5.64216in;height:1.25844in" />

**Searchsploit:**

Okay lets check ssh version with searchsploit:

<img src="./media/media/image5.png"
style="width:2.89192in;height:0.27502in" />

SSH version allows username enumeration**:**

<img src="./media/media/image6.png"
style="width:6.5in;height:1.12292in" />

Let's remember this, it might be necessary.

When we check http server we see apache2 default page.

<img src="./media/media/image7.png"
style="width:6.5in;height:2.66597in" />

Let’s check first source code.When we check source code we see jessie
name in source code.

<img src="./media/media/image8.png"
style="width:4.46705in;height:0.64172in" />

l try brute force with this username to ssh with hydra but l can’t find
password.

**Dirsearch:**

It is time to directory search with dirsearch.

<img src="./media/media/image9.png"
style="width:5.12544in;height:0.30836in" />

We found <u>/sitemap directory.</u>

<img src="./media/media/image10.png"
style="width:4.64207in;height:0.94175in" />

Let’s check it.

<img src="./media/media/image11.png"
style="width:6.5in;height:2.80903in" />

l full check site but l can’t find anything.

Let’s again directory search.

<img src="./media/media/image12.png"
style="width:5.50881in;height:0.50838in" />

We found **/sitemap/.ssh** directory.

<img src="./media/media/image13.png"
style="width:5.70883in;height:1.26678in" />

l check it and found id_rsa.

<img src="./media/media/image14.png"
style="width:4.88376in;height:2.08351in" />

<img src="./media/media/image15.png"
style="width:4.09202in;height:3.64198in" />

Let’s first save this by **id_rsa**,give permission after use this for
connect to ssh with jessie user.

<img src="./media/media/image16.png"
style="width:2.76691in;height:0.43337in" />

<img src="./media/media/image17.png"
style="width:6.5in;height:2.87153in" />

<img src="./media/media/image18.png"
style="width:2.91692in;height:0.51671in" />

<img src="./media/media/image19.png"
style="width:4.56706in;height:1.84183in" />

Successful login and right now check **/home/jessie**.

<img src="./media/media/image20.png"
style="width:2.46688in;height:0.23335in" />

<img src="./media/media/image21.png"
style="width:5.17545in;height:4.04202in" />

When we check Document we find **user_flag.txt.**

<img src="./media/media/image22.png"
style="width:4.33371in;height:0.67506in" />

First we try sudo -l command for privileges escalation.

<img src="./media/media/image23.png"
style="width:6.5in;height:0.76806in" />

We see **/usr/bin/wget** we can use wget for found root flag.We check
gtfobins website.

<img src="./media/media/image24.png"
style="width:6.5in;height:1.69236in" />

Okay use this for read the root flag.

<img src="./media/media/image25.png"
style="width:6.5in;height:0.74306in" />

We found root flag.
