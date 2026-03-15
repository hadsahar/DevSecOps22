---
layout: default
title: Python Lesson 2 - Conditionals (if, elif, else)
---

# Python Lesson 2 - Conditionals (if, elif, else)

---

## 1) Why we need conditionals

Most real programs must make decisions.

Examples:

- If the user enters the correct password, log them in.
- If CPU usage is above 90%, send an alert.
- If a file exists, read it; else create it.

In Python, decisions are written using **conditional statements**:

- `if` for the first check
- `elif` (else-if) for additional checks
- `else` for the “default” case

---

## 2) The `bool` type and boolean expressions

Python has a boolean type:

- `True`
- `False`

A **boolean expression** is any expression that results in a boolean.

```python
print(10 > 5)     # True
print(10 == 5)    # False
print(10 != 5)    # True
```

In an `if` statement, Python evaluates the condition. If it is `True`, it runs the block.

---

## 3) Basic `if` syntax

```python
age = 20

if age >= 18:
    print("Adult")
```

Important rules:

1. The condition ends with a colon `:`
2. The code block is defined by **indentation** (usually 4 spaces)
3. If the condition is `False`, the block is skipped

### 3.1 Indentation matters

This is correct:

```python
x = 5
if x > 0:
    print("positive")
    print("still inside")
print("outside")
```

This is wrong (indentation error):

```python
# if x > 0:
# print("positive")
```

---

## 4) `if` + `else`

Use `else` when you want a fallback action.

```python
temp = 16

if temp >= 20:
    print("T-shirt")
else:
    print("Jacket")
```

Only one branch runs:

- If condition `True`  -> `if` block runs
- If condition `False` -> `else` block runs

---

## 5) `if` + `elif` + `else`

Use `elif` when you have multiple cases.

```python
score = 83

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
```

How Python executes it:

1. Check the `if` condition
2. If `False`, check the first `elif`
3. Keep checking `elif` blocks in order
4. If none match, run `else` (if present)

Important notes:

- You can have **zero or more** `elif`
- `else` is optional
- Only the **first** matching branch runs

---

## 6) Comparison operators

These return `True` or `False`:

- `==` equal
- `!=` not equal
- `<` less than
- `<=` less than or equal
- `>` greater than
- `>=` greater than or equal

Examples:

```python
x = 10

print(x == 10)  # True
print(x != 10)  # False
print(x < 3)    # False
print(x >= 8)   # True
```

### 6.1 The biggest beginner mistake: `=` vs `==`

- `=` assigns a value
- `==` compares two values

Wrong:

```python
# if x = 10:
#     print("...")
```

Correct:

```python
if x == 10:
    print("x is 10")
```

---

## 7) Boolean operators: `and`, `or`, `not`

### 7.1 `and`

`and` is `True` only if **both sides** are `True`.

```python
age = 22
has_id = True

if age >= 18 and has_id:
    print("Enter")
else:
    print("No entry")
```

### 7.2 `or`

`or` is `True` if **at least one side** is `True`.

```python
is_admin = False
is_manager = True

if is_admin or is_manager:
    print("Access granted")
```

### 7.3 `not`

`not` reverses the boolean.

```python
logged_in = False

if not logged_in:
    print("Please login")
```

### 7.4 Grouping conditions with parentheses

Use parentheses to make your logic clear.

```python
age = 19
has_ticket = True
is_vip = False

if (age >= 18 and has_ticket) or is_vip:
    print("Allowed")
```

---

## 8) Truthy and falsy (very important)

In Python, not only `True` and `False` exist. Many values are treated as boolean in conditions.

### 8.1 Falsy values

These are considered `False`:

- `False`
- `None`
- `0` and `0.0`
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dict)
- `set()` (empty set)

Everything else is considered **truthy**.

```python
name = ""

if name:
    print("Name exists")
else:
    print("Name is empty")
```

### 8.2 Why this matters

Instead of writing:

```python
# if len(items) > 0:
#     ...
```

You can write:

```python
items = [1, 2, 3]
if items:
    print("Not empty")
```

---

## 9) Nested conditionals

You can put an `if` inside another `if`:

```python
username = "admin"
password = "1234"

if username == "admin":
    if password == "1234":
        print("Welcome admin")
    else:
        print("Wrong password")
else:
    print("Unknown user")
```

Nesting is sometimes necessary, but too much nesting can make code hard to read.

Tip:

- If nesting becomes deep, consider rewriting the logic with `and`/`or`, or using functions and early returns.

---

## 10) Common patterns

### 10.1 Input validation (don’t crash on bad input)

`input()` returns a string. If you do `int(input())` and the user types letters, your program crashes.

A safe pattern:

```python
text = input("Enter age: ")

if text.isdigit():
    age = int(text)
    print(f"Your age is {age}")
else:
    print("Invalid age. Please enter numbers only.")
```

### 10.2 Ranges (important ordering)

Always go from most specific / highest range to lowest range.

Correct:

```python
score = 95

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("Below 80")
```

Incorrect ordering:

```python
# score = 95
# if score >= 80:
#     print("B")
# elif score >= 90:
#     print("A")
```

### 10.3 Simple menu program

```python
print("1) Show profile")
print("2) Settings")
print("3) Exit")

choice = input("Choose: ")

if choice == "1":
    print("Profile")
elif choice == "2":
    print("Settings")
elif choice == "3":
    print("Bye")
else:
    print("Invalid option")
```

---

## 11) Common mistakes (and fixes)

### 11.1 Missing `:`

Wrong:

```python
# if x > 0
#     print("...")
```

Correct:

```python
if x > 0:
    print("...")
```

### 11.2 Comparing numbers as strings

If you forget to convert input to int, comparisons become wrong.

```python
age = input("Enter age: ")

# age is a string
# "20" > "100" is True (because it compares text)
```

Fix:

```python
age = int(input("Enter age: "))
if age > 100:
    print("Very old")
```

### 11.3 Using `and` / `or` incorrectly

Wrong:

```python
# if x == 1 or 2:
#     print("x is 1 or 2")
```

Correct:

```python
if x == 1 or x == 2:
    print("x is 1 or 2")

# or using membership
if x in (1, 2):
    print("x is 1 or 2")
```

--