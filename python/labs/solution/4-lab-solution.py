# Lab 4 - For Loops (Iteration Practice) Solutions

# ── Section 1 — List Iteration ────────────────────────────────────────────────

# Exercise 1.1 — Print All Services
services = ["nginx", "redis", "postgres"]

for service in services:
    print(service)

print()

# Exercise 1.2 — Build a New List (Uppercase)
services = ["nginx", "redis", "postgres"]
upper_services = []

for service in services:
    upper_services.append(service.upper())

print(upper_services)

print()

# Exercise 1.3 — Count Values Above a Threshold
cpu_usage = [12, 88, 76, 45, 90, 75, 77]
threshold = 75
count = 0

for usage in cpu_usage:
    if usage > threshold:
        count += 1

print(count)

print()

# ── Section 2 — String Iteration ─────────────────────────────────────────────

# Exercise 2.1 — Count a Character
log_line = "joey doesnt share food, how you doin'?"
target = "e"
count = 0

for char in log_line:
    if char == target:
        count += 1

print(count)

print()

# Exercise 2.2 — Extract Only Letters
msg = "DevSecOps-22!!!"
letters = ""

for char in msg:
    if char.isalpha():
        letters += char

print(letters)

print()

# ── Section 3 — Tuple Iteration ──────────────────────────────────────────────

# Exercise 3.1 — Validate Allowed Environments
allowed_envs = ("dev", "staging", "prod")
user_env = "prod"
is_allowed = False

for env in allowed_envs:
    if env == user_env:
        is_allowed = True

print(is_allowed)

print()

# Exercise 3.2 — Find the Longest Word
words = ("dev", "security", "ops", "automation")
longest = ""

for word in words:
    if len(word) > len(longest):
        longest = word

print(longest)

print()

# ── Section 4 — Set Iteration ─────────────────────────────────────────────────

# Exercise 4.1 — Print Unique Ports
ports = {22, 80, 443, 80, 22}

for port in ports:
    print(port)

print()

# Exercise 4.2 — Classify Secure vs Not Secure
ports = {22, 80, 443}

for port in ports:
    if port == 443:
        print("secure")
    else:
        print("not secure")
