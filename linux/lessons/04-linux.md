---
layout: default
title: Linux Runlevels, Filesystem, and systemctl
---

# Linux Runlevels, Filesystem, and systemctl

## What you will learn

In this lesson you will learn:

1. What “runlevels” are, and how modern Linux uses systemd “targets” instead
2. How Linux organizes files and folders (filesystem layout)
3. How to manage services with `systemctl` (start/stop/enable, logs, troubleshooting)

---

## 1) Runlevels vs systemd targets

### 1.1 The idea: Linux boot modes

Historically, Linux systems used **SysV init**. SysV init defined **runlevels** (numbered modes) that represented “how much of the system is up”.

Modern distributions (Ubuntu, Debian, RHEL, etc.) mostly use **systemd**. systemd uses **targets** instead of runlevels. Targets are named groupings of units (services, mounts, sockets).

The important thing: the concept is the same.

- A runlevel/target is a “boot goal”
- The system starts the required services to reach that goal

### 1.2 Common runlevels (classic SysV)

Typical SysV runlevels:

- `0`  Shutdown
- `1`  Single-user / rescue mode
- `2`  Multi-user mode (varies by distro)
- `3`  Multi-user mode with networking (text UI)
- `4`  Usually unused / custom
- `5`  Multi-user + graphical (GUI)
- `6`  Reboot

On Debian/Ubuntu, the meaning of `2`, `3`, `4`, `5` is often the same (multi-user) and GUI is handled differently.

### 1.3 systemd targets (modern)

systemd targets you will see often:

- `poweroff.target` (similar to runlevel 0)
- `rescue.target` (similar to runlevel 1)
- `multi-user.target` (similar to runlevel 3)
- `graphical.target` (similar to runlevel 5)
- `reboot.target` (similar to runlevel 6)
- `emergency.target` (very minimal environment)

### 1.4 Check the current target

```bash
systemctl get-default
systemctl list-units --type=target
systemctl list-units --type=target --state=active
```

### 1.5 Change the default boot target

For a server you usually want `multi-user.target` (no GUI).

```bash
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target
```

### 1.6 Switch targets (without reboot)

```bash
sudo systemctl isolate multi-user.target
sudo systemctl isolate graphical.target
sudo systemctl isolate rescue.target
```

`isolate` will stop units that are not part of the target and start required ones.

---

## 2) Linux filesystem: files and folders

Linux uses a single directory tree that starts at the root directory: `/`.

### 2.1 Everything is a file

A key Linux concept:

- Regular files are files
- Directories are special files
- Devices are represented as files (e.g. `/dev/sda`)
- Many system interfaces are files (e.g. `/proc`, `/sys`)

This design makes automation and scripting easier.

### 2.2 Important directories (high value for DevOps)

#### `/`
The root of the entire filesystem.

#### `/bin` and `/usr/bin`
Essential user commands:

- Examples: `ls`, `cp`, `mv`, `cat`, `grep`

On many distros, `/bin` may be a symlink to `/usr/bin`.

#### `/sbin` and `/usr/sbin`
System/admin commands (often require root):

- Examples: `ip`, `iptables`, `useradd`, `systemctl` (location varies)

#### `/etc`
System configuration.

- Service configs (e.g. `sshd_config`)
- Network configs
- Users/groups: `/etc/passwd`, `/etc/group`, `/etc/shadow`

Rule: treat `/etc` as critical. Back it up and change it carefully.

#### `/var`
Variable data that changes over time.

- Logs: `/var/log`
- Package cache (distro-specific)
- Spool directories (mail, printing)

#### `/home`
User home directories.

- Example: `/home/ubuntu`, `/home/hothaifa`

#### `/root`
Home directory of the root user.

#### `/tmp`
Temporary files. Usually cleaned automatically.

#### `/dev`
Device files.

#### `/proc` and `/sys`
Pseudo-filesystems exposing kernel and process information.

- `/proc/cpuinfo`, `/proc/meminfo`

### 2.3 How to explore the filesystem safely

```bash
pwd
ls -la
cd /etc
ls

# Find files
find /etc -maxdepth 2 -type f | head

# Locate a command
which systemctl
whereis systemctl
```

### 2.4 Permissions and ownership (quick recap)

```bash
ls -l

# change owner/group
sudo chown user:group file

# change permissions
chmod 644 file
chmod 755 script.sh
```

---

## 3) Managing services with systemctl

systemd manages “units”. The most common unit type is a **service**.

### 3.1 Service lifecycle commands

```bash
# start/stop/restart
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx

# reload (if supported)
sudo systemctl reload nginx

# status
systemctl status nginx
```

### 3.2 Enable vs start (common confusion)

- `start` means: start now
- `enable` means: start automatically at boot

```bash
sudo systemctl enable nginx
sudo systemctl disable nginx

# enable and start now
sudo systemctl enable --now nginx
```

### 3.3 List services

```bash
systemctl list-units --type=service --state=running
systemctl list-units --type=service
systemctl list-unit-files --type=service
```

### 3.4 Logs with journalctl

If something fails, check logs.

```bash
# logs for a service
journalctl -u nginx

# follow logs live
journalctl -u nginx -f

# last 100 lines
journalctl -u nginx -n 100

# logs since boot
journalctl -u nginx -b
```

### 3.5 Troubleshooting a failing service

1. Check status

```bash
systemctl status nginx
```

2. Check logs

```bash
journalctl -u nginx -n 200 --no-pager
```

3. Validate configuration (service-specific)

- Nginx: `nginx -t`
- Apache: `apachectl configtest`

4. Confirm ports

```bash
ss -tulpen | grep -E ':(80|443)'
```

### 3.6 Unit file locations (useful for DevOps)

Common locations:

- `/etc/systemd/system/` (custom overrides, your own units)
- `/lib/systemd/system/` or `/usr/lib/systemd/system/` (packaged units)

After editing unit files:

```bash
sudo systemctl daemon-reload
sudo systemctl restart your-service
```

---

## Practice tasks

1. Find your default target and list active targets
2. Switch to `multi-user.target` (if you’re on a VM)
3. Pick any service (e.g. `ssh`) and:
   - view status
   - restart it
   - check its logs
4. Find where its unit file is located
