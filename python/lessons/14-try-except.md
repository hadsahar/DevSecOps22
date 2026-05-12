---
layout: default
title: Python Exception Handling: Try-Except and Custom Exceptions
---

# Python Exception Handling: Try-Except and Custom Exceptions

## Table of Contents

1. [Introduction to Exceptions](#1-introduction-to-exceptions)
2. [Basic Try-Except Syntax](#2-basic-try-except-syntax)
3. [Exception Types](#3-exception-types)
4. [Handling Multiple Exceptions](#4-handling-multiple-exceptions)
5. [The Else and Finally Blocks](#5-the-else-and-finally-blocks)
6. [Raising Exceptions](#6-raising-exceptions)
7. [Custom Exceptions](#7-custom-exceptions)
8. [Exception Chaining](#8-exception-chaining)
9. [Context Managers for Exception Handling](#9-context-managers-for-exception-handling)
10. [Best Practices](#10-best-practices)
11. [Common Mistakes](#11-common-mistakes)
12. [Practical Examples](#12-practical-examples)

---

## 1. Introduction to Exceptions

### What are Exceptions?

**Exceptions** are events that occur during program execution that disrupt the normal flow of the program. When an error occurs, Python raises an exception, which can be caught and handled.

### Why Handle Exceptions?

| Benefit | Description |
|---------|-------------|
| **Prevent Crashes** | Gracefully handle errors instead of crashing |
| **User Experience** | Provide meaningful error messages |
| **Debugging** | Log errors for troubleshooting |
| **Resource Cleanup** | Ensure resources (files, connections) are closed |
| **Recovery** | Allow program to continue after error |

### Exception Hierarchy

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    ├── AttributeError
    ├── NameError
    ├── IOError
    ├── ImportError
    ├── RuntimeError
    └── ... (and many more)
```

---

## 2. Basic Try-Except Syntax

### Basic Structure

```python
try:
    # Code that might raise an exception
    risky_code()
except ExceptionType:
    # Code to handle the exception
    handle_error()
```

### Simple Example

```python
# Without exception handling
result = 10 / 0  # ZeroDivisionError - program crashes

# With exception handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    # Output: Cannot divide by zero!
```

### Multiple Statements in Try Block

```python
try:
    # Multiple statements
    file = open('nonexistent.txt', 'r')
    content = file.read()
    file.close()
except FileNotFoundError:
    print("File not found!")
```

---

## 3. Exception Types

### Common Built-in Exceptions

| Exception | When Raised | Example |
|-----------|-------------|---------|
| `ZeroDivisionError` | Division by zero | `10 / 0` |
| `ValueError` | Invalid value for operation | `int("abc")` |
| `TypeError` | Operation on wrong type | `"2" + 3` |
| `IndexError` | Index out of range | `list[10]` on list of 5 items |
| `KeyError` | Key not found in dictionary | `dict['missing']` |
| `AttributeError` | Invalid attribute access | `"hello".length` |
| `FileNotFoundError` | File doesn't exist | `open('missing.txt')` |
| `NameError` | Name not defined | `print(undefined_var)` |
| `ImportError` | Module not found | `import nonexistent_module` |
| `RuntimeError` | Generic runtime error | `raise RuntimeError()` |

### Examples

```python
# ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")  # Error: division by zero

# ValueError
try:
    number = int("not a number")
except ValueError as e:
    print(f"Error: {e}")  # Error: invalid literal for int()

# TypeError
try:
    result = "hello" + 5
except TypeError as e:
    print(f"Error: {e}")  # Error: can only concatenate str

# IndexError
try:
    items = [1, 2, 3]
    print(items[10])
except IndexError as e:
    print(f"Error: {e}")  # Error: list index out of range

# KeyError
try:
    data = {'name': 'John'}
    print(data['age'])
except KeyError as e:
    print(f"Error: {e}")  # Error: 'age'

# AttributeError
try:
    text = "hello"
    print(text.length)  # Should be len(text)
except AttributeError as e:
    print(f"Error: {e}")  # Error: 'str' object has no attribute 'length'
```

---

## 4. Handling Multiple Exceptions

### Multiple Except Blocks

```python
try:
    # Risky code
    result = int(input("Enter a number: "))
    print(10 / result)
except ValueError:
    print("Please enter a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Catching Multiple Exceptions in One Block

```python
try:
    # Risky code
    result = int(input("Enter a number: "))
    print(10 / result)
except (ValueError, ZeroDivisionError) as e:
    print(f"Error occurred: {e}")
```

### Generic Exception Handler

```python
try:
    # Risky code
    result = 10 / 0
except ZeroDivisionError:
    print("Specific error: division by zero")
except Exception as e:
    print(f"Generic error: {e}")
```

### Accessing Exception Details

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception message: {e}")
    print(f"Exception args: {e.args}")
    # Output:
    # Exception type: ZeroDivisionError
    # Exception message: division by zero
    # Exception args: ('division by zero',)
```

### Exception Hierarchy

```python
try:
    result = 10 / 0
except ArithmeticError:  # Parent class of ZeroDivisionError
    print("Arithmetic error occurred")
except ZeroDivisionError:  # Never reached!
    print("Division by zero")
```

**Important**: More specific exceptions should come before general ones.

```python
# Correct order
try:
    result = 10 / 0
except ZeroDivisionError:  # More specific
    print("Division by zero")
except ArithmeticError:  # More general
    print("Arithmetic error")
except Exception:  # Most general
    print("Generic error")
```

---

## 5. The Else and Finally Blocks

### The Else Block

The `else` block executes if no exception occurs in the try block.

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print(f"Result is: {result}")  # Only runs if no exception
    # Output: Result is: 5.0
```

### The Finally Block

The `finally` block always executes, regardless of whether an exception occurred.

```python
try:
    file = open('example.txt', 'r')
    content = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("Cleanup code runs here")
    # This always runs
```

### Complete Structure

```python
try:
    # Code that might raise an exception
    file = open('example.txt', 'r')
    content = file.read()
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error: {e}")
else:
    print("File read successfully")
    print(content)
finally:
    print("Cleanup - always runs")
    # file.close() would go here
```

### Finally with Return

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    else:
        return result
    finally:
        print("Finally always runs!")

print(divide(10, 2))
# Finally always runs!
# 5.0

print(divide(10, 0))
# Finally always runs!
# Cannot divide by zero
```

### Resource Management with Finally

```python
file = None
try:
    file = open('example.txt', 'r')
    content = file.read()
    # Process content
except FileNotFoundError:
    print("File not found")
finally:
    if file:
        file.close()
    print("File closed")
```

---

## 6. Raising Exceptions

### Raising Built-in Exceptions

```python
# Raise a simple exception
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age < 18:
        raise ValueError("Must be 18 or older")
    return True

try:
    check_age(-5)
except ValueError as e:
    print(f"Error: {e}")  # Error: Age cannot be negative
```

### Raising with Custom Messages

```python
def calculate_discount(price, discount):
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    if discount < 0 or discount > 100:
        raise ValueError(f"Discount must be between 0-100: {discount}")
    return price * (1 - discount / 100)

try:
    calculate_discount(100, 150)
except ValueError as e:
    print(f"Error: {e}")  # Error: Discount must be between 0-100: 150
```

### Re-raising Exceptions

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Handling error...")
    raise  # Re-raise the same exception

# Output:
# Handling error...
# ZeroDivisionError: division by zero
```

### Raising Different Exception

```python
try:
    result = int("not a number")
except ValueError:
    print("Conversion failed")
    raise TypeError("Invalid input type") from None

# Output:
# Conversion failed
# TypeError: Invalid input type
```

### Conditional Raising

```python
def process_payment(amount):
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > 10000:
        raise ValueError("Amount exceeds maximum limit")
    return "Payment processed"

try:
    process_payment(-100)
except (TypeError, ValueError) as e:
    print(f"Payment failed: {e}")
```

---

## 7. Custom Exceptions

### Creating Custom Exceptions

```python
class CustomError(Exception):
    """Base custom exception"""
    pass

class InvalidAgeError(CustomError):
    """Exception for invalid age"""
    pass

class InsufficientFundsError(CustomError):
    """Exception for insufficient funds"""
    pass
```

### Custom Exception with Attributes

```python
class InsufficientFundsError(Exception):
    """Exception for insufficient bank balance"""
    
    def __init__(self, balance, required):
        self.balance = balance
        self.required = required
        message = f"Insufficient funds: ${balance} available, ${required} required"
        super().__init__(message)
    
    def __str__(self):
        return f"Balance: ${self.balance}, Required: ${self.required}"

# Usage
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(100, 200)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Balance: ${e.balance}, Required: ${e.required}")
```

### Custom Exception with Methods

```python
class ValidationError(Exception):
    """Custom validation exception with details"""
    
    def __init__(self, field, value, message):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(f"{field}: {message}")
    
    def get_details(self):
        return {
            'field': self.field,
            'value': self.value,
            'message': self.message
        }

# Usage
def validate_email(email):
    if '@' not in email:
        raise ValidationError('email', email, 'Must contain @ symbol')
    if '.' not in email.split('@')[1]:
        raise ValidationError('email', email, 'Must contain domain extension')
    return email

try:
    validate_email('invalid-email')
except ValidationError as e:
    print(f"Error: {e}")
    print(f"Details: {e.get_details()}")
```

### Exception Hierarchy

```python
class BankError(Exception):
    """Base exception for bank operations"""
    pass

class AccountError(BankError):
    """Exception for account-related errors"""
    pass

class InsufficientFundsError(AccountError):
    """Exception for insufficient funds"""
    pass

class InvalidAmountError(AccountError):
    """Exception for invalid amount"""
    pass

class TransactionError(BankError):
    """Exception for transaction errors"""
    pass

# Usage
def transfer(from_account, to_account, amount):
    if amount <= 0:
        raise InvalidAmountError(f"Invalid transfer amount: {amount}")
    if from_account.balance < amount:
        raise InsufficientFundsError(
            from_account.balance, 
            amount
        )
    # Process transfer
    return True

try:
    transfer(account1, account2, -100)
except InvalidAmountError as e:
    print(f"Invalid amount: {e}")
except InsufficientFundsError as e:
    print(f"Insufficient funds: {e}")
except BankError as e:
    print(f"Bank error: {e}")
```

### Custom Exception with Context

```python
class APIError(Exception):
    """Custom exception for API errors"""
    
    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"{status_code}: {message}")
    
    def to_dict(self):
        return {
            'status_code': self.status_code,
            'message': self.message,
            'details': self.details
        }

# Usage
def fetch_user(user_id):
    if user_id <= 0:
        raise APIError(
            status_code=400,
            message="Invalid user ID",
            details={'user_id': user_id}
        )
    # Fetch user
    return {'id': user_id, 'name': 'John'}

try:
    fetch_user(-1)
except APIError as e:
    print(f"Error: {e}")
    print(f"Details: {e.to_dict()}")
```

---

## 8. Exception Chaining

### Exception Chaining Basics

```python
try:
    try:
        result = 10 / 0
    except ZeroDivisionError:
        raise ValueError("Cannot process zero division")
except ValueError as e:
    print(f"Caught: {e}")
    print(f"Caused by: {e.__cause__}")
```

### Using `raise ... from`

```python
try:
    result = int("not a number")
except ValueError as e:
    raise TypeError("Invalid input") from e

# Shows the chain:
# TypeError: Invalid input
# The above exception was the direct cause of the following exception:
# ValueError: invalid literal for int()
```

### Suppressing Exception Context

```python
try:
    result = int("not a number")
except ValueError:
    raise TypeError("Invalid input") from None

# No exception chain shown
# TypeError: Invalid input
```

### Exception Context in Custom Exceptions

```python
class DataProcessingError(Exception):
    """Custom exception for data processing errors"""
    pass

def process_data(data):
    try:
        return int(data)
    except ValueError as e:
        raise DataProcessingError(f"Failed to process: {data}") from e

try:
    process_data("invalid")
except DataProcessingError as e:
    print(f"Error: {e}")
    print(f"Caused by: {e.__cause__}")
```

---

## 9. Context Managers for Exception Handling

### Using `with` Statement

```python
# Automatic resource cleanup
with open('example.txt', 'r') as file:
    content = file.read()
    # File automatically closed even if exception occurs
```

### Custom Context Manager

```python
from contextlib import contextmanager

@contextmanager
def safe_operation():
    try:
        print("Starting operation")
        yield
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    finally:
        print("Cleanup completed")

# Usage
with safe_operation():
    result = 10 / 0
```

### Context Manager Class

```python
class FileHandler:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing file")
        if self.file:
            self.file.close()
        # Return False to propagate exception, True to suppress
        return False

# Usage
with FileHandler('example.txt', 'r') as f:
    content = f.read()
```

### Suppressing Exceptions with Context Manager

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    # FileNotFoundError is suppressed
    with open('nonexistent.txt', 'r') as f:
        content = f.read()

print("Program continues")
```

---

## 10. Best Practices

### 1. Be Specific with Exceptions

```python
# ✅ GOOD - Specific exception
try:
    result = int(user_input)
except ValueError:
    print("Please enter a valid number")

# ❌ BAD - Too generic
try:
    result = int(user_input)
except Exception:
    print("Error occurred")
```

### 2. Handle Exceptions Appropriately

```python
# ✅ GOOD - Handle and recover
try:
    file = open('config.txt', 'r')
except FileNotFoundError:
    file = open('default_config.txt', 'r')

# ❌ BAD - Just pass (silent failure)
try:
    file = open('config.txt', 'r')
except:
    pass
```

### 3. Use Finally for Cleanup

```python
# ✅ GOOD - Ensure cleanup
file = None
try:
    file = open('data.txt', 'r')
    process_data(file)
except Exception as e:
    log_error(e)
finally:
    if file:
        file.close()

# ❌ BAD - Might not close on error
file = open('data.txt', 'r')
process_data(file)
file.close()
```

### 4. Provide Meaningful Error Messages

```python
# ✅ GOOD - Descriptive error
raise ValueError(f"Age must be positive, got: {age}")

# ❌ BAD - Generic error
raise ValueError("Invalid age")
```

### 5. Don't Catch Everything

```python
# ✅ GOOD - Specific exceptions
try:
    result = 10 / number
except ZeroDivisionError:
    handle_division_error()

# ❌ BAD - Catches everything (hard to debug)
try:
    result = 10 / number
except:
    pass
```

### 6. Use Custom Exceptions for Business Logic

```python
# ✅ GOOD - Custom exception
class InsufficientFundsError(Exception):
    pass

def withdraw(amount):
    if balance < amount:
        raise InsufficientFundsError()

# ❌ BAD - Using generic exception
def withdraw(amount):
    if balance < amount:
        raise Exception("No money")
```

### 7. Log Exceptions

```python
import logging

logging.basicConfig(level=logging.ERROR)

try:
    risky_operation()
except Exception as e:
    logging.error(f"Operation failed: {e}", exc_info=True)
    raise
```

---

## 11. Common Mistakes

### 1. Silent Failures

```python
# ❌ BAD - Silent failure
try:
    critical_operation()
except:
    pass  # Error is swallowed

# ✅ GOOD - At least log the error
try:
    critical_operation()
except Exception as e:
    logging.error(f"Error: {e}")
```

### 2. Catching Too Broad

```python
# ❌ BAD - Catches everything
try:
    operation()
except:
    pass

# ✅ GOOD - Specific exceptions
try:
    operation()
except (ValueError, TypeError) as e:
    handle_error(e)
```

### 3. Wrong Exception Order

```python
# ❌ BAD - Generic before specific
try:
    result = 10 / 0
except Exception:
    print("Generic error")
except ZeroDivisionError:
    print("Division by zero")  # Never reached

# ✅ GOOD - Specific before generic
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero")
except Exception:
    print("Generic error")
```

### 4. Not Using Finally for Resources

```python
# ❌ BAD - Resource might not close
file = open('data.txt', 'r')
try:
    process_data(file)
except Exception:
    pass
file.close()

# ✅ GOOD - Always closes
file = open('data.txt', 'r')
try:
    process_data(file)
except Exception:
    pass
finally:
    file.close()
```

### 5. Raising Generic Exceptions

```python
# ❌ BAD - Generic exception
if not email:
    raise Exception("Email required")

# ✅ GOOD - Specific exception
if not email:
    raise ValueError("Email is required")
```

---

## 12. Practical Examples

### Example 1: File Processing

```python
import os

def process_file(filename):
    """Process a file with proper error handling"""
    try:
        # Check if file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        # Open and read file
        with open(filename, 'r') as file:
            content = file.read()
        
        # Process content
        lines = content.splitlines()
        return len(lines)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 0
    except PermissionError as e:
        print(f"Permission denied: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0

# Usage
line_count = process_file('example.txt')
print(f"Line count: {line_count}")
```

### Example 2: API Error Handling

```python
class APIError(Exception):
    """Custom API error"""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded"""
    pass

class AuthenticationError(APIError):
    """Authentication failed"""
    pass

def fetch_data(url, headers=None):
    """Fetch data from API with error handling"""
    try:
        import requests
        response = requests.get(url, headers=headers)
        
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code >= 400:
            raise APIError(f"API error: {response.status_code}")
        
        return response.json()
        
    except requests.RequestException as e:
        raise APIError(f"Request failed: {e}")

# Usage
try:
    data = fetch_data('https://api.example.com/data')
except AuthenticationError as e:
    print("Authentication failed - check API key")
except RateLimitError as e:
    print("Rate limit exceeded - wait before retrying")
except APIError as e:
    print(f"API error: {e}")
```

### Example 3: User Input Validation

```python
class ValidationError(Exception):
    """Custom validation error"""
    pass

def get_positive_integer(prompt):
    """Get positive integer from user"""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValidationError("Value must be positive")
            return value
        except ValueError:
            print("Please enter a valid integer")
        except ValidationError as e:
            print(f"Error: {e}")

# Usage
age = get_positive_integer("Enter your age: ")
print(f"Age: {age}")
```

### Example 4: Database Operations

```python
class DatabaseError(Exception):
    """Base database error"""
    pass

class ConnectionError(DatabaseError):
    """Connection failed"""
    pass

class QueryError(DatabaseError):
    """Query failed"""
    pass

def execute_query(query, params=None):
    """Execute database query with error handling"""
    import sqlite3
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise ConnectionError(f"Database connection failed: {e}")
    except sqlite3.Error as e:
        raise QueryError(f"Query failed: {e}")
    except Exception as e:
        raise DatabaseError(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

# Usage
try:
    results = execute_query("SELECT * FROM users WHERE id = ?", (1,))
except ConnectionError as e:
    print(f"Connection error: {e}")
except QueryError as e:
    print(f"Query error: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
```

### Example 5: Retry Mechanism

```python
import time

class MaxRetriesExceededError(Exception):
    """Maximum retries exceeded"""
    pass

def retry_operation(operation, max_retries=3, delay=1):
    """Retry operation with exponential backoff"""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
    
    raise MaxRetriesExceededError(
        f"Operation failed after {max_retries} attempts. Last error: {last_error}"
    )

# Usage
def unreliable_operation():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Connection failed")
    return "Success"

try:
    result = retry_operation(unreliable_operation, max_retries=5)
    print(f"Result: {result}")
except MaxRetriesExceededError as e:
    print(f"Failed: {e}")
```

---

## Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Try-Except** | Catch and handle exceptions |
| **Multiple Exceptions** | Handle different exceptions differently |
| **Else Block** | Execute if no exception occurred |
| **Finally Block** | Always execute (cleanup) |
| **Raise** | Manually raise exceptions |
| **Custom Exceptions** | Create domain-specific exceptions |
| **Exception Chaining** | Link related exceptions |
| **Context Managers** | Automatic resource management |

### Best Practices Recap

1. **Be specific** with exception types
2. **Handle appropriately** - don't just pass
3. **Use finally** for cleanup
4. **Provide meaningful** error messages
5. **Don't catch everything** - be selective
6. **Use custom exceptions** for business logic
7. **Log exceptions** for debugging

---

## Practice Exercises

1. **File Processor**: Write a function that reads a file, processes it, and handles all possible errors
2. **User Input**: Create input validation with custom exceptions for different validation rules
3. **API Client**: Build an API client with proper error handling and retry logic
4. **Database Wrapper**: Create a database wrapper with custom exceptions for different error types
5. **Config Parser**: Write a configuration file parser with comprehensive error handling

---

## Additional Resources

- [Python Exception Handling Documentation](https://docs.python.org/3/tutorial/errors.html)
- [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Context Managers](https://docs.python.org/3/library/contextlib.html)
