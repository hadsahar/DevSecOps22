---
layout: default
title: Python Lesson 3 - Match-Case, Nested If, Lists, Tuples & Sets
---

#  Match-Case, Nested If, Lists, Tuples & Sets

---

## 1. Match-Case Statement

>  **Introduced in Python 3.10** — Think of it as a supercharged `switch` statement from other languages, but much more powerful.

###  Basic Syntax

```python
match variable:
    case value1:
        # do something
    case value2:
        # do something else
    case _:
        # default — runs when nothing else matches
```

---

### 🔹 Example 1 — HTTP Status Codes (DevOps Classic!)

```python
status_code = 404

match status_code:
    case 200:
        print(" OK — Request successful")
    case 201:
        print(" Created — Resource was created")
    case 301:
        print(" Moved Permanently")
    case 400:
        print(" Bad Request — Check your payload")
    case 401:
        print("🔐 Unauthorized — Invalid credentials")
    case 403:
        print(" Forbidden — You don't have permission")
    case 404:
        print(" Not Found — Resource doesn't exist")
    case 500:
        print(" Internal Server Error")
    case _:
        print(f"  Unknown status code: {status_code}")
```

**Output:**
```
🔍 Not Found — Resource doesn't exist
```

---

###  Example 2 — Matching Multiple Values in One Case

```python
day = "Saturday"

match day:
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("💼 Work day — stand-up at 9am!")
    case "Saturday" | "Sunday":
        print("🏖️  Weekend — no deployments today!")
    case _:
        print("🤔 Not a valid day")
```

**Output:**
```
🏖️  Weekend — no deployments today!
```

---

###  Example 3 — Matching Tuples (Coordinates / Commands)

```python
command = ("move", 10, 20)

match command:
    case ("move", x, y):
        print(f" Moving to coordinates ({x}, {y})")
    case ("shoot", direction):
        print(f" Shooting {direction}")
    case ("stop",):
        print(" Stopping")
    case _:
        print(" Unknown command")
```

**Output:**
```
 Moving to coordinates (10, 20)
```

---

### 🔹 Example 5 — Using `if` Guards in Match-Case

```python
score = 85

match score:
    case s if s >= 90:
        print(f"Grade A — Excellent! ({s})")
    case s if s >= 80:
        print(f"Grade B — Good job! ({s})")
    case s if s >= 70:
        print(f"Grade C — Keep practicing ({s})")
    case s if s >= 60:
        print(f"Grade D — Study harder ({s})")
    case _:
        print(f"Grade F — Please retry ({score})")
```

**Output:**
```
Grade B — Good job! (85)
```

---


## 2. Nested If Statements

>  **Nested if** means placing one `if` block inside another. Use it when decisions depend on previous decisions — like a decision tree.

###  Golden Rules for Nested Ifs:
- Keep nesting to **max 3 levels** — deeper = harder to read
- Consider **early returns** or **match-case** to flatten deep nesting
- Always add **comments** when logic is complex

---

### 🔹 Example 1 — Login System

```python
username = "admin"
password = "secret123"
is_active = True

if username == "admin":
    print("👤 Username recognized")
    if password == "secret123":
        print("🔐 Password correct")
        if is_active:
            print("Login successful! Welcome, Admin.")
        else:
            print("Account is deactivated. Contact support.")
    else:
        print("Wrong password. Try again.")
else:
    print("Username not found.")
```

**Output:**
```
Username recognized
Password correct
Login successful! Welcome, Admin.
```

---

### Example 3 — Weather Advice App

```python
temperature = 28
is_raining = False
is_sunny = True

if temperature > 30:
    print("Very hot day!")
    if is_sunny:
        print("🕶️  Wear sunglasses and sunscreen.")
    else:
        print(" Hot and cloudy — stay hydrated.")
elif temperature >= 20:
    print("Comfortable weather!")
    if is_raining:
        print("☂️  Take an umbrella just in case.")
    elif is_sunny:
        print(" Great day to go outside!")
    else:
        print(" Mild and cloudy — enjoy the breeze.")
elif temperature >= 10:
    print("Chilly weather")
    if is_raining:
        print(" Wear a raincoat and boots.")
    else:
        print("A jacket will do!")
else:
    print("  Freezing! Stay indoors if possible.")
```

