#!/bin/bash
# =============================================================================
# Exercise file generator — called by generate_data.sh
# Writes all exercise.md and HARD_CHALLENGE.md files
# =============================================================================
BASE="${1:-/home/student/labs}"

# ─── NAVIGATION/LS ────────────────────────────────────────────────────────────
cat > "$BASE/navigation/ls/exercise.md" <<'EXEOF'
# Exercise: ls — List Directory Contents
## Working directory: ~/labs/navigation/data/

### Ex 1 — Basic listing
```bash
ls ~/labs/navigation/data/
```

### Ex 2 — Show hidden files  (files starting with .)
```bash
ls -a ~/labs/navigation/data/
```
**Q:** How many hidden files are there?

### Ex 3 — Long listing (permissions, owner, size, date)
```bash
ls -la ~/labs/navigation/data/
```
**Q:** What permissions does `large_file.bin` have?

### Ex 4 — Human-readable sizes, sorted by size (largest first)
```bash
ls -lhS ~/labs/navigation/data/
```

### Ex 5 — Recursive listing of a subdirectory
```bash
ls -lR ~/labs/navigation/data/projects/
```

### Ex 6 — Show directories only
```bash
ls -d ~/labs/navigation/data/*/
```
EXEOF

cat > "$BASE/navigation/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Navigation Mastery

### Challenge 1
Navigate to `~/labs/navigation/data/archive/2024` and list its contents recursively with human-readable sizes. Save the output to `~/labs/navigation/data/tree_report.txt`.

### Challenge 2
Count the total number of **files** (not directories) under `~/labs/navigation/data/` recursively.  
Hint: combine `ls -lR` + `grep "^-"` + `wc -l`

### Challenge 3
Write a one-liner that: prints the current directory, moves into `projects/python`, prints that directory, then returns to where it started — without using `cd ~`.

### Challenge 4
Find all hidden files under `~/labs/navigation/data/` and save only their **filenames** (not full paths) to `hidden_list.txt`.
EXEOF

# ─── NAVIGATION/CD ────────────────────────────────────────────────────────────
cat > "$BASE/navigation/cd/exercise.md" <<'EXEOF'
# Exercise: cd — Change Directory

### Ex 1 — Absolute path
```bash
cd ~/labs/navigation/data/archive/2024/jan
pwd
```

### Ex 2 — Relative path
From `~/labs/navigation/data/` navigate into `projects/devops` using a relative path.

### Ex 3 — Go up one level
```bash
cd ..
```

### Ex 4 — Jump to home
```bash
cd ~
```

### Ex 5 — Toggle between two dirs with `cd -`
```bash
cd ~/labs/navigation/data/logs
cd ~/labs/navigation/data/archive/2024/feb
cd -    # back to logs
cd -    # back to feb
```
**Q:** What does `cd -` print each time?
EXEOF

# ─── NAVIGATION/PWD ───────────────────────────────────────────────────────────
cat > "$BASE/navigation/pwd/exercise.md" <<'EXEOF'
# Exercise: pwd — Print Working Directory

### Ex 1
```bash
cd ~/labs/navigation/data/archive/2024/feb
pwd
```

### Ex 2 — Capture in a variable
```bash
MYPATH=$(pwd)
echo "I am at: $MYPATH"
```

### Ex 3 — Subshell test
```bash
(cd /etc && pwd)
pwd
```
**Q:** Does the parent shell's directory change?
EXEOF

# ─── TEXT/ECHO ────────────────────────────────────────────────────────────────
cat > "$BASE/text/echo/exercise.md" <<'EXEOF'
# Exercise: echo — Display Text

### Ex 1
```bash
echo "Hello, DevOps!"
```

### Ex 2 — Write to file (overwrite)
```bash
echo "Welcome to Linux" > greeting.txt
```

### Ex 3 — Append to file
```bash
echo "Automation is power" >> greeting.txt
```

### Ex 4 — Variable interpolation
```bash
NAME="DevOps Student"
echo "My name is $NAME"
```

### Ex 5 — Multiline with \n
```bash
echo -e "Line one\nLine two\nLine three"
```

### Ex 6 — Suppress trailing newline
```bash
echo -n "Hello "; echo "World"
```

### Ex 7 — Command substitution
```bash
echo "User: $(whoami) | Date: $(date +%Y-%m-%d) | Dir: $(pwd)"
```
EXEOF

cat > "$BASE/text/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Text Tools Mastery

### Challenge 1 — System Snapshot
Using ONLY `echo` with command substitution, create `~/labs/text/snapshot.txt` containing:
- Hostname, current user, date/time, working directory, number of files in /etc  
All neatly labeled: `"Hostname: myserver"`

### Challenge 2
Using `cat` + heredoc, append a "Notes" section to `snapshot.txt` with 3 automation tips.

### Challenge 3
Create files `report_01.txt` through `report_10.txt` using `touch` + a loop.  
Merge all of them into `all_reports.txt` using `cat` with a wildcard.

### Challenge 4
Display `all_reports.txt` with line numbers and save the numbered version to `all_reports_numbered.txt`.
EXEOF

# ─── TEXT/CAT ─────────────────────────────────────────────────────────────────
cat > "$BASE/text/cat/exercise.md" <<'EXEOF'
# Exercise: cat — Concatenate & Display Files
## Files: part1.txt  part2.txt

### Ex 1
```bash
cat part1.txt
```

### Ex 2 — Line numbers
```bash
cat -n part1.txt
```

### Ex 3 — Concatenate two files
```bash
cat part1.txt part2.txt
```

### Ex 4 — Merge into new file
```bash
cat part1.txt part2.txt > combined.txt
```

### Ex 5 — Append
```bash
cat part2.txt >> part1.txt
```

### Ex 6 — Create with heredoc
```bash
cat > notes.txt <<EOF
Note 1: study grep
Note 2: practice awk
Note 3: automate everything
EOF
```

### Ex 7 — Show end-of-line markers
```bash
cat -A combined.txt
```
EXEOF

# ─── TEXT/TOUCH ───────────────────────────────────────────────────────────────
cat > "$BASE/text/touch/exercise.md" <<'EXEOF'
# Exercise: touch — Create Files & Update Timestamps

### Ex 1
```bash
touch empty.log
ls -l empty.log
```

### Ex 2 — Multiple at once
```bash
touch a.txt b.txt c.txt
```

### Ex 3 — Loop
```bash
for i in {1..5}; do touch log_$i.txt; done
```

### Ex 4 — Update timestamp
```bash
touch empty.log
ls -l empty.log
```
**Q:** Did the timestamp change?

### Ex 5 — Set specific timestamp
```bash
touch -t 202401150900 a.txt
ls -l a.txt
```
EXEOF

# ─── GREP ─────────────────────────────────────────────────────────────────────
cat > "$BASE/grep/exercise.md" <<'EXEOF'
# Exercise: grep — Search & Filter Text
## Files: access.log  emails.txt  code_sample.py

