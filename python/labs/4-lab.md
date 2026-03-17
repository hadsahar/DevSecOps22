---
layout: default
title: Python Lab 4 - For Loops (Iteration Practice)
---

# for loop lab 

### For Loop Iterations (List | String | Tuple | Set)

## Section 1 — List Iteration

---

### Exercise 1.1 — Print All Services

**Scenario:** You’re writing a simple script to print all running services.
**Starter Code:**

```python
services = ["nginx", "redis", "postgres"]

# YOUR CODE HERE
# Print each service on a separate line
```

**Expected Output:**

```
nginx
redis
postgres
```

---

### Exercise 1.2 — Build a New List (Uppercase)

**Scenario:** You want to normalize service names to uppercase.
**Starter Code:**

```python
services = ["nginx", "redis", "postgres"]
upper_services = []

# YOUR CODE HERE
# Loop and add each service in uppercase into upper_services

print(upper_services)
```

**Expected Output:**

```
['NGINX', 'REDIS', 'POSTGRES']
```

---

### Exercise 1.3 — Count Values Above a Threshold

**Scenario:** You want to count how many servers have CPU usage above 75.
**Starter Code:**

```python
cpu_usage = [12, 88, 76, 45, 90, 75, 77]
threshold = 75
count = 0

# YOUR CODE HERE
# Count how many items are strictly greater than threshold

print(count)
```

**Expected Output:**

```
4
```

---

## Section 2 — String Iteration

---

### Exercise 2.1 — Count a Character

**Scenario:** You want to count how many times the letter `e` appears in a log message.
**Starter Code:**

```python
log_line = "joey doesnt share food, how you doin'?"


# YOUR CODE HERE
# Count how many times target appears in log_line

print()
```

**Expected Output:**

```
3
```

---

### Exercise 2.2 — Extract Only Letters

**Scenario:** You received a message that contains spaces and symbols. You want a new string with only letters.
**Starter Code:**

```python
msg = "DevSecOps-22!!!"
letters = ""

# YOUR CODE HERE
# Build a new string containing only alphabetic characters

print(letters)
```

**Expected Output:**

```
DevSecOps
```

---

## Section 3 — Tuple Iteration

---

### Exercise 3.1 — Validate Allowed Environments

**Scenario:** Only certain environments are allowed.
**Starter Code:**

```python
allowed_envs = ("dev", "staging", "prod")
user_env = "prod"
is_allowed = False

# YOUR CODE HERE
# Loop over allowed_envs and set is_allowed to True if user_env exists

print(is_allowed)
```

**Expected Output:**

```
True
```

---

### Exercise 3.2 — Find the Longest Word

**Scenario:** You want to find the longest string in a tuple.
**Starter Code:**

```python
words = ("dev", "security", "ops", "automation")
longest = ""

# YOUR CODE HERE
# Find the longest word and store it in longest

print(longest)
```

**Expected Output:**

```
automation
```

---

## Section 4 — Set Iteration

---

### Exercise 4.1 — Print Unique Ports

**Scenario:** You want to check unique ports that appear in a scan result.
**Starter Code:**

```python
ports = {22, 80, 443, 80, 22}

# YOUR CODE HERE
# Print each port on a separate line
```

**Expected Output (order can be different):**

```
22
80
443
```

---

### Exercise 4.2 — Classify Secure vs Not Secure

**Scenario:** Mark port 443 as secure and all other ports as not secure.
**Starter Code:**

```python
ports = {22, 80, 443}

# YOUR CODE HERE
# For each port:
# - if it is 443 print "secure"
# - else print "not secure"
```

**Expected Output (order can be different):**

```
not secure
not secure
secure
```

---

