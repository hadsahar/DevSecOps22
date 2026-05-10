# Python Object-Oriented Programming (OOP) - Complete Tutorial

## Table of Contents

1. [Introduction to OOP](#1-introduction-to-oop)
2. [Classes and Objects](#2-classes-and-objects)
3. [The Four Pillars of OOP](#3-the-four-pillars-of-oop)
   - [3.1 Encapsulation](#31-encapsulation)
   - [3.2 Inheritance](#32-inheritance)
   - [3.3 Polymorphism](#33-polymorphism)
   - [3.4 Abstraction](#34-abstraction)
4. [Special Methods (Magic/Dunder Methods)](#4-special-methods-magicdunder-methods)
5. [Class Methods and Static Methods](#5-class-methods-and-static-methods)
6. [Composition vs Inheritance](#6-composition-vs-inheritance)
7. [Best Practices](#7-best-practices)
8. [Practical Examples](#8-practical-examples)

---

## 1. Introduction to OOP

### What is Object-Oriented Programming?

**Object-Oriented Programming (OOP)** is a programming paradigm that organizes code around **objects** rather than functions and logic. It models real-world entities as software objects that contain:

- **Attributes (Data)**: Characteristics or properties of the object
- **Methods (Behavior)**: Actions the object can perform

### Why Use OOP?

| Benefit | Description |
|---------|-------------|
| **Modularity** | Code is organized into discrete, manageable units |
| **Reusability** | Classes can be reused across different programs |
| **Maintainability** | Easier to modify and extend code |
| **Data Protection** | Internal data can be hidden from external access |
| **Real-world Modeling** | Natural way to model real-world entities |

### Procedural vs Object-Oriented

```python
# Procedural Approach
def get_car_info(brand, model, year):
    return f"{year} {brand} {model}"

def start_car(brand, model):
    return f"Starting {brand} {model}..."

car_brand = "Toyota"
car_model = "Camry"
car_year = 2024

print(get_car_info(car_brand, car_model, car_year))
print(start_car(car_brand, car_model))
```

```python
# Object-Oriented Approach
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
    
    def get_info(self):
        return f"{self.year} {self.brand} {self.model}"
    
    def start(self):
        return f"Starting {self.brand} {self.model}..."

my_car = Car("Toyota", "Camry", 2024)
print(my_car.get_info())
print(my_car.start())
```

---

## 2. Classes and Objects

### What is a Class?

A **class** is a blueprint or template for creating objects. It defines:
- What attributes objects will have
- What methods objects can perform

### What is an Object?

An **object** (also called an **instance**) is a specific realization of a class. Each object has:
- Its own set of attribute values
- Access to all methods defined in its class

### Defining a Class

```python
class ClassName:
    """Class docstring - describes the class"""
    
    # Class attribute (shared by all instances)
    class_attribute = "I am shared"
    
    # Constructor method (initializer)
    def __init__(self, param1, param2):
        # Instance attributes (unique to each instance)
        self.attribute1 = param1
        self.attribute2 = param2
    
    # Instance method
    def method_name(self):
        return f"Method called with {self.attribute1}"
```

### Creating Objects (Instantiation)

```python
class Dog:
    # Class attribute
    species = "Canis familiaris"
    
    def __init__(self, name, age, breed):
        # Instance attributes
        self.name = name
        self.age = age
        self.breed = breed
    
    def bark(self):
        return f"{self.name} says: Woof!"
    
    def description(self):
        return f"{self.name} is a {self.age} year old {self.breed}"

# Creating objects (instances)
dog1 = Dog("Buddy", 3, "Golden Retriever")
dog2 = Dog("Max", 5, "German Shepherd")

# Accessing attributes
print(dog1.name)          # Output: Buddy
print(dog2.breed)         # Output: German Shepherd
print(Dog.species)        # Output: Canis familiaris

# Calling methods
print(dog1.bark())        # Output: Buddy says: Woof!
print(dog2.description()) # Output: Max is a 5 year old German Shepherd
```

### The `self` Parameter

- `self` refers to the current instance of the class
- It must be the first parameter of every instance method
- It's used to access attributes and methods within the class
- Python passes it automatically when calling methods

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width    # self.width belongs to this specific instance
        self.height = height  # self.height belongs to this specific instance
    
    def area(self):
        return self.width * self.height  # Uses self to access instance attributes
    
    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(5, 3)
print(rect.area())       # Output: 15
print(rect.perimeter())  # Output: 16
```

### Class vs Instance Attributes

```python
class Student:
    # Class attribute - shared by ALL instances
    school = "Python Academy"
    student_count = 0
    
    def __init__(self, name, grade):
        # Instance attributes - unique to EACH instance
        self.name = name
        self.grade = grade
        Student.student_count += 1  # Modify class attribute

# Creating instances
s1 = Student("Alice", 90)
s2 = Student("Bob", 85)

print(s1.school)           # Python Academy (accessed via instance)
print(Student.school)      # Python Academy (accessed via class)
print(Student.student_count)  # 2

# Changing class attribute
Student.school = "Python University"
print(s1.school)           # Python University
print(s2.school)           # Python University
```

---

## 3. The Four Pillars of OOP

The four fundamental principles of OOP are:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FOUR PILLARS OF OOP                              │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│  ENCAPSULATION  │   INHERITANCE   │  POLYMORPHISM   │  ABSTRACTION  │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Bundle data and │ Create new      │ Same interface, │ Hide complex  │
│ methods, hide   │ classes from    │ different       │ details, show │
│ internal state  │ existing ones   │ implementations │ only essential│
└─────────────────┴─────────────────┴─────────────────┴───────────────┘
```

---

### 3.1 Encapsulation

**Encapsulation** is the bundling of data (attributes) and methods that operate on that data within a single unit (class), while restricting direct access to some of the object's components.

#### Why Encapsulation?

- **Data Protection**: Prevent accidental modification of data
- **Controlled Access**: Validate data before modification
- **Flexibility**: Change internal implementation without affecting external code
- **Maintainability**: Easier to debug and maintain

#### Access Modifiers in Python

Python uses naming conventions (not strict enforcement):

| Convention | Syntax | Description |
|------------|--------|-------------|
| Public | `name` | Accessible everywhere |
| Protected | `_name` | Accessible in class and subclasses (convention) |
| Private | `__name` | Name mangling applied, harder to access |

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner         # Public
        self._account_id = "123"   # Protected (convention)
        self.__balance = balance   # Private (name mangling)
    
    # Getter method
    def get_balance(self):
        return self.__balance
    
    # Setter method with validation
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

account = BankAccount("John", 1000)

# Public - accessible
print(account.owner)        # John

# Protected - accessible but discouraged
print(account._account_id)  # 123

# Private - name mangling applied
# print(account.__balance)  # AttributeError!
print(account._BankAccount__balance)  # 1000 (not recommended)

# Proper way - use methods
print(account.get_balance())  # 1000
account.deposit(500)
print(account.get_balance())  # 1500
```

#### Property Decorators

The `@property` decorator provides a Pythonic way to implement getters and setters:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Getter for radius"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Setter for radius with validation"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """Deleter for radius"""
        print("Deleting radius...")
        del self._radius
    
    @property
    def area(self):
        """Read-only property"""
        return 3.14159 * self._radius ** 2
    
    @property
    def diameter(self):
        """Computed property"""
        return 2 * self._radius

# Usage
circle = Circle(5)
print(circle.radius)    # 5 (uses getter)
print(circle.area)      # 78.53975
print(circle.diameter)  # 10

circle.radius = 10      # Uses setter
print(circle.radius)    # 10

try:
    circle.radius = -5  # Validation in setter
except ValueError as e:
    print(e)  # Radius cannot be negative

# circle.area = 100  # AttributeError! (read-only)
```

#### Complete Encapsulation Example

```python
class Employee:
    """Demonstrates comprehensive encapsulation"""
    
    # Class attribute
    __employee_count = 0
    
    def __init__(self, name, salary, department):
        self._name = name
        self.__salary = salary
        self._department = department
        self.__id = Employee.__generate_id()
    
    @classmethod
    def __generate_id(cls):
        cls.__employee_count += 1
        return f"EMP{cls.__employee_count:04d}"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value
    
    @property
    def employee_id(self):
        """Read-only property"""
        return self.__id
    
    def give_raise(self, percentage):
        """Controlled method to modify salary"""
        if not 0 <= percentage <= 50:
            raise ValueError("Raise must be between 0-50%")
        self.__salary *= (1 + percentage / 100)
        return f"New salary: ${self.__salary:.2f}"
    
    def __str__(self):
        return f"{self.__id}: {self._name} ({self._department})"

# Usage
emp = Employee("John Doe", 50000, "Engineering")
print(emp)                    # EMP0001: John Doe (Engineering)
print(emp.employee_id)        # EMP0001 (read-only)
print(emp.salary)             # 50000

emp.salary = 55000            # Uses setter
print(emp.give_raise(10))     # New salary: $60500.00
```

---

### 3.2 Inheritance

**Inheritance** allows a class (child/derived class) to inherit attributes and methods from another class (parent/base class). This promotes code reusability and establishes a natural hierarchy.

#### Types of Inheritance

```
1. SINGLE INHERITANCE        2. MULTI-LEVEL INHERITANCE
   
   Parent                       Grandparent
     ↓                              ↓
   Child                         Parent
                                    ↓
                                  Child

3. MULTIPLE INHERITANCE      4. HIERARCHICAL INHERITANCE

   Parent1   Parent2              Parent
      ↘     ↙                    ↙  ↓  ↘
       Child                 Child1 Child2 Child3


5. HYBRID INHERITANCE

       Parent
      ↙     ↘
   Child1  Child2
      ↘     ↙
      GrandChild
```

#### Single Inheritance

```python
class Animal:
    """Parent/Base class"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def eat(self):
        return f"{self.name} is eating"

class Dog(Animal):
    """Child class inherits from Animal"""
    
    def __init__(self, name, age, breed):
        # Call parent constructor
        super().__init__(name, age)
        self.breed = breed
    
    def speak(self):
        """Override parent method"""
        return f"{self.name} says: Woof!"
    
    def fetch(self):
        """New method specific to Dog"""
        return f"{self.name} is fetching the ball"

class Cat(Animal):
    """Another child class"""
    
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def speak(self):
        return f"{self.name} says: Meow!"
    
    def climb(self):
        return f"{self.name} is climbing"

# Usage
dog = Dog("Buddy", 3, "Golden Retriever")
cat = Cat("Whiskers", 2, "Orange")

print(dog.name)      # Buddy (inherited attribute)
print(dog.eat())     # Buddy is eating (inherited method)
print(dog.speak())   # Buddy says: Woof! (overridden method)
print(dog.fetch())   # Buddy is fetching the ball (new method)

print(cat.speak())   # Whiskers says: Meow!
print(cat.climb())   # Whiskers is climbing
```

#### Multi-level Inheritance

```python
class Vehicle:
    """Grandparent class"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        return f"{self.brand} {self.model} starting..."

class Car(Vehicle):
    """Parent class - inherits from Vehicle"""
    
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors
    
    def drive(self):
        return f"Driving {self.brand} {self.model}"

class ElectricCar(Car):
    """Child class - inherits from Car"""
    
    def __init__(self, brand, model, doors, battery_capacity):
        super().__init__(brand, model, doors)
        self.battery = battery_capacity
    
    def charge(self):
        return f"Charging {self.battery}kWh battery"

# Usage
tesla = ElectricCar("Tesla", "Model 3", 4, 75)

# Access from all levels
print(tesla.start())   # From Vehicle (grandparent)
print(tesla.drive())   # From Car (parent)
print(tesla.charge())  # From ElectricCar (child)
print(tesla.doors)     # 4 (attribute from parent)
```

#### Multiple Inheritance

```python
class Flyable:
    """Mixin class for flying capability"""
    
    def __init__(self):
        self.altitude = 0
    
    def fly(self):
        self.altitude = 1000
        return "Flying high!"
    
    def land(self):
        self.altitude = 0
        return "Landed safely"

class Swimmable:
    """Mixin class for swimming capability"""
    
    def __init__(self):
        self.depth = 0
    
    def swim(self):
        self.depth = 10
        return "Swimming!"
    
    def surface(self):
        self.depth = 0
        return "Surfaced"

class Animal:
    def __init__(self, name):
        self.name = name

class Duck(Animal, Flyable, Swimmable):
    """Duck inherits from multiple classes"""
    
    def __init__(self, name):
        Animal.__init__(self, name)
        Flyable.__init__(self)
        Swimmable.__init__(self)
    
    def quack(self):
        return f"{self.name} says: Quack!"

# Usage
duck = Duck("Donald")
print(duck.quack())   # Donald says: Quack!
print(duck.fly())     # Flying high!
print(duck.swim())    # Swimming!
print(duck.land())    # Landed safely
```

#### Method Resolution Order (MRO)

Python uses **C3 Linearization** algorithm to determine the order in which base classes are searched:

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

# Check MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

d = D()
print(d.method())  # B (follows MRO: D -> B -> C -> A)
```

#### The `super()` Function

`super()` returns a proxy object that delegates method calls to a parent class:

```python
class Parent:
    def __init__(self, value):
        self.value = value
        print(f"Parent init: {value}")
    
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def __init__(self, value, extra):
        super().__init__(value)  # Call parent's __init__
        self.extra = extra
        print(f"Child init: {extra}")
    
    def greet(self):
        parent_greeting = super().greet()  # Call parent's method
        return f"{parent_greeting} and Child"

child = Child(10, 20)
# Output:
# Parent init: 10
# Child init: 20

print(child.greet())  # Hello from Parent and Child
```

#### `isinstance()` and `issubclass()`

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

dog = Dog()
cat = Cat()

# isinstance() - check if object is instance of class
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True (inheritance)
print(isinstance(dog, Cat))      # False

# issubclass() - check if class is subclass of another
print(issubclass(Dog, Animal))   # True
print(issubclass(Cat, Animal))   # True
print(issubclass(Dog, Cat))      # False
```

---

### 3.3 Polymorphism

**Polymorphism** means "many forms". It allows objects of different classes to be treated as objects of a common type. The same method or operator can behave differently based on the object it's acting on.

#### Types of Polymorphism

1. **Method Overriding** (Runtime Polymorphism)
2. **Duck Typing** (Pythonic Polymorphism)
3. **Operator Overloading** (Ad-hoc Polymorphism)

#### Method Overriding

Different classes implement the same method differently:

```python
class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement this")
    
    def describe(self):
        return f"I am a {self.__class__.__name__}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

# Polymorphism in action
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(6, 4)
]

# Same method call, different behavior
for shape in shapes:
    print(f"{shape.describe()}: Area = {shape.area():.2f}")

# Output:
# I am a Rectangle: Area = 15.00
# I am a Circle: Area = 50.27
# I am a Triangle: Area = 12.00
```

#### Duck Typing

> "If it walks like a duck and quacks like a duck, then it must be a duck."

Python doesn't require explicit inheritance for polymorphism - just the presence of required methods:

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "Beep boop!"

class Human:
    def speak(self):
        return "Hello!"

# Function that works with any object having speak() method
def make_speak(entity):
    print(entity.speak())

# Works with ANY object that has a speak() method
entities = [Dog(), Cat(), Robot(), Human()]

for entity in entities:
    make_speak(entity)

# Output:
# Woof!
# Meow!
# Beep boop!
# Hello!
```

#### Operator Overloading

Define custom behavior for operators using special methods:

| Operator | Method | Description |
|----------|--------|-------------|
| `+` | `__add__` | Addition |
| `-` | `__sub__` | Subtraction |
| `*` | `__mul__` | Multiplication |
| `/` | `__truediv__` | Division |
| `==` | `__eq__` | Equality |
| `<` | `__lt__` | Less than |
| `>` | `__gt__` | Greater than |
| `len()` | `__len__` | Length |
| `str()` | `__str__` | String representation |

```python
class Vector:
    """2D Vector with operator overloading"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Overload + operator"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """Overload - operator"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """Overload * operator (vector * scalar)"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """Support scalar * vector"""
        return self.__mul__(scalar)
    
    def __eq__(self, other):
        """Overload == operator"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __abs__(self):
        """Overload abs() - magnitude"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

# Usage
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)      # Vector(4, 6)
print(v1 - v2)      # Vector(2, 2)
print(v1 * 3)       # Vector(9, 12)
print(3 * v1)       # Vector(9, 12)
print(abs(v1))      # 5.0 (magnitude)
print(v1 == v2)     # False
print(v1 == Vector(3, 4))  # True
```

#### Function Polymorphism

Functions that work with different types:

```python
# Built-in len() works with different types
print(len("Hello"))        # 5 (string)
print(len([1, 2, 3]))      # 3 (list)
print(len({'a': 1, 'b': 2}))  # 2 (dict)

# Custom polymorphic function
def add(a, b):
    return a + b

print(add(5, 3))           # 8 (integers)
print(add(2.5, 3.5))       # 6.0 (floats)
print(add("Hello ", "World"))  # Hello World (strings)
print(add([1, 2], [3, 4]))     # [1, 2, 3, 4] (lists)
```

---

### 3.4 Abstraction

**Abstraction** hides complex implementation details and shows only the necessary features of an object. It defines a common interface while allowing different implementations.

#### Abstract Base Classes (ABC)

Python's `abc` module provides tools for creating abstract classes:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class - cannot be instantiated"""
    
    @abstractmethod
    def area(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Another abstract method"""
        pass
    
    def description(self):
        """Concrete method - can be used by subclasses"""
        return f"I am a {self.__class__.__name__}"

# Cannot instantiate abstract class
# shape = Shape()  # TypeError!

class Rectangle(Shape):
    """Concrete implementation"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """Another concrete implementation"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Usage
rect = Rectangle(5, 3)
circle = Circle(4)

print(rect.description())   # I am a Rectangle
print(rect.area())          # 15
print(circle.perimeter())   # 25.13272
```

#### Abstract Properties

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Abstract class with abstract properties"""
    
    @property
    @abstractmethod
    def max_speed(self):
        """Maximum speed in km/h"""
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        """Type of fuel"""
        pass
    
    @abstractmethod
    def start(self):
        pass

class SportsCar(Vehicle):
    @property
    def max_speed(self):
        return 350
    
    @property
    def fuel_type(self):
        return "Premium Gasoline"
    
    def start(self):
        return "VROOM! Engine started!"

class ElectricScooter(Vehicle):
    @property
    def max_speed(self):
        return 45
    
    @property
    def fuel_type(self):
        return "Electricity"
    
    def start(self):
        return "Beep! Powered on!"

# Usage
car = SportsCar()
scooter = ElectricScooter()

print(f"Car max speed: {car.max_speed} km/h")     # 350 km/h
print(f"Scooter fuel: {scooter.fuel_type}")       # Electricity
```

#### Real-World Abstraction Example

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract payment processor - defines interface"""
    
    @abstractmethod
    def process_payment(self, amount):
        """Process a payment"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id, amount):
        """Process a refund"""
        pass
    
    def validate_amount(self, amount):
        """Concrete method - shared validation"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return True

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card = card_number[-4:]  # Store last 4 digits
    
    def process_payment(self, amount):
        self.validate_amount(amount)
        return {"success": True, "card": f"****{self.card}", "amount": amount}
    
    def refund(self, transaction_id, amount):
        return {"success": True, "refund_id": f"REF-{transaction_id}"}

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def process_payment(self, amount):
        self.validate_amount(amount)
        fee = amount * 0.029 + 0.30
        return {"success": True, "email": self.email, "net": amount - fee}
    
    def refund(self, transaction_id, amount):
        return {"success": True, "refund_id": f"PP-{transaction_id}"}

# Usage - same interface, different implementations
def checkout(processor, amount):
    """Works with ANY payment processor"""
    result = processor.process_payment(amount)
    print(f"Payment result: {result}")

cc = CreditCardProcessor("4532015112830366")
pp = PayPalProcessor("user@example.com")

checkout(cc, 100)  # Credit card payment
checkout(pp, 100)  # PayPal payment
```

---

## 4. Special Methods (Magic/Dunder Methods)

Special methods (also called magic methods or dunder methods) allow you to define how objects behave with built-in operations.

### Common Special Methods

```python
class Book:
    def __init__(self, title, author, pages):
        """Constructor - called when creating object"""
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        """Human-readable string - str(obj), print(obj)"""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self):
        """Developer-readable string - repr(obj)"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        """Length - len(obj)"""
        return self.pages
    
    def __eq__(self, other):
        """Equality - obj1 == obj2"""
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False
    
    def __lt__(self, other):
        """Less than - obj1 < obj2"""
        if isinstance(other, Book):
            return self.pages < other.pages
        return NotImplemented
    
    def __hash__(self):
        """Hash - hash(obj), enables use in sets/dicts"""
        return hash((self.title, self.author))
    
    def __bool__(self):
        """Boolean - bool(obj), if obj:"""
        return self.pages > 0
    
    def __contains__(self, item):
        """Membership - item in obj"""
        return item.lower() in self.title.lower()

# Usage
book1 = Book("Python Crash Course", "Eric Matthes", 544)
book2 = Book("Clean Code", "Robert Martin", 464)

print(str(book1))        # 'Python Crash Course' by Eric Matthes
print(repr(book1))       # Book('Python Crash Course', 'Eric Matthes', 544)
print(len(book1))        # 544
print(book1 == book2)    # False
print(book1 < book2)     # False (544 > 464)
print("Python" in book1) # True
print(bool(book1))       # True
```

### Collection-like Methods

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []
    
    def add(self, song):
        self._songs.append(song)
    
    def __len__(self):
        """len(playlist)"""
        return len(self._songs)
    
    def __getitem__(self, index):
        """playlist[index] - enables indexing and iteration"""
        return self._songs[index]
    
    def __setitem__(self, index, value):
        """playlist[index] = value"""
        self._songs[index] = value
    
    def __delitem__(self, index):
        """del playlist[index]"""
        del self._songs[index]
    
    def __iter__(self):
        """for song in playlist:"""
        return iter(self._songs)
    
    def __contains__(self, song):
        """song in playlist"""
        return song in self._songs
    
    def __reversed__(self):
        """reversed(playlist)"""
        return reversed(self._songs)

# Usage
playlist = Playlist("My Favorites")
playlist.add("Song A")
playlist.add("Song B")
playlist.add("Song C")

print(len(playlist))        # 3
print(playlist[0])          # Song A
print(playlist[-1])         # Song C
print("Song B" in playlist) # True

for song in playlist:
    print(f"Playing: {song}")

playlist[1] = "New Song B"
print(playlist[1])          # New Song B
```

### Context Manager Methods

```python
class FileHandler:
    """Custom context manager for file handling"""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        # Return False to propagate exceptions, True to suppress
        return False

# Usage
# with FileHandler("test.txt", "w") as f:
#     f.write("Hello, World!")
# Output:
# Opening test.txt
# Closing test.txt
```

### Callable Objects

```python
class Multiplier:
    """Object that can be called like a function"""
    
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, value):
        """Makes the object callable"""
        return value * self.factor

# Usage
double = Multiplier(2)
triple = Multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Can be used as a function
numbers = [1, 2, 3, 4, 5]
doubled = list(map(double, numbers))
print(doubled)     # [2, 4, 6, 8, 10]
```

---

## 5. Class Methods and Static Methods

### Instance Methods (Default)

```python
class Counter:
    count = 0
    
    def __init__(self, value=0):
        self.value = value
        Counter.count += 1
    
    # Instance method - requires self
    def increment(self):
        self.value += 1
        return self.value

c = Counter(10)
print(c.increment())  # 11
```

### Class Methods (@classmethod)

- Bound to the class, not an instance
- First parameter is `cls` (the class itself)
- Can modify class state
- Often used as alternative constructors

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        """Alternative constructor - create from string"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Alternative constructor - create today's date"""
        import datetime
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)
    
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

# Usage
d1 = Date(2024, 1, 15)           # Regular constructor
d2 = Date.from_string("2024-06-20")  # From string
d3 = Date.today()                 # Today's date

print(d1)  # 2024-01-15
print(d2)  # 2024-06-20
```

### Static Methods (@staticmethod)

- Not bound to class or instance
- No automatic first parameter
- Used for utility functions related to the class

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        """Check if number is even"""
        return n % 2 == 0
    
    @staticmethod
    def is_prime(n):
        """Check if number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def factorial(n):
        """Calculate factorial"""
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# Usage - no instance needed
print(MathUtils.is_even(4))     # True
print(MathUtils.is_prime(17))   # True
print(MathUtils.factorial(5))   # 120
```

### Comparison Summary

```python
class Demo:
    class_var = "class variable"
    
    def __init__(self):
        self.instance_var = "instance variable"
    
    def instance_method(self):
        """Has access to self (instance) and cls (via self.__class__)"""
        return f"Instance: {self.instance_var}, Class: {self.class_var}"
    
    @classmethod
    def class_method(cls):
        """Has access to cls (class), not self (instance)"""
        return f"Class var: {cls.class_var}"
    
    @staticmethod
    def static_method():
        """No access to self or cls"""
        return "Static method - no access to instance or class"

d = Demo()
print(d.instance_method())      # Uses instance
print(Demo.class_method())      # Uses class
print(Demo.static_method())     # Standalone
```

---

## 6. Composition vs Inheritance

### When to Use Inheritance

Use inheritance for **"is-a"** relationships:
- A Dog **is a** Animal
- A Car **is a** Vehicle
- A Manager **is an** Employee

### When to Use Composition

Use composition for **"has-a"** relationships:
- A Car **has an** Engine
- A Library **has** Books
- A Computer **has** Components

### Composition Example

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
        self.running = False
    
    def start(self):
        self.running = True
        return "Engine started"
    
    def stop(self):
        self.running = False
        return "Engine stopped"

class Wheels:
    def __init__(self, size):
        self.size = size
        self.rotating = False
    
    def rotate(self):
        self.rotating = True
    
    def stop(self):
        self.rotating = False

class Car:
    """Car uses composition - it HAS an engine and wheels"""
    
    def __init__(self, brand, engine_hp, wheel_size):
        self.brand = brand
        self.engine = Engine(engine_hp)  # Composition
        self.wheels = [Wheels(wheel_size) for _ in range(4)]  # Composition
    
    def start(self):
        result = self.engine.start()
        for wheel in self.wheels:
            wheel.rotate()
        return f"{self.brand}: {result}"
    
    def stop(self):
        self.engine.stop()
        for wheel in self.wheels:
            wheel.stop()
        return f"{self.brand} stopped"

# Usage
car = Car("Toyota", 200, 17)
print(car.start())  # Toyota: Engine started
print(car.engine.horsepower)  # 200
```

### Favor Composition Over Inheritance

```python
# Instead of this (deep inheritance):
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

class SwimmingDog(Dog):  # Too deep!
    pass

# Consider this (composition):
class SwimmingAbility:
    def swim(self):
        return "Swimming!"

class Dog:
    def __init__(self, can_swim=False):
        self.swimming = SwimmingAbility() if can_swim else None
    
    def bark(self):
        return "Woof!"
    
    def swim(self):
        if self.swimming:
            return self.swimming.swim()
        return "This dog can't swim!"

dog1 = Dog(can_swim=True)
dog2 = Dog(can_swim=False)

print(dog1.swim())  # Swimming!
print(dog2.swim())  # This dog can't swim!
```

---

## 7. Best Practices

### 1. Single Responsibility Principle

Each class should have one reason to change:

```python
# Bad - class does too much
class Report:
    def calculate_data(self):
        pass
    def format_report(self):
        pass
    def save_to_file(self):
        pass
    def send_email(self):
        pass

# Good - separate concerns
class ReportCalculator:
    def calculate(self, data):
        pass

class ReportFormatter:
    def format(self, report):
        pass

class ReportSaver:
    def save(self, report, filename):
        pass
```

### 2. Open/Closed Principle

Classes should be open for extension but closed for modification:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

# Add new shapes without modifying existing code
class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2
```

### 3. Liskov Substitution Principle

Subtypes must be substitutable for their base types:

```python
class Bird:
    def fly(self):
        return "Flying"

# Bad - Penguin can't fly!
class Penguin(Bird):
    def fly(self):
        raise Exception("Can't fly!")  # Breaks LSP

# Good - separate flying and non-flying birds
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return "Swimming"
```

### 4. Interface Segregation Principle

Many specific interfaces are better than one general interface:

```python
# Bad - forcing implementations of unnecessary methods
class Worker:
    def work(self):
        pass
    def eat(self):
        pass

# Good - separate interfaces
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        return "Working"
    def eat(self):
        return "Eating"

class Robot(Workable):  # Robot doesn't need to eat
    def work(self):
        return "Working"
```

### 5. Dependency Inversion Principle

Depend on abstractions, not concrete implementations:

```python
from abc import ABC, abstractmethod

# Abstract interface
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

# Concrete implementations
class MySQLDatabase(Database):
    def save(self, data):
        return "Saved to MySQL"

class MongoDatabase(Database):
    def save(self, data):
        return "Saved to MongoDB"

# High-level module depends on abstraction
class UserService:
    def __init__(self, database: Database):  # Depends on abstraction
        self.db = database
    
    def create_user(self, user):
        return self.db.save(user)

# Can easily switch databases
mysql_service = UserService(MySQLDatabase())
mongo_service = UserService(MongoDatabase())
```

### 6. Use Meaningful Names

```python
# Bad
class C:
    def m(self, x):
        return x * 2

# Good
class NumberDoubler:
    def double(self, number):
        return number * 2
```

### 7. Keep Methods Small

```python
# Bad - method does too much
def process_order(self, order):
    # Validate
    # Calculate totals
    # Apply discounts
    # Save to database
    # Send email
    # Update inventory
    pass

# Good - break into smaller methods
def process_order(self, order):
    self._validate_order(order)
    total = self._calculate_total(order)
    total = self._apply_discounts(total, order)
    self._save_order(order, total)
    self._send_confirmation(order)
    self._update_inventory(order)
```

---

## 8. Practical Examples

### Example 1: E-commerce System

```python
from abc import ABC, abstractmethod
from datetime import datetime

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class ShoppingCart:
    def __init__(self):
        self._items = {}  # {product: quantity}
    
    def add_item(self, product, quantity=1):
        if product in self._items:
            self._items[product] += quantity
        else:
            self._items[product] = quantity
    
    def remove_item(self, product):
        if product in self._items:
            del self._items[product]
    
    @property
    def total(self):
        return sum(p.price * q for p, q in self._items.items())
    
    def __len__(self):
        return sum(self._items.values())

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def __init__(self, number, cvv):
        self.number = number[-4:]
        self.cvv = cvv
    
    def pay(self, amount):
        return f"Paid ${amount} with card ending in {self.number}"

class Order:
    _order_count = 0
    
    def __init__(self, cart, payment_method):
        Order._order_count += 1
        self.id = f"ORD-{Order._order_count:05d}"
        self.items = dict(cart._items)
        self.total = cart.total
        self.payment = payment_method
        self.date = datetime.now()
    
    def process(self):
        payment_result = self.payment.pay(self.total)
        return f"Order {self.id} processed: {payment_result}"

# Usage
laptop = Product("Laptop", 999.99, 10)
mouse = Product("Mouse", 29.99, 50)

cart = ShoppingCart()
cart.add_item(laptop, 1)
cart.add_item(mouse, 2)

print(f"Cart total: ${cart.total}")  # $1059.97
print(f"Items in cart: {len(cart)}")  # 3

payment = CreditCard("4532015112830366", "123")
order = Order(cart, payment)
print(order.process())
```

### Example 2: Game Character System

```python
from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.alive = True
    
    @abstractmethod
    def special_ability(self):
        pass
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            return f"{self.name} has been defeated!"
        return f"{self.name} takes {damage} damage. HP: {self.health}/{self.max_health}"
    
    def attack_enemy(self, enemy):
        if not self.alive:
            return f"{self.name} cannot attack (defeated)"
        damage = self.attack
        return enemy.take_damage(damage)

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack=20)
        self.shield = 30
    
    def special_ability(self):
        self.shield += 10
        return f"{self.name} raises shield! Defense +10"
    
    def take_damage(self, damage):
        reduced = max(0, damage - self.shield // 3)
        return super().take_damage(reduced)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack=15)
        self.mana = 100
    
    def special_ability(self):
        if self.mana >= 30:
            self.mana -= 30
            return f"{self.name} casts Fireball! 50 damage!"
        return f"{self.name} has no mana!"
    
    def cast_heal(self):
        if self.mana >= 20:
            self.mana -= 20
            heal = 30
            self.health = min(self.max_health, self.health + heal)
            return f"{self.name} heals for {heal}. HP: {self.health}"
        return "Not enough mana!"

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack=25)
        self.crit_chance = 0.3
    
    def special_ability(self):
        import random
        if random.random() < self.crit_chance:
            return f"{self.name} lands a CRITICAL HIT! Double damage!"
        return f"{self.name} performs a quick strike!"

# Usage
warrior = Warrior("Thor")
mage = Mage("Gandalf")
rogue = Rogue("Shadow")

print(warrior.special_ability())
print(mage.cast_heal())
print(warrior.attack_enemy(mage))
print(mage.health)
```

### Example 3: Logging System with Decorators

```python
from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps

class Logger(ABC):
    @abstractmethod
    def log(self, message, level):
        pass

class ConsoleLogger(Logger):
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

class FileLogger(Logger):
    def __init__(self, filename):
        self.filename = filename
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # In real implementation, would write to file
        print(f"Writing to {self.filename}: [{timestamp}] [{level}] {message}")

def log_calls(logger):
    """Decorator factory that logs function calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.log(f"{func.__name__} returned {result}")
            return result
        return wrapper
    return decorator

# Usage
console = ConsoleLogger()

@log_calls(console)
def add(a, b):
    return a + b

@log_calls(console)
def greet(name):
    return f"Hello, {name}!"

add(5, 3)
greet("Alice")
```

---

## Summary

### Key Concepts Recap

| Concept | Description | Python Implementation |
|---------|-------------|----------------------|
| **Class** | Blueprint for objects | `class ClassName:` |
| **Object** | Instance of a class | `obj = ClassName()` |
| **Encapsulation** | Data hiding | `_protected`, `__private`, `@property` |
| **Inheritance** | Reuse code from parent | `class Child(Parent):` |
| **Polymorphism** | Same interface, different behavior | Method overriding, duck typing |
| **Abstraction** | Hide complexity | `ABC`, `@abstractmethod` |

### The Four Pillars Summary

1. **Encapsulation**: Bundle data and methods, control access
2. **Inheritance**: Create hierarchies, reuse code
3. **Polymorphism**: Same interface, different implementations
4. **Abstraction**: Define interfaces, hide implementation

---

## Practice Exercises

1. **Create a Bank System**: Implement `BankAccount`, `SavingsAccount`, and `CheckingAccount` classes with inheritance and encapsulation.

2. **Build a Shape Calculator**: Create an abstract `Shape` class with `area()` and `perimeter()` methods. Implement `Rectangle`, `Circle`, `Triangle`.

3. **Design a Library System**: Create `Book`, `Member`, `Library` classes with composition. Include borrowing and returning functionality.

4. **Implement a Game**: Create a character system with `Character` base class, subclasses like `Warrior`, `Mage`, `Archer` with different abilities.

5. **Build a Notification System**: Abstract `Notifier` class with `EmailNotifier`, `SMSNotifier`, `PushNotifier` implementations.

---

## Additional Resources

- [Python Official Documentation - Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python ABC Module](https://docs.python.org/3/library/abc.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns](https://refactoring.guru/design-patterns/python)

---

> **Note**: See the code examples in `/python/classcode/python-oop/oop/` directory:
> - `inheritance.py` - Detailed inheritance examples
> - `polymorphism.py` - Polymorphism demonstrations
> - `abstraction.py` - Abstract classes examples
> - `encapsulation.py` - Encapsulation basics
> - `encapsulation_advanced.py` - Advanced encapsulation techniques
