# Regular Expressions (Regex) in Bash

## What is Regex?

A **Regular Expression (Regex)** is a pattern used to search, match, validate, and manipulate text.

Regex is commonly used with commands such as:

* `grep`
* `sed`
* `awk`
* Bash conditional expressions (`[[ ]]`)

---

# Why Learn Regex?

Regex allows you to:

* Search for specific words
* Validate email addresses
* Find IP addresses
* Extract data from logs
* Filter files and text
* Process large datasets

---

# Basic Regex Characters

## `.` (Any Character)

Matches any single character except a newline.

Pattern:

```regex
a.c
```

Matches:

```text
abc
axc
a1c
```

Does NOT match:

```text
ac
abbc
```

---

## `*` (Zero or More)

Matches the previous character zero or more times.

Pattern:

```regex
ab*c
```

Matches:

```text
ac
abc
abbc
abbbc
```

---

## `+` (One or More)

Matches one or more occurrences.

Pattern:

```regex
ab+c
```

Matches:

```text
abc
abbc
abbbc
```

Does NOT match:

```text
ac
```

Example:

```bash
grep -E 'ab+c' file.txt
```

---

## `?` (Zero or One)

Pattern:

```regex
colou?r
```

Matches:

```text
color
colour
```

---

## `^` (Beginning of Line)

Pattern:

```regex
^ERROR
```

Matches:

```text
ERROR Database Failed
```

Does NOT match:

```text
WARNING ERROR Database Failed
```

Example:

```bash
grep '^ERROR' app.log
```

---

## `$` (End of Line)

Pattern:

```regex
txt$
```

Matches:

```text
notes.txt
```

Does NOT match:

```text
notes.txt.backup
```

Example:

```bash
grep 'txt$' files.txt
```

---

# Character Classes

## `[abc]`

Match any character inside brackets.

Pattern:

```regex
gr[ae]y
```

Matches:

```text
gray
grey
```

---

## `[0-9]`

Any digit.

Pattern:

```regex
[0-9]
```

Matches:

```text
5
8
1
```

---

## `[a-z]`

Lowercase letters.

---

## `[A-Z]`

Uppercase letters.

---

## `[a-zA-Z]`

Any letter.

---

## `[a-zA-Z0-9]`

Letters and digits.

---

# Negation

## `[^ ]`

Match anything except.

Pattern:

```regex
[^0-9]
```

Matches:

```text
a
b
#
```

Does NOT match:

```text
5
8
```

---

# Repetition

## `{n}`

Exactly n times.

Pattern:

```regex
[0-9]{3}
```

Matches:

```text
123
456
```

---

## `{n,m}`

Between n and m times.

Pattern:

```regex
[0-9]{2,4}
```

Matches:

```text
12
123
1234
```

---

## `{n,}`

At least n times.

Pattern:

```regex
[0-9]{3,}
```

Matches:

```text
123
12345
987654
```

---

# Common Regex Examples

## Find Numbers

```bash
grep -E '[0-9]+' file.txt
```

Matches:

```text
123
555
```

---

## Find Emails

```bash
grep -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
```

Matches:

```text
admin@example.com
john@gmail.com
```

---

## Find IPv4 Addresses

```bash
grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}'
```

Matches:

```text
192.168.1.1
10.0.0.5
```

---

## Find URLs

```bash
grep -E 'https?://'
```

Matches:

```text
http://google.com
https://github.com
```

---

# Regex with grep

## Search for Digits

```bash
grep -E '[0-9]+' users.txt
```

---

## Search for Email

```bash
grep -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' users.txt
```

---

## Search Lines Starting with ERROR

```bash
grep '^ERROR' app.log
```

---

## Search Lines Ending with .log

```bash
grep '\.log$' files.txt
```

---

# Regex with sed

Replace all numbers:

```bash
sed -E 's/[0-9]+/NUMBER/g'
```

Input:

```text
User 123
Order 456
```

Output:

```text
User NUMBER
Order NUMBER
```

---

# Regex with awk

Show lines containing digits:

```bash
awk '/[0-9]+/' file.txt
```

---

# Regex in Bash Conditions

## Check Username

```bash
username="john123"

if [[ $username =~ ^[a-zA-Z0-9]+$ ]]
then
    echo "Valid username"
fi
```

---

## Validate Email

```bash
email="john@gmail.com"

if [[ $email =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]
then
    echo "Valid email"
else
    echo "Invalid email"
fi
```

---

# Practical DevOps Examples

## Find Failed Logins

```bash
grep 'Failed' auth.log
```

---

## Find IP Addresses

```bash
grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log
```

---

## Find Docker Containers

```bash
docker ps | grep nginx
```

---

## Find Kubernetes Pods

```bash
kubectl get pods | grep Running
```

---

# Most Important Regex Symbols

| Symbol | Meaning               |
| ------ | --------------------- |
| .      | Any character         |
| *      | Zero or more          |
| +      | One or more           |
| ?      | Zero or one           |
| ^      | Start of line         |
| $      | End of line           |
| []     | Character set         |
| [^]    | Negation              |
| {n}    | Exactly n times       |
| {n,m}  | Between n and m times |
| |      | OR                    |
| ()     | Grouping              |

---
