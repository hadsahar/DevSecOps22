# Lab 2 - Bash Scripting Exercises

Run all scripts on your Ubuntu server. Make each script executable with `chmod +x script.sh` before running.

---

## Exercise 1 - Hello DevOps

Write a script that prints "Hello, DevOps World!" to the terminal.

---

## Exercise 2 - System Info

Write a script that prints the hostname, current user, and today's date.

---

## Exercise 3 - Disk Usage

Write a script that displays disk usage in human-readable format and highlights any partition over 80% usage.

---

## Exercise 4 - User Input

Write a script that asks the user for their name and prints a greeting message.

---

## Exercise 5 - File Existence Check

Write a script that takes a filename as an argument and checks if the file exists. Print an appropriate message for each case.

---

## Exercise 6 - Even or Odd

Write a script that takes a number as an argument and prints whether it is even or odd.

---

## Exercise 7 - Service Status Checker

Write a script that checks if a given service (e.g., nginx, docker) is running. If it's not running, print a warning message.

---

## Exercise 8 - Backup Script

Write a script that takes a directory path as an argument and creates a compressed `.tar.gz` backup of it with a timestamp in the filename.

---

## Exercise 9 - Loop Through Users

Write a script that reads `/etc/passwd` and prints only the usernames (first field).

---

## Exercise 10 - Process Monitor

Write a script that lists the top 5 memory-consuming processes on the server.

---

## Exercise 11 - Log File Analyzer

Write a script that counts the number of ERROR, WARNING, and INFO lines in a log file passed as an argument.

---

## Exercise 12 - Bulk User Creation

Write a script that reads a list of usernames from a file (one per line) and creates each user on the system. Skip any user that already exists.

---

## Exercise 13 - Port Scanner

Write a script that checks if ports 22, 80, 443, and 8080 are open on localhost using `/dev/tcp` or `nc`.

---

## Exercise 14 - Automated Updates

Write a script that updates the system packages, upgrades them, and removes unused packages. Log the output to `/var/log/auto-update.log` with a timestamp.

---

## Exercise 15 - Directory Cleanup

Write a script that deletes all files older than 30 days in `/tmp` and prints how many files were removed.

---

## Exercise 16 - Health Check Script

Write a script that checks CPU load, memory usage, and disk space. If any metric exceeds a threshold (e.g., 90%), print an alert message.

---

## Exercise 17 - Deploy Script

Write a script that:

1. Pulls the latest code from a git repository
2. Installs dependencies
3. Restarts a service
4. Prints success or failure status for each step

---

## Exercise 18 - Cron Job Installer

Write a script that adds a cron job to run a backup script every day at 3 AM. The script should check if the cron job already exists before adding it.

---

## Exercise 19 - Multi-Server Ping

Write a script that reads a list of server IPs from a file and pings each one. Report which servers are reachable and which are not.

---

## Exercise 20 - Full Server Setup Script

Write a script that automates a fresh Ubuntu server setup:

1. Update and upgrade packages
2. Install essential tools (curl, wget, git, vim, htop, net-tools)
3. Create a deploy user with sudo privileges
4. Configure the firewall (allow SSH, HTTP, HTTPS)
5. Print a summary of all actions taken

---

> **Note:** Run all exercises on your Ubuntu server. Test each script thoroughly before moving to the next one.