**Output:**
```
Comfortable weather!
 Great day to go outside!
```

---

### 🔹 Example 4 — Number Classifier (Nested + Logical)

```python
def classify_number(n):
    if n > 0:
        print(f"✅ {n} is Positive")
        if n % 2 == 0:
            print(f"   └── Even number")
            if n % 10 == 0:
                print(f"       └── Also a multiple of 10!")
        else:
            print(f"   └── Odd number")
            if n % 3 == 0:
                print(f"       └── Also divisible by 3!")
    elif n < 0:
        print(f"❌ {n} is Negative")
        if n % 2 == 0:
            print(f"   └── Negative Even number")
        else:
            print(f"   └── Negative Odd number")
    else:
        print("⚪ It's Zero — neither positive nor negative")

classify_number(30)
classify_number(-7)
classify_number(0)
```

**Output:**
```
✅ 30 is Positive
   └── Even number
       └── Also a multiple of 10!
❌ -7 is Negative
   └── Negative Odd number
⚪ It's Zero — neither positive nor negative
```

---

### 🔹 Example 5 — DevOps Server Health Check

```python
cpu_usage = 85       # percentage
memory_usage = 60    # percentage
disk_usage = 92      # percentage
is_production = True

print("=== Server Health Report ===")

if cpu_usage > 90:
    print(" CRITICAL: CPU usage is dangerously high!")
elif cpu_usage > 75:
    print("WARNING: CPU usage is elevated")
    if is_production:
        print("  Consider scaling up production servers NOW")
    else:
        print("  Monitor closely in staging")
else:
    print(" CPU: Normal")

if memory_usage > 90:
    print(" CRITICAL: Memory almost full! Risk of OOM crash.")
elif memory_usage > 70:
    print("  WARNING: Memory usage is high")
else:
    print(" Memory: Normal")

if disk_usage > 95:
    print(" CRITICAL: Disk nearly full! Immediate action required.")
elif disk_usage > 80:
    print(" WARNING: Disk usage above 80%")
    if is_production:
        print("     Run log cleanup script immediately!")
    else:
        print("     Clean up test artifacts")
else:
    print(" Disk: Normal")
```

**Output:**
```
  === Server Health Report ===
  WARNING: CPU usage is elevated
     Consider scaling up production servers NOW
 Memory: Normal
 CRITICAL: Disk nearly full! Immediate action required.
```

---

## 3. Lists — The Swiss Army Knife

>  A **list** is an **ordered**, **mutable** (changeable), and **allows duplicates** collection.  
> Syntax: `my_list = [item1, item2, item3]`

---

### 🔹 Creating Lists

```python
# Empty list
empty = []

# List of strings
fruits = ["apple", "banana", "cherry", "mango"]

# Mixed types list
mixed = [42, "hello", 3.14, True, None]

# Nested list (matrix)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# List using list() constructor
numbers = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(fruits)       # ['apple', 'banana', 'cherry', 'mango']
print(numbers)      # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(matrix[1][2]) # 6
```

---

###  Indexing & Slicing

```python
servers = ["web-01", "web-02", "db-01", "cache-01", "worker-01"]

# Positive indexing
print(servers[0])    # web-01 (first)
print(servers[-1])   # worker-01 (last)
print(servers[-2])   # cache-01 (second to last)

# Slicing [start:stop:step]
print(servers[1:3])  # ['web-02', 'db-01']
print(servers[:2])   # ['web-01', 'web-02'] (first 2)
print(servers[2:])   # ['db-01', 'cache-01', 'worker-01'] (from index 2)
print(servers[::2])  # ['web-01', 'db-01', 'worker-01'] (every other)
print(servers[::-1]) # Reversed list
```

---

###  All List Methods — Complete Reference

#### ➕ `append(item)` — Add one item to the end

```python
shopping = ["milk", "eggs"]
shopping.append("bread")
shopping.append("butter")
print(shopping)  # ['milk', 'eggs', 'bread', 'butter']
```

---

