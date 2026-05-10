"""
=============================================================================
ABSTRACTION IN PYTHON - Detailed Examples
=============================================================================
Abstraction hides complex implementation details and shows only the 
necessary features of an object. In Python, we achieve abstraction
using Abstract Base Classes (ABC) and abstract methods.
=============================================================================
"""

from abc import ABC, abstractmethod


# =============================================================================
# EXAMPLE 1: Abstract Base Class - Payment System
# =============================================================================

class PaymentProcessor(ABC):
    """Abstract base class for payment processing"""
    
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
        self.transactions = []
    
    @abstractmethod
    def process_payment(self, amount):
        """Process a payment - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id, amount):
        """Process a refund - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_balance(self):
        """Get current balance - must be implemented by subclasses"""
        pass
    
    # Concrete method - shared by all subclasses
    def log_transaction(self, transaction_type, amount, status):
        """Log a transaction - concrete method"""
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "status": status,
            "merchant": self.merchant_id
        }
        self.transactions.append(transaction)
        return len(self.transactions)  # Return transaction ID


class CreditCardProcessor(PaymentProcessor):
    """Credit card payment implementation"""
    
    def __init__(self, merchant_id, card_number, cvv):
        super().__init__(merchant_id)
        self._card_number = self._mask_card(card_number)
        self._cvv = cvv
        self._balance = 0
    
    def _mask_card(self, card_number):
        """Hide all but last 4 digits"""
        return "**** **** **** " + card_number[-4:]
    
    def process_payment(self, amount):
        # Complex credit card processing logic hidden
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}
        
        # Simulate processing
        self._balance += amount
        tx_id = self.log_transaction("payment", amount, "success")
        return {
            "success": True,
            "transaction_id": tx_id,
            "card": self._card_number,
            "amount": amount
        }
    
    def refund(self, transaction_id, amount):
        if amount > self._balance:
            return {"success": False, "error": "Insufficient balance"}
        
        self._balance -= amount
        tx_id = self.log_transaction("refund", amount, "success")
        return {"success": True, "refund_id": tx_id}
    
    def get_balance(self):
        return self._balance


class PayPalProcessor(PaymentProcessor):
    """PayPal payment implementation"""
    
    def __init__(self, merchant_id, email):
        super().__init__(merchant_id)
        self._email = email
        self._balance = 0
    
    def process_payment(self, amount):
        # PayPal-specific processing logic
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}
        
        fee = amount * 0.029 + 0.30  # PayPal fee
        net_amount = amount - fee
        self._balance += net_amount
        
        tx_id = self.log_transaction("payment", amount, "success")
        return {
            "success": True,
            "transaction_id": tx_id,
            "email": self._email,
            "gross": amount,
            "fee": round(fee, 2),
            "net": round(net_amount, 2)
        }
    
    def refund(self, transaction_id, amount):
        if amount > self._balance:
            return {"success": False, "error": "Insufficient balance"}
        
        self._balance -= amount
        tx_id = self.log_transaction("refund", amount, "success")
        return {"success": True, "refund_id": tx_id}
    
    def get_balance(self):
        return round(self._balance, 2)


class CryptoProcessor(PaymentProcessor):
    """Cryptocurrency payment implementation"""
    
    def __init__(self, merchant_id, wallet_address, crypto_type="BTC"):
        super().__init__(merchant_id)
        self._wallet = wallet_address
        self._crypto = crypto_type
        self._balance = 0
    
    def process_payment(self, amount):
        # Crypto-specific processing
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}
        
        # Simulate blockchain confirmation
        self._balance += amount
        tx_id = self.log_transaction("payment", amount, "confirmed")
        
        return {
            "success": True,
            "transaction_id": tx_id,
            "crypto": self._crypto,
            "wallet": self._wallet[:8] + "..." + self._wallet[-4:],
            "confirmations": 6
        }
    
    def refund(self, transaction_id, amount):
        if amount > self._balance:
            return {"success": False, "error": "Insufficient balance"}
        
        self._balance -= amount
        tx_id = self.log_transaction("refund", amount, "confirmed")
        return {"success": True, "refund_id": tx_id}
    
    def get_balance(self):
        return self._balance


# =============================================================================
# EXAMPLE 2: Abstract Base Class - Database Connector
# =============================================================================

