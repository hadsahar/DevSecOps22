# System Monitoring Commands in Bash

System monitoring commands help administrators, DevOps engineers, and developers understand what is happening on a Linux system in real time.

---

# `ps` - Process Status

## Purpose

Displays information about currently running processes.

## Syntax

```bash
ps [OPTIONS]
```

---

## Common Flags

### `ps`

Show processes running in the current terminal.

```bash
ps
```

Example Output:

```text
PID TTY          TIME CMD
2451 pts/0    00:00:00 bash
2510 pts/0    00:00:00 ps
```

---

### `ps -e`

Show all processes.

```bash
ps -e
```

---

### `ps -ef`

Full detailed view of all processes.

```bash
ps -ef
```

Output:

```text
UID       PID   PPID  CMD
root        1      0  /sbin/init
student  2541   2451  python app.py
```

---

### `ps aux`

Most commonly used option.

```bash
ps aux
```

Shows:

* User
* PID
* CPU %
* Memory %
* Command

---

### Search Specific Process

```bash
ps aux | grep nginx
```

---

### Process Tree

```bash
ps -ef --forest
```

Example:

```text
systemd
 ├─ sshd
 ├─ nginx
 └─ docker
```

---

# `top` - Real-Time Process Monitor

## Purpose

Displays live system activity.

## Syntax

```bash
top
```

---

## Common Actions Inside top

| Key | Action         |
| --- | -------------- |
| q   | Quit           |
| P   | Sort by CPU    |
| M   | Sort by Memory |
| k   | Kill Process   |
| h   | Help           |
| 1   | Show CPU Cores |

---

## Useful Options

### Refresh Every 2 Seconds

```bash
top -d 2
```

---

### Show Specific User

```bash
top -u student
```

---

### Batch Mode

Useful for scripts.

```bash
top -b -n 1
```

---

# `df` - Disk Free Space

## Purpose

Shows filesystem disk usage.

## Syntax

```bash
df [OPTIONS]
```

---

## Common Flags

### Human Readable

```bash
df -h
```

Output:

```text
Filesystem      Size Used Avail Use%
/dev/sda1       100G 45G 55G 45%
```

---

### Show Filesystem Type

```bash
df -Th
```

Output:

```text
Filesystem Type Size Used Avail Use%
ext4       ext4 100G 45G 55G 45%
```

---

### Specific Path

```bash
df -h /home
```

---

### Inodes

```bash
df -i
```

---

# `du` - Directory Usage

## Purpose

Shows how much space files and directories consume.

## Syntax

```bash
du [OPTIONS]
```

---

## Common Flags

### Human Readable

```bash
du -h
```

---

### Summary Only

```bash
du -sh project/
```

Output:

```text
1.2G project/
```

---

### Show All Subdirectories

```bash
du -h project/
```

---

### Maximum Depth

```bash
du -h --max-depth=1
```

Output:

```text
200M logs
1.5G docker
500M backups
```

---

### Sort Largest Directories

```bash
du -h --max-depth=1 | sort -hr
```

---

# `free` - Memory Usage

## Purpose

Displays RAM and swap usage.

## Syntax

```bash
free [OPTIONS]
```

---

## Common Flags

### Human Readable

```bash
free -h
```

Output:

```text
              total used free
Mem:           16Gi  8Gi  6Gi
Swap:           2Gi 500Mi
```

---

### Show Every 2 Seconds

```bash
free -s 2
```

---

### Display in MB

```bash
free -m
```

---

### Display in GB

```bash
free -g
```

---

# `kill` - Terminate Processes

## Purpose

Stops running processes.

## Syntax

```bash
kill SIGNAL PID
```

---

## Find PID

```bash
ps aux | grep nginx
```

Example:

```text
root 2451 nginx
```

PID:

```text
2451
```

---

## Common Signals

### SIGTERM (15)

Graceful shutdown.

```bash
kill 2451
```

Equivalent:

```bash
kill -15 2451
```

---

### SIGKILL (9)

Force termination.

```bash
kill -9 2451
```

⚠️ Process cannot clean up resources.

---

### SIGHUP (1)

Reload configuration.

```bash
kill -1 2451
```

Used by:

* Nginx
* Apache
* HAProxy

---

### Kill Multiple Processes

```bash
kill 1234 5678 9999
```

---

### Kill by Name

```bash
pkill nginx
```

---

### Kill All Matching Processes

```bash
killall nginx
```

---

# `uptime` - System Uptime

## Purpose

Shows how long the system has been running.

## Syntax

```bash
uptime
```

Example:

```text
10:45:00 up 15 days, 4:32, 2 users, load average: 0.32, 0.41, 0.35
```

---

## What Does It Mean?

```text
up 15 days
```

System has been running for 15 days.

---

```text
2 users
```

Two users are logged in.

---

```text
load average
```

CPU workload over:

* 1 minute
* 5 minutes
* 15 minutes

Example:

```text
0.32 0.41 0.35
```

Low system load.

---

# Practical DevOps Examples

## Find High CPU Processes

```bash
ps aux --sort=-%cpu | head
```

---

## Find High Memory Processes

```bash
ps aux --sort=-%mem | head
```

---

## Watch Logs Live

```bash
tail -f /var/log/syslog
```

---

## Check Disk Usage

```bash
df -h
```

---

## Find Large Directories

```bash
du -h --max-depth=1 | sort -hr
```

---

## Monitor Memory

```bash
watch free -h
```

---

## Kill a Stuck Application

```bash
ps aux | grep python

kill -9 PID
```

---

# Quick Reference

| Command | Purpose                   |
| ------- | ------------------------- |
| ps      | Show processes            |
| top     | Real-time process monitor |
| df      | Disk space usage          |
| du      | Directory size usage      |
| free    | Memory usage              |
| kill    | Terminate processes       |
| uptime  | System uptime             |

---

# Mini Lab

Run the following commands:

```bash
ps aux

top

free -h

df -h

du -sh ~

uptime

sleep 300 &
ps aux | grep sleep

kill %1
```