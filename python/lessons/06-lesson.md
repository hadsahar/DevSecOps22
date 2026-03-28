---
layout: default
title: Python Lesson 6 - Dictionaries (dict) + Looping Patterns for DevOps
---

# Dictionaries (`dict`) + Looping Patterns for DevOps

---

## 1. Why `dict` is important 

A `dict` stores data as **key → value**.

You use dictionaries in DevOps all the time:

- Tags/labels: `{"env": "prod", "owner": "devops"}`
- Metrics: `{"service_auth": 129, "service_payment": 122}`
- JSON/YAML structures (APIs, Kubernetes manifests)
- Inventory-like data: instances, servers, config objects

---

## 2. What is a dictionary?

A dictionary is a mapping:

- Keys must be unique.
- Keys are typically `str` (can also be `int`, `tuple`, etc.).
- Values can be any type.

Example:

```python
grades = {"guy": 50, "dylan": 80, "eitan": 90, "rotem": 100}
```

---

## 3. Creating dictionaries

### 3.1 Literal

```python
d = {"env": "e2e", "owner": "all"}
```

### 3.2 Empty dict then fill

```python
d = {}
d["env"] = "e2e"
d["owner"] = "all"
```

### 3.3 `dict()` constructor

```python
d = dict(env="e2e", owner="all")
```

---

## 4. Reading values (access)

### 4.1 Using brackets `[]`

```python
grades = {"guy": 50, "dylan": 80}
print(grades["guy"])
```

If the key doesn’t exist, this raises a `KeyError`:

```python
print(grades["hen"])
```

### 4.2 Safe access with `.get()`

```python
grades = {"guy": 50, "dylan": 80}
print(grades.get("hen"))
print(grades.get("hen", 0))
```

Use `.get()` when missing keys are normal.

---

## 5. Adding and updating values

### 5.1 Add a new key

```python
grades = {"guy": 50}
grades["hen"] = 99
print(grades)
```

### 5.2 Override an existing key

```python
grades = {"guy": 50}
grades["guy"] = 100
print(grades)
```

---

## 6. Deleting items

### 6.1 `del`

```python
grades = {"guy": 50, "dylan": 80}
del grades["guy"]
print(grades)
```

### 6.2 `.pop(key)`

`.pop()` returns the removed value.

```python
grades = {"guy": 50, "dylan": 80}
x = grades.pop("guy")
print(x)
print(grades)
```

### 6.3 `.clear()`

```python
grades = {"guy": 50, "dylan": 80}
grades.clear()
print(grades)
```

---

## 7. Dictionary views: `.keys()`, `.values()`, `.items()`

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

print(grades.keys())
print(grades.values())
print(grades.items())
```

- `keys()` returns a view of keys
- `values()` returns a view of values
- `items()` returns key-value pairs as tuples like: `(key, value)`

---

## 8. `for` loops with dictionaries (every common case)

### 8.1 Loop over keys (default)

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

for key in grades:
    print(key)
```

Same as:

```python
for key in grades.keys():
    print(key)
```

### 8.2 Loop over values

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

for value in grades.values():
    print(value)
```

### 8.3 Loop over items (tuple pairs)

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

for item in grades.items():
    print(item)
    print(item[0], item[1])
```

### 8.4 Loop over items (recommended: unpacking)

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

for key, value in grades.items():
    print(f"the key is {key} and the value is {value}")
```

### 8.5 Using `continue` inside dict loops

```python
grades = {"guy": 50, "dylan": 80, "rotem": 100}

for key, value in grades.items():
    if key == "rotem":
        continue
    print(value)
```

---

## 9. Membership checks

### 9.1 Check if a key exists

```python
grades = {"guy": 50, "dylan": 80}

if "guy" in grades:
    print("exists")
```

### 9.2 Check if a value exists

```python
grades = {"guy": 50, "dylan": 80}

if 80 in grades.values():
    print("found 80")
```

---

## 10. Common DevOps pattern: list of dictionaries (inventory)

This is a very common shape:

```python
infrastructure = [
    {"id": "i-01", "status": "running", "type": "t2.micro", "os": "amazon linux"},
    {"id": "i-02", "status": "running", "type": "m5.large", "os": "amazon linux"},
    {"id": "i-03", "status": "stopped", "type": "r6.large", "os": "ubuntu"},
]
```

### 10.1 Loop and check status

```python
for instance in infrastructure:
    if instance["status"] == "running":
        print(f"{instance['id']} is up and running")
    else:
        print(f"{instance['id']} is NOT running")
```

---

## 11. Merging dictionaries (tags use-case)

Example from class:

```python
global_tags = {"env": "e2e", "owner": "all", "project": "AIdev"}
s3_tags = {"env": "e2e", "owner": "devops", "parent_asset_id": "46128461"}
```

Requirement:

- In case of conflict, take the value from `s3_tags`.

### 11.1 Merge using loops

```python
merged_tags = {}

for key in global_tags:
    merged_tags[key] = global_tags[key]

for key in s3_tags:
    merged_tags[key] = s3_tags[key]

print(merged_tags)
```

### 11.2 Merge with `.copy()` + `.update()`

```python
merged_tags = global_tags.copy()
merged_tags.update(s3_tags)
print(merged_tags)
```

### 11.3 Merge with `|` (Python 3.9+)

```python
merged_tags = global_tags | s3_tags
print(merged_tags)
```

---

## 12. Summing values (metrics use-case)

Example from class:

```python
cpu_usage = {
    "service_auth": 129,
    "service_validate": 60,
    "service_payment": 122
}
```

### 12.1 Sum using a loop

```python
total = 0
for key in cpu_usage:
    total += cpu_usage[key]
print(total)
```

### 12.2 Sum using `.values()`

```python
print(sum(cpu_usage.values()))
```

---

## 13. Build a dict of squares (practice pattern)

Goal: keys are numbers, values are squares.

```python
import random

dict1 = {}
iterations = 0

while True:
    r = input("enter a number (1-15) : (q to exit) ")

    if r == "q":
        if len(dict1) >= 10:
            break
        print("need more items")
        continue

    if r == "":
        r = random.randrange(1, 15)
    else:
        r = int(r)

    if r < 1 or r > 15:
        continue

    dict1[r] = r ** 2
    iterations += 1

print(dict1)
print(iterations)
```

---

## 14. Quick recap

- Use `d[key]` when the key must exist.
- Use `d.get(key, default)` when missing keys are normal.
- Loop patterns:
  - `for k in d:` keys
  - `for v in d.values():` values
  - `for k, v in d.items():` pairs
- Use `.update()` or `|` to merge dictionaries.

---
