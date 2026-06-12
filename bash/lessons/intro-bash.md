# Introduction to Bash

## What is Bash?

**Bash** stands for **Bourne Again SHell**. It is a command-line interpreter that allows users to interact with the operating system by running commands and writing scripts.

Bash is the default shell on most Linux distributions and was the default shell on macOS for many years. It is widely used by system administrators, DevOps engineers, developers, and power users to automate tasks and manage systems efficiently.

---

## Why Learn Bash?

Bash is one of the most important tools in the Linux and Unix ecosystem. Learning Bash allows you to:

* Automate repetitive tasks
* Manage servers and operating systems
* Write scripts to simplify daily work
* Process and manipulate files and data
* Build deployment and automation pipelines
* Improve productivity when working in Linux environments

Whether you are a developer, DevOps engineer, cloud engineer, or system administrator, Bash is a fundamental skill.

---

## Shell vs. Bash

A **shell** is a program that provides a command-line interface between the user and the operating system.

There are several different shells available, including:

* Bash (Bourne Again Shell)
* Zsh (Z Shell)
* Ksh (Korn Shell)
* Csh (C Shell)
* Fish (Friendly Interactive Shell)

**Bash** is simply one type of shell, but because it is the most widely used shell on Linux systems, people often use the terms *shell* and *Bash* interchangeably.

### Example

When you type:

```bash
ls
```

The shell receives the command, interprets it, and asks the operating system to execute it.

---

## History of Bash

Bash was developed in **1989** by **Brian Fox** as part of the GNU Project.

It was created as a free software replacement for the original Bourne Shell (`sh`), which was commonly used on Unix systems.

Over the years, Bash incorporated useful features from other popular shells such as:

* Korn Shell (ksh)
* C Shell (csh)

As a result, Bash became one of the most powerful and versatile command-line environments available.

Today, Bash is installed by default on most Linux distributions and remains one of the most widely used shells in the world.

---

## Practical Uses of Bash

### For System Administrators

System administrators use Bash to:

* Automate maintenance tasks
* Manage users and permissions
* Monitor system performance
* Configure servers
* Manage backups
* Process logs

#### Example

```bash
#!/bin/bash

echo "Disk Usage Report"
df -h
```

This script displays disk usage information in a human-readable format.

---

### For Developers

Developers use Bash to:

* Automate builds
* Run tests
* Deploy applications
* Manage development environments
* Process files and data

#### Example

```bash
#!/bin/bash

echo "Running Tests..."
pytest

echo "Deploying Application..."
docker compose up -d
```

This script automates testing and deployment tasks.

---

## Your First Bash Command

Open a terminal and run:

```bash
echo "Hello Bash!"
```

Output:

```text
Hello Bash!
```

The `echo` command prints text to the screen.

---

## Summary

* Bash stands for **Bourne Again SHell**.
* Bash is the most popular shell on Linux systems.
* A shell is a command-line interface; Bash is a specific type of shell.
* Bash was created in 1989 by Brian Fox.
* Bash is used for automation, system administration, development, and DevOps tasks.
* Learning Bash is an essential skill for anyone working with Linux, cloud platforms, containers, or infrastructure automation.

In the next lesson, we will learn how to navigate the Linux filesystem using commands such as:

```bash
pwd
ls
cd
mkdir
touch
```
