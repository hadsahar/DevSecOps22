"""
=============================================================================
ENCAPSULATION IN PYTHON - Advanced Detailed Examples
=============================================================================
Encapsulation bundles data (attributes) and methods that operate on the data
into a single unit (class), and restricts direct access to some components.
This protects the internal state and provides a controlled interface.
=============================================================================
"""


# =============================================================================
# EXAMPLE 1: Access Modifiers (Convention-based)
# =============================================================================

class BankAccount:
    """
    Demonstrates Python's naming conventions for access control:
    - public:     name        (accessible everywhere)
    - protected:  _name       (accessible in class and subclasses)
    - private:    __name      (name mangling - harder to access)
    """
    
    bank_name = "Python National Bank"  # Public class attribute
    
    def __init__(self, owner, account_number, initial_balance=0):
        # Public attributes
        self.owner = owner
        
        # Protected attributes (single underscore)
        self._account_number = account_number
        self._created_date = "2024-01-15"
        
        # Private attributes (double underscore)
        self.__balance = initial_balance
        self.__pin = "0000"
        self.__transaction_history = []
    
    # Public method
    def deposit(self, amount):
        """Deposit money - validates before modifying private balance"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.__balance += amount
        self.__log_transaction("deposit", amount)
        return f"Deposited ${amount}. New balance: ${self.__balance}"
    
    # Public method
    def withdraw(self, amount, pin):
        """Withdraw money - requires PIN verification"""
        if not self.__verify_pin(pin):
            raise PermissionError("Invalid PIN")
        
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        
        self.__balance -= amount
        self.__log_transaction("withdrawal", amount)
        return f"Withdrew ${amount}. New balance: ${self.__balance}"
    
    # Public method - getter
    def get_balance(self, pin):
        """Get balance - requires PIN"""
        if not self.__verify_pin(pin):
            raise PermissionError("Invalid PIN")
        return self.__balance
    
    # Public method - setter
    def set_pin(self, old_pin, new_pin):
        """Change PIN - requires old PIN verification"""
        if not self.__verify_pin(old_pin):
            raise PermissionError("Invalid PIN")
        
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise ValueError("PIN must be exactly 4 digits")
        
        self.__pin = new_pin
        return "PIN changed successfully"
    
    # Protected method
    def _get_account_info(self):
        """Get account info - intended for internal/subclass use"""
        return {
            "owner": self.owner,
            "account": self._account_number,
            "created": self._created_date
        }
    
    # Private method
    def __verify_pin(self, pin):
        """Verify PIN - private method"""
        return pin == self.__pin
    
    # Private method
    def __log_transaction(self, trans_type, amount):
        """Log transaction - private method"""
        import datetime
        self.__transaction_history.append({
            "type": trans_type,
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def get_transaction_history(self, pin):
        """Get transaction history - requires PIN"""
        if not self.__verify_pin(pin):
            raise PermissionError("Invalid PIN")
        return self.__transaction_history.copy()


# =============================================================================
# EXAMPLE 2: Property Decorators (Getters, Setters, Deleters)
# =============================================================================

class Employee:
    """Demonstrates @property decorator for controlled access"""
    
    def __init__(self, first_name, last_name, salary):
        self._first_name = first_name
        self._last_name = last_name
        self._salary = salary
        self._email = None
    
    # Getter for full_name
    @property
    def full_name(self):
        """Get full name - computed property"""
        return f"{self._first_name} {self._last_name}"
    
    # Setter for full_name
    @full_name.setter
    def full_name(self, value):
        """Set full name - parses into first and last"""
        parts = value.split()
        if len(parts) != 2:
            raise ValueError("Full name must be 'FirstName LastName'")
        self._first_name, self._last_name = parts
    
    # Getter for salary
    @property
    def salary(self):
        """Get salary"""
        return self._salary
    
    # Setter for salary with validation
    @salary.setter
    def salary(self, value):
        """Set salary with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
    
    # Deleter for salary
    @salary.deleter
    def salary(self):
        """Reset salary to 0"""
        print("Resetting salary...")
        self._salary = 0
    
    # Read-only property
    @property
    def email(self):
        """Generate email - read-only computed property"""
        return f"{self._first_name.lower()}.{self._last_name.lower()}@company.com"
    
    # Property with caching
    @property
    def annual_salary(self):
        """Calculate annual salary"""
        return self._salary * 12
    
    def give_raise(self, percentage):
        """Give a raise by percentage"""
        if percentage < 0:
            raise ValueError("Raise percentage cannot be negative")
        self._salary *= (1 + percentage / 100)
        return f"New salary: ${self._salary:.2f}"


# =============================================================================
# EXAMPLE 3: Data Validation with Encapsulation
# =============================================================================

