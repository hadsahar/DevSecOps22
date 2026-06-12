# 02 - Bash Scripts

## What is a Bash Script?

A Bash script is a text file containing Linux commands.

Example:

```bash
#!/bin/bash

echo "Starting deployment"

docker ps

echo "Deployment complete"
```

---

## Creating Scripts

```bash
touch deploy.sh
```

Edit:

```bash
nano deploy.sh
```

---

## Make Executable

```bash
chmod +x deploy.sh
```

---

## Execute

```bash
./deploy.sh
```

or

```bash
bash deploy.sh
```

---

## Script Arguments

Script:

```bash
#!/bin/bash

echo "Hello $1"
```

Run:

```bash
./hello.sh John
```

Output:

```text
Hello John
```

---

## Useful Variables

| Variable | Meaning             |
| -------- | ------------------- |
| $0       | Script Name         |
| $1       | First Argument      |
| $2       | Second Argument     |
| $#       | Number of Arguments |
| $@       | All Arguments       |
| $$       | Process ID          |

Example:

```bash
echo $0
echo $1
echo $#
```