### Ex 1 — Basic
```bash
grep "ERROR" access.log
```

### Ex 2 — Case-insensitive
```bash
grep -i "error" access.log
```

### Ex 3 — Invert match
```bash
grep -v "INFO" access.log
```

### Ex 4 — Count matches
```bash
grep -c "ERROR" access.log
```

### Ex 5 — Show line numbers
```bash
grep -n "WARNING" access.log
```

### Ex 6 — Context (2 lines after match)
```bash
grep -A 2 "ERROR" access.log
```

### Ex 7 — Search all files in directory
```bash
grep "admin" ~/labs/grep/*
```

### Ex 8 — Recursive search
```bash
grep -r "DevOps" ~/labs/
```

### Ex 9 — Regex: find gmail addresses
```bash
grep "@gmail\.com" emails.txt
```

### Ex 10 — Extract matching part only
```bash
grep -oE "[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]+" emails.txt
```

### Ex 11 — OR pattern with -E
```bash
grep -E "ERROR|WARNING" access.log
```

### Ex 12 — Count unique IPs with failed login
```bash
grep "Login failed" access.log | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c
```

### Ex 13 — Conditional alert
```bash
grep -q "ERROR" access.log && echo "ALERT: errors found!" || echo "All clear"
```
EXEOF

cat > "$BASE/grep/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — grep Mastery

### Challenge 1 — Log Security Audit
From `access.log`:
1. Extract unique IPs that had "Login failed"
2. Count attempts per IP
3. Print only IPs with MORE than 1 attempt
4. Save to `suspicious_ips.txt`

### Challenge 2 — Email Domain Report
From `emails.txt`:
1. Find duplicate email addresses
2. Extract the domain of every unique email
3. Count emails per domain
4. Save sorted by count (highest first) to `domain_report.txt`

### Challenge 3 — Code Security Audit
From `code_sample.py`:
1. Find all function definitions (`def `)
2. Find all TODO comments
3. Find hardcoded passwords/secrets
4. Save `security_report.txt` with line numbers for all findings

### Challenge 4 — Log Summary Script
Write a bash script that reads `access.log` and prints:
```
Total lines:    12
ERROR count:    4
WARNING count:  2
INFO count:     6
```
Then alerts "CRITICAL: 3+ errors!" if ERROR count >= 3.
EXEOF

# ─── AWK ──────────────────────────────────────────────────────────────────────
cat > "$BASE/awk/exercise.md" <<'EXEOF'
# Exercise: awk — Field Processing
## Files: employees.csv  server_stats.txt

### Ex 1 — Print columns
```bash
awk -F',' 'NR>1 {print $2, $3}' employees.csv
```

### Ex 2 — Custom format
```bash
awk -F',' 'NR>1 {print $2 " works in " $3}' employees.csv
```

### Ex 3 — Filter by value
```bash
awk -F',' '$3 == "DevOps" {print $2}' employees.csv
```

### Ex 4 — Numeric comparison
```bash
awk -F',' 'NR>1 && $4 > 7000 {print $2, $4}' employees.csv
```

### Ex 5 — Sum a column
```bash
awk -F',' 'NR>1 {total += $4} END {print "Total salaries:", total}' employees.csv
```

### Ex 6 — Count per department
```bash
awk -F',' 'NR>1 {count[$3]++} END {for (d in count) print d, count[d]}' employees.csv
```

### Ex 7 — Average salary
```bash
awk -F',' 'NR>1 {sum+=$4; n++} END {printf "Avg salary: %.0f\n", sum/n}' employees.csv
```

### Ex 8 — Add line numbers
```bash
awk -F',' 'NR>1 {print NR-1 ". " $2 " - " $3}' employees.csv
```

### Ex 9 — Flag high-CPU servers
```bash
awk '{split($2,a,"="); split(a[2],b,"%"); if(b[1]+0 > 60) print $1, "HIGH CPU:", $2}' server_stats.txt
```

### Ex 10 — BEGIN/END blocks
```bash
awk -F',' 'BEGIN{print "=== Report ==="} NR>1{print $2,$3,$4} END{print "=== End ==="}' employees.csv
```
EXEOF

cat > "$BASE/awk/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — awk Mastery

### Challenge 1 — Department Salary Report
Produce a formatted table with: Department | Headcount | Total Salary | Avg Salary  
All departments, sorted alphabetically.

### Challenge 2 — Server Health Check
From `server_stats.txt`:
- Parse cpu, mem, disk for each server
- Flag any metric > 80% as WARN
- Print: `server | cpu | mem | disk` status
- Summary: total servers, number with ≥1 WARN

### Challenge 3 — CSV to HTML Table
Convert `employees.csv` into a valid HTML `<table>` and save as `report.html`

### Challenge 4 — Top Earner per City
From `employees.csv`, find the highest-paid employee per city:
```
City: TelAviv | Top Earner: David | Salary: 8100
```
EXEOF

# ─── SED ──────────────────────────────────────────────────────────────────────
cat > "$BASE/sed/exercise.md" <<'EXEOF'
# Exercise: sed — Stream Editor
## Files: config.ini  template.html

### Ex 1 — Basic substitution (preview only)
```bash
sed 's/localhost/10.0.0.1/g' config.ini
```

### Ex 2 — Edit in-place
```bash
sed -i 's/changeme123/SecurePass!/g' config.ini
grep "password" config.ini
```

### Ex 3 — Delete blank lines
```bash
sed '/^$/d' config.ini
```

### Ex 4 — Delete lines matching pattern
```bash
sed '/debug/d' config.ini
```

### Ex 5 — Print line range
```bash
sed -n '1,5p' config.ini
```

### Ex 6 — Print matching lines
```bash
sed -n '/port/p' config.ini
```

### Ex 7 — Insert line before match
```bash
sed '/db_name/i # Production database' config.ini
```

### Ex 8 — Append line after match
```bash
sed '/log_level/a # end of web section' config.ini
```

### Ex 9 — Multi-expression template substitution
```bash
sed -e 's/TITLE_PLACEHOLDER/DevOps Dashboard/' \
    -e 's/USERNAME/student/' \
    -e 's/USER_ROLE/engineer/' \
    -e 's/ENV_NAME/production/' \
    -e 's/APP_VERSION/2.1.0/' template.html
```

### Ex 10 — Replace port numbers with regex
```bash
sed 's/port=[0-9]*/port=9999/g' config.ini
```
EXEOF

cat > "$BASE/sed/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — sed Mastery

### Challenge 1 — Config Deployer Script
Write a script that takes `config.ini`, creates `config.prod.ini`, and:
- Replaces all `localhost` with `$DB_HOST` (use env var)
- Sets `debug=false`
- Removes blank lines
- Prepends `# Auto-generated by deploy.sh` as line 1

### Challenge 2 — Log Sanitizer
Create `dirty.log` with lines like `password=abc123` and `token=xyz789`.  
Write a sed one-liner that replaces all values after `password=` or `token=` with `***REDACTED***` and saves to `clean.log`.

