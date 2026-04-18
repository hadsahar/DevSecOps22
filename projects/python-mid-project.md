# Python – Mid project

## Question 1: Treasure Hunt Game

Write a Python program for a treasure hunt game.

**Step 1:** Create a new file (or delete the existing file upon initialization). Inside it, write a sequence of digits from 0 to 9. Each digit appears a random number of times (1-20 times). After the last digit 9, write the word `TREASURE`. Then, write the digits again in descending order (from 9 to 0), each appearing a random number of times (1-20 times).

```bash
000000000000011111111111122222222222222333333333333333344444444455555555555555555555555555555555555555555566666666666666666677788888888888889999999999999999999999999999 TREASURE 999999999999999999999999999999999999999988888888888888888888888877777777777777776666666666666666666666666666655555555555555555555555555444444444444444333333333333333333332222222222222222222221111111111111111
````
**Step 2:** Open the file in read-only mode. Allow the user to move forward or backward as they wish. The user moves a cursor until they hit one of the letters in `TREASURE`. Each time, print the character the user landed on. After finding the treasure, print how many moves it took.

```bash
Where you want to move? [1- forward 2-backwards]
1
How many characters?
30
You hit "1"
... again ... until hit one of the "TREASURE" letters...
```

**Challenge:** Maintain a leaderboard of the top 10 best results (in a file). At the end of each game, check if the player's score is lower than the 10th score in the table. If yes, ask for their name and insert their result into the file in the appropriate position (each line contains: score and player name). When the file is empty, all results are inserted.

---

## Question 2: Get File Size

Write a function called `GetFileSize` that receives a string representing a filename and returns the file size.

---

## Question 3: Validate String Format 

Write a function called `ValidateStringFormat` that receives a string and validates that it matches a specific pattern:
- Starts with 3 uppercase letters
- Followed by 4 digits
- Followed by 2 lowercase letters

Return `True` if valid, otherwise `False`. **Do not use regular expressions.**

---

## Question 4: Get Sum Size

Write a function called `GetSumSize` that receives a list of files and returns the sum of their sizes.

---

## Question 5: Get Words From File

Write a function called `GetWordsFromFile` that receives a string representing a filename and returns a list of all unique words that appeared in the file (no duplicates).

---

## Question 6: Generate Random Numbers File

Write a function called `GenerateRandomNumbersFile` that receives a filename and an integer `n`. Generate `n` random integers between 1 and 1000, calculate their:
- Average
- Standard deviation
- Median
- Mode

Then write all results (the generated numbers + statistics) to the file. **Use only the `random` module** (no NumPy or statistics module).

**Requirements:**
- Calculate standard deviation manually using the formula: √(Σ(x - μ)² / n)
- Calculate median (if n is even, average the two middle numbers)
- Calculate mode (if multiple modes, list all of them)

---

## Question 7: Write Reverse

Write a function called `WriteReverse` that receives:
- First parameter: input filename
- Second parameter: output filename

The function should read the input file and write its contents reversed (from end to beginning) into the output file.

---

## Question 8: Find Pattern Without Builtins 

Write a function called `FindPatternWithoutBuiltins` that receives a filename and a pattern string. Find all occurrences of the pattern in the file **without using** `find()`, `index()`, `in`, or regular expressions. Use only basic loops and string indexing. Return a list of starting positions where the pattern appears.

---

## Question 9: Add Word If Not Exist 

Write a function called `AddWordIfNotExist` that receives a filename and a word. If the word does not appear in the file, the program adds it to the end of the file.

---

## Submission Requirements

**You must solve Questions 1–5 and choose ONE of Questions 6–9 (total: 6 solved questions).**

After completing the code:

1. Upload the code to your GitHub repository
2. Send the repository link along with your **full name** and **phone number** to:  
   **hothaifazoubi@gmail.com**

---

## Best Practices Tips for Students

1. **Use meaningful variable names** – Avoid single-letter names except for loop counters (i, j, k). Names like `file_path`, `char_count`, `player_moves` are much better.

2. **Handle file exceptions** – Always use `try-except` blocks when working with files to catch `FileNotFoundError`, `PermissionError`, etc.

3. **Use `with` statements for file handling** – This ensures files are automatically closed even if an error occurs.

4. **Write modular code** – Each function should do one thing and do it well. Avoid functions that are too long (typically > 30-40 lines).

5. **Add docstrings** – Every function should have a docstring explaining what it does, its parameters, and return value.

6. **Use constants for magic numbers** – Instead of writing `1`, `2`, `20` directly, use named constants like `FORWARD = 1`, `BACKWARD = 2`, `MAX_RANDOM_REPEAT = 20`.

---

Good luck!