#### ➕ `insert(index, item)` — Add item at a specific position

```python
queue = ["Alice", "Bob", "Dave"]
queue.insert(2, "Charlie")  # Insert Charlie at index 2
print(queue)  # ['Alice', 'Bob', 'Charlie', 'Dave']

queue.insert(0, "Zara")    # Insert at the beginning
print(queue)  # ['Zara', 'Alice', 'Bob', 'Charlie', 'Dave']
```

---

#### ➕ `extend(iterable)` — Add multiple items at once

```python
team_a = ["Alice", "Bob"]
team_b = ["Charlie", "Dave", "Eve"]

team_a.extend(team_b)
print(team_a)  # ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']

# Also works with any iterable
scores = [90, 85]
scores.extend(range(80, 84))  # Adds 80, 81, 82, 83
print(scores)  # [90, 85, 80, 81, 82, 83]
```

---

####  `remove(item)` — Remove first occurrence of a value

```python
colors = ["red", "green", "blue", "green", "yellow"]
colors.remove("green")          # Removes FIRST "green" only
print(colors)  # ['red', 'blue', 'green', 'yellow']

# Safe removal with check
if "pink" in colors:
    colors.remove("pink")
else:
    print("⚠️  'pink' not found in list")
```

---

#### ❌ `pop(index)` — Remove and return item by index

```python
stack = ["task1", "task2", "task3", "task4"]

last = stack.pop()      # Removes and returns last item
print(last)             # task4
print(stack)            # ['task1', 'task2', 'task3']

second = stack.pop(1)   # Remove and return index 1
print(second)           # task2
print(stack)            # ['task1', 'task3']
```

---

#### ❌ `clear()` — Remove ALL items

```python
temp_data = [1, 2, 3, 4, 5]
print(f"Before: {temp_data}")   # Before: [1, 2, 3, 4, 5]
temp_data.clear()
print(f"After:  {temp_data}")   # After:  []
```

---

#### 🔍 `index(item)` — Find the position of an item

```python
fruits = ["apple", "banana", "cherry", "banana", "mango"]

pos = fruits.index("banana")          # First occurrence
print(f"First 'banana' at: {pos}")    # 1

pos2 = fruits.index("banana", 2)      # Search starting from index 2
print(f"Second 'banana' at: {pos2}")  # 3

# Safe search with try-except
try:
    pos3 = fruits.index("grape")
except ValueError:
    print("❌ 'grape' is not in the list")
```

---

#### 🔢 `count(item)` — Count how many times a value appears

```python
votes = ["yes", "no", "yes", "yes", "no", "yes", "abstain"]

yes_count = votes.count("yes")
no_count  = votes.count("no")

print(f"✅ Yes: {yes_count}")       # ✅ Yes: 4
print(f"❌ No:  {no_count}")        # ❌ No:  2
print(f"📊 Result: {'YES wins!' if yes_count > no_count else 'NO wins!'}")
```

---

#### 🔃 `sort()` — Sort the list in-place

```python
# Sorting numbers
scores = [45, 92, 78, 63, 88, 55, 100]
scores.sort()
print(f"Ascending:  {scores}")   # [45, 55, 63, 78, 88, 92, 100]

scores.sort(reverse=True)
print(f"Descending: {scores}")   # [100, 92, 88, 78, 63, 55, 45]

# Sorting strings
names = ["Zara", "Alice", "Mike", "Bob", "Charlie"]
names.sort()
print(f"Alphabetical: {names}")  # ['Alice', 'Bob', 'Charlie', 'Mike', 'Zara']

# Sort by key (e.g. string length)
names.sort(key=len)
print(f"By length: {names}")     # ['Bob', 'Zara', 'Mike', 'Alice', 'Charlie']
```

---

#### 🔃 `sorted()` — Return a NEW sorted list (original unchanged)

```python
original = [5, 2, 8, 1, 9, 3]
new_sorted = sorted(original)

print(f"Original:  {original}")    # [5, 2, 8, 1, 9, 3]  (unchanged)
print(f"New Sorted: {new_sorted}") # [1, 2, 3, 5, 8, 9]

# Sort list of dicts by a key
students = [
    {"name": "Alice", "grade": 88},
    {"name": "Bob",   "grade": 95},
    {"name": "Carol", "grade": 72},
]
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")
```

