# Basic Bash Commands

## Introduction

When working with Linux or Unix systems, you interact with the operating system through commands entered in the terminal. These commands allow you to navigate the filesystem, create files and directories, view content, and manage your environment.

This chapter introduces some of the most commonly used Bash commands.

---

# 1. `pwd`

## Purpose

Displays the current working directory.

## Syntax

```bash
pwd
```

## Example

```bash
pwd
```

Output:

```text
/home/student/projects
```

### When to Use

Use `pwd` whenever you want to know your current location in the filesystem.

---

# 2. `ls`

## Purpose

Lists files and directories.

## Syntax

```bash
ls
```

## Example

```bash
ls
```

Output:

```text
Documents Downloads notes.txt projects
```

### Useful Flags

```bash
ls -l
```

Long format listing.

```bash
ls -a
```

Show hidden files.

```bash
ls -lh
```

Human-readable file sizes.

---

# 3. `mkdir`

## Purpose

Creates directories.

## Syntax

```bash
mkdir DIRECTORY_NAME
```

## Example

```bash
mkdir projects
```

Creates:

```text
projects/
```

### Create Nested Directories

```bash
mkdir -p projects/devops/docker
```

Creates all missing parent directories.

---

# 4. `rmdir`

## Purpose

Removes empty directories.

## Syntax

```bash
rmdir DIRECTORY_NAME
```

## Example

```bash
rmdir old_project
```

⚠️ The directory must be empty.

---

# 5. `touch`

## Purpose

Creates empty files.

## Syntax

```bash
touch FILE_NAME
```

## Example

```bash
touch notes.txt
```

Creates:

```text
notes.txt
```

### Create Multiple Files

```bash
touch file1.txt file2.txt file3.txt
```

---

# 6. `cp`

## Purpose

Copies files and directories.

## Syntax

```bash
cp SOURCE DESTINATION
```

## Example

```bash
cp notes.txt backup.txt
```

Creates:

```text
notes.txt
backup.txt
```

### Copy a Directory

```bash
cp -r project backup_project
```

The `-r` flag means recursive.

---

# 7. `mv`

## Purpose

Moves or renames files and directories.

## Syntax

```bash
mv SOURCE DESTINATION
```

## Example 1: Rename a File

```bash
mv notes.txt notes_old.txt
```

### Example 2: Move a File

```bash
mv notes.txt Documents/
```

Moves the file into the Documents directory.

---

# 8. `echo`

## Purpose

Displays text on the screen.

## Syntax

```bash
echo "TEXT"
```

## Example

```bash
echo "Hello World"
```

Output:

```text
Hello World
```

### Save Output to a File

```bash
echo "Docker is awesome" > notes.txt
```

Contents of notes.txt:

```text
Docker is awesome
```

---

# 9. `cat`

## Purpose

Displays file contents.

## Syntax

```bash
cat FILE_NAME
```

## Example

```bash
cat notes.txt
```

Output:

```text
Docker is awesome
```

### Display Line Numbers

```bash
cat -n notes.txt
```

Output:

```text
1 Docker is awesome
```

### Combine Files

```bash
cat file1.txt file2.txt
```

Displays both files together.

---

# 10. `man`

## Purpose

Displays the manual page for a command.

## Syntax

```bash
man COMMAND
```

## Example

```bash
man ls
```

Opens the documentation for the `ls` command.

### Navigate Inside Man Pages

| Key   | Action        |
| ----- | ------------- |
| Space | Next page     |
| b     | Previous page |
| /     | Search        |
| q     | Quit          |

---

# 11. `alias`

## Purpose

Creates shortcuts for commands.

## Syntax

```bash
alias NAME='COMMAND'
```

## Example

```bash
alias ll='ls -lah'
```

Now instead of:

```bash
ls -lah
```

You can simply run:

```bash
ll
```

### View Existing Aliases

```bash
alias
```

---

# 12. `dir`

## Purpose

Lists directory contents.

## Syntax

```bash
dir
```

## Example

```bash
dir
```

Output:

```text
Documents Downloads notes.txt projects
```

### Difference Between `dir` and `ls`

* `ls` is the standard Linux command.
* `dir` is similar but less commonly used.
* Most Linux administrators prefer `ls`.

---

# Quick Summary Table

| Command | Purpose                    |
| ------- | -------------------------- |
| `pwd`   | Show current directory     |
| `ls`    | List files and directories |
| `mkdir` | Create directories         |
| `rmdir` | Remove empty directories   |
| `touch` | Create empty files         |
| `cp`    | Copy files and directories |
| `mv`    | Move or rename files       |
| `echo`  | Print text                 |
| `cat`   | Display file contents      |
| `man`   | Show command documentation |
| `alias` | Create command shortcuts   |
| `dir`   | List directory contents    |
