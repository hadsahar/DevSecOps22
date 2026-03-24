---
layout: default
title: Python Lab 5 - Loops & Practice Challenges
---

#  Python Exercises & Labs
### Loops Practice (while | for | break | continue)

## Section 1 — Date & Time
---

###  Exercise 1.1 — Display Current Date and Time
**Scenario:** Print the current date and time.
**Starter Code:**
```python
import datetime

# YOUR CODE HERE
```
**Sample Output:**
```
Current date and time :
2014-07-05 14:34:14
```

---

## Section 2 — While Loops
---

###  Exercise 2.1 — Guess a Number (1 to 9)
**Scenario:** The program generates a random number and keeps asking the user to guess until correct.

**Rules:**
- Generate a random number between 1 and 9.
- If the guess is wrong, ask again.
- When correct, print `Well guessed!` and exit.

**Starter Code:**
```python
import random

secret = random.randint(1, 9)

# YOUR CODE HERE
```
**Expected Output (example):**
```
Guess a number between 1 and 9: 3
Wrong, try again!
Guess a number between 1 and 9: 7
Wrong, try again!
Guess a number between 1 and 9: 5
Well guessed!
```

---

###  Exercise 2.2 — Reverse a Word (Using Loops)
**Scenario:** Accept a word from the user and reverse it.

**Rules:**
- Use loops.
- Do not use slicing like `word[::-1]`.

**Starter Code:**
```python
word = input("Enter a word: ")
reversed_word = ""

# YOUR CODE HERE

print(reversed_word)
```
**Expected Output (example):**
```
Enter a word: hello
olleh
```

---

## Section 3 — For Loops
---

###  Exercise 3.1 — Divisible by 7 and Multiple of 5 (1500 to 2700)
**Scenario:** Find all numbers divisible by 7 and multiples of 5 between 1500 and 2700 (inclusive).

**Starter Code:**
```python
# YOUR CODE HERE
```
**Expected Output:**
- Print the numbers that match.

---

###  Exercise 3.2 — Count Even and Odd Numbers
**Scenario:** Count how many even and odd numbers exist in a series.

**Starter Code:**
```python
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9)

even_count = 0
odd_count = 0

# YOUR CODE HERE

print("Number of even numbers :", even_count)
print("Number of odd numbers :", odd_count)
```
**Expected Output:**
```
Number of even numbers : 5
Number of odd numbers : 4
```

---

###  Exercise 3.3 — Multiplication Table (1 to 10)
**Scenario:** Create the multiplication table of a user-provided number.

**Starter Code:**
```python
num = int(input("Input a number: "))

# YOUR CODE HERE
```
**Expected Output (example):**
```
Input a number: 6
6 x 1 = 6
6 x 2 = 12
6 x 3 = 18
6 x 4 = 24
6 x 5 = 30
6 x 6 = 36
6 x 7 = 42
6 x 8 = 48
6 x 9 = 54
6 x 10 = 60
```

---

## Section 4 — `continue`
---

###  Exercise 4.1 — Print 0 to 6 Except 3 and 6
**Scenario:** Print all numbers from 0 to 6 except 3 and 6.

**Rules:**
- Use `continue`.

**Starter Code:**
```python
# YOUR CODE HERE
```
**Expected Output:**
```
0 1 2 4 5
```

---

## Section 5 — Fibonacci
---

###  Exercise 5.1 — Fibonacci Series (0 to 50)
**Scenario:** Print Fibonacci numbers between 0 and 50.

**Rules:**
- Use loops.
- Print the series on one line, separated by spaces.

**Starter Code:**
```python
# YOUR CODE HERE
```
**Expected Output:**
```
1 1 2 3 5 8 13 21 34
```

---

## Section 6 — Letters and Digits
---

###  Exercise 6.1 — Count Letters and Digits
**Scenario:** Accept a string and calculate the number of digits and letters.

**Starter Code:**
```python
s = "Python 3.2"

letters = 0
digits = 0

# YOUR CODE HERE

print("Letters", letters)
print("Digits", digits)
```
**Expected Output:**
```
Letters 6
Digits 2
```

---

## Section 7 — Challenge: Print Alphabet Pattern 'G'
---

###  Challenge 7.1 — Print the 'G' Pattern
**Scenario:** Print the following pattern exactly.

**Expected Output:**
```
  ***
 *   *
 *
 * ***
 *   *
 *   *
  ***
```

**Starter Code:**
```python
# YOUR CODE HERE
```

---

## Section 8 — Challenge: Adaptive Hangman Engine
---

###  Challenge 8.1 — Adaptive Hangman Engine
**Scenario:** Build a smart Hangman system that "cheats" the player by dynamically changing the possible word list.

**Idea:**
- Instead of picking a fixed word, keep a list of possible words.
- Every guess, group the words by the pattern that guess creates.
- Always choose the largest group.

**Requirements:**
- Start with a list of words (at least 20 words), all the same length.
- Ask the user for:
  - word length
  - max attempts

**Core Logic:**
- Use a `while` loop to keep the game running until win/lose.
- Each round:
  - Ask user to guess a letter.
  - Use a `for` loop to group all possible words by their pattern.
  - Choose the largest group.
  - Update the displayed pattern.

**Win / Lose:**
- Player wins if they guess all letters.
- Player loses if attempts reach 0.

**Constraints:**
- No built-in libraries like `collections`
- No regex
- Only: `for`, `while`, `if`, lists, strings
- Must handle repeated guesses
- Must handle words with repeated letters