**Output:**
```
  Bob: 95
  Alice: 88
  Carol: 72
```

---

#### 🔄 `reverse()` — Reverse the list in-place

```python
countdown = [1, 2, 3, 4, 5]
countdown.reverse()
print(countdown)   # [5, 4, 3, 2, 1]

# Also works with strings in a list
words = ["Hello", "World", "Python"]
words.reverse()
print(words)       # ['Python', 'World', 'Hello']
```

---

#### 📋 `copy()` — Create a shallow copy

```python
original = [1, 2, 3, 4, 5]

#  Wrong way — both variables point to SAME list
bad_copy = original
bad_copy.append(99)
print(original)  # [1, 2, 3, 4, 5, 99]  ← Original was changed!

#  Correct way — creates an INDEPENDENT copy
original2 = [10, 20, 30]
good_copy = original2.copy()
good_copy.append(99)
print(original2)  # [10, 20, 30]         ← Original untouched 
print(good_copy)  # [10, 20, 30, 99]
```

---

#### 📏 `len()` — Get the number of items (built-in)

```python
students = ["Alice", "Bob", "Charlie", "Dave"]
print(f"Total students: {len(students)}")    # 4

matrix = [[1, 2, 3], [4, 5, 6]]
print(f"Rows: {len(matrix)}")               # 2
print(f"Cols: {len(matrix[0])}")            # 3
```

---

## 4. Tuples — The Read-Only List

>  A **tuple** is an **ordered**, **immutable** (unchangeable), and **allows duplicates** collection.  
> Use tuples for data that should **never change** — coordinates, RGB colors, database records.  
> Syntax: `my_tuple = (item1, item2, item3)`

---

### 🔹 Creating Tuples

```python
# Basic tuple
point = (10, 20)

# Single-item tuple — MUST have trailing comma!
single = (42,)           # This is a tuple
not_a_tuple = (42)       #  This is just the integer 42!

# Without parentheses (tuple packing)
coordinates = 40.7128, -74.0060   # New York City lat/lng

# From a list
my_list = [1, 2, 3]
my_tuple = tuple(my_list)

# Named values — clean and readable
RGB_RED   = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE  = (0, 0, 255)

print(f"Red color: R={RGB_RED[0]}, G={RGB_RED[1]}, B={RGB_RED[2]}")
```

---

### 🔹 Indexing & Slicing (same as lists)

```python
months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

print(months[0])     # Jan
print(months[-1])    # Dec
print(months[3:6])   # ('Apr', 'May', 'Jun')
print(months[:3])    # ('Jan', 'Feb', 'Mar')  — Q1
```

---

### 🔹 Tuple Unpacking — A Superpower

```python
# Basic unpacking
x, y = (10, 20)
print(f"x={x}, y={y}")

# Swap variables without temp variable!
a, b = 5, 10
a, b = b, a
print(f"a={a}, b={b}")  # a=10, b=5

# Extended unpacking with *
first, *rest = (1, 2, 3, 4, 5)
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

*beginning, last = (10, 20, 30, 40)
print(beginning)  # [10, 20, 30]
print(last)       # 40

# Unpack from a function return
def get_user():
    return ("Alice", 30, "alice@example.com")

name, age, email = get_user()
print(f"Name: {name}, Age: {age}, Email: {email}")
```

---

### 🔹 All Tuple Methods

