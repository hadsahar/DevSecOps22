# Lab 3 - Match-Case, Nested If, Lists, Tuples & Sets Solutions

# ── Section 1 — Nested If Exercises ──────────────────────────────────────────

# Exercise 1.1 — ATM Machine
is_card_valid   = True
entered_pin     = 1234
correct_pin     = 1234
account_balance = 500
withdraw_amount = 200

if is_card_valid:
    print("Card accepted")
    if entered_pin == correct_pin:
        print("PIN verified")
        if account_balance >= withdraw_amount:
            print(f"Withdrawing ${withdraw_amount}...")
            account_balance -= withdraw_amount
            print("Success!")
            print(f"Remaining balance: ${account_balance}")
        else:
            print("Insufficient balance")
    else:
        print("Incorrect PIN")
else:
    print("Card is not valid")

print()

# Exercise 1.2 — Job Application Filter
years_experience = 5
has_degree       = True
can_start_now    = False
applicant_name   = "Sarah"

print(f"Reviewing application for: {applicant_name}")
if years_experience >= 3:
    print(f"Experience requirement met ({years_experience} years)")
    if has_degree:
        print("Education requirement met")
        if can_start_now:
            print("Fast-track interview")
        else:
            print("Schedule for next month")
    else:
        print("Consider for junior role")
else:
    print("Not eligible at this time")

print()

# Exercise 1.3 — Smart Home Thermostat
hour        = 14
is_home     = True
temperature = 18
is_winter   = True

if 6 <= hour < 12:
    period = "Morning"
elif 12 <= hour < 18:
    period = "Afternoon"
elif 18 <= hour < 23:
    period = "Evening"
else:
    period = "Night"

print(f"Time: {hour:02d}:00 — {period}")

if not is_home:
    print("Nobody is home — eco mode")
else:
    print("Someone is home")
    print(f" Current temperature: {temperature}°C")
    if period == "Morning":
        if temperature < 21:
            print(" It's cold — heating to 21°C")
        else:
            print(" Temperature is comfortable")
    elif period == "Afternoon":
        if temperature > 26:
            print(" It's hot — cooling to 23°C")
        elif temperature < 20:
            print(" It's chilly — heating to 20°C")
        else:
            print(" Temperature is comfortable")
    elif period == "Evening":
        print(" Setting comfort mode — 22°C")
    else:
        print(" Night eco mode — 17°C")

print()

# ── Section 2 — Match-Case Exercises ─────────────────────────────────────────

# Exercise 2.1 — Traffic Light Controller
light_color = "yellow"

match light_color:
    case "red":
        print("Stop! Do not cross.")
    case "yellow":
        print("Slow down, prepare to stop.")
    case "green":
        print("Go! Proceed safely.")
    case _:
        print("Unknown signal — treat as red.")

print()

# ── Section 3 — List Exercises ────────────────────────────────────────────────

# Exercise 3.1 — To-Do List Manager
todo = ["Buy groceries", "Call doctor", "Fix bug #42", "Read book"]

todo.append("Go to gym")
todo.insert(0, "Morning standup")
todo.remove("Read book")
todo[todo.index("Fix bug #42")] = " Fix bug #42"

print(f"To-Do List ({len(todo)} tasks):")
for i, task in enumerate(todo, 1):
    print(f"{i}. {task}")

print()

# Exercise 3.2 — Scoreboard
scores = [78, 92, 45, 88, 100, 63, 77, 55, 91, 84]

print("Highest:", max(scores))
print("Lowest: ", min(scores))
print(f"Average: {sum(scores) / len(scores):.2f}")
print("Ranked:", sorted(scores, reverse=True))
above_80 = [s for s in scores if s > 80]
print("Students above 80:", len(above_80))
print("Their scores:", above_80)

print()

# ── Bonus Challenge — Mini Python Academy ────────────────────────────────────
from collections import namedtuple

Student = namedtuple("Student", ["name", "exercises_done", "badges"])

topics_completed = ("Python Basics", "Conditions", "Loops", "Functions", "Lists")
total_topics = len(topics_completed)

students = [
    Student("Alice", ["ex1", "ex2", "ex3", "ex4", "ex5", "ex6", "ex7", "ex8", "ex9", "ex10"], set()),
    Student("Bob",   ["ex1", "ex2", "ex3", "ex4", "ex5"], set()),
    Student("Carol", ["ex1", "ex2", "ex3"], set()),
]

def award_badge(exercises_count):
    match True:
        case _ if exercises_count >= 9:
            return "gold"
        case _ if exercises_count >= 6:
            return "silver"
        case _ if exercises_count >= 3:
            return "bronze"
        case _:
            return None

leaderboard = []
all_badges = {"bronze", "silver", "gold"}

print("=== Mini Python Academy Dashboard ===")
for student in students:
    badge = award_badge(len(student.exercises_done))
    if badge:
        student.badges.add(badge)

    completion_pct = (len(topics_completed) / total_topics) * 100
    qualifies = (
        completion_pct >= 80
        and badge in ("silver", "gold")
    )

    leaderboard.append((student.name, len(student.exercises_done), badge))
    certificate = "✓ Certificate" if qualifies else "✗ No certificate"
    print(f"{student.name}: {len(student.exercises_done)} exercises | badge={badge} | {certificate}")

leaderboard.sort(key=lambda x: x[1], reverse=True)
print("\nLeaderboard:")
for rank, (name, count, badge) in enumerate(leaderboard, 1):
    print(f"  {rank}. {name} — {count} exercises ({badge})")

all_earners = {s.name for s in students if all_badges.issubset(s.badges)}
print(f"\nStudents with ALL badges: {all_earners if all_earners else 'None'}")
