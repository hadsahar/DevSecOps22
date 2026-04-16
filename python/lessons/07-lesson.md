---
layout: default
title: Python Lesson 7 - Functions
---

# Functions

---

## 1. Why functions matter

A **function** is a reusable block of code that performs a task.

Instead of copy-pasting the same logic over and over, you define it once and call it wherever you need it.

In DevOps you use functions constantly:

- Validate user input before running a deployment
- Push code to Git after checking ticket numbers
- Build cloud objects (EC2, S3, RDS) with consistent keys
- Apply logic across hundreds of servers or containers

---

## 2. Defining and calling a basic function

```python
def function_name():
    print('hello')


function_name()
function_name()
```

- `def` starts the definition.
- The function name follows Python naming conventions (snake_case).
- The indented block is the **body** — it runs every time you call the function.

### Adding a docstring

```python
def greet():
    '''
    this function prints hello to the user
    :return:
    '''
    print('hello')
```

A **docstring** is a string literal right below the `def` line. It documents what the function does and shows up in `help()`.

---

## 3. Parameters — giving the function input

### 3.1 Single parameter

```python
def greet_with_name(name):        # input ✓  output ✗
    print(f'hello {name}')
```

```python
greet_with_name('hodi')
```

### 3.2 Multiple parameters

```python
def greet_with_name_and_age(name, age):
    print(f'hello {name} , {age} years old ')
```

```python
greet_with_name_and_age('guy', 50)
```

### 3.3 Type hints (recommended)

```python
def greet_with_name_and_age(name: str, age: int):
    print(f'hello {name} , {age} years old ')
```

Type hints are **not enforced** at runtime, but they make code more readable and help your editor warn you about mistakes.

### 3.4 Passing a list as a parameter

```python
def greet_all(names: list):
    for name in names:
        greet_with_name(name)


greet_all(['or', 'elia', 'rotem'])
# greet_all(150)  # TypeError — int is not iterable
```

---

## 4. Return values — giving the function output

### 4.1 No return (returns `None`)

```python
def your_sum():
    x = 12 + 3    # x -> 15
    # nothing returned


print(your_sum())   # None
```

A function with no `return` statement always returns `None` (same idea as `null` / `void` in other languages).

### 4.2 Returning a value

```python
def my_sum(a, b):
    return a + b


def get_number():
    return 66


print(my_sum(1, 2))      # 3
ans = get_number()
print(ans)               # 66
print(get_number())      # 66
```

---

## 5. Default parameter values

You can give a parameter a **default value**. If the caller skips it, the default is used.

```python
def login(username='spooky33'):
    print(f'welcome back {username}')


login()               # uses default → welcome back spooky33
login('iusechatgpt')  # overrides default
```

### 5.1 Multiple defaults — positional vs keyword arguments

```python
def hard_login(username, password, otp=11, token=1):
    pass
```

```python
hard_login(1, 2, 3, 4)              # all positional
hard_login(14, 55, token=88)        # skip otp, set token by name
# hard_login(username=123, otp=1, 44, password=1)  # SyntaxError
```

**Rule:** positional arguments must come before keyword arguments in a call.

---

## 6. Real-world DevOps example — `git_save()`

```python
import time


def git_save(userid, ticket_number, version=0.1, approved=False, env='dev'):
    if approved:
        print(f'{userid} saved the code .....')
        time.sleep(2)
        print(f'git add ..........{1 + version}')
        time.sleep(1)
        print(f'git commit -m {ticket_number} fix ..')
    else:
        inline_approval = True if input('approved ? Y/N only ') == 'Y' else False
        if inline_approval:
            print(f'{userid} saved the code .....')
            time.sleep(2)
            print(f'git add ........{version}')
            time.sleep(1)
            print(f'git commit -m {ticket_number} fix ..')
        else:
            print('declined ')
            exit()
```

```python
# Various ways to call git_save:
git_save(147852, 'infra123')
git_save(147852, ticket_number='infra123', env='prd')
git_save(147852, 'infra123', 1.1, True, 'dev')
git_save(userid=147852, version=0.5, approved=True, ticket_number='infra123', env='prd')
# git_save(userid=147852, env='prd', 'infra123')  # SyntaxError
```

Key takeaways:
- `approved=False` and `env='dev'` are optional with sensible defaults.
- Keyword arguments let you skip optional parameters in the middle.
- You can mix positional and keyword arguments, but positionals must come first.

---

## 7. `*args` — variable number of positional arguments