### Challenge 3 — Batch replace in multiple files
Using a loop + sed, replace `INFO` with `DEBUG` in every `.log` file under `~/labs/grep/` and save each as `.debug.log`.

### Challenge 4 — CSV Column Prefix
Using sed, prefix every salary value in `employees.csv` with `USD ` (e.g. `7500` → `USD 7500`). Do not modify any other columns.
EXEOF

# ─── CUT ──────────────────────────────────────────────────────────────────────
cat > "$BASE/cut/exercise.md" <<'EXEOF'
# Exercise: cut — Extract Fields
## Files: passwd_sample.txt  services.csv

### Ex 1 — Extract usernames (field 1, delimiter :)
```bash
cut -d':' -f1 passwd_sample.txt
```

### Ex 2 — Multiple fields
```bash
cut -d':' -f1,6 passwd_sample.txt
```

### Ex 3 — Field range
```bash
cut -d':' -f1-4 passwd_sample.txt
```

### Ex 4 — CSV: name + port
```bash
cut -d',' -f1,2 services.csv
```

### Ex 5 — Skip header
```bash
tail -n +2 services.csv | cut -d',' -f1,4
```

### Ex 6 — Cut by character position
```bash
cut -c1-10 passwd_sample.txt
```

### Ex 7 — Pipeline: ports of running services
```bash
grep "running" services.csv | cut -d',' -f2
```

### Ex 8 — Extract domain from email
```bash
echo "user@devops.example.com" | cut -d'@' -f2
```

### Ex 9 — Extract shell for every user
```bash
cut -d':' -f7 passwd_sample.txt
```
EXEOF

cat > "$BASE/cut/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — cut Mastery

### Challenge 1 — User Report
From `passwd_sample.txt`, print a clean table:
```
Username     UID    Shell
--------     ---    -----
root         0      /bin/bash
...
```
Only show users whose shell is `/bin/bash`.

### Challenge 2 — Service Port Map
From `services.csv`, format **running** services:
```
nginx       -> 80/TCP
postgres    -> 5432/TCP
```

### Challenge 3 — Live /etc/passwd extraction
Extract all users with UID >= 1000, show username/UID/home, sort by UID, save to `real_users.txt`.

### Challenge 4 — Log field extraction
Given log format: `"2024-01-15 08:01:32 ERROR [auth] message"`  
Use `cut` to extract separately: date, time, and log level.
EXEOF

# ─── SORT ─────────────────────────────────────────────────────────────────────
cat > "$BASE/sort/exercise.md" <<'EXEOF'
# Exercise: sort — Sort Lines
## Files: scores.txt  mixed.txt  versions.txt

### Ex 1 — Alphabetical
```bash
sort mixed.txt
```

### Ex 2 — Case-insensitive
```bash
sort -f mixed.txt
```

### Ex 3 — Reverse
```bash
sort -r scores.txt
```

### Ex 4 — Numeric sort (field 2)
```bash
sort -k2 -n scores.txt
```

### Ex 5 — Highest first
```bash
sort -k2 -nr scores.txt
```

### Ex 6 — Remove duplicates
```bash
echo "apple" >> mixed.txt
sort -u mixed.txt
```

### Ex 7 — Sort IPs by 4th octet
```bash
# first create ips.txt:
printf "10.0.0.5\n192.168.1.100\n172.16.0.1\n10.0.0.1\n" > ips.txt
sort -t'.' -k4 -n ips.txt
```

### Ex 8 — Sort CSV by salary descending
```bash
tail -n +2 ~/labs/awk/employees.csv | sort -t',' -k4 -nr
```

### Ex 9 — Version sort
```bash
sort -V versions.txt
```
EXEOF

cat > "$BASE/sort/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — sort Mastery

### Challenge 1 — Leaderboard
From `scores.txt`: sort by score desc, name asc for ties, add rank numbers.  
Format: `1. Carol - 95` → save to `leaderboard.txt`

### Challenge 2 — Top 3 Salaries per Department
From `~/labs/awk/employees.csv`, find the top 3 earners per department using sort + awk.

### Challenge 3 — Log Level Frequency
From `~/labs/grep/access.log`, count ERROR/WARNING/INFO occurrences, sorted by count descending.

### Challenge 4 — Correct Version Sort
Prove that `sort -V` correctly orders `versions.txt` and explain why plain `sort` fails.
EXEOF

# ─── HEAD & TAIL ──────────────────────────────────────────────────────────────
cat > "$BASE/head-tail/exercise.md" <<'EXEOF'
# Exercise: head & tail
## File: big.log (200 lines)

### Ex 1 — First 10 lines
```bash
head big.log
```

### Ex 2 — First 25 lines
```bash
head -n 25 big.log
```

### Ex 3 — Last 10 lines
```bash
tail big.log
```

### Ex 4 — Last 30 lines
```bash
tail -n 30 big.log
```

### Ex 5 — Skip first line (skip header)
```bash
tail -n +2 big.log
```

### Ex 6 — All but last 5
```bash
head -n -5 big.log
```

### Ex 7 — Live monitor (follow)
```bash
tail -f big.log &
echo "NEW ENTRY $(date)" >> big.log
sleep 2
kill %1
```

### Ex 8 — Last 20 ERRORs
```bash
grep "ERROR" big.log | tail -n 20
```

### Ex 9 — Line range (lines 50–60)
```bash
head -n 60 big.log | tail -n 11
```
EXEOF

cat > "$BASE/head-tail/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — head & tail Mastery

### Challenge 1 — Rolling error window
From the last 50 lines of `big.log`, filter ERRORs and WARNINGs, sort by level, count each.

### Challenge 2 — Log rotation simulation
Write a script that appends 10 new timestamped entries to `big.log`, then trims it to keep only the last 100 lines.

### Challenge 3 — Reusable line extractor
Write a bash function `extract_lines file start end` that prints lines `$start` through `$end` of any file. Test on `big.log` lines 100-110.

### Challenge 4 — Top 5 Unique Messages
From `big.log`, extract the message text (after the `[svc]` tag), find the top 5 most frequent, sorted by frequency.
EXEOF

# ─── PROCESSES ────────────────────────────────────────────────────────────────
cat > "$BASE/processes/ps/exercise.md" <<'EXEOF'
# Exercise: ps — Process Status

### Ex 1
```bash
ps
```

### Ex 2 — Full list
```bash
ps aux
```

### Ex 3 — Filter by name
```bash
ps aux | grep bash
```

### Ex 4 — Sort by CPU
```bash
ps aux --sort=-%cpu | head -11
```

### Ex 5 — Sort by memory
```bash
ps aux --sort=-%mem | head -11
```

### Ex 6 — Tree view
```bash
ps auxf
```

### Ex 7 — Specific PID
```bash
MYPID=$(pgrep bash | head -1)
ps -p $MYPID -o pid,ppid,cmd,%cpu,%mem
```

