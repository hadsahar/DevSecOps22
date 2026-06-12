# 01 - Bash Syntax

## What is Bash Syntax?

Bash syntax is the set of rules used to write commands and scripts.

Every Bash script usually starts with a **Shebang**.

```bash
#!/bin/bash
```

This tells Linux to execute the script using Bash.

---

## Your First Script

```bash
#!/bin/bash

echo "Hello World"
```

Run:

```bash
chmod +x hello.sh
./hello.sh
```

Output:

```text
Hello World
```

---

## Comments

Single line:

```bash
# This is a comment
```

Example:

```bash
#!/bin/bash

# Print welcome message
echo "Welcome"
```

---

## Commands

```bash
pwd
ls -la
whoami
date
```

Each command executes sequentially.

---

## Multiple Commands

```bash
echo "Start"
pwd
date
echo "End"
```

---

## Exit Codes

```bash
ls

echo $?
```

0 = Success

Non-zero = Failure

---

## Mini Lab

Create:

```bash
nano syntax.sh
```

Add:

```bash
#!/bin/bash

echo "Student Name"
whoami
pwd
date
```

