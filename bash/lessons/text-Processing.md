# Bash Text Processing Commands

Text processing is one of Bash's strongest features. These commands allow you to search, filter, transform, sort, and analyze text files efficiently.

---

# `grep` - Search Text

## Purpose

Search for lines that match a pattern.

## Syntax

```bash
grep [OPTIONS] PATTERN FILE
```

---

## Common Flags

### `-i` (Ignore Case)

```bash
grep -i docker notes.txt
```

Matches:

```text
Docker
docker
DOCKER
```

---

### `-n` (Show Line Numbers)

```bash
grep -n error app.log
```

Output:

```text
15:error connecting database
32:error timeout
```

---

### `-v` (Invert Match)

Show lines that DO NOT match.

```bash
grep -v INFO app.log
```

---

### `-r` (Recursive Search)

```bash
grep -r "database" project/
```

---

### `-c` (Count Matches)

```bash
grep -c error app.log
```

Output:

```text
5
```

---

### `-w` (Whole Word)

```bash
grep -w docker notes.txt
```

Matches:

```text
docker
```

Does not match:

```text
dockerfile
```

---

### `-l` (Show File Names Only)

```bash
grep -l error *.log
```

---

### `-A` (Lines After Match)

```bash
grep -A 3 ERROR app.log
```

Show 3 lines after the match.

---

### `-B` (Lines Before Match)

```bash
grep -B 3 ERROR app.log
```

Show 3 lines before the match.

---

### `-C` (Context)

```bash
grep -C 2 ERROR app.log
```

Show 2 lines before and after.

---

# `awk` - Pattern Scanning and Processing

## Purpose

Process structured text column by column.

## Syntax

```bash
awk 'pattern { action }' file
```

---

## Common Examples

### Print Entire Line

```bash
awk '{print}' users.txt
```

---

### Print First Column

```bash
awk '{print $1}' users.txt
```

Example file:

```text
john 25 devops
sara 30 developer
```

Output:

```text
john
sara
```

---

### Print Multiple Columns

```bash
awk '{print $1,$3}' users.txt
```

Output:

```text
john devops
sara developer
```

---

### Count Lines

```bash
awk 'END {print NR}' users.txt
```

---

### Show Lines Matching Pattern

```bash
awk '/docker/' notes.txt
```

---

### Custom Separator

CSV Example:

```bash
awk -F ',' '{print $1}' users.csv
```

Input:

```text
john,25,devops
sara,30,developer
```

Output:

```text
john
sara
```

---

# `sed` - Stream Editor

## Purpose

Search, replace, delete, and edit text streams.

## Syntax

```bash
sed [OPTIONS] 'command' file
```

---

## Common Flags

### Replace First Match

```bash
sed 's/docker/kubernetes/' notes.txt
```

---

### Replace All Matches

```bash
sed 's/docker/kubernetes/g' notes.txt
```

---

### Ignore Case

```bash
sed 's/docker/kubernetes/gi' notes.txt
```

---

### Edit File In Place

```bash
sed -i 's/docker/kubernetes/g' notes.txt
```

---

### Delete Line

```bash
sed '3d' notes.txt
```

Deletes line 3.

---

### Delete Range

```bash
sed '2,5d' notes.txt
```

Deletes lines 2-5.

---

### Print Specific Line

```bash
sed -n '5p' notes.txt
```

---

# `cut` - Extract Sections

## Purpose

Extract specific columns or characters.

## Syntax

```bash
cut [OPTIONS]
```

---

## Common Flags

### `-d` (Delimiter)

```bash
cut -d ':' -f1 /etc/passwd
```

---

### `-f` (Field)

```bash
cut -d ',' -f2 users.csv
```

Input:

```text
john,25,devops
sara,30,developer
```

Output:

```text
25
30
```

---

### `-c` (Characters)

```bash
cut -c1-5 notes.txt
```

---

### Multiple Fields

```bash
cut -d ',' -f1,3 users.csv
```

Output:

```text
john,devops
sara,developer
```

---

# `sort` - Sort Lines

## Purpose

Sort text alphabetically or numerically.

## Syntax

```bash
sort [OPTIONS] FILE
```

---

## Common Flags

### Alphabetical Sort

```bash
sort names.txt
```

---

### Reverse Sort

```bash
sort -r names.txt
```

---

### Numeric Sort

```bash
sort -n numbers.txt
```

Input:

```text
100
2
50
```

Output:

```text
2
50
100
```

---

### Remove Duplicates

```bash
sort -u names.txt
```

---

### Sort by Column

```bash
sort -k2 employees.txt
```

---

# `head` - View Beginning of File

## Purpose

Display first lines of a file.

## Syntax

```bash
head [OPTIONS] FILE
```

---

## Common Flags

### Default (10 Lines)

```bash
head app.log
```

---

### First 5 Lines

```bash
head -n 5 app.log
```

---

### First 20 Lines

```bash
head -20 app.log
```

---

# `tail` - View End of File

## Purpose

Display last lines of a file.

## Syntax

```bash
tail [OPTIONS] FILE
```

---

## Common Flags

### Default (10 Lines)

```bash
tail app.log
```

---

### Last 5 Lines

```bash
tail -n 5 app.log
```

---

### Follow Live Updates

```bash
tail -f app.log
```

Useful for:

* Watching logs
* Monitoring applications
* Debugging containers

---

### Follow and Retry

```bash
tail -F app.log
```

Keeps following even if file is recreated.

---

# Powerful Command Combinations

### Search Errors in Logs

```bash
grep ERROR app.log
```

---

### Count Errors

```bash
grep ERROR app.log | wc -l
```

---

### Show Top 5 Largest Files

```bash
ls -lh | sort -k5 -h | tail -5
```

---

### Extract Usernames

```bash
cut -d ':' -f1 /etc/passwd
```

---

### Replace Text

```bash
sed 's/http/https/g' config.txt
```

---

### Show First Column of CSV

```bash
awk -F ',' '{print $1}' users.csv
```

---

# Quick Reference

| Command | Purpose                      |
| ------- | ---------------------------- |
| grep    | Search text                  |
| awk     | Process columns and patterns |
| sed     | Edit and replace text        |
| cut     | Extract fields               |
| sort    | Sort lines                   |
| head    | Show beginning of file       |
| tail    | Show end of file             |

