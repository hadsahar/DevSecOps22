---
layout: default
title: Python Lab 2 - Practice Exercises
---

1. How can you convert the return value of input() into an integer? A float?
   What does the in operator do (between an element and a list)?
2. How do you write conditions in Python? What is the difference between else and elif?
3. How does Python know which lines belong to an if block?
4. Program: read 2 numbers and print the bigger
5. Program: read 3 numbers and print the biggest
6. Program: ask the user for a number and print "Even" or "Odd" (hint: use % 2)
7. Program: ask the user for a score (0-100) and print the grade (A, B, C, D, F)
   - 90-100 -> A
   - 80-89 -> B
   - 70-79 -> C
   - 60-69 -> D
   - 0-59 -> F
   - handle the case where the score is not in the range 0-100
8. Program: login simulation
   - Hardcode: `username = "admin"`, `password = "P@ssw0rd"`
   - Ask the user for username and password
   - Print `Welcome` if both correct, `Wrong username` if username wrong, `Wrong password` if username correct but password wrong

9. Program: shipping cost
   - Ask the user for country ("IL" or "US" or "EU")
   - Ask the user for total order amount
   - If total >= 300 -> free shipping
   - Else if country is "IL" -> shipping 20
   - Else if country is "US" -> shipping 50
   - Else -> shipping 70

10. Program: password rules
    - Ask the user for a password
    - Check if the password meets the following rules:
      - length at least 8
      - the first half of the passwords equals the second half

11. Challenge: parse "3 + 4 = 7" and print TRUE/FALSE (use .split())
12. Challenge: support more than one operator (not only +)
