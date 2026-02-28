---
layout: default
title: Python Lesson 1 - Setup, Basics, and Strings
---

# Python Lesson 1 - Setup, Basics, and Strings

## What you will learn

In this lesson you will learn:

1. Python versions and why they matter
2. Why Java can run the “same code” on multiple operating systems (JVM) and how that compares to Python
3. How to install Python on Linux, macOS, and Windows
4. IDEs: VS Code and PyCharm, and how to open new/existing projects
5. Python basics:
   - arithmetic operators
   - comments and printing
   - strings and escaping
   - variables and naming styles
   - data types and casting
   - input from the user
   - string slicing
   - common string methods

---

## 1) Python versions (what students must know)

Python has major versions:

- Python 2 (old, end-of-life)
- Python 3 (current)

Most modern learning and production code uses **Python 3**.

### Check your Python version

On Linux/macOS:

```bash
python3 --version
```

On Windows (PowerShell):

```powershell
py --version
python --version
```

---

## 2) JVM vs Python: “write once run anywhere”

### 2.1 How Java does it

Java code is compiled into **bytecode** (`.class`) that runs on the **JVM** (Java Virtual Machine).

- Each OS has a JVM implementation
- Your Java bytecode runs on top of the JVM

That is why the same Java program can run on Windows, Linux, and macOS.

### 2.2 How Python does it

Python code is usually executed by a Python interpreter.

- Each OS has a Python interpreter build
- Your `.py` files run on the interpreter

Python also compiles to bytecode internally (`.pyc`), but the main point for beginners:

- You need Python installed (or packaged) on the system where you run your code

---

## 3) Installing Python

### 3.1 Linux

Many Linux distributions come with Python 3 already.

- Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-pip
python3 --version
pip3 --version
```

### 3.2 macOS

You can use:

- Official installer from python.org
- Homebrew

Homebrew example:

```bash
brew install python
python3 --version
```

### 3.3 Windows

Recommended:

- Install Python from python.org
- During install, check: **Add Python to PATH**

Then verify:

```powershell
python --version
py --version
```

---

## 4) IDEs: VS Code and PyCharm (projects)

### 4.1 VS Code

- Install the **Python** extension
- Open a folder:
  - File -> Open Folder
- Create a new file: `main.py`
- Run:
  - the Run button
  - or terminal: `python3 main.py`

### 4.2 PyCharm

- Create project:
  - New Project
  - Choose Python interpreter (system or virtual environment)
- Open existing project:
  - Open
  - Select the folder

---

## 5) The code we learned (explained)

### 5.1 Arithmetic operators

```python
# + : add
print(1 + 1)

# - : subtract
print(1 - 6)

# * : multiply
print(10 * 4)

# / : divide (always returns float)
print(10 / 3)

