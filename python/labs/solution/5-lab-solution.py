# Lab 5 - Loops & Practice Challenges Solutions

import datetime
import random

# ── Section 1 — Date & Time ───────────────────────────────────────────────────

# Exercise 1.1 — Display Current Date and Time
now = datetime.datetime.now()
print("Current date and time :")
print(now.strftime("%Y-%m-%d %H:%M:%S"))

print()

# ── Section 2 — While Loops ───────────────────────────────────────────────────

# Exercise 2.1 — Guess a Number (1 to 9)
secret = random.randint(1, 9)

while True:
    guess = int(input("Guess a number between 1 and 9: "))
    if guess == secret:
        print("Well guessed!")
        break
    else:
        print("Wrong, try again!")

print()

# Exercise 2.2 — Reverse a Word (Using Loops)
word = input("Enter a word: ")
reversed_word = ""

for i in range(len(word) - 1, -1, -1):
    reversed_word += word[i]

print(reversed_word)

print()

# ── Section 3 — For Loops ─────────────────────────────────────────────────────

# Exercise 3.1 — Divisible by 7 and Multiple of 5 (1500 to 2700)
for num in range(1500, 2701):
    if num % 7 == 0 and num % 5 == 0:
        print(num)

print()

# Exercise 3.2 — Count Even and Odd Numbers
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9)

even_count = 0
odd_count = 0

for n in numbers:
    if n % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Number of even numbers :", even_count)
print("Number of odd numbers :", odd_count)

print()

# Exercise 3.3 — Multiplication Table (1 to 10)
num = int(input("Input a number: "))

for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

print()

# ── Section 4 — continue ──────────────────────────────────────────────────────

# Exercise 4.1 — Print 0 to 6 Except 3 and 6
result = []
for i in range(7):
    if i == 3 or i == 6:
        continue
    result.append(str(i))

print(" ".join(result))

print()

# ── Section 5 — Fibonacci ────────────────────────────────────────────────────

# Exercise 5.1 — Fibonacci Series (0 to 50)
a, b = 1, 1
fib_series = []

while a <= 50:
    fib_series.append(str(a))
    a, b = b, a + b

print(" ".join(fib_series))

print()

# ── Section 6 — Letters and Digits ───────────────────────────────────────────

# Exercise 6.1 — Count Letters and Digits
s = "Python 3.2"

letters = 0
digits = 0

for char in s:
    if char.isalpha():
        letters += 1
    elif char.isdigit():
        digits += 1

print("Letters", letters)
print("Digits", digits)

print()

# ── Section 7 — Challenge: Print Alphabet Pattern 'G' ────────────────────────

# Challenge 7.1 — Print the 'G' Pattern
print("  ***")
print(" *   *")
print(" *")
print(" * ***")
print(" *   *")
print(" *   *")
print("  ***")

print()

# ── Section 8 — Challenge: Adaptive Hangman Engine ───────────────────────────

# Challenge 8.1 — Adaptive Hangman Engine
word_pool = [
    "python", "script", "server", "devops", "clouds",
    "deploy", "docker", "branch", "commit", "rebase",
    "kernel", "socket", "router", "packet", "buffer",
    "thread", "module", "object", "lambda", "syntax"
]

word_length = int(input("Enter word length: "))
max_attempts = int(input("Enter max attempts: "))

possible_words = [w for w in word_pool if len(w) == word_length]

if not possible_words:
    print("No words available for that length.")
else:
    pattern = ["_"] * word_length
    guessed_letters = []
    attempts_left = max_attempts

    while attempts_left > 0 and "_" in pattern:
        print(f"\nWord: {' '.join(pattern)}")
        print(f"Attempts left: {attempts_left}")
        print(f"Guessed: {guessed_letters}")

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("Already guessed that letter!")
            continue

        guessed_letters.append(guess)

        groups = {}
        for word in possible_words:
            key = ""
            for i in range(word_length):
                if word[i] == guess:
                    key += guess
                else:
                    key += pattern[i]
            if key not in groups:
                groups[key] = []
            groups[key].append(word)

        best_key = ""
        best_size = 0
        for key in groups:
            if len(groups[key]) > best_size:
                best_size = len(groups[key])
                best_key = key

        possible_words = groups[best_key]

        new_pattern = list(best_key)
        revealed = False
        for i in range(word_length):
            if new_pattern[i] == guess:
                pattern[i] = guess
                revealed = True

        if not revealed:
            attempts_left -= 1
            print(f"Wrong! '{guess}' is not in the word.")
        else:
            print(f"Good guess! '{guess}' is in the word.")

    if "_" not in pattern:
        print(f"\nYou win! The word was: {''.join(pattern)}")
    else:
        print(f"\nGame over! A possible word was: {possible_words[0]}")
