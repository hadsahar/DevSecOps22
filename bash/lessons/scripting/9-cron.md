# Cron Jobs

## What is Cron?

Cron is a time-based job scheduler in Unix/Linux. It runs commands or scripts automatically at specified intervals.

---

## Cron Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

---

## Common Examples

| Schedule | Cron Expression |
|----------|----------------|
| Every minute | `* * * * *` |
| Every hour | `0 * * * *` |
| Every day at midnight | `0 0 * * *` |
| Every Monday at 9 AM | `0 9 * * 1` |
| Every 5 minutes | `*/5 * * * *` |
| Twice a day (9 AM and 6 PM) | `0 9,18 * * *` |
| Every weekday at 8 AM | `0 8 * * 1-5` |
| First day of month at noon | `0 12 1 * *` |

---

## Managing Crontab

### View current cron jobs

```bash
crontab -l
```

### Edit cron jobs

```bash
crontab -e
```

### Remove all cron jobs

```bash
crontab -r
```

### Edit another user's crontab (root)

```bash
crontab -u username -e
```

---

## Practical Examples

### Run a backup script daily at 2 AM

```bash
0 2 * * * /home/user/scripts/backup.sh
```

### Clear tmp files every Sunday at midnight

```bash
0 0 * * 0 rm -rf /tmp/*
```

### Run a health check every 10 minutes

```bash
*/10 * * * * /usr/local/bin/health_check.sh
```

### Log disk usage hourly

```bash
0 * * * * df -h >> /var/log/disk_usage.log
```

---

## Cron with Output Redirection

### Redirect output to a log file

```bash
0 3 * * * /home/user/script.sh >> /var/log/script.log 2>&1
```

### Discard output (silent)

```bash
0 3 * * * /home/user/script.sh > /dev/null 2>&1
```

### Send output via mail

```bash
MAILTO="user@example.com"
0 6 * * * /home/user/report.sh
```

---

## Special Strings

| String | Equivalent |
|--------|-----------|
| @reboot | Run once at startup |
| @hourly | 0 * * * * |
| @daily | 0 0 * * * |
| @weekly | 0 0 * * 0 |
| @monthly | 0 0 1 * * |
| @yearly | 0 0 1 1 * |

### Example

```bash
@reboot /home/user/startup.sh
@daily /home/user/cleanup.sh
```

---

## Cron Environment

Cron runs with a minimal environment. Always use full paths.

```bash
# Bad
0 * * * * my_script.sh

# Good
0 * * * * /home/user/scripts/my_script.sh
```

### Set environment variables in crontab

```bash
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash

0 5 * * * /home/user/scripts/deploy.sh
```

---

## Cron Logs

### View cron logs

```bash
# Debian/Ubuntu
grep CRON /var/log/syslog

# RHEL/CentOS
cat /var/log/cron
```

---
