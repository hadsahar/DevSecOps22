# Bash Networking Commands

Networking commands are essential for Linux administrators, DevOps engineers, cloud engineers, and developers. They help verify connectivity, transfer files, access remote servers, and automate deployments.

---

# `ping` - Test Network Connectivity

## Purpose

Checks whether a host is reachable over the network.

## Syntax

```bash
ping [OPTIONS] HOST
```

---

## Common Flags

### Default Ping

```bash
ping google.com
```

Continuously sends ICMP packets until stopped.

Stop with:

```bash
CTRL + C
```

---

### `-c` (Count)

Send a specific number of packets.

```bash
ping -c 4 google.com
```

Output:

```text
4 packets transmitted
4 received
0% packet loss
```

---

### `-i` (Interval)

Specify time between packets.

```bash
ping -i 2 google.com
```

Send one packet every 2 seconds.

---

### `-s` (Packet Size)

```bash
ping -s 1000 google.com
```

Send larger packets.

---

### `-W` (Timeout)

```bash
ping -W 3 google.com
```

Wait 3 seconds for a reply.

---

# `curl` - Transfer Data from URLs

## Purpose

Used to communicate with APIs, download content, and test web services.

## Syntax

```bash
curl [OPTIONS] URL
```

---

## Common Flags

### Basic Request

```bash
curl https://api.github.com
```

---

### `-I` (Headers Only)

```bash
curl -I https://google.com
```

Output:

```text
HTTP/2 200
content-type: text/html
```

---

### `-v` (Verbose)

```bash
curl -v https://google.com
```

Shows:

* DNS lookup
* TLS handshake
* Request headers
* Response headers

---

### `-L` (Follow Redirects)

```bash
curl -L http://google.com
```

---

### `-o` (Save Output)

```bash
curl -o page.html https://example.com
```

---

### `-O` (Save Using Original Filename)

```bash
curl -O https://example.com/file.zip
```

---

### `-H` (Add Header)

```bash
curl -H "Authorization: Bearer TOKEN" \
https://api.example.com
```

---

### `-X` (HTTP Method)

GET:

```bash
curl -X GET https://api.example.com/users
```

POST:

```bash
curl -X POST https://api.example.com/users
```

DELETE:

```bash
curl -X DELETE https://api.example.com/users/1
```

---

### `-d` (Request Body)

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name":"John"}' \
https://api.example.com/users
```

---

### `-u` (Basic Authentication)

```bash
curl -u admin:password https://example.com
```

---

# `wget` - Download Files

## Purpose

Downloads files from the web.

## Syntax

```bash
wget [OPTIONS] URL
```

---

## Common Flags

### Download File

```bash
wget https://example.com/file.zip
```

---

### `-O` (Rename Download)

```bash
wget -O backup.zip https://example.com/file.zip
```

---

### `-c` (Continue Download)

```bash
wget -c https://example.com/file.zip
```

Resume interrupted downloads.

---

### `-q` (Quiet Mode)

```bash
wget -q https://example.com/file.zip
```

---

### `--limit-rate`

```bash
wget --limit-rate=500k \
https://example.com/file.zip
```

Limit download speed.

---

### Recursive Download

```bash
wget -r https://example.com
```

---

# `ssh` - Secure Shell

## Purpose

Connect to remote servers securely.

## Syntax

```bash
ssh [OPTIONS] USER@HOST
```

---

## Basic Connection

```bash
ssh ubuntu@192.168.1.10
```

---

## Common Flags

### `-p` (Port)

```bash
ssh -p 2222 ubuntu@192.168.1.10
```

---

### `-i` (Private Key)

```bash
ssh -i mykey.pem ubuntu@ec2.amazonaws.com
```

---

### `-v` (Verbose)

```bash
ssh -v ubuntu@server
```

Useful for troubleshooting.

---

### Execute Remote Command

```bash
ssh ubuntu@server "hostname"
```

Output:

```text
web-server-01
```

---

# `scp` - Secure Copy

## Purpose

Copy files between machines using SSH.

## Syntax

```bash
scp [OPTIONS] SOURCE DESTINATION
```

---

## Common Examples

### Upload File

```bash
scp app.py ubuntu@server:/home/ubuntu/
```

---

### Download File

```bash
scp ubuntu@server:/tmp/log.txt .
```

---

### Copy Directory

```bash
scp -r project/ ubuntu@server:/home/ubuntu/
```

---

## Common Flags

### `-r` (Recursive)

```bash
scp -r folder server:/tmp/
```

---

### `-P` (Port)

```bash
scp -P 2222 file.txt user@server:/tmp/
```

---

### `-i` (SSH Key)

```bash
scp -i mykey.pem file.txt \
ubuntu@server:/tmp/
```

---

# `rsync` - Synchronize Files

## Purpose

Efficiently synchronize files and directories.

Unlike `scp`, rsync only transfers changes.

## Syntax

```bash
rsync [OPTIONS] SOURCE DESTINATION
```

---

## Most Common Flags

### `-a` (Archive)

Preserves:

* Permissions
* Ownership
* Symlinks
* Timestamps

```bash
rsync -a project/ backup/
```

---

### `-v` (Verbose)

```bash
rsync -av project/ backup/
```

---

### `-h` (Human Readable)

```bash
rsync -avh project/ backup/
```

---

### `--delete`

Delete files not present in source.

```bash
rsync -av --delete project/ backup/
```

⚠️ Dangerous if used incorrectly.

---

### `-z` (Compress)

```bash
rsync -avz project/ server:/backup/
```

---

### `-P` (Progress)

```bash
rsync -avP project/ server:/backup/
```

Shows:

* Progress bar
* Resume capability

---

## Remote Sync

```bash
rsync -avz project/ \
ubuntu@server:/var/www/html/
```

---

# Practical DevOps Examples

## Check Internet Connectivity

```bash
ping -c 4 8.8.8.8
```

---

## Test API

```bash
curl -I https://api.github.com
```

---

## Download Kubernetes Binary

```bash
wget https://example.com/kubectl
```

---

## Connect to EC2

```bash
ssh -i mykey.pem ubuntu@ec2-host
```

---

## Upload Deployment Files

```bash
scp -r app/ ubuntu@server:/opt/app
```

---

## Synchronize Website

```bash
rsync -avz website/ \
ubuntu@server:/var/www/html/
```

---

# Quick Reference

| Command | Purpose              |
| ------- | -------------------- |
| ping    | Test connectivity    |
| curl    | Transfer data / APIs |
| wget    | Download files       |
| ssh     | Remote login         |
| scp     | Secure file copy     |
| rsync   | Synchronize files    |

---

# Mini Lab

### Step 1 – Test Connectivity

```bash
ping -c 4 google.com
```

---

### Step 2 – Check Website Headers

```bash
curl -I https://google.com
```

---

### Step 3 – Download a File

```bash
wget https://example.com/file.zip
```

---

### Step 4 – Connect to Remote Server

```bash
ssh user@server
```

---

### Step 5 – Upload a File

```bash
scp notes.txt user@server:/tmp/
```

---

### Step 6 – Sync a Directory

```bash
rsync -avP project/ backup/
```