class DatabaseConnector(ABC):
    """Abstract database connector"""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
    
    @abstractmethod
    def connect(self):
        """Establish database connection"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query):
        """Execute a query"""
        pass
    
    @abstractmethod
    def fetch_all(self, table):
        """Fetch all records from a table"""
        pass
    
    # Template method pattern - uses abstract methods
    def safe_query(self, query):
        """Execute query with automatic connection handling"""
        try:
            if not self.connected:
                self.connect()
            result = self.execute_query(query)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if self.connected:
                self.disconnect()


class MySQLConnector(DatabaseConnector):
    """MySQL database implementation"""
    
    def connect(self):
        print(f"Connecting to MySQL at {self.host}:{self.port}/{self.database}")
        self.connected = True
        return "MySQL connection established"
    
    def disconnect(self):
        print("Closing MySQL connection")
        self.connected = False
    
    def execute_query(self, query):
        if not self.connected:
            raise Exception("Not connected to database")
        print(f"Executing MySQL query: {query}")
        return f"MySQL result for: {query}"
    
    def fetch_all(self, table):
        return self.execute_query(f"SELECT * FROM {table}")


class PostgreSQLConnector(DatabaseConnector):
    """PostgreSQL database implementation"""
    
    def connect(self):
        print(f"Connecting to PostgreSQL at {self.host}:{self.port}/{self.database}")
        self.connected = True
        return "PostgreSQL connection established"
    
    def disconnect(self):
        print("Closing PostgreSQL connection")
        self.connected = False
    
    def execute_query(self, query):
        if not self.connected:
            raise Exception("Not connected to database")
        print(f"Executing PostgreSQL query: {query}")
        return f"PostgreSQL result for: {query}"
    
    def fetch_all(self, table):
        return self.execute_query(f"SELECT * FROM {table}")


class MongoDBConnector(DatabaseConnector):
    """MongoDB database implementation"""
    
    def connect(self):
        print(f"Connecting to MongoDB at {self.host}:{self.port}/{self.database}")
        self.connected = True
        return "MongoDB connection established"
    
    def disconnect(self):
        print("Closing MongoDB connection")
        self.connected = False
    
    def execute_query(self, query):
        if not self.connected:
            raise Exception("Not connected to database")
        print(f"Executing MongoDB query: {query}")
        return f"MongoDB result for: {query}"
    
    def fetch_all(self, collection):
        return self.execute_query(f"db.{collection}.find()")


# =============================================================================
# EXAMPLE 3: Abstract Properties
# =============================================================================

class Vehicle(ABC):
    """Abstract vehicle with abstract properties"""
    
    @property
    @abstractmethod
    def max_speed(self):
        """Maximum speed in km/h"""
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        """Type of fuel used"""
        pass
    
    @abstractmethod
    def start_engine(self):
        pass
    
    def describe(self):
        return f"Vehicle with max speed {self.max_speed} km/h, using {self.fuel_type}"


class SportsCar(Vehicle):
    """Sports car implementation"""
    
    @property
    def max_speed(self):
        return 350
    
    @property
    def fuel_type(self):
        return "Premium Gasoline"
    
    def start_engine(self):
        return "VROOM! Sports car engine started!"


class ElectricScooter(Vehicle):
    """Electric scooter implementation"""
    
    @property
    def max_speed(self):
        return 45
    
    @property
    def fuel_type(self):
        return "Electricity"
    
    def start_engine(self):
        return "Beep! Electric scooter powered on!"


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PAYMENT PROCESSOR ABSTRACTION")
    print("=" * 60)
    
    # Cannot instantiate abstract class
    # processor = PaymentProcessor("123")  # This would raise TypeError
    
    # Use concrete implementations
    credit_card = CreditCardProcessor("MERCHANT001", "4532015112830366", "123")
    paypal = PayPalProcessor("MERCHANT002", "business@example.com")
    crypto = CryptoProcessor("MERCHANT003", "1A2b3C4d5E6f7G8h9I0j")
    
    print("\n--- Credit Card Payment ---")
    result = credit_card.process_payment(100)
    print(f"Result: {result}")
    print(f"Balance: ${credit_card.get_balance()}")
    
    print("\n--- PayPal Payment ---")
    result = paypal.process_payment(100)
    print(f"Result: {result}")
    print(f"Balance: ${paypal.get_balance()}")
    
    print("\n--- Crypto Payment ---")
    result = crypto.process_payment(100)
    print(f"Result: {result}")
    print(f"Balance: {crypto.get_balance()} BTC")
    
    # Polymorphism in action - same interface, different implementations
    print("\n" + "=" * 60)
    print("POLYMORPHISM WITH ABSTRACTION")
    print("=" * 60)
    
    processors = [credit_card, paypal, crypto]
    for processor in processors:
        result = processor.process_payment(50)
        print(f"{processor.__class__.__name__}: Balance = {processor.get_balance()}")
    
    print("\n" + "=" * 60)
    print("DATABASE CONNECTOR ABSTRACTION")
    print("=" * 60)
    
    mysql = MySQLConnector("localhost", 3306, "myapp")
    postgres = PostgreSQLConnector("localhost", 5432, "myapp")
    mongo = MongoDBConnector("localhost", 27017, "myapp")
    
    databases = [mysql, postgres, mongo]
    
    for db in databases:
        print(f"\n--- {db.__class__.__name__} ---")
        result = db.safe_query("SELECT * FROM users")
        print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("ABSTRACT PROPERTIES")
    print("=" * 60)
    
    sports_car = SportsCar()
    scooter = ElectricScooter()
    
    vehicles = [sports_car, scooter]
    
    for vehicle in vehicles:
        print(f"\n{vehicle.__class__.__name__}:")
        print(f"  {vehicle.describe()}")
        print(f"  {vehicle.start_engine()}")
