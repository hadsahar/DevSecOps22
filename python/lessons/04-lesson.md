---
layout: default
title: Python Lesson 4 - Loops (for) and Iterating Collections
---

# Loops (for) and Iterating Collections

---

## 1. Why do we need loops?

Loops let you repeat the same logic over many items **without copy/paste**.

You use loops when you need to:

- Process many values (files, users, lines in a log, servers, ports).
- Apply the same validation/transformation to each item.
- Search for something (first match, count matches).
- Build new collections (filtered list, cleaned text, aggregated data).

### Example: without a loop (bad)

```python
numbers = [10, 20, 30, 40]

print(numbers[0] * 2)
print(numbers[1] * 2)
print(numbers[2] * 2)
print(numbers[3] * 2)
```

### Example: with a loop (good)

```python
numbers = [10, 20, 30, 40]

for n in numbers:
    print(n * 2)
```

---

## 2. What is a `for` loop?

In Python, `for` loops are mainly used to iterate over an **iterable** (something you can loop through), like:

- `list`
- `str`
- `tuple`
- `set`
- `dict` (keys/values/items)
- `range(...)`

### Basic syntax

```python
for item in iterable:
    # code that runs once per item
    print(item)
```

Important rules:

- Python uses **indentation** to know what belongs to the loop.
- `item` is a variable name you choose.
- The loop ends after the iterable is exhausted.

---

## 3. Iterating over collections

### 3.1 Loop over a `list`

Lists keep order and allow duplicates.

```python
services = ["nginx", "redis", "postgres"]

for s in services:
    print("Starting", s)
```

#### When you need the index too: `enumerate()`

```python
services = ["nginx", "redis", "postgres"]

for i, s in enumerate(services):
    print(i, s)
```

You can start counting from 1:

```python
for i, s in enumerate(services, start=1):
    print(i, s)
```

---

### 3.2 Loop over a `str`

A string is a sequence of characters.

```python
text = "DevSecOps"

for ch in text:
    print(ch)
```

Common use: count letters

```python
text = "banana"
count_a = 0

for ch in text:
    if ch == "a":
        count_a += 1

print(count_a)
```

---

### 3.3 Loop over a `tuple`

Tuples are like lists but **immutable** (you can’t change them).

```python
coordinates = (10, 20, 30)

for value in coordinates:
    print(value)
```

Tuples are often used to represent fixed structure data.

---

### 3.4 Loop over a `set`

Sets are **unordered** and contain **unique** values.

```python
ports = {22, 80, 443, 80}

for p in ports:
    print("Checking port", p)
```

Notes:

- You cannot rely on the order of items in a set.
- Sets are great when you want uniqueness (no duplicates).

---

## 4. Looping a specific number of times with `range()`

`range(n)` generates numbers from `0` up to `n-1`.

```python
for i in range(5):
    print(i)
```

Output:

```
0
1
2
3
4
```

### Start/stop/step

```python
for i in range(2, 10, 2):
    print(i)
```

This prints:

```
2
4
6
8
```

---

## 5. Common patterns with `for` loops

### 5.1 Sum / accumulate

```python
numbers = [3, 5, 10]
total = 0

for n in numbers:
    total += n

print(total)
```

### 5.2 Count items that match a condition

```python
statuses = [200, 200, 404, 500, 200]
ok_count = 0

for code in statuses:
    if code == 200:
        ok_count += 1

print(ok_count)
```

### 5.3 Filter into a new list

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = []

for n in numbers:
    if n % 2 == 0:
        evens.append(n)

print(evens)
```

### 5.4 Build a string (careful)

```python
words = ["dev", "sec", "ops"]
result = ""

for w in words:
    result += w + "-"

print(result)
```

---

## 6. `break` and `continue`

### 6.1 `break` (stop the loop)

```python
numbers = [3, 7, 2, 9]

for n in numbers:
    if n == 2:
        print("Found 2")
        break
    print("Not 2:", n)
```

### 6.2 `continue` (skip to next iteration)

```python
numbers = [1, 2, 3, 4, 5]

for n in numbers:
    if n % 2 == 1:
        continue
    print("Even:", n)
```

---

## 7. Nested loops (loop inside loop)

Useful for:

- Matrix/table processing
- Comparing every item to every other item
- Working with lists of lists

```python
rows = [
    ["server1", "up"],
    ["server2", "down"],
]

for row in rows:
    for cell in row:
        print(cell)
```

---

## 8. Iteration summary (list vs str vs tuple vs set)

- **List**: ordered, mutable, can have duplicates.
- **String**: ordered sequence of characters.
- **Tuple**: ordered, immutable, can have duplicates.
- **Set**: unordered, unique elements.

In all of them you can do:

```python
for item in collection:
    print(item)
```

---

## 9. How a Python `list` is stored in RAM (and why it’s not like an array)

When people say “array”, they usually mean a low-level (C-style) array:

- Elements are stored **contiguously** (one after another in memory).
- Usually all elements are the **same type** (e.g., 32-bit integers).
- Indexing is computed as: `address = base_address + index * element_size`.

Python `list` is different.

### 9.1 A Python list is a dynamic array of references

In CPython (the normal Python you install), a `list` is implemented as:

- A **contiguous block of pointers/references**.
- Each reference points to a Python object stored somewhere else in memory.

So the list memory looks conceptually like this:

```
list:  [ ref -> obj,  ref -> obj,  ref -> obj,  ... ]
```

The objects those references point to are stored separately:

```
obj: int(10)     obj: str("hi")     obj: float(3.14)
```

That explains why a Python list can contain mixed types:

```python
items = [10, "hi", 3.14]
```

### 9.2 “Next address” intuition

Inside the list itself, the **references** are contiguous (next to each other), so moving from index `0` to `1` is like moving to the “next slot”.

But the **actual objects** (like the `int` or `str`) are not guaranteed to be stored next to each other.

You can see that each element is a separate object by looking at its identity:

```python
items = [10, 11, 12]

for x in items:
    print(x, id(x))
```

`id(x)` is the identity/address-like value of that object (implementation detail, but useful for intuition).

### 9.3 Why it’s not the same as a low-level array

Key differences:

- **Type**:
  - C array: elements usually same type.
  - Python list: elements can be different types.

- **What is stored contiguously**:
  - C array: actual values stored contiguously.
  - Python list: references stored contiguously, values are separate objects.

- **Resize behavior**:
  - C array: fixed size.
  - Python list: can grow/shrink. When it grows beyond its current capacity, Python allocates a larger block and copies references.

### 9.4 What this means in practice

- Indexing `items[i]` is still fast (O(1)) because Python can jump directly to the reference at position `i`.
- Appending is usually fast (amortized O(1)), but sometimes slower when resizing happens.
- A list of ints uses more RAM than a low-level int array because:
  - list stores references
  - each int is a full Python object