# // : floor division (whole number result)
print(10 // 3)

# % : modulo (remainder)
print(10 % 3)

# ** : power
print(2 ** 3)
```

### 5.2 Comments

```python
# This is a comment. Python ignores it.
```

---

## 6) Printing strings

### 6.1 Single, double, and multi-line strings

```python
print('hello world!')
print("hello world!")

print('''hello
world!''')

print("""hello
world!""")
```

### 6.2 Quotes inside strings (escaping)

This is wrong:

```python
# print('i'm')  # wrong
```

Correct ways:

```python
print("i'm")
print('i"m')
print('i\'"m')
```

---

## 7) Special characters: new lines, tabs, raw strings

### 7.1 New line (\n)

```python
print('hello\ncat')
print('hello')
print('cat')
```

### 7.2 Windows paths (escaping backslashes)

```python
print('C:\\USERS\\neria\\tomer')
print('hodi\thodi')
```

### 7.3 Raw strings (r'...')

Raw strings treat backslashes as normal characters:

```python
print(r'C:\\USERS\\neria\\tomer')
```

---

## 8) Variables and naming styles

### 8.1 Variables

```python
eli_age = 34
student3_name = 'eytan'
guy_height = 1.82
is_on = False

def1 = 'hello'
```

### 8.2 Naming styles

```python
# PascalCase
SaharLastName = "sahar"

# camelCase
saharLastName = "sahar"

# snake_case (recommended in Python)
sahar_last_name = "sahar"

# CONSTANT_CASE (used for constants)
SAHAR_LAST_NAME = "sahar"
```

---

## 9) Basic data types

Common types:

- `int` (1, -22, 0)
- `float` (1.0, 0.66, -7.5)
- `bool` (`True` / `False`)
- `str` ("text")

Examples:

```python
up = False
print(type(up))

name = 'donAld tRump'
print(type(name))
```

---

## 10) Casting (type conversion)

### 10.1 int to float

```python
a = 10
b = 1.5
print(type(a))
print(type(b))
print(float(a))
```

### 10.2 division results

```python
a = 100
b = 13
ans = a // b
print(type(ans))
print(ans)
```

### 10.3 Converting strings to numbers

```python
f = '55'
print(int(f))

# int('3.5') is invalid
# int('hodi') is invalid
```

---

## 11) String concatenation

String concatenation means joining strings together to form a new string.

### 11.1 Using `+` (string + string)

When you use `+` with two strings, Python joins them.

```python
print('11' + '22')
print('hothaifa ' + 'zoubi')

domain = '@hr.com'
print('guy' + domain)
```

Important notes:

- `str + str` produces `str`
- `str + int` is an error (you must convert first)

Example:

```python
age = 20

# print('Age: ' + age)  # error
print('Age: ' + str(age))
```

### 11.2 Adding spaces correctly

If you want a space between words, you must include it:

```python
first = 'hen'
last = 'keter'
full = first + ' ' + last
print(full)
```

### 11.3 Better printing: `print(a, b)` and f-strings

Instead of concatenating, you can let `print()` add spaces:

```python
first = 'hen'
last = 'keter'
print(first, last)
```

For variables inside strings, f-strings are usually the cleanest:

```python
first = 'hen'
last = 'keter'
age = 20
print(f'{first} {last} is {age} years old')
```

---

## 12) User input

`input()` always returns a string.

```python
first_name = input('enter your name: ')
last_name = input('enter your last name: ')
full_name = first_name + ' ' + last_name
print(full_name)
```

If you want a number, cast it:

```python
current_year = 2026
birth_year = int(input('Enter your birth year: '))
age = current_year - birth_year
print(f'{age=}')
```

---

## 13) String slicing (indexes)

### 13.1 Indexing (single character)

In Python, strings are sequences.

- Indexes start at `0`
- The last character can be accessed with `-1`

Example string:

```python
name = 'hen kEteR'
```

Index map (for understanding):

```text
h  e  n     k  E  t  e  R
0  1  2  3  4  5  6  7  8
-9 -8 -7 -6 -5 -4 -3 -2 -1
```

```python
name = 'hen kEteR'

print(name[0])
print(name[-1])
print(len(name))

print(name[0:3])
print(name[4:9])
print(name[4:])
print(name[:4])
print(name[:])
```

### 13.2 Slicing rules (start:stop)

Slicing uses this format:

- `text[start:stop]`

Rules:

- `start` is included
- `stop` is excluded

So:

- `name[0:3]` returns characters at index `0,1,2`

### 13.3 Slicing with step (start:stop:step)

You can add a step:

- `text[start:stop:step]`

Examples:

```python
name = 'hen kEteR'

print(name[::2])   # every 2nd character
print(name[::-1])  # reverse the string
```

### 13.4 Common slicing patterns

```python
name = 'hen kEteR'

# first 2 characters
print(name[:2])

# last 2 characters
print(name[-2:])

# everything except the last character
print(name[:-1])

# remove the first and last character
print(name[1:-1])

# split the string into two halves
mid = len(name) // 2
print(name[:mid])
print(name[mid:])
```

---

## 14) String methods

```python
name = 'hen kEteR'

print(name.upper())
print(name.lower())
print(name.title())
print(name.count('e'))
print(name.lower().count('e'))
print(name.find('e', 4))
print(name.rfind('e'))

print(name.isalpha())
print(name.isupper())
print(name.islower())
```

Notes:

- `isalpha()` is true only if the string contains letters only (no spaces)
- `isupper()` and `islower()` check if the letters are all upper/lower

---

