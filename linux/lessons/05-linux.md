---
layout: default
title: APT, Package Management, and Linux Networking
---

# APT, Package Management, and Linux Networking

## What you will learn

In this lesson you will learn:

1. What a package manager is and why it exists
2. How `apt` works on Debian/Ubuntu (repositories, metadata, dependencies)
3. The most useful `apt` commands for DevOps work
4. Linux networking basics (interfaces, IP, DNS, routing)
5. Common Linux networking commands and what to use them for

---

## 1) How package managers work (the big picture)

### 1.1 The problem package managers solve

On a Linux server you often need to install software like:

- Nginx
- Docker
- Python
- OpenSSH

A package manager solves these problems:

- Downloading software securely
- Installing it in the correct locations
- Installing dependencies (libraries and tools it needs)
- Upgrading and patching
- Removing software cleanly
- Tracking what files belong to what package

### 1.2 Packages, repositories, and metadata

On Debian/Ubuntu:

- A **package** is usually a `.deb` file.
- A **repository** is a server that hosts packages and index metadata.
- `apt` downloads repository metadata (indexes) and uses it to resolve dependencies.

The most important mental model:

- `apt update` downloads the latest package lists (metadata)
- `apt install` uses that metadata to download + install packages

### 1.3 Dependencies (why `apt` is so valuable)

Most software depends on libraries.

When you run:

```bash
sudo apt install nginx
```

`apt` will automatically install the required dependencies so that Nginx works.

### 1.4 Where `apt` reads repository configuration

Common files:

- `/etc/apt/sources.list`
- `/etc/apt/sources.list.d/*.list`

A typical entry looks like:

```
deb http://archive.ubuntu.com/ubuntu jammy main restricted universe multiverse
```

Meaning:

- `deb`: binary packages
- URL: repository mirror
- `jammy`: distribution codename
- components: `main`, `universe`, etc.

---

## 2) APT essentials (commands you’ll actually use)

### 2.1 Update package lists

```bash
sudo apt update
```

If you forget this, you may not see the latest versions.

### 2.2 Install a package

```bash
sudo apt install curl
sudo apt install nginx
```

### 2.3 Remove a package

```bash
sudo apt remove nginx
```

This keeps configuration files in many cases.

### 2.4 Purge (remove including config)

```bash
sudo apt purge nginx
```

### 2.5 Upgrade installed packages

```bash
sudo apt upgrade
```

For a “bigger” upgrade (may remove/install packages):

```bash
sudo apt full-upgrade
```

### 2.6 Search and inspect packages

```bash
apt search nginx
apt show nginx
apt-cache policy nginx
```

### 2.7 Clean up

```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
```

### 2.8 Check what files a package installed

```bash
dpkg -L nginx
```

### 2.9 Find which package owns a file

```bash
dpkg -S /usr/sbin/nginx
```

### 2.10 Hold a package (prevent upgrades)

Useful in production to avoid unexpected upgrades.

```bash
sudo apt-mark hold nginx
sudo apt-mark unhold nginx
```

---

## 3) Security and best practices with apt

### 3.1 Don’t blindly run scripts

Prefer installing from official repositories. If you must use third-party repos, understand what you add.

### 3.2 Know what changed

Before upgrades:

- Take snapshots (VM) or backups
- Read changelogs when possible
- Consider staged rollouts

### 3.3 Reproducibility

In DevOps, the goal is repeatable builds.

- Use IaC/config management (Ansible, Dockerfiles)
- Pin versions when needed
- Document repo additions

---

## 4) Linux networking basics

### 4.1 Interfaces and IP addresses

An interface can be:

- Physical NIC (ethernet)
- Wi-Fi
- Virtual interface (VM, container, VPN)

IP address types:

- IPv4: `192.168.1.10`
- IPv6: `2001:db8::1`

### 4.2 DNS (name resolution)

DNS turns names into IP addresses.

Important files/commands:

- `/etc/resolv.conf` (resolver config; sometimes managed automatically)
- `resolvectl status` (systemd-resolved environments)

### 4.3 Routing

Routing decides how packets leave your machine.

Key concept:

- **default route / gateway**: where traffic goes if not local

---

## 5) Networking commands (what to use and why)

### 5.1 See IP addresses and interfaces

```bash
ip addr
ip link
```

Old command (still common):

```bash
ifconfig
```

### 5.2 Routing table

```bash
ip route
```

### 5.3 Test connectivity

```bash
ping 8.8.8.8
ping google.com
```

If IP ping works but DNS ping fails, your DNS is likely broken.

### 5.4 DNS lookup

```bash
getent hosts google.com
nslookup google.com

dig google.com
```

### 5.5 Check listening ports and services

```bash
ss -tulpen
```

Common patterns:

```bash
ss -tulpen | grep :22
ss -tulpen | grep :80
```

### 5.6 Check active connections

```bash
ss -tunp
```

### 5.7 Download / HTTP testing

```bash
curl -I https://example.com
curl -v https://example.com
```

### 5.8 Tracing the path (where packets go)

```bash
traceroute google.com

# often better on firewalled networks
tracepath google.com
```

### 5.9 Quick bandwidth / throughput checks

Common tools:

- `iperf3` (requires server/client)
- `speedtest-cli` (third-party)

### 5.10 ARP / Neighbor table

```bash
ip neigh
```

### 5.11 Firewall (very common in DevOps)

Depending on distro:

- `ufw status`
- `iptables -L`
- `nft list ruleset`

---

## Practice tasks

1. Update apt metadata, install `curl`, and verify its version
2. Use `apt show` to inspect `nginx`
3. Display your IP address and default route
4. Use `ss` to confirm what ports are listening on your machine
5. Use `dig` or `nslookup` to verify DNS resolution