### Ex 8 — Count per user
```bash
ps aux | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn
```
EXEOF

cat > "$BASE/processes/kill/exercise.md" <<'EXEOF'
# Exercise: kill — Terminate Processes

### Ex 1 — List signals
```bash
kill -l
```

### Ex 2 — Background process
```bash
sleep 300 &
echo "PID: $!"
```

### Ex 3 — Find the PID
```bash
pgrep sleep
```

### Ex 4 — Graceful terminate (SIGTERM=15)
```bash
kill -15 $(pgrep sleep)
```

### Ex 5 — Force kill (SIGKILL=9)
```bash
sleep 300 &
kill -9 $!
```

### Ex 6 — killall by name
```bash
sleep 300 & sleep 300 & sleep 300 &
killall sleep
```

### Ex 7 — pkill by pattern
```bash
sleep 300 &
pkill -f "sleep 300"
```

### Ex 8 — Theory
**Q:** When would you send SIGHUP instead of SIGTERM?  
**A:** SIGHUP is used to reload a process config without restarting (e.g., nginx -s reload).
EXEOF

cat > "$BASE/processes/uptime/exercise.md" <<'EXEOF'
# Exercise: uptime — System Uptime & Load Average

### Ex 1
```bash
uptime
```
Output: `up X days, HH:MM, N users, load average: 1min, 5min, 15min`

### Ex 2 — Pretty format
```bash
uptime -p
```

### Ex 3 — Last boot time
```bash
uptime -s
```

### Ex 4 — How many CPU cores?
```bash
nproc
```
**Rule:** load average > core count = system overloaded

### Ex 5 — Extract 1-min load average
```bash
uptime | awk '{print "1-min load:", $(NF-2)}' | tr -d ','
```
EXEOF

cat > "$BASE/processes/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Process Monitoring

### Challenge 1 — Process Health Check Script
Write `process_health.sh <process_name>` that:
- If running: prints PID, CPU%, MEM%, start time
- If not running: prints `ALERT: [name] is not running` and exits with code 1

### Challenge 2 — High Resource Alert
Scan all processes and log any using >1% CPU or >5% MEM to `alert.log` with timestamp.

### Challenge 3 — Process Monitor Loop
Every 5 seconds (5 iterations): print total process count + top 3 CPU consumers, log to `process_monitor.log`.

### Challenge 4 — Zombie Finder
Explain zombie processes. Write a command to find all zombies and display their PID and PPID.
EXEOF

# ─── DISK & MEMORY ────────────────────────────────────────────────────────────
cat > "$BASE/disk-memory/df/exercise.md" <<'EXEOF'
# Exercise: df — Disk Free Space

### Ex 1
```bash
df
```

### Ex 2 — Human-readable
```bash
df -h
```

### Ex 3 — Root filesystem only
```bash
df -h /
```

### Ex 4 — Show filesystem type
```bash
df -hT
```

### Ex 5 — Inode usage
```bash
df -i
```

### Ex 6 — Extract Use% column
```bash
df -h | awk 'NR>1 {print $5, $6}'
```

### Ex 7 — Alert if over 80%
```bash
df -h | awk 'NR>1 {gsub(/%/,"",$5); if($5+0 > 80) print "WARNING:", $6, "is", $5"% full"}'
```
EXEOF

cat > "$BASE/disk-memory/du/exercise.md" <<'EXEOF'
# Exercise: du — Disk Usage
## Working dir: ~/labs/disk-memory/du/

### Ex 1 — Total size of directory
```bash
du -sh ~/labs/disk-memory/du/
```

### Ex 2 — Size of each item
```bash
du -h ~/labs/disk-memory/du/*
```

### Ex 3 — Recursive breakdown
```bash
du -ah ~/labs/disk-memory/du/
```

### Ex 4 — One level deep
```bash
du -h --max-depth=1 ~/labs/disk-memory/du/
```

### Ex 5 — Top 5 largest items under labs/
```bash
du -ah ~/labs/ | sort -rh | head -5
```

### Ex 6 — Exclude a directory
```bash
du -sh --exclude=disk-memory ~/labs/
```
EXEOF

cat > "$BASE/disk-memory/free/exercise.md" <<'EXEOF'
# Exercise: free — Memory Usage

### Ex 1
```bash
free
```

### Ex 2 — Human-readable
```bash
free -h
```

### Ex 3 — In megabytes
```bash
free -m
```

### Ex 4 — Continuous (every 2s, 5 times)
```bash
free -h -s 2 -c 5
```

### Ex 5 — Extract used RAM
```bash
free -m | awk '/Mem:/ {print "Used RAM:", $3, "MB"}'
```

### Ex 6 — Free percentage
```bash
free -m | awk '/Mem:/ {printf "Free: %.1f%%\n", ($4/$2)*100}'
```
EXEOF

cat > "$BASE/disk-memory/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Disk & Memory

### Challenge 1 — Resource Dashboard Script
Write `resource_dash.sh` that prints:
```
=== System Resource Dashboard ===
--- Disk ---
/       45% used  (20G / 45G)
--- Memory ---
RAM:   Used 2.1G / 8G  (26%)
Swap:  Used 0G   / 2G  (0%)
--- Top 3 disk consumers under ~/labs ---
...
```

### Challenge 2 — Disk Alert System
Check all filesystems; log to `disk_alert.log` if any exceeds a configurable threshold (default 80%). Also alert if free RAM drops below 20%.

### Challenge 3 — Cleanup Finder
Scan `/tmp` and `~/labs/` for files >500KB and not accessed in 7 days. List sorted by size. Ask for confirmation before deleting.
EXEOF

# ─── NETWORKING ───────────────────────────────────────────────────────────────
cat > "$BASE/networking/ping/exercise.md" <<'EXEOF'
# Exercise: ping — Test Connectivity

### Ex 1
```bash
ping 8.8.8.8
```

### Ex 2 — Limit packets
```bash
ping -c 4 8.8.8.8
```

### Ex 3 — By hostname
```bash
ping -c 4 google.com
```

### Ex 4 — Custom interval (2s)
```bash
ping -c 4 -i 2 8.8.8.8
```

### Ex 5 — With timeout
```bash
ping -c 4 -W 1 8.8.8.8
```

### Ex 6 — Extract RTT summary
```bash
ping -c 5 8.8.8.8 | tail -1
```

### Ex 7 — Multi-host check
```bash
for host in 8.8.8.8 8.8.4.4 1.1.1.1; do
  ping -c 1 -W 1 $host &>/dev/null && echo "$host UP" || echo "$host DOWN"
done
```
EXEOF

cat > "$BASE/networking/curl/exercise.md" <<'EXEOF'
# Exercise: curl — HTTP Requests

### Ex 1 — GET request
```bash
curl https://httpbin.org/get
```

### Ex 2 — Save to file
```bash
curl -o response.json https://httpbin.org/get
```