class Temperature:
    """Temperature class with strict validation"""
    
    ABSOLUTE_ZERO_CELSIUS = -273.15
    
    def __init__(self, celsius=0):
        self._celsius = None
        self.celsius = celsius  # Use setter for validation
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < self.ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(f"Temperature cannot be below absolute zero ({self.ABSOLUTE_ZERO_CELSIUS}°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        celsius = (value - 32) * 5/9
        self.celsius = celsius  # Use celsius setter for validation
    
    @property
    def kelvin(self):
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        self.celsius = value - 273.15  # Use celsius setter for validation
    
    def __str__(self):
        return f"{self._celsius:.2f}°C / {self.fahrenheit:.2f}°F / {self.kelvin:.2f}K"


# =============================================================================
# EXAMPLE 4: Encapsulation with __slots__
# =============================================================================

class Point:
    """
    Using __slots__ for memory efficiency and restricting attributes.
    Prevents adding new attributes dynamically.
    """
    
    __slots__ = ['_x', '_y']
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Coordinate must be a number")
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Coordinate must be a number")
        self._y = value
    
    def distance_from_origin(self):
        return (self._x ** 2 + self._y ** 2) ** 0.5
    
    def __str__(self):
        return f"Point({self._x}, {self._y})"


# =============================================================================
# EXAMPLE 5: Immutable Class (Strong Encapsulation)
# =============================================================================

class ImmutablePoint:
    """
    An immutable point class - once created, cannot be modified.
    All attributes are read-only.
    """
    
    __slots__ = ['_x', '_y', '_frozen']
    
    def __init__(self, x, y):
        object.__setattr__(self, '_x', x)
        object.__setattr__(self, '_y', y)
        object.__setattr__(self, '_frozen', True)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __setattr__(self, name, value):
        if getattr(self, '_frozen', False):
            raise AttributeError(f"Cannot modify immutable {self.__class__.__name__}")
        object.__setattr__(self, name, value)
    
    def __delattr__(self, name):
        raise AttributeError(f"Cannot delete attribute from immutable {self.__class__.__name__}")
    
    def __str__(self):
        return f"ImmutablePoint({self._x}, {self._y})"
    
    def __hash__(self):
        return hash((self._x, self._y))
    
    def __eq__(self, other):
        if isinstance(other, ImmutablePoint):
            return self._x == other._x and self._y == other._y
        return False


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BANK ACCOUNT - ACCESS MODIFIERS")
    print("=" * 60)
    
    account = BankAccount("John Doe", "ACC-12345", 1000)
    
    # Public access
    print(f"Owner: {account.owner}")
    print(f"Bank: {account.bank_name}")
    
    # Protected access (allowed but discouraged)
    print(f"Account Number (protected): {account._account_number}")
    
    # Private access - Name mangling
    # print(account.__balance)  # AttributeError!
    # But can still access with name mangling (not recommended):
    print(f"Balance (via name mangling): {account._BankAccount__balance}")
    
    # Proper way - use public methods
    print(account.deposit(500))
    print(f"Balance: ${account.get_balance('0000')}")
    
    print(account.set_pin("0000", "1234"))
    print(account.withdraw(200, "1234"))
    
    print("\nTransaction History:")
    for tx in account.get_transaction_history("1234"):
        print(f"  {tx}")
    
    print("\n" + "=" * 60)
    print("EMPLOYEE - PROPERTY DECORATORS")
    print("=" * 60)
    
    emp = Employee("John", "Smith", 5000)
    
    print(f"Full Name: {emp.full_name}")
    print(f"Email: {emp.email}")
    print(f"Monthly Salary: ${emp.salary}")
    print(f"Annual Salary: ${emp.annual_salary}")
    
    # Using setter
    emp.full_name = "Jane Doe"
    print(f"\nAfter name change:")
    print(f"Full Name: {emp.full_name}")
    print(f"Email: {emp.email}")
    
    # Salary validation
    emp.salary = 6000
    print(f"\nAfter raise: ${emp.salary}")
    
    try:
        emp.salary = -1000
    except ValueError as e:
        print(f"Error (expected): {e}")
    
    print("\n" + "=" * 60)
    print("TEMPERATURE - DATA VALIDATION")
    print("=" * 60)
    
    temp = Temperature(25)
    print(f"Temperature: {temp}")
    
    temp.fahrenheit = 100
    print(f"After setting 100°F: {temp}")
    
    temp.kelvin = 300
    print(f"After setting 300K: {temp}")
    
    try:
        temp.celsius = -300  # Below absolute zero
    except ValueError as e:
        print(f"Error (expected): {e}")
    
    print("\n" + "=" * 60)
    print("POINT - __slots__ ENCAPSULATION")
    print("=" * 60)
    
    p = Point(3, 4)
    print(f"Point: {p}")
    print(f"Distance from origin: {p.distance_from_origin()}")
    
    p.x = 5
    print(f"After x = 5: {p}")
    
    try:
        p.z = 10  # Cannot add new attributes with __slots__
    except AttributeError as e:
        print(f"Error (expected): {e}")
    
    print("\n" + "=" * 60)
    print("IMMUTABLE POINT")
    print("=" * 60)
    
    ip = ImmutablePoint(10, 20)
    print(f"Immutable Point: {ip}")
    print(f"x = {ip.x}, y = {ip.y}")
    
    try:
        ip.x = 100  # Cannot modify
    except AttributeError as e:
        print(f"Error (expected): {e}")
    
    # Immutable objects can be used as dictionary keys
    point_dict = {ip: "origin"}
    print(f"Used as dict key: {point_dict[ip]}")