What if you don't know in advance how many numbers you'll receive?

### 7.1 The problem

```python
def total(a, b):      return a + b       # works for 2
def total(a, b, c):   return a + b + c   # works for 3
# ... not scalable
```

### 7.2 Solution: `*args`

```python
def total(*args):       # args is a tuple
    print(type(args))   # <class 'tuple'>
    s = 0
    for arg in args:
        s += arg
    return s


print(total(1, 2, 3, 4, 5))   # 15
print(total(1))                # 1
print(total(55, 77))           # 132
# print(total('a','b','c',1,2,3))  # TypeError — can't add str + int
```

`*args` collects all extra positional arguments into a **tuple** named `args`.

### 7.3 Mixing fixed params, `*args`, and keyword-only params

```python
def foo(a, *args, z=123):
    print(a)
    print(args)
    print(z)
```

```python
foo(5)                           # a=5  args=()    z=123
foo(1, 2, 3, 4, 5, 6, 7, 8, 9)  # a=1  args=(2..9) z=123
foo(88, 84, 4, 4, 8, 48, 64, 6, z=88)  # z=88 (keyword only)
```

After `*args`, any parameter can **only** be passed by keyword — that's called a **keyword-only argument**.

### 7.4 Practical example: printing names

```python
def print_the_names(count, *names, lines=1):
    for name in names:
        for i in range(lines):
            print()
        print(name.upper())


print_the_names(4, 'avi', 'moshe', 'ziv', 'mor', 'eden', 'yaki')
```

---

## 8. `**kwargs` — variable number of keyword arguments

`**kwargs` collects any extra **keyword arguments** into a **dict**.

### 8.1 Basic usage

```python
def objs(**kwargs):        # kwargs is a dict
    print(type(kwargs))    # <class 'dict'>
    for k, v in kwargs.items():
        print(k, v)


objs(len=11, size='3XL', color=144)
objs(cal=1990, toppings='cheese')
```

### 8.2 Real-world DevOps example — `car_def()`

**Problem:** two end users submit car data, but they use different key names for the same attribute:

| Attribute | User 1 writes | User 2 writes |
|-----------|--------------|--------------|
| color     | `color`      | `clr`, `cr`, `c` |
| make      | `make`       | `m`, `mk`, `manufacturer` |

```python
def car_def(model, year, **kwargs):
    car = dict()
    car['model'] = model
    car['year'] = year
    for k, v in kwargs.items():
        if k in ['clr', 'cr', 'c', 'color']:
            car['color'] = v
        elif k in ['make', 'm', 'mk', 'manufacturer']:
            car['make'] = v
    return car


car1 = car_def('m4',  2026, make='bmw',  c='black')
car2 = car_def('Q7',  2020, manufacturer='audi', clr='white')

print(car1)   # {'model': 'm4', 'year': 2026, 'color': 'black', 'make': 'bmw'}
print(car2)   # {'model': 'Q7', 'year': 2020, 'color': 'white', 'make': 'audi'}
```

`**kwargs` makes your functions flexible to accept varying key names without breaking.

---

## 9. Combining `*args` and `**kwargs`

You can use both in the same function. The order must always be:

```
def func(fixed_args, *args, **kwargs):
```

```python
def debug_info(label, *values, **meta):
    print(f'[{label}]', values, meta)


debug_info('deploy', 'step1', 'step2', env='prod', version=1.2)
# [deploy] ('step1', 'step2') {'env': 'prod', 'version': 1.2}
```

---

## 10. Summary

| Concept | Syntax | What it does |
|---------|--------|--------------|
| Define a function | `def name():` | Creates a reusable block |
| Docstring | `'''...'''` | Documents the function |
| Parameter | `def f(x):` | Accepts input |
| Type hint | `def f(x: int):` | Documents expected type |
| Return | `return value` | Sends output back to caller |
| Default value | `def f(x=10):` | Optional parameter |
| Keyword argument | `f(x=5)` | Pass by name |
| `*args` | `def f(*args):` | Variable positional → tuple |
| `**kwargs` | `def f(**kwargs):` | Variable keyword → dict |

---

## 11. Quick recap

- Define with `def`, call by name.
- Use **type hints** to document expected types.
- Functions that don't `return` give back `None`.
- **Default parameters** make arguments optional — put them after required ones.
- **Positional arguments** must come before keyword arguments in a call.
- `*args` → tuple of extra positional values.
- `**kwargs` → dict of extra keyword values.
- Use `**kwargs` when users might pass data with inconsistent key names.

---