### Ex 3 — Show status code only
```bash
curl -o /dev/null -s -w "%{http_code}\n" https://httpbin.org/get
```

### Ex 4 — Follow redirects
```bash
curl -L https://httpbin.org/redirect/1
```

### Ex 5 — Custom headers
```bash
curl -H "X-Custom-Header: DevOps" https://httpbin.org/headers
```

### Ex 6 — POST JSON
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name":"student","role":"devops"}' \
     https://httpbin.org/post
```

### Ex 7 — Parse response
```bash
curl -s https://httpbin.org/get | grep "origin"
```

### Ex 8 — Check multiple URLs
```bash
for url in https://httpbin.org/get https://httpbin.org/status/404; do
  code=$(curl -o /dev/null -s -w "%{http_code}" $url)
  echo "$url -> $code"
done
```
EXEOF

cat > "$BASE/networking/wget/exercise.md" <<'EXEOF'
# Exercise: wget — Download Files

### Ex 1
```bash
wget https://httpbin.org/get
```

### Ex 2 — Custom filename
```bash
wget -O data.json https://httpbin.org/get
```

### Ex 3 — Background download
```bash
wget -b -o wget.log https://httpbin.org/get
```

### Ex 4 — Limit speed
```bash
wget --limit-rate=50k https://httpbin.org/get
```

### Ex 5 — Retry on failure
```bash
wget --tries=3 https://httpbin.org/status/503
```

### Ex 6 — Quiet mode
```bash
wget -q -O silent.json https://httpbin.org/get
```

### Ex 7 — Check without downloading
```bash
wget --spider https://httpbin.org/get 2>&1 | grep "200 OK"
```
EXEOF

cat > "$BASE/networking/ssh/exercise.md" <<'EXEOF'
# Exercise: ssh — Secure Shell

### Ex 1
```bash
ssh username@hostname
```

### Ex 2 — Custom port
```bash
ssh -p 2222 username@hostname
```

### Ex 3 — Run command remotely
```bash
ssh username@hostname "uptime && df -h"
```

### Ex 4 — Generate key pair
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/devops_key -N ""
```

### Ex 5 — Copy public key
```bash
ssh-copy-id -i ~/.ssh/devops_key.pub username@hostname
```

### Ex 6 — Use specific key
```bash
ssh -i ~/.ssh/devops_key username@hostname
```

### Ex 7 — SSH config file
```
# ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User devops
    Port 2222
    IdentityFile ~/.ssh/devops_key
```
Then: `ssh myserver`

### Ex 8 — Port forwarding
```bash
ssh -L 8080:localhost:80 username@hostname
```
EXEOF

cat > "$BASE/networking/rsync/exercise.md" <<'EXEOF'
# Exercise: rsync — File Synchronization

### Ex 1 — Local copy
```bash
rsync -av ~/labs/grep/ /tmp/grep_backup/
```

### Ex 2 — Dry run (preview)
```bash
rsync -avn ~/labs/grep/ /tmp/grep_backup/
```

### Ex 3 — Sync + delete extras
```bash
rsync -av --delete ~/labs/grep/ /tmp/grep_backup/
```

### Ex 4 — Exclude files
```bash
rsync -av --exclude="*.log" ~/labs/grep/ /tmp/grep_backup/
```

### Ex 5 — Show progress
```bash
rsync -av --progress ~/labs/ /tmp/labs_backup/
```

### Ex 6 — Remote sync
```bash
rsync -avz ~/labs/grep/ username@hostname:/backup/grep/
```

### Ex 7 — Incremental demo
1. Sync `~/labs/grep/` to `/tmp/grep_backup/`
2. Add a new file
3. Sync again — only the new file should transfer
EXEOF

cat > "$BASE/networking/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Networking Mastery

### Challenge 1 — Network Health Script
Write `network_check.sh` that:
- Pings 5 hosts (8.8.8.8, 8.8.4.4, 1.1.1.1, google.com, github.com)
- Reports UP/DOWN + average RTT
- Checks HTTP status of google.com and github.com with curl
- Saves timestamped report to `network_report.txt`

### Challenge 2 — API Pipeline
1. Fetch `https://httpbin.org/get` → `raw.json`
2. Extract the `origin` IP with grep
3. Ping it and report reachable/not
4. Log result to `api_check.log`

### Challenge 3 — Rsync Backup Automation
Write `backup.sh <src> <dest>` that:
- Creates `dest/YYYY-MM-DD_HHMMSS/` timestamp folder
- Uses rsync to copy only changed files
- Logs files transferred and total size
- Keeps only the last 5 backup folders

### Challenge 4 — SSH Hardening Doc
Write `ssh_hardening.md` listing 5 SSH security best practices with exact `sshd_config` changes and how to test each safely.
EXEOF

# ─── ARCHIVE ──────────────────────────────────────────────────────────────────
cat > "$BASE/archive/zip/exercise.md" <<'EXEOF'
# Exercise: zip & unzip

### Ex 1 — Create zip
```bash
zip -r project.zip ~/labs/archive/data/project/
```

### Ex 2 — List contents
```bash
unzip -l project.zip
```

### Ex 3 — Extract
```bash
mkdir extracted && unzip project.zip -d extracted/
```

### Ex 4 — Extract single file
```bash
unzip project.zip "data/project/docs/README.md"
```

### Ex 5 — Password-protected zip
```bash
zip -r -e secure_project.zip ~/labs/archive/data/project/
```

### Ex 6 — Add file to existing zip
```bash
echo "patch notes" > patch.txt
zip project.zip patch.txt
```

### Ex 7 — Max compression
```bash
zip -9 -r project_max.zip ~/labs/archive/data/project/
ls -lh project.zip project_max.zip
```
EXEOF

cat > "$BASE/archive/tar/exercise.md" <<'EXEOF'
# Exercise: tar — Tape Archive

### Ex 1 — Create .tar (no compression)
```bash
tar -cvf project.tar ~/labs/archive/data/project/
```

### Ex 2 — Create .tar.gz (gzip)
```bash
tar -czvf project.tar.gz ~/labs/archive/data/project/
```

### Ex 3 — Create .tar.bz2 (bzip2, better compression)
```bash
tar -cjvf project.tar.bz2 ~/labs/archive/data/project/
ls -lh project.tar project.tar.gz project.tar.bz2
```

### Ex 4 — List contents
```bash
tar -tzvf project.tar.gz
```

### Ex 5 — Extract
```bash
mkdir restored && tar -xzvf project.tar.gz -C restored/
```

### Ex 6 — Extract single file
```bash
tar -xzvf project.tar.gz --wildcards "*/requirements.txt"
```

### Ex 7 — Incremental backup (files modified today)
```bash
tar -czvf recent.tar.gz --newer-mtime="1 day ago" ~/labs/archive/data/project/
```

### Ex 8 — Verify integrity
```bash
tar -tzvf project.tar.gz > /dev/null && echo "OK" || echo "CORRUPT"
```
EXEOF

