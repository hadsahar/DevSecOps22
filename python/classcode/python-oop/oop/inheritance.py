"""
=============================================================================
INHERITANCE IN PYTHON - Detailed Examples
=============================================================================
Inheritance allows a class (child/derived) to inherit attributes and methods
from another class (parent/base). This promotes code reusability.
=============================================================================
"""

# =============================================================================
# EXAMPLE 1: Single Inheritance
# =============================================================================
# One child class inherits from one parent class

class Animal:
    """Base class representing an animal"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def eat(self):
        return f"{self.name} is eating."
    
    def sleep(self):
        return f"{self.name} is sleeping."
    
    def speak(self):
        return f"{self.name} makes a sound."


class Dog(Animal):
    """Dog class inherits from Animal"""
    
    def __init__(self, name, age, breed):
        # Call parent constructor using super()
        super().__init__(name, age)
        self.breed = breed
    
    def speak(self):
        # Override parent method
        return f"{self.name} says: Woof! Woof!"
    
    def fetch(self):
        # New method specific to Dog
        return f"{self.name} is fetching the ball!"


class Cat(Animal):
    """Cat class inherits from Animal"""
    
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def speak(self):
        return f"{self.name} says: Meow!"
    
    def climb(self):
        return f"{self.name} is climbing the tree!"


# =============================================================================
# EXAMPLE 2: Multi-level Inheritance
# =============================================================================
# A class inherits from a class that inherits from another class
# Grandparent -> Parent -> Child

class Vehicle:
    """Grandparent class"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        return f"{self.brand} {self.model} is starting..."
    
    def stop(self):
        return f"{self.brand} {self.model} is stopping..."


class Car(Vehicle):
    """Parent class - inherits from Vehicle"""
    
    def __init__(self, brand, model, num_doors):
        super().__init__(brand, model)
        self.num_doors = num_doors
    
    def drive(self):
        return f"Driving the {self.brand} {self.model}"
    
    def honk(self):
        return "Beep! Beep!"


class ElectricCar(Car):
    """Child class - inherits from Car which inherits from Vehicle"""
    
    def __init__(self, brand, model, num_doors, battery_capacity):
        super().__init__(brand, model, num_doors)
        self.battery_capacity = battery_capacity
        self.charge_level = 100
    
    def charge(self):
        self.charge_level = 100
        return f"{self.brand} {self.model} is fully charged!"
    
    def get_range(self):
        return f"Estimated range: {self.battery_capacity * 4} km"


# =============================================================================
# EXAMPLE 3: Multiple Inheritance
# =============================================================================
# A class inherits from multiple parent classes

class Flyable:
    """Mixin class for flying capability"""
    
    def __init__(self):
        self.is_flying = False
    
    def fly(self):
        self.is_flying = True
        return "Taking off into the sky!"
    
    def land(self):
        self.is_flying = False
        return "Landing safely."


class Swimmable:
    """Mixin class for swimming capability"""
    
    def __init__(self):
        self.is_swimming = False
    
    def swim(self):
        self.is_swimming = True
        return "Swimming in the water!"
    
    def dive(self):
        return "Diving deep!"


class Duck(Animal, Flyable, Swimmable):
    """Duck inherits from Animal, Flyable, and Swimmable"""
    
    def __init__(self, name, age):
        # Initialize all parent classes
        Animal.__init__(self, name, age)
        Flyable.__init__(self)
        Swimmable.__init__(self)
    
    def speak(self):
        return f"{self.name} says: Quack! Quack!"


# =============================================================================
# EXAMPLE 4: Hierarchical Inheritance
# =============================================================================
# Multiple child classes inherit from the same parent class

class Employee:
    """Base Employee class"""
    
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
    
    def get_details(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Salary: ${self.salary}"
    
    def work(self):
        return f"{self.name} is working."


class Developer(Employee):
    """Developer inherits from Employee"""
    
    def __init__(self, emp_id, name, salary, programming_language):
        super().__init__(emp_id, name, salary)
        self.programming_language = programming_language
    
    def work(self):
        return f"{self.name} is coding in {self.programming_language}."
    
    def debug(self):
        return f"{self.name} is debugging the code."


class Designer(Employee):
    """Designer inherits from Employee"""
    
    def __init__(self, emp_id, name, salary, design_tool):
        super().__init__(emp_id, name, salary)
        self.design_tool = design_tool
    
    def work(self):
        return f"{self.name} is designing using {self.design_tool}."
    
    def create_mockup(self):
        return f"{self.name} is creating a mockup."


class Manager(Employee):
    """Manager inherits from Employee"""
    
    def __init__(self, emp_id, name, salary, team_size):
        super().__init__(emp_id, name, salary)
        self.team_size = team_size
        self.team_members = []
    
    def work(self):
        return f"{self.name} is managing a team of {self.team_size} people."
    
    def add_team_member(self, employee):
        self.team_members.append(employee)
        return f"{employee.name} added to the team."


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SINGLE INHERITANCE EXAMPLE")
    print("=" * 60)
    
    dog = Dog("Buddy", 3, "Golden Retriever")
    cat = Cat("Whiskers", 2, "Orange")
    
    print(dog.eat())         # Inherited from Animal
    print(dog.speak())       # Overridden in Dog
    print(dog.fetch())       # Specific to Dog
    print()
    print(cat.eat())         # Inherited from Animal
    print(cat.speak())       # Overridden in Cat
    print(cat.climb())       # Specific to Cat
    
    print("\n" + "=" * 60)
    print("MULTI-LEVEL INHERITANCE EXAMPLE")
    print("=" * 60)
    
    tesla = ElectricCar("Tesla", "Model 3", 4, 75)
    print(tesla.start())     # From Vehicle (grandparent)
    print(tesla.drive())     # From Car (parent)
    print(tesla.honk())      # From Car (parent)
    print(tesla.charge())    # From ElectricCar (child)
    print(tesla.get_range()) # From ElectricCar (child)
    
    print("\n" + "=" * 60)
    print("MULTIPLE INHERITANCE EXAMPLE")
    print("=" * 60)
    
    duck = Duck("Donald", 5)
    print(duck.eat())        # From Animal
    print(duck.speak())      # Overridden in Duck
    print(duck.fly())        # From Flyable
    print(duck.swim())       # From Swimmable
    print(duck.land())       # From Flyable
    
    print("\n" + "=" * 60)
    print("HIERARCHICAL INHERITANCE EXAMPLE")
    print("=" * 60)
    
    dev = Developer(101, "Alice", 80000, "Python")
    designer = Designer(102, "Bob", 75000, "Figma")
    manager = Manager(103, "Charlie", 100000, 5)
    
    print(dev.get_details())      # Inherited from Employee
    print(dev.work())             # Overridden in Developer
    print(dev.debug())            # Specific to Developer
    print()
    print(designer.get_details()) # Inherited from Employee
    print(designer.work())        # Overridden in Designer
    print()
    print(manager.get_details())  # Inherited from Employee
    print(manager.work())         # Overridden in Manager
    print(manager.add_team_member(dev))

    print("\n" + "=" * 60)
    print("METHOD RESOLUTION ORDER (MRO)")
    print("=" * 60)
    print("Duck MRO:", Duck.__mro__)
    print("ElectricCar MRO:", ElectricCar.__mro__)
