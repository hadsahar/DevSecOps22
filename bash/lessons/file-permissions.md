# File Permissions and Ownership in Bash

Linux is a multi-user operating system. Every file and directory has:

* An **Owner**
* A **Group**
* A set of **Permissions**

Understanding permissions is critical for Linux administrators, DevOps engineers, and developers.

---

# Understanding File Permissions

Run:

```bash
ls -l
```

Example output:

```text
-rwxr-xr-- 1 student developers 1250 Jun 12 10:30 deploy.sh
```

Let's break it down:

```text
-rwxr-xr--
```

| Position | Meaning            |
| -------- | ------------------ |
| -        | File Type          |
| rwx      | Owner Permissions  |
| r-x      | Group Permissions  |
| r--      | Others Permissions |

---

# Permission Types

| Symbol | Permission | Value |
| ------ | ---------- | ----- |
| r      | Read       | 4     |
| w      | Write      | 2     |
| x      | Execute    | 1     |

---

# Permission Examples

### Read Only

```text
r--
```

Value:

```text
4
```

---

### Read + Write

```text
rw-
```

Value:

```text
6
```

---

### Read + Write + Execute

```text
rwx
```

Value:

```text
7
```

---

# Numeric Permission Table

| Number | Permission |
| ------ | ---------- |
| 0      | ---        |
| 1      | --x        |
| 2      | -w-        |
| 3      | -wx        |
| 4      | r--        |
| 5      | r-x        |
| 6      | rw-        |
| 7      | rwx        |

---

# Common Permission Modes

| Mode | Meaning                         |
| ---- | ------------------------------- |
| 777  | Everyone Full Access            |
| 755  | Owner Full, Others Read/Execute |
| 750  | Owner Full, Group Read/Execute  |
| 700  | Owner Only                      |
| 644  | Owner Read/Write, Others Read   |
| 600  | Owner Read/Write Only           |

---

# `chmod` - Change Permissions

## Purpose

Modify file and directory permissions.

## Syntax

```bash
chmod [OPTIONS] MODE FILE
```

---

# Numeric Mode

## 755

```bash
chmod 755 deploy.sh
```

Result:

```text
rwxr-xr-x
```

Owner:

* Read
* Write
* Execute

Group:

* Read
* Execute

Others:

* Read
* Execute

---

## 644

```bash
chmod 644 notes.txt
```

Result:

```text
rw-r--r--
```

Common for:

* Text files
* Config files

---

## 600

```bash
chmod 600 secrets.txt
```

Result:

```text
rw-------
```

Common for:

* Password files
* SSH keys

---

## 700

```bash
chmod 700 script.sh
```

Result:

```text
rwx------
```

Only owner can access.

---

# Symbolic Mode

## Add Execute Permission

```bash
chmod +x deploy.sh
```

Before:

```text
rw-r--r--
```

After:

```text
rwxr--r--
```

---

## Remove Execute Permission

```bash
chmod -x deploy.sh
```

---

## Add Write Permission for Group

```bash
chmod g+w project.txt
```

---

## Remove Read Permission for Others

```bash
chmod o-r project.txt
```

---

## Give Owner Full Permissions

```bash
chmod u+rwx script.sh
```

---

# Recursive Permissions

### Apply to Entire Directory

```bash
chmod -R 755 website/
```

⚠️ Applies permissions to all files and subdirectories.

---

# `chown` - Change Owner

## Purpose

Change file owner.

## Syntax

```bash
chown [OPTIONS] OWNER FILE
```

---

## Change Owner

```bash
sudo chown john file.txt
```

---

## Change Owner and Group

```bash
sudo chown john:developers file.txt
```

---

## Change Entire Directory

```bash
sudo chown -R john project/
```

---

# Common Flags

### `-R` (Recursive)

```bash
sudo chown -R ubuntu:ubuntu app/
```

Changes ownership for:

* Directory
* Files
* Subdirectories

---

### `-v` (Verbose)

```bash
sudo chown -v john file.txt
```

Shows changes performed.

---

# `chgrp` - Change Group

## Purpose

Change a file's group ownership.

## Syntax

```bash
chgrp [OPTIONS] GROUP FILE
```

---

## Change Group

```bash
sudo chgrp developers app.py
```

---

## Recursive Group Change

```bash
sudo chgrp -R developers project/
```

---

## Verbose Mode

```bash
sudo chgrp -v developers app.py
```

---

# Viewing Ownership

Use:

```bash
ls -l
```

Example:

```text
-rw-r--r-- 1 john developers 2500 app.py
```

Meaning:

| Field | Value      |
| ----- | ---------- |
| Owner | john       |
| Group | developers |

---

# Finding Current User

```bash
whoami
```

Output:

```text
student
```

---

# Find User Groups

```bash
groups
```

Output:

```text
student docker developers
```

---

# Practical DevOps Examples

## Make Script Executable

```bash
chmod +x deploy.sh
```

Run:

```bash
./deploy.sh
```

---

## Secure SSH Key

```bash
chmod 600 ~/.ssh/id_rsa
```

Required by SSH.

---

## Give Nginx Access

```bash
sudo chown -R www-data:www-data /var/www/html
```

---

## Share Directory with Team

```bash
sudo chgrp -R developers project/

chmod -R 775 project/
```

---

## Secure Secret Files

```bash
chmod 600 secrets.env
```

---

# Quick Reference

| Command | Purpose            |
| ------- | ------------------ |
| ls -l   | View permissions   |
| chmod   | Change permissions |
| chown   | Change owner       |
| chgrp   | Change group       |
| whoami  | Show current user  |
| groups  | Show user groups   |

---

# Mini Lab

Create a test environment:

```bash
mkdir permissions-lab

cd permissions-lab

touch notes.txt

touch deploy.sh

ls -l
```

---

Make script executable:

```bash
chmod +x deploy.sh

ls -l
```

---

Change permissions:

```bash
chmod 644 notes.txt

chmod 700 deploy.sh

ls -l
```

---

Create shared directory:

```bash
mkdir team-project

chmod 775 team-project

ls -ld team-project
```

---

View user information:

```bash
whoami

groups
```