cat > "$BASE/archive/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Archive Mastery

### Challenge 1 — Automated Backup Script
Write `backup_project.sh <dir>` that:
- Creates timestamped `backup_YYYYMMDD_HHMMSS.tar.gz`
- Excludes `__pycache__/`, `*.pyc`, `.git/`
- Verifies archive after creation
- Prints archive name, size, number of files inside

### Challenge 2 — Compression Comparison
Create two versions of the project dir (add a file). Compare tar.gz vs tar.bz2 compression ratios. Show diff between the two archives.

### Challenge 3 — Patch Workflow
Extract `project.tar.gz` → `patched/`, modify `src/app.py`, re-archive as `project_v2.tar.gz`. Show what changed between v1 and v2 using tar + diff.

### Challenge 4 — Secure Archive Pipeline
Write a script that: creates tar.gz, encrypts with gpg (passphrase from `$BACKUP_PASS`), verifies decryption, generates SHA256 checksum file.
EXEOF

# ─── PERMISSIONS ──────────────────────────────────────────────────────────────
cat > "$BASE/permissions/chmod/exercise.md" <<'EXEOF'
# Exercise: chmod — Change File Permissions
## Permission reference:  r=4  w=2  x=1
## 755=rwxr-xr-x  644=rw-r--r--  600=rw-------  400=r--------

### Ex 1 — View permissions
```bash
ls -l ~/labs/permissions/chmod/
```

### Ex 2 — Make script executable
```bash
chmod u+x script.sh
ls -l script.sh
```

### Ex 3 — Restrict secret file (owner read-only)
```bash
chmod 400 secret.txt
```

### Ex 4 — Standard file perms
```bash
chmod 644 public.txt
```

### Ex 5 — Standard directory perms
```bash
mkdir testdir && chmod 755 testdir
```

### Ex 6 — Remove all permissions
```bash
chmod 000 readonly.cfg
cat readonly.cfg   # what happens?
chmod 444 readonly.cfg  # restore
```

### Ex 7 — Recursive chmod (files=644, dirs=755)
```bash
mkdir -p myproject/src myproject/docs
touch myproject/src/app.py myproject/docs/readme.txt
find myproject -type f -exec chmod 644 {} \;
find myproject -type d -exec chmod 755 {} \;
```

### Ex 8 — Symbolic vs Octal (both equivalent)
```bash
chmod 764 public.txt
chmod u=rwx,g=rw,o=r public.txt
```

### Ex 9 — SUID bit
```bash
chmod u+s script.sh
ls -l script.sh   # notice the 's' in owner execute
```
**Q:** What does SUID do when set on an executable?
EXEOF

cat > "$BASE/permissions/chown/exercise.md" <<'EXEOF'
# Exercise: chown — Change Ownership
## Note: chown requires sudo

### Ex 1 — View ownership
```bash
ls -la ~/labs/permissions/chmod/
```

### Ex 2 — Change owner
```bash
sudo chown root public.txt
ls -l public.txt
```

### Ex 3 — Change owner:group
```bash
sudo chown student:student public.txt
```

### Ex 4 — Recursive
```bash
sudo chown -R student:student ~/labs/permissions/
```

### Ex 5 — Your UID/GID
```bash
id
```

### Ex 6 — Change only group via chown
```bash
sudo chown :root secret.txt
```
EXEOF

cat > "$BASE/permissions/chgrp/exercise.md" <<'EXEOF'
# Exercise: chgrp — Change Group

### Ex 1 — Your groups
```bash
groups
```

### Ex 2 — Change group of file
```bash
sudo chgrp root ~/labs/permissions/chmod/public.txt
ls -l ~/labs/permissions/chmod/public.txt
```

### Ex 3 — Recursive group change
```bash
sudo chgrp -R root ~/labs/permissions/chmod/
```

### Ex 4 — Shared directory
```bash
mkdir /tmp/shared_lab
sudo chgrp root /tmp/shared_lab
chmod g+w /tmp/shared_lab
ls -la /tmp/ | grep shared_lab
```
EXEOF

cat > "$BASE/permissions/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Permissions Mastery

### Challenge 1 — Secure Web Directory
Create `/tmp/webroot/` with: `html/`, `cgi-bin/`, `conf/`
- `html/` → owner=www-data, perms=755
- `conf/` → owner=root, perms=640
- `cgi-bin/` → scripts must be executable by owner only (700)
- Verify: create a test user can read html/ but NOT conf/

### Challenge 2 — Permission Audit Script
Write `perm_audit.sh` that scans a directory and reports:
- World-writable files (perm includes o+w)
- SUID/SGID executables
- Files with no owner (UID not in /etc/passwd)
Save report to `perm_report.txt`

### Challenge 3 — Minimal Permission Principle
Given a web app structure, assign the most restrictive permissions that still allow the app to function:
- Config files: readable by app user, not others
- Log directory: app can write, others can read
- Scripts: executable by app user only
Write the exact chmod/chown commands.

### Challenge 4 — umask
Explain umask. Set umask to 027, create a file and directory, observe default permissions. Reset umask to 022.
EXEOF

# ─── BASH SCRIPTING ───────────────────────────────────────────────────────────
cat > "$BASE/bash-scripting/syntax/exercise.md" <<'EXEOF'
# Exercise: Bash Script Syntax

### Ex 1 — Your first script
```bash
cat > hello.sh <<'EOF'
#!/bin/bash
echo "Hello, $(whoami)!"
echo "Today is $(date +%A, %B %d %Y)"
echo "You are in: $(pwd)"
EOF
chmod +x hello.sh
./hello.sh
```

### Ex 2 — Script arguments
```bash
cat > greet.sh <<'EOF'
#!/bin/bash
echo "Hello, $1! You passed $# arguments."
echo "All args: $@"
echo "Script name: $0"
EOF
chmod +x greet.sh
./greet.sh Alice Bob Carol
```

### Ex 3 — Exit codes
```bash
cat > check_file.sh <<'EOF'
#!/bin/bash
ls /nonexistent 2>/dev/null
echo "Exit code was: $?"
ls /etc 2>/dev/null
echo "Exit code was: $?"
EOF
chmod +x check_file.sh
./check_file.sh
```

### Ex 4 — Redirect stdout and stderr
```bash
./check_file.sh > output.txt 2> errors.txt
cat output.txt
cat errors.txt
```
EXEOF

cat > "$BASE/bash-scripting/variables-datatypes/exercise.md" <<'EXEOF'
# Exercise: Variables & Data Types

### Ex 1 — String variable
```bash
NAME="DevOps"
GREETING="Hello $NAME"
echo $GREETING
echo ${#NAME}        # length of string
echo ${NAME,,}       # lowercase
echo ${NAME^^}       # uppercase
```

### Ex 2 — Integer variable
```bash
NUM=42
echo $((NUM * 2))
echo $((NUM + 8))
let NUM2=NUM+10
echo $NUM2
```

