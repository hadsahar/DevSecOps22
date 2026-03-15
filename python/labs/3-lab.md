---
layout: default
title: Python Lab 3 - Match-Case, Nested If, Lists, Tuples & Sets
---

# Python Exercises & Labs

### Match-Case | Nested If | List | Tuple | Set

> **Instructions:** Each exercise gives you starter code with variables already set.  
> Your job is to **fill in the logic** and make the output match the expected result.  
>  = Beginner | = Intermediate | = Advanced

## Section 1 — Nested If Exercises

---

### Exercise 1.1 — ATM Machine

**Scenario:** You're building the logic for an ATM. The user must be verified before they can withdraw, and the balance must be sufficient.
**Starter Code:**

```python
is_card_valid   = True
entered_pin     = 1234
correct_pin     = 1234
account_balance = 500
withdraw_amount = 200
# YOUR CODE HERE
# Step 1: Check if the card is valid
# Step 2: If valid, check if the PIN is correct
# Step 3: If PIN correct, check if balance >= withdraw amount
# Step 4: If enough balance, print success and show new balance
# Step 5: Handle every failure case with a message
```

**Expected Output:**

```
Card accepted
PIN verified
Withdrawing $200...
Success!
Remaining balance: $300
```

---

### Exercise 1.2 — Job Application Filter

**Scenario:** A company filters job applicants based on experience, education, and availability.
**Requirements:**

- Must have **3+ years** of experience
- Must have a **degree** (any level)
- If both met → check if they can start **immediately**
- If yes → "Fast-track interview"
- If no → "Schedule for next month"
- If experience met but no degree → "Consider for junior role"
- If no experience → "Not eligible at this time"
  **Starter Code:**

```python
years_experience = 5
has_degree       = True
can_start_now    = False
applicant_name   = "Sarah"
```

**Expected Output:**

```
Reviewing application for: Sarah
Experience requirement met (5 years)
Education requirement met
Schedule for next month
```

---

### Exercise 1.3 — Smart Home Thermostat

**Scenario:** A smart thermostat adjusts settings based on time of day, whether someone is home, and current temperature.
**Starter Code:**

```python
hour        = 14       # 24-hour format (14 = 2pm)
is_home     = True
temperature = 18       # Celsius
is_winter   = True
# YOUR CODE HERE
# Morning (6-12): if home and cold → heat to 21°C
# Afternoon (12-18): if home and hot (>26) → cool to 23°C; if cold → heat to 20°C
# Evening (18-23): if home → set to 22°C comfort mode
# Night (23-6): eco mode → set to 17°C regardless
# If nobody is home: eco mode always
```

**Expected Output:**

```
Time: 14:00 — Afternoon
Someone is home
 Current temperature: 18°C
 It's chilly — heating to 20°C
```

---

## Section 2 — Match-Case Exercises

---

### Exercise 2.1 — Traffic Light Controller

**Starter Code:**

```python
light_color = "yellow"
# "red"    → Stop! Do not cross.
# "yellow" → Slow down, prepare to stop.
# "green"  → Go! Proceed safely.
# anything else → Unknown signal — treat as red.
```

**Expected Output:**

```
Slow down, prepare to stop.
```

---

## Section 3 — List Exercises

---

### Exercise 3.1 — To-Do List Manager

**Starter Code:**

```python
todo = ["Buy groceries", "Call doctor", "Fix bug #42", "Read book"]
# 1. Add "Go to gym" to the end
# 2. Add "Morning standup" at position 0 (beginning)
# 3. Remove "Read book"
# 4. Mark "Fix bug #42" as done by replacing it → " Fix bug #42"
# 5. Print total tasks
# 6. Print each task with a number (1. 2. 3. ...)
```

**Expected Output:**

```
To-Do List (5 tasks):
1. Morning standup
2. Buy groceries
3. Call doctor
4.  Fix bug #42
5. Go to gym
```

---

### Exercise 3.2 — Scoreboard

**Starter Code:**

```python
scores = [78, 92, 45, 88, 100, 63, 77, 55, 91, 84]
# YOUR CODE HERE:
# 1. Print highest score
# 2. Print lowest score
# 3. Print average score (2 decimal places)
# 4. Print sorted scores from highest to lowest
# 5. Print how many students scored above 80
# 6. Print scores above 80 as a new list (use list comprehension)
```

**Expected Output:**

```
Highest: 100
Lowest:  45
Average: 77.30
Ranked: [100, 92, 91, 88, 84, 78, 77, 63, 55, 45]
Students above 80: 5
Their scores: [92, 88, 100, 91, 84]
```

## Bonus Challenge — Bring It All Together

```
Build a "Mini Python Academy" tracker:
Data to track:
- Students (namedtuple): name, exercises_done (list), badges (set)
- Topics completed (tuple — immutable syllabus)
- Leaderboard (list of tuples, sorted by score)
Features to implement:
- Award badges using match-case (bronze/silver/gold based on exercises done)
- Use nested if to check if student qualifies for certificate:
   - Must complete 80%+ of topics
   - Must have silver or gold badge
   - No failed exercises
- Use set operations to find:
   - Students who earned ALL badges
   - Topics nobody has completed yet
- Print a full academy dashboard
```