> Tuples only have **2 built-in methods** (because they're immutable), but they support many built-in functions.

---

#### 🔍 `count(item)` — Count occurrences

```python
lottery = (7, 14, 7, 3, 22, 7, 14)

print(lottery.count(7))   # 3
print(lottery.count(14))  # 2
print(lottery.count(99))  # 0 — no error if not found
```

---

#### 🔍 `index(item)` — Find first occurrence

```python
colors = ("red", "green", "blue", "green", "yellow")

print(colors.index("green"))     # 1 — first occurrence
print(colors.index("green", 2))  # 3 — search from index 2

try:
    colors.index("purple")
except ValueError:
    print("❌ 'purple' not found in tuple")
```

---

#### 📏 Built-in Functions with Tuples

```python
temperatures = (23.5, 19.0, 31.2, 25.8, 17.4, 29.6, 22.1)

print(f"Count:    {len(temperatures)}")     # 7
print(f"Max:      {max(temperatures)}")     # 31.2
print(f"Min:      {min(temperatures)}")     # 17.4
print(f"Sum:      {sum(temperatures)}")     # 168.6
print(f"Average:  {sum(temperatures)/len(temperatures):.2f}")  # 24.09
print(f"Sorted:   {sorted(temperatures)}")  # Returns a new list

# Check membership
print(23.5 in temperatures)   # True
print(100 in temperatures)    # False
```

---

#### 🔄 Converting Tuple ↔ List

```python
# Tuple to List (to modify it)
config = ("localhost", 8080, "production")
config_list = list(config)
config_list[1] = 9090          # Change port
config = tuple(config_list)    # Convert back
print(config)  # ('localhost', 9090, 'production')

# List to Tuple
servers = ["web-01", "web-02", "db-01"]
immutable_servers = tuple(servers)
print(immutable_servers)  # ('web-01', 'web-02', 'db-01')
```

---

#### 🔗 Concatenation & Repetition

```python
# Concatenation
t1 = (1, 2, 3)
t2 = (4, 5, 6)
combined = t1 + t2
print(combined)  # (1, 2, 3, 4, 5, 6)

# Repetition
echo = ("Hello",) * 3
print(echo)  # ('Hello', 'Hello', 'Hello')

separator = ("-",) * 20
print("".join(separator))  # --------------------
```

---

## 5. Sets — The Unique Collection

> 🔑 A **set** is an **unordered**, **mutable**, and **NO duplicates** collection.  
> Perfect for: removing duplicates, membership testing, and mathematical set operations.  
> Syntax: `my_set = {item1, item2, item3}`

---

###  Creating Sets

```python
# Basic set — duplicates are automatically removed!
numbers = {1, 2, 3, 2, 1, 4, 3}
print(numbers)  # {1, 2, 3, 4}  ← Only unique values

# Empty set — MUST use set(), not {}
empty_set  = set()     # ✅ Correct
empty_dict = {}        # ❌ This creates an empty DICT, not a set!

# From a list (great for removing duplicates)
tags = ["python", "devops", "python", "linux", "devops", "git"]
unique_tags = set(tags)
print(unique_tags)  # {'python', 'devops', 'linux', 'git'}

# From a string (unique characters)
chars = set("hello world")
print(chars)  # {' ', 'd', 'e', 'h', 'l', 'o', 'r', 'w'}
```

---

### 🔹 All Set Methods — Complete Reference

---

#### ➕ `add(item)` — Add a single item

```python
permissions = {"read", "write"}
permissions.add("execute")
permissions.add("read")        # Already exists — no duplicate added
print(permissions)  # {'read', 'write', 'execute'}
```

---

#### ➕ `update(iterable)` — Add multiple items

```python
skills = {"python", "linux"}
skills.update(["docker", "kubernetes", "git"])
print(skills)  # {'python', 'linux', 'docker', 'kubernetes', 'git'}

# Can accept multiple iterables
skills.update(["aws", "terraform"], {"ansible", "jenkins"})
print(skills)
```

---

#### ❌ `remove(item)` — Remove item (raises error if not found)

```python
fruits = {"apple", "banana", "cherry"}
fruits.remove("banana")
print(fruits)  # {'apple', 'cherry'}

try:
    fruits.remove("mango")     # ❌ Raises KeyError
except KeyError:
    print("❌ 'mango' not in set")
```

---

#### ❌ `discard(item)` — Remove item (NO error if not found)

```python
fruits = {"apple", "banana", "cherry"}
fruits.discard("banana")    # Removed ✅
fruits.discard("mango")     # ✅ No error, just nothing happens
print(fruits)  # {'apple', 'cherry'}
```

---

#### ❌ `pop()` — Remove and return a random item

```python
bag = {"pen", "pencil", "eraser", "ruler"}
item = bag.pop()             # Removes a RANDOM item
print(f"Removed: {item}")
print(f"Remaining: {bag}")
```

---

#### ❌ `clear()` — Remove ALL items

```python
cache = {"key1", "key2", "key3"}
cache.clear()
print(cache)  # set()
```

---

### 🔹 Set Mathematical Operations

> This is where sets truly shine! 🌟

---

#### 🔗 `union()` or `|` — All items from BOTH sets

```python
python_devs  = {"Alice", "Bob", "Charlie"}
java_devs    = {"Bob", "Dave", "Eve"}

all_devs = python_devs.union(java_devs)
# Or: python_devs | java_devs

print(all_devs)  # {'Alice', 'Bob', 'Charlie', 'Dave', 'Eve'}
```

---

#### 🔀 `intersection()` or `&` — Items in BOTH sets

```python
python_devs  = {"Alice", "Bob", "Charlie"}
java_devs    = {"Bob", "Dave", "Charlie"}

both = python_devs.intersection(java_devs)
# Or: python_devs & java_devs

print(f"Know both languages: {both}")  # {'Bob', 'Charlie'}
```

---

#### ➖ `difference()` or `-` — Items in first set but NOT in second

```python
all_employees   = {"Alice", "Bob", "Charlie", "Dave", "Eve"}
on_vacation     = {"Bob", "Eve"}

available = all_employees.difference(on_vacation)
# Or: all_employees - on_vacation

print(f"Available today: {available}")  # {'Alice', 'Charlie', 'Dave'}
```

---

### 🔹 Real-World Set Examples

```python
#  Find duplicate entries in a log file
log_entries = ["192.168.1.1", "10.0.0.1", "192.168.1.1",
               "172.16.0.1", "10.0.0.1", "192.168.1.1"]

unique_ips  = set(log_entries)
duplicates  = [ip for ip in log_entries if log_entries.count(ip) > 1]
unique_dups = set(duplicates)

print(f"Total entries: {len(log_entries)}")   # 6
print(f"Unique IPs:    {len(unique_ips)}")    # 3
print(f"Duplicate IPs: {unique_dups}")

# ✅ Find common elements across datasets
users_viewed_page_a = {"user1", "user2", "user3", "user4", "user5"}
users_viewed_page_b = {"user3", "user4", "user5", "user6", "user7"}
users_purchased     = {"user4", "user5", "user8"}

# Who saw page A AND B but didn't purchase?
saw_both   = users_viewed_page_a & users_viewed_page_b
no_purchase = saw_both - users_purchased
print(f"Potential leads: {no_purchase}")  # {'user3'}

# ✅ Quickly check if item exists (O(1) vs list O(n))
banned_words = {"spam", "phishing", "scam", "fraud"}
message = "This is a scam website"

for word in message.split():
    if word.lower() in banned_words:
        print(f"🚨 Banned word detected: '{word}'")
```

---

```
✅ Use MATCH-CASE when:
   → You have many specific value conditions to check
   → Replacing long if/elif chains
   → Matching against patterns, types, or structures

✅ Use NESTED IF when:
   → Decisions depend on the outcome of previous decisions
   → Keep nesting ≤ 3 levels for readability
   → Consider extracting deep nesting into helper functions

✅ Use LIST when:
   → You need an ordered, changeable collection
   → You need to add, remove, or sort items frequently
   → You need duplicates

✅ Use TUPLE when:
   → Data should NOT change (coordinates, config, DB records)
   → Returning multiple values from a function
   → Keys in a dictionary (lists can't be dict keys!)

✅ Use SET when:
   → You need unique values only
   → You need fast membership testing (x in set)
   → You need mathematical set operations (union, intersection)
```

---

> 🚀 **Practice Challenge:** Write a program that:  
> 1. Takes a list of student scores  
> 2. Uses match-case to assign grades  
> 3. Stores names in a tuple (immutable class roster)  
> 4. Uses a set to track which students passed  
> 5. Prints a summary using nested if for honors/standard/fail categories

---

*Happy Coding! 🐍 — Your DevOps Teacher*