### Ex 3 — Readonly variable
```bash
readonly PI=3.14159
echo $PI
PI=3    # this should fail
```

### Ex 4 — Environment vs local
```bash
export MY_ENV="visible to child processes"
LOCAL="only this shell"
bash -c 'echo "ENV: $MY_ENV | LOCAL: $LOCAL"'
```

### Ex 5 — Unset variable
```bash
VAR="hello"
echo $VAR
unset VAR
echo ${VAR:-"default_value"}   # use default if unset
```

### Ex 6 — Command substitution
```bash
CURRENT_DATE=$(date +%Y-%m-%d)
FILE_COUNT=$(ls /etc | wc -l)
echo "Date: $CURRENT_DATE | Files in /etc: $FILE_COUNT"
```
EXEOF

cat > "$BASE/bash-scripting/operators/exercise.md" <<'EXEOF'
# Exercise: Operators

### Arithmetic operators
```bash
A=10; B=3
echo "$A + $B = $((A+B))"
echo "$A - $B = $((A-B))"
echo "$A * $B = $((A*B))"
echo "$A / $B = $((A/B))"
echo "$A % $B = $((A%B))"
echo "$A ** $B = $((A**B))"
```

### Comparison operators (numeric)
```bash
[[ 10 -eq 10 ]] && echo "equal"
[[ 10 -ne 5  ]] && echo "not equal"
[[ 10 -gt 5  ]] && echo "greater"
[[ 5  -lt 10 ]] && echo "less"
[[ 10 -ge 10 ]] && echo "greater or equal"
[[ 5  -le 10 ]] && echo "less or equal"
```

### String comparison
```bash
A="hello"; B="world"
[[ $A == $B ]] && echo "same" || echo "different"
[[ -z ""     ]] && echo "empty string"
[[ -n "hi"   ]] && echo "non-empty string"
```

### File test operators
```bash
[[ -f /etc/passwd ]]  && echo "regular file exists"
[[ -d /etc        ]]  && echo "directory exists"
[[ -r /etc/passwd ]]  && echo "file is readable"
[[ -w /tmp        ]]  && echo "directory is writable"
[[ -x /bin/bash   ]]  && echo "file is executable"
[[ -s /etc/passwd ]]  && echo "file is not empty"
```

### Logical operators
```bash
[[ -f /etc/passwd && -r /etc/passwd ]] && echo "exists AND readable"
[[ -f /nope || -f /etc/passwd       ]] && echo "at least one exists"
[[ ! -f /nope ]]                        && echo "does NOT exist"
```
EXEOF

cat > "$BASE/bash-scripting/if-else/exercise.md" <<'EXEOF'
# Exercise: if / elif / else

### Ex 1 — Basic if
```bash
NUM=15
if [[ $NUM -gt 10 ]]; then
    echo "$NUM is greater than 10"
fi
```

### Ex 2 — if/else
```bash
read -p "Enter a number: " N
if [[ $N -ge 0 ]]; then
    echo "Positive or zero"
else
    echo "Negative"
fi
```

### Ex 3 — if/elif/else
```bash
read -p "Enter score (0-100): " SCORE
if   [[ $SCORE -ge 90 ]]; then echo "A"
elif [[ $SCORE -ge 80 ]]; then echo "B"
elif [[ $SCORE -ge 70 ]]; then echo "C"
elif [[ $SCORE -ge 60 ]]; then echo "D"
else                            echo "F"
fi
```

### Ex 4 — File existence check
```bash
FILE=~/labs/grep/access.log
if [[ -f $FILE ]]; then
    echo "Found: $FILE ($(wc -l < $FILE) lines)"
else
    echo "File not found: $FILE"
fi
```

### Ex 5 — String comparison
```bash
read -p "Enter your role: " ROLE
if [[ $ROLE == "admin" ]]; then
    echo "Welcome, admin. Full access granted."
elif [[ $ROLE == "devops" ]]; then
    echo "Welcome, DevOps engineer."
else
    echo "Unknown role: $ROLE"
fi
```

### Ex 6 — Nested if
```bash
SERVICE="nginx"
RUNNING=true
if [[ $RUNNING == true ]]; then
    if pgrep $SERVICE &>/dev/null; then
        echo "$SERVICE process found"
    else
        echo "$SERVICE marked running but process missing"
    fi
else
    echo "$SERVICE is stopped"
fi
```
EXEOF

cat > "$BASE/bash-scripting/loops/exercise.md" <<'EXEOF'
# Exercise: Loops (for, while, until)

### Ex 1 — for loop over list
```bash
for fruit in apple banana cherry; do
    echo "Fruit: $fruit"
done
```

### Ex 2 — for loop with range
```bash
for i in {1..5}; do
    echo "Step $i"
done
```

### Ex 3 — for loop with step
```bash
for i in {0..20..5}; do
    echo $i
done
```

### Ex 4 — for loop over files
```bash
for file in ~/labs/grep/*.log; do
    echo "Lines in $file: $(wc -l < $file)"
done
```

### Ex 5 — C-style for loop
```bash
for ((i=1; i<=5; i++)); do
    echo "Count: $i"
done
```

### Ex 6 — while loop
```bash
COUNT=1
while [[ $COUNT -le 5 ]]; do
    echo "While count: $COUNT"
    ((COUNT++))
done
```

### Ex 7 — until loop
```bash
N=10
until [[ $N -le 0 ]]; do
    echo "Countdown: $N"
    ((N--))
done
echo "Launch!"
```

### Ex 8 — break and continue
```bash
for i in {1..10}; do
    [[ $i -eq 4 ]] && continue   # skip 4
    [[ $i -eq 8 ]] && break      # stop at 8
    echo $i
done
```

### Ex 9 — Loop with pipeline input
```bash
while IFS=',' read -r id name dept salary city; do
    echo "Employee: $name | Dept: $dept"
done < <(tail -n +2 ~/labs/awk/employees.csv)
```
EXEOF

cat > "$BASE/bash-scripting/functions/exercise.md" <<'EXEOF'
# Exercise: Functions

### Ex 1 — Basic function
```bash
greet() {
    echo "Hello, $1!"
}
greet "DevOps"
greet "World"
```

### Ex 2 — Return value via echo
```bash
add() {
    echo $(( $1 + $2 ))
}
RESULT=$(add 5 3)
echo "5 + 3 = $RESULT"
```

### Ex 3 — Return status code
```bash
is_even() {
    [[ $(( $1 % 2 )) -eq 0 ]]
}
is_even 4 && echo "4 is even" || echo "4 is odd"
is_even 7 && echo "7 is even" || echo "7 is odd"
```

### Ex 4 — Local variables
```bash
counter=0
increment() {
    local counter=99   # local: doesn't affect outer
    echo "Inside: $counter"
}
increment
echo "Outside: $counter"   # still 0
```

