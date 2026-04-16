# Lab 1 - Practice Exercises Solutions

# Exercise 1 - Two numbers: sum, subtraction, multiplication, division
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Sum:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
if b != 0:
    print("Division:", a / b)
else:
    print("Division: cannot divide by zero")

# Exercise 2 - Sentence: uppercase and count letter 'a'
sentence = input("Enter a sentence: ")
print(sentence.upper())
print("Count of 'a':", sentence.lower().count("a"))

# Exercise 3 - Print first half and second half using slicing
text = input("Enter a string: ")
half = len(text) // 2
print("First half:", text[:half])
print("Second half:", text[half:])

# Exercise 4 - Check if input is only letters using isalpha()
user_input = input("Enter text (no spaces): ")
print(user_input.isalpha())
