---
layout: default
title: Python Lesson 5 - Loops (for/while/do-while), break/continue, loop else + random/time/datetime
---

# Loops (for/while/do-while), `break`/`continue`, loop `else` + `random` / `time` / `datetime`

---

## 1. What you used in `python5.py` (quick scan summary)

This class code demonstrates:

- `for` loops (including iterating over collections)
- `range()` patterns (start/stop/step, reverse)
- Nested loops (pattern printing)
- `continue` (skip an iteration)
- `break` (stop the loop)
- `for ... else` (else runs only if the loop finishes without `break`)
- `while` loops (repeat while condition is true)
- “do-while” style using `while True` + `break`
- Measuring time using `datetime.datetime.now()` and subtracting timestamps
- Using standard library modules: `random`, `time`, `datetime`

---

## 2. `for` loop (iterate over a collection)

Use `for` when you want to run the same logic for each item in an iterable.

### 2.1 Syntax

```python
for item in iterable:
    print(item)
```

### 2.2 Iterating over common collections

#### List

```python
services = ["ec2", "ebs", "rds"]
for s in services:
    print(s)
```

#### String

```python
name = "sahar"
for ch in name:
    print(ch)
```

#### Tuple

```python
envs = ("dev", "staging", "prod")
for env in envs:
    print(env)
```

#### Set

```python
ports = {22, 80, 443}
for p in ports:
    print(p)
```

---

## 3. `while` loop (repeat while a condition is true)

Use `while` when you don’t know how many iterations you need in advance.

### 3.1 Syntax

```python
while condition:
    # repeat
    pass
```

### 3.2 Example: keep asking until correct PIN

```python
pin = "1744"
guess = input("enter the pin code : ")

while guess != pin:
    guess = input("enter the pin code : ")

print("welcome")
```

---

## 4. “Do-While” in Python (emulation)

Python doesn’t have a real `do { } while (condition)` statement.

The common pattern is:

- `while True:` to run at least once
- then `break` when you want to stop

### 4.1 Example: stop only when user enters 100

```python
while True:
    x = int(input("enter a number  "))
    if x == 100:
        break
```

### 4.2 Example: menu loop (calculator idea)

```python
while True:
    print("press 1 for + or q to exit ")
    print("press 2 for - or q to exit ")
    print("press 3 for * or q to exit ")
    print("press 4 for // or q to exit ")

    choice = input(" : ")
    if choice == "q":
        break

    if choice in "1234":
        x = int(input("enter a number "))
        y = int(input("enter a number "))

    match choice:
        case "1":
            print(f"{x} + {y} = {x + y}")
        case "2":
            print(f"{x} - {y} = {x - y}")
        case "3":
            print(f"{x} * {y} = {x * y}")
        case "4":
            print(f"{x} // {y} = {x // y}")
        case _:
            print("invalid choice")
```

---

## 5. `break` vs `continue`

### 5.1 `break`

- Ends the loop immediately.
- Use it when you found what you need or when something failed.

```python
services = ["ec2", "s3", "rds"]
status = [True, False, True]

offline = None

for i in range(len(services)):
    if not status[i]:
        offline = services[i]
        break

print(offline)
```

### 5.2 `continue`

- Skips the rest of the current iteration and moves to the next.

```python
meals = ["starter", "salad", "main dish", "dessert"]

for meal in meals:
    if meal == "salad":
        continue
    print(meal)
```

---

## 6. Loop `else` (important)

Python has a special `else` on loops:

- The `else` block runs only if the loop finished **normally**
- The `else` block does **not** run if the loop ended with `break`

### 6.1 `for ... else` example (like your meals example)

```python
meals = ["starter", "salad", "main dish", "dessert"]

for meal in meals:
    if meal == "salad":
        continue
    print(f"{meal} is arriving")
else:
    print("discount 30% for ordering all the menu")
```

### 6.2 `for ... else` as a “search” pattern

```python
services = ["nginx", "redis", "postgres"]
target = "redis"

for s in services:
    if s == target:
        print("found")
        break
else:
    print("not found")
```

### 6.3 `while ... else`

Works the same idea:

```python
i = 0

while i < 3:
    pwd = input("enter password: ")
    if pwd == "secret":
        print("welcome")
        break
    i += 1
else:
    print("locked")
```

