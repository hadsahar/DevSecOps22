"""
=============================================================================
POLYMORPHISM IN PYTHON - Detailed Examples
=============================================================================
Polymorphism means "many forms". It allows objects of different classes
to be treated as objects of a common superclass. The same method name
can behave differently based on which object calls it.
=============================================================================
"""

from abc import ABC, abstractmethod
from math import pi


# =============================================================================
# EXAMPLE 1: Method Overriding (Runtime Polymorphism)
# =============================================================================
# Child classes provide specific implementations of methods defined in parent

class Shape(ABC):
    """Abstract base class for shapes"""
    
    @abstractmethod
    def area(self):
        """Calculate area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate perimeter of the shape"""
        pass
    
    def describe(self):
        return f"I am a {self.__class__.__name__}"


class Rectangle(Shape):
    """Rectangle implementation"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Circle implementation"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * pi * self.radius


class Triangle(Shape):
    """Triangle implementation"""
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        # Heron's formula
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self):
        return self.a + self.b + self.c


# =============================================================================
# EXAMPLE 2: Duck Typing (Pythonic Polymorphism)
# =============================================================================
# "If it walks like a duck and quacks like a duck, it's a duck"
# No need for inheritance - just implement the required methods

class Dog:
    def speak(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"


class Cat:
    def speak(self):
        return "Meow!"
    
    def move(self):
        return "Walking gracefully"


class Robot:
    def speak(self):
        return "Beep boop!"
    
    def move(self):
        return "Rolling on wheels"


class Human:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"Hello, I'm {self.name}!"
    
    def move(self):
        return "Walking on two legs"


def make_speak(entity):
    """Function that works with any object that has a speak() method"""
    print(f"Entity says: {entity.speak()}")


def make_move(entity):
    """Function that works with any object that has a move() method"""
    print(f"Movement: {entity.move()}")


# =============================================================================
# EXAMPLE 3: Operator Overloading (Ad-hoc Polymorphism)
# =============================================================================
# The same operator behaves differently based on operand types

class Vector:
    """2D Vector with overloaded operators"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Overload + operator"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector to Vector")
    
    def __sub__(self, other):
        """Overload - operator"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        raise TypeError("Can only subtract Vector from Vector")
    
    def __mul__(self, scalar):
        """Overload * operator for scalar multiplication"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        raise TypeError("Can only multiply Vector by scalar")
    
    def __rmul__(self, scalar):
        """Support scalar * vector"""
        return self.__mul__(scalar)
    
    def __eq__(self, other):
        """Overload == operator"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __abs__(self):
        """Overload abs() function - returns magnitude"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


class Money:
    """Money class with operator overloading"""
    
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
    
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.amount + other.amount, self.currency)
            raise ValueError("Cannot add different currencies")
        elif isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        raise TypeError("Unsupported operand type")
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.amount - other.amount, self.currency)
            raise ValueError("Cannot subtract different currencies")
        elif isinstance(other, (int, float)):
            return Money(self.amount - other, self.currency)
        raise TypeError("Unsupported operand type")
    
    def __mul__(self, multiplier):
        if isinstance(multiplier, (int, float)):
            return Money(self.amount * multiplier, self.currency)
        raise TypeError("Can only multiply by number")
    
    def __rmul__(self, multiplier):
        return self.__mul__(multiplier)
    
    def __gt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount > other.amount
        raise ValueError("Cannot compare different currencies")
    
    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        raise ValueError("Cannot compare different currencies")
    
    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return False
    
    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"


# =============================================================================
# EXAMPLE 4: Function Polymorphism with *args
# =============================================================================

class Calculator:
    """Calculator demonstrating polymorphic methods"""
    
    @staticmethod
    def add(*args):
        """Add any number of arguments"""
        return sum(args)
    
    @staticmethod
    def multiply(*args):
        """Multiply any number of arguments"""
        result = 1
        for num in args:
            result *= num
        return result
    
    @staticmethod
    def concatenate(*args, separator=" "):
        """Concatenate strings - works with any number of strings"""
        return separator.join(str(arg) for arg in args)


# =============================================================================
# EXAMPLE 5: Polymorphism with Built-in Functions
# =============================================================================

class BookCollection:
    """Collection of books with len() and iter() support"""
    
    def __init__(self):
        self.books = []
    
    def add_book(self, title):
        self.books.append(title)
    
    def __len__(self):
        """Support len() function"""
        return len(self.books)
    
    def __iter__(self):
        """Support iteration"""
        return iter(self.books)
    
    def __getitem__(self, index):
        """Support indexing"""
        return self.books[index]
    
    def __contains__(self, title):
        """Support 'in' operator"""
        return title in self.books


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("METHOD OVERRIDING EXAMPLE")
    print("=" * 60)
    
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5)
    ]
    
    # Same method call, different behavior based on object type
    for shape in shapes:
        print(f"\n{shape.describe()}")
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")
    
    print("\n" + "=" * 60)
    print("DUCK TYPING EXAMPLE")
    print("=" * 60)
    
    entities = [Dog(), Cat(), Robot(), Human("Alice")]
    
    for entity in entities:
        make_speak(entity)
        make_move(entity)
        print()
    
    print("=" * 60)
    print("OPERATOR OVERLOADING EXAMPLE - Vector")
    print("=" * 60)
    
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"2 * v2 = {2 * v2}")
    print(f"|v1| (magnitude) = {abs(v1)}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 == Vector(3, 4): {v1 == Vector(3, 4)}")
    
    print("\n" + "=" * 60)
    print("OPERATOR OVERLOADING EXAMPLE - Money")
    print("=" * 60)
    
    wallet1 = Money(100, "USD")
    wallet2 = Money(50, "USD")
    
    print(f"Wallet 1: {wallet1}")
    print(f"Wallet 2: {wallet2}")
    print(f"Total: {wallet1 + wallet2}")
    print(f"Difference: {wallet1 - wallet2}")
    print(f"Double wallet1: {wallet1 * 2}")
    print(f"wallet1 > wallet2: {wallet1 > wallet2}")
    
    print("\n" + "=" * 60)
    print("FUNCTION POLYMORPHISM EXAMPLE")
    print("=" * 60)
    
    calc = Calculator()
    print(f"add(1, 2): {calc.add(1, 2)}")
    print(f"add(1, 2, 3, 4, 5): {calc.add(1, 2, 3, 4, 5)}")
    print(f"multiply(2, 3): {calc.multiply(2, 3)}")
    print(f"multiply(2, 3, 4): {calc.multiply(2, 3, 4)}")
    print(f"concatenate('Hello', 'World'): {calc.concatenate('Hello', 'World')}")
    print(f"concatenate('a', 'b', 'c', separator='-'): {calc.concatenate('a', 'b', 'c', separator='-')}")
    
    print("\n" + "=" * 60)
    print("BUILT-IN FUNCTION POLYMORPHISM")
    print("=" * 60)
    
    library = BookCollection()
    library.add_book("Python Crash Course")
    library.add_book("Clean Code")
    library.add_book("Design Patterns")
    
    print(f"Number of books: {len(library)}")
    print(f"First book: {library[0]}")
    print(f"'Clean Code' in library: {'Clean Code' in library}")
    print("\nAll books:")
    for book in library:
        print(f"  - {book}")