### Ex 5 — Log function
```bash
log() {
    local level=$1; shift
    echo "[$(date +%H:%M:%S)] [$level] $*"
}
log INFO  "Server started"
log ERROR "Connection refused"
log WARN  "Disk at 85%"
```

### Ex 6 — Recursive function
```bash
factorial() {
    [[ $1 -le 1 ]] && echo 1 && return
    echo $(( $1 * $(factorial $(($1 - 1))) ))
}
echo "5! = $(factorial 5)"
```
EXEOF

cat > "$BASE/bash-scripting/arrays/exercise.md" <<'EXEOF'
# Exercise: Arrays

### Ex 1 — Declare and access
```bash
FRUITS=("apple" "banana" "cherry" "date")
echo ${FRUITS[0]}        # first element
echo ${FRUITS[-1]}       # last element
echo ${FRUITS[@]}        # all elements
echo ${#FRUITS[@]}       # length
```

### Ex 2 — Loop over array
```bash
SERVERS=("web01" "web02" "db01" "cache01")
for server in "${SERVERS[@]}"; do
    echo "Checking: $server"
done
```

### Ex 3 — Add / modify elements
```bash
TOOLS=("git" "docker")
TOOLS+=("kubectl")          # append
TOOLS[0]="git2"             # modify
echo "${TOOLS[@]}"
```

### Ex 4 — Array slice
```bash
NUMS=(10 20 30 40 50 60)
echo "${NUMS[@]:1:3}"       # 3 elements starting at index 1
```

### Ex 5 — Associative array (dictionary)
```bash
declare -A PORTS
PORTS["nginx"]=80
PORTS["postgres"]=5432
PORTS["redis"]=6379
for svc in "${!PORTS[@]}"; do
    echo "$svc listens on port ${PORTS[$svc]}"
done
```

### Ex 6 — Read file into array
```bash
mapfile -t LINES < ~/labs/grep/emails.txt
echo "Total emails: ${#LINES[@]}"
echo "First: ${LINES[0]}"
echo "Last:  ${LINES[-1]}"
```
EXEOF

cat > "$BASE/bash-scripting/cron/exercise.md" <<'EXEOF'
# Exercise: cron — Schedule Jobs

### Cron syntax:
```
*  *  *  *  *   command
|  |  |  |  |
|  |  |  |  └── Day of week (0=Sun, 6=Sat)
|  |  |  └───── Month (1-12)
|  |  └──────── Day of month (1-31)
|  └─────────── Hour (0-23)
└────────────── Minute (0-59)
```

### Ex 1 — View crontab
```bash
crontab -l
```

### Ex 2 — Edit crontab
```bash
crontab -e
```

### Ex 3 — Common schedule examples
```
*/5 * * * *         echo "every 5 min"
0 * * * *           echo "top of every hour"
0 0 * * *           echo "midnight every day"
0 9 * * 1-5         echo "9am weekdays"
0 0 1 * *           echo "1st of every month"
@reboot             echo "on system boot"
```

### Ex 4 — Add a job via crontab
Add a cron job that appends a heartbeat to `/tmp/heartbeat.log` every minute:
```
* * * * * echo "alive: $(date)" >> /tmp/heartbeat.log
```

### Ex 5 — Remove a job
Edit crontab and delete the heartbeat entry. Then verify: `crontab -l`

### Ex 6 — System-wide cron
View `/etc/cron.d/` and `/etc/crontab` for system jobs.
```bash
ls /etc/cron.d/
cat /etc/crontab
```
EXEOF

cat > "$BASE/bash-scripting/systemctl/exercise.md" <<'EXEOF'
# Exercise: systemctl — Manage Services

### Ex 1 — Check service status
```bash
systemctl status ssh
```

### Ex 2 — Start / stop / restart
```bash
sudo systemctl start  nginx
sudo systemctl stop   nginx
sudo systemctl restart nginx
```

### Ex 3 — Enable / disable at boot
```bash
sudo systemctl enable  nginx    # start on boot
sudo systemctl disable nginx    # don't start on boot
```

### Ex 4 — Reload config without restart
```bash
sudo systemctl reload nginx
```

### Ex 5 — List all running services
```bash
systemctl list-units --type=service --state=running
```

### Ex 6 — List failed services
```bash
systemctl --failed
```

### Ex 7 — View service logs (via journalctl)
```bash
journalctl -u ssh -n 20        # last 20 lines for ssh
journalctl -u ssh --since today
journalctl -f                  # follow all logs live
```

### Ex 8 — Create a simple systemd service
```bash
cat > /tmp/hello.service <<'EOF'
[Unit]
Description=Hello World Service

[Service]
ExecStart=/bin/bash -c "while true; do echo hello; sleep 60; done"
Restart=always

[Install]
WantedBy=multi-user.target
EOF
sudo cp /tmp/hello.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start hello
sudo systemctl status hello
sudo systemctl stop hello
```
EXEOF

cat > "$BASE/bash-scripting/HARD_CHALLENGE.md" <<'EXEOF'
# HARD CHALLENGE — Bash Scripting Mastery

### Challenge 1 — System Health Monitor
Write `health_monitor.sh` that accepts no arguments and:
1. Checks CPU load (from uptime) — alerts if 1min load > core count
2. Checks disk usage — alerts on any filesystem > 80%
3. Checks memory — alerts if free RAM < 20%
4. Checks if nginx/ssh/cron services are running (use pgrep)
5. Outputs a color-coded report (green=OK, red=ALERT) to terminal
6. Saves a plain text report to `health_$(date +%Y%m%d_%H%M%S).log`

### Challenge 2 — CSV Report Generator
Write `csv_report.sh <csvfile>` that:
- Reads any CSV with headers on line 1
- Prints header row formatted as a table
- Allows user to pass a column number to sort by
- Shows total row count
- Shows min/max/average of any numeric column specified
- Works with `~/labs/awk/employees.csv`

### Challenge 3 — Automated Log Analyzer
Write `log_analyzer.sh <logfile>` that:
- Counts occurrences of each log level (ERROR/WARN/INFO)
- Finds the busiest hour (most log entries)
- Extracts all unique services (the [service] tags)
- Identifies the top 3 most repeated messages
- Generates an HTML summary report

### Challenge 4 — Deployment Script
Write `deploy.sh <environment>` where environment is dev/staging/prod:
- Validates the environment argument
- Creates a timestamped backup of current deployment files
- Simulates deploying (copy files from a source dir to target)
- Verifies deployment success (check key files exist)
- Rolls back if verification fails
- Logs all actions with timestamps
- Uses functions, arrays, and proper error handling (set -euo pipefail)

### Challenge 5 — Cron-powered Watchdog
Write a script `watchdog.sh` that:
- Monitors a list of services (array)
- Restarts any stopped service (use `systemctl start` or `pkill/sleep` simulation)
- Logs restart events with timestamp
- If a service restarts more than 3 times in 10 minutes, alerts and stops retrying
Set it up as a cron job running every 2 minutes.
EXEOF

echo "[+] All exercise files written."
