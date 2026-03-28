---
layout: default
title: Python Lab 6 - Dictionaries (dict) Practice
---

#  Python Exercises & Labs
### Dictionaries Practice (dict | keys | values | items)

## Section 1 — Key Existence
---

###  Exercise 1.1 — Check Key Existence in Dictionary
**Scenario:** Check whether a given key already exists in a dictionary.

**Starter Code:**
```python
person = {"name": "Dana", "role": "DevOps", "age": 27}
key_to_check = "role"

# YOUR CODE HERE
# Print True if key exists, otherwise print False
```
**Expected Output:**
```
True
```

---

## Section 2 — Multiply Dictionary Values
---

###  Exercise 2.1 — Multiply All Items
**Scenario:** Multiply all the values in a dictionary.

**Starter Code:**
```python
prices = {"apple": 2, "banana": 3, "orange": 4}
result = 1

# YOUR CODE HERE
# Multiply all values and store in result

print(result)
```
**Expected Output:**
```
24
```

---

## Section 3 — Map Two Lists into a Dictionary
---

###  Exercise 3.1 — Create Dict from Two Lists
**Scenario:** Map two lists into a dictionary.

**Starter Code:**
```python
keys = ["env", "owner", "project"]
values = ["prod", "devops", "payments"]

result = {}

# YOUR CODE HERE
# Create a dictionary so that:
# env -> prod
# owner -> devops
# project -> payments

print(result)
```
**Expected Output:**
```
{'env': 'prod', 'owner': 'devops', 'project': 'payments'}
```

---

## Section 4 — Max and Min Values
---

###  Exercise 4.1 — Get Maximum and Minimum Values
**Scenario:** Find the maximum and minimum values in a dictionary.

**Starter Code:**
```python
cpu_usage = {"auth": 129, "validate": 60, "payment": 122}

# YOUR CODE HERE
# Print the max value and min value
```
**Expected Output:**
```
Max: 129
Min: 60
```

---

## Section 5 — Distinct Values
---

###  Exercise 5.1 — Print All Distinct Values
**Scenario:** Print all unique values in a list of dictionaries.

**Sample Data:**
```python
data = [{"V": "S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII": "S005"}, {"V": "S009"}, {"VIII": "S007"}]

# YOUR CODE HERE
# Build a set of unique values and print it
```
**Expected Output:**
```
Unique Values: {'S005', 'S002', 'S007', 'S001', 'S009'}
```

---

## Section 6 — Dictionary from a String (Letter Counting)
---

###  Exercise 6.1 — Count Characters in a String
**Scenario:** Create a dictionary from a string by tracking the count of each character.

**Sample String:**
```python
s = "pizza is great"
counts = {}

# YOUR CODE HERE

print(counts)
```
**Expected Output:**
```
{'p': 1, 'i': 2, 'z': 2, 'a': 2, ' ': 2, 's': 1, 'g': 1, 'r': 1, 'e': 1, 't': 1}
```

---

## Section 7 — Split Dict of Lists into List of Dicts
---

###  Exercise 7.1 — Split Dictionary of Lists
**Scenario:** Split a dictionary of lists into a list of dictionaries.

**Original Dictionary of Lists:**
```python
scores = {"Science": [88, 89, 62, 95], "Language": [77, 78, 84, 80]}

# YOUR CODE HERE
# Build:
# [{'Science': 88, 'Language': 77}, {'Science': 89, 'Language': 78}, {'Science': 62, 'Language': 84}, {'Science': 95, 'Language': 80}]

print(result)
```
**Expected Output:**
```
[{'Science': 88, 'Language': 77}, {'Science': 89, 'Language': 78}, {'Science': 62, 'Language': 84}, {'Science': 95, 'Language': 80}]
```