---

## 7. `import` basics (what it means)

Python has a huge standard library. `import` lets you use modules that live outside your current `.py` file.

### 7.1 Basic forms

```python
import random
import time
import datetime
```

Then you access things using the module name:

```python
x = random.randint(1, 10)
```

### 7.2 Import specific objects

```python
from datetime import datetime, timedelta
```

Then you can use them directly:

```python
now = datetime.now()
```

---

## 8. `random` module (full tutorial)

`random` is for pseudo-random numbers (good for games/simulations/tests). It is **not** for cryptography.

### 8.1 Common functions

#### `random.randint(a, b)`

Random integer, inclusive.

```python
import random
print(random.randint(-100, 1500))
```

#### `random.random()`

Random float between 0.0 and 1.0.

```python
import random
print(random.random())
```

#### `random.uniform(a, b)`

Random float between `a` and `b`.

```python
import random
print(random.uniform(10.0, 100.5))
```

#### `random.choice(seq)`

Pick one random item from a list/tuple/string.

```python
import random
colors = ["red", "blue", "yellow", "black"]
print(random.choice(colors))
print(random.choice(["heads", "tails"]))
```

#### `random.shuffle(list)`

Shuffles a list in-place.

```python
import random
cards = ["Ace", "King", "Queen", "Jack", "10"]
random.shuffle(cards)
print(cards)
```

#### `random.randrange(start, stop, step)`

Like picking a random value from a range.

```python
import random
print(random.randrange(1, 100, 2))
```

### 8.2 `random.seed()`

Use seed if you want repeatable results.

```python
import random
random.seed(42)
print(random.randint(1, 10))
print(random.randint(1, 10))
```

---

## 9. `time` module (full tutorial)

`time` is low-level time utilities.

### 9.1 `time.sleep(seconds)`

Pause execution.

```python
import time
print("x")
time.sleep(3)
print("y")
```

### 9.2 `time.time()`

Returns Unix timestamp (seconds since 1970).

```python
import time
print(time.time())
```

### 9.3 `time.ctime([seconds])`

Human-readable time string.

```python
import time
print(time.ctime())
```

### 9.4 Measuring elapsed time (recommended)

For measuring durations, prefer `time.perf_counter()`:

```python
import time

start = time.perf_counter()

time.sleep(0.5)

end = time.perf_counter()
print(end - start)
```

---

## 10. `datetime` module (full tutorial)

`datetime` is higher-level date/time tools.

### 10.1 Key classes

- `datetime.datetime`: date + time together
- `datetime.date`: only date
- `datetime.time`: only time
- `datetime.timedelta`: a duration (difference)

### 10.2 Get current date/time

```python
import datetime

t = datetime.datetime.now()
print(t)
print(t.date())
print(t.time())
print(t.month)
print(t.second)
print(t.microsecond)
```

### 10.3 Datetime arithmetic (duration)

```python
import datetime

start_time = datetime.datetime.now()

input("press Enter to stop")

end_time = datetime.datetime.now()
print(end_time - start_time)
```

### 10.4 `timedelta`

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now)
print(now + timedelta(days=7))
print(now - timedelta(hours=2))
```

### 10.5 Formatting: `strftime`

```python
from datetime import datetime

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
```

Common format codes:

- `%Y` year (2026)
- `%m` month (01-12)
- `%d` day (01-31)
- `%H` hour (00-23)
- `%M` minute (00-59)
- `%S` second (00-59)

### 10.6 Parsing: `strptime`

```python
from datetime import datetime

s = "2026-03-24 13:45:00"
dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
print(dt)
```

---

## 11. Practice tasks

### Loops

1. Ask the user for a password. Give them 3 tries. If correct: print `welcome` and stop. If not: after 3 tries print `locked`.
2. Given a list of services and a list of booleans for status, print which services are up. If a service is down, stop checking.
3. Use a `for ... else` loop to search for an item in a list and print `found` / `not found`.

### Modules

1. Use `random.choice()` to simulate coin toss 10 times and count heads vs tails.
2. Use `time.sleep()` to print a countdown message every second (no `range` required).
3. Use `datetime` to print:
   - current timestamp
   - timestamp after 3 days
   - elapsed time between two moments
