---
layout: default
title: Layered Architecture
---

# Layered Architecture: DAO, DTO, POJO/POCO, and PDBC

## Table of Contents

1. [Introduction to Layered Architecture](#1-introduction-to-layered-architecture)
2. [The Layers](#2-the-layers)
3. [POJO/POCO (Plain Old Python/Java Objects)](#3-pojo-poco-plain-old-pythonjava-objects)
4. [DTO (Data Transfer Objects)]#4-dto-data-transfer-objects)
5. [DAO (Data Access Objects)](#5-dao-data-access-objects)
6. [PDBC (Python Database Connectivity)](#6-pdbc-python-database-connectivity)
7. [Service Layer](#7-service-layer)
8. [Controller Layer](#8-controller-layer)
9. [Complete Example: Flask Meals API](#9-complete-example-flask-meals-api)
10. [Best Practices](#10-best-practices)
11. [Comparison with Other Patterns](#11-comparison-with-other-patterns)

---

## 1. Introduction to Layered Architecture

### What is Layered Architecture?

**Layered Architecture** (also known as **N-Tier Architecture**) is a software design pattern that organizes code into distinct layers, each with a specific responsibility. This separation of concerns makes applications:

- **Maintainable**: Easier to modify one layer without affecting others
- **Testable**: Each layer can be tested independently
- **Scalable**: Layers can be scaled independently
- **Reusable**: Components can be reused across different parts of the application

### Typical Layer Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                             │
│              (Controllers, Routes, Views)                         │
│                    Handles HTTP requests                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                     SERVICE LAYER                                │
│              (Business Logic, Use Cases)                         │
│           Implements application rules and workflows             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      DAO / REPOSITORY LAYER                       │
│           (Data Access Objects, Database Operations)              │
│              Handles all database interactions                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      DATABASE LAYER                               │
│              (PostgreSQL, MySQL, SQLite, MongoDB)                 │
│                  Persistent data storage                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 MODELS / DTO / POCO (Cross-layer)                 │
│         Domain models, data transfer objects, DTOs               │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
HTTP Request → Controller → Service → DAO → Database
                                                    │
                                                    ▼
Response ← DTO ← Service ← POCO ← DAO ← Database
```

### Benefits of Layered Architecture

| Benefit | Description |
|---------|-------------|
| **Separation of Concerns** | Each layer has a single, well-defined responsibility |
| **Loose Coupling** | Layers depend on abstractions, not concrete implementations |
| **High Cohesion** | Related functionality is grouped together |
| **Testability** | Each layer can be unit tested in isolation |
| **Reusability** | Components can be reused across different applications |
| **Parallel Development** | Teams can work on different layers simultaneously |
| **Easy Maintenance** | Changes in one layer don't cascade to others |

---

## 2. The Layers

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER              RESPONSIBILITY                                │
├─────────────────────────────────────────────────────────────────┤
│ Presentation     - Handle HTTP requests/responses                │
│ (Controller)      - Validate input                               │
│                   - Return appropriate HTTP status codes          │
│                   - No business logic                             │
├─────────────────────────────────────────────────────────────────┤
│ Service          - Implement business rules                      │
│ (Business Logic)  - Orchestrate DAO operations                    │
│                   - Transform DTOs to POCOs and vice versa       │
│                   - Handle transactions                           │
├─────────────────────────────────────────────────────────────────┤
│ DAO/Repository   - Execute SQL queries                          │
│ (Data Access)     - Map database rows to POCOs                   │
│                   - Handle database connections                   │
│                   - No business logic                             │
├─────────────────────────────────────────────────────────────────┤
│ Database         - Store and retrieve data                       │
│                   - Ensure data integrity                         │
│                   - Handle persistence                            │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Communication Rules

- **Downward dependency**: Upper layers depend on lower layers
- **No upward calls**: Lower layers should never call upper layers
- **Interface-based**: Layers communicate through well-defined interfaces
- **DTOs for boundaries**: Use DTOs when data crosses layer boundaries

---

## 3. POJO/POCO (Plain Old Python/Java Objects)

### What are POJO/POCO?

**POJO** (Plain Old Java Object) and **POCO** (Plain Old CLR Object) are simple objects that:

- Contain only data (fields/attributes)
- Have minimal behavior (getters/setters)
- Don't depend on frameworks
- Are independent of any specific technology

In Python, we call them **POPO** (Plain Old Python Objects).

### Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Simple** | No complex inheritance or dependencies |
| **Self-contained** | Doesn't require external frameworks |
| **Serializable** | Can be easily converted to/from JSON, XML |
| **Testable** | Easy to instantiate and test |
| **Domain-focused** | Represents domain concepts |

### Example: POPO vs DTO

```python
# POPO - Domain Model (represents business entity)
class Meal:
    """Domain model - represents a meal in the system"""
    
    def __init__(self, id: int, name: str, meal_type: str, 
                 price: float, calories: int):
        self.id = id
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    def calculate_calories_per_dollar(self) -> float:
        """Business logic method"""
        if self.price > 0:
            return self.calories / self.price
        return 0
    
    def is_healthy(self) -> bool:
        """Business logic method"""
        return self.calories < 500
    
    def __repr__(self):
        return f"Meal(id={self.id}, name='{self.name}', price=${self.price})"
    
    def __eq__(self, other):
        if isinstance(other, Meal):
            return self.id == other.id
        return False

# DTO - Data Transfer Object (for API communication)
class MealRequestDTO:
    """DTO for incoming meal data"""
    
    def __init__(self, name: str, meal_type: str, 
                 price: float, calories: int):
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MealRequestDTO':
        """Create DTO from dictionary (e.g., from JSON request)"""
        return cls(
            name=data['name'],
            meal_type=data['type'],
            price=data['price'],
            calories=data['calories']
        )
    
    def validate(self) -> bool:
        """Validate DTO data"""
        return (self.name and 
                self.type and 
                self.price > 0 and 
                self.calories > 0)

class MealResponseDTO:
    """DTO for outgoing meal data"""
    
    def __init__(self, id: int, name: str, meal_type: str, 
                 price: float, calories: int):
        self.id = id
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    @classmethod
    def from_poco(cls, meal: Meal) -> 'MealResponseDTO':
        """Create DTO from POPO"""
        return cls(
            id=meal.id,
            name=meal.name,
            meal_type=meal.type,
            price=meal.price,
            calories=meal.calories
        )
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary (for JSON response)"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'price': self.price,
            'calories': self.calories
        }
```

### When to Use POPO vs DTO

| Scenario | Use |
|----------|-----|
| **Database mapping** | POPO |
| **Business logic** | POPO |
| **API requests** | DTO |
| **API responses** | DTO |
| **Internal processing** | POPO |
| **Cross-service communication** | DTO |

---

## 4. DTO (Data Transfer Objects)

### What is a DTO?

**Data Transfer Object** is an object that carries data between processes. DTOs are used to:

- Transfer data between layers
- Serialize/deserialize data for APIs
- Reduce number of method calls (chunking data)
- Hide internal structure of domain models

### Why Use DTOs?

```
Without DTOs:
┌─────────────┐
│ Controller  │ → Directly returns POPO → Could expose sensitive data
└─────────────┘

With DTOs:
┌─────────────┐     ┌─────────┐     ┌──────────┐     ┌─────────────┐
│ Controller  │ →   │ Service  │ →   │   DTO    │ →   │ JSON/Client │
└─────────────┘     └─────────┘     └──────────┘     └─────────────┘
                      ↓
                    ┌─────────┐
                    │  POPO   │
                    └─────────┘
```

### Benefits of DTOs

| Benefit | Description |
|---------|-------------|
| **Security** | Hide sensitive fields (passwords, internal IDs) |
| **Validation** | Validate data before it enters business logic |
| **Flexibility** | Different DTOs for different use cases |
| **Versioning** | Maintain API compatibility while changing internals |
| **Performance** | Include only needed data (reduce payload size) |

### DTO Patterns

#### 1. Request DTO

```python
class CreateMealRequestDTO:
    """DTO for creating a new meal"""
    
    def __init__(self, name: str, meal_type: str, 
                 price: float, calories: int):
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    def validate(self) -> tuple[bool, str]:
        """Validate request data"""
        if not self.name or len(self.name) > 100:
            return False, "Name must be 1-100 characters"
        if self.type not in ['breakfast', 'lunch', 'dinner', 'snack']:
            return False, "Invalid meal type"
        if self.price <= 0 or self.price > 1000:
            return False, "Price must be between 0 and 1000"
        if self.calories <= 0 or self.calories > 5000:
            return False, "Calories must be between 0 and 5000"
        return True, ""
    
    @classmethod
    def from_json(cls, json_data: dict) -> 'CreateMealRequestDTO':
        """Create from JSON request body"""
        return cls(
            name=json_data['name'],
            meal_type=json_data['type'],
            price=float(json_data['price']),
            calories=int(json_data['calories'])
        )
```

#### 2. Response DTO

```python
class MealResponseDTO:
    """DTO for meal response"""
    
    def __init__(self, id: int, name: str, meal_type: str, 
                 price: float, calories: int):
        self.id = id
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    @classmethod
    def from_meal(cls, meal: Meal) -> 'MealResponseDTO':
        """Create from domain model"""
        return cls(
            id=meal.id,
            name=meal.name,
            meal_type=meal.type,
            price=meal.price,
            calories=meal.calories
        )
    
    def to_json(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'price': self.price,
            'calories': self.calories
        }

class MealListResponseDTO:
    """DTO for list of meals with metadata"""
    
    def __init__(self, meals: list[MealResponseDTO], 
                 total: int, page: int, page_size: int):
        self.meals = meals
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = (total + page_size - 1) // page_size
    
    def to_json(self) -> dict:
        return {
            'data': [meal.to_json() for meal in self.meals],
            'meta': {
                'total': self.total,
                'page': self.page,
                'page_size': self.page_size,
                'total_pages': self.total_pages
            }
        }
```

#### 3. Update DTO

```python
class UpdateMealRequestDTO:
    """DTO for updating a meal (all fields optional)"""
    
    def __init__(self, name: str = None, meal_type: str = None,
                 price: float = None, calories: int = None):
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    def has_updates(self) -> bool:
        """Check if any fields are set"""
        return any([
            self.name is not None,
            self.type is not None,
            self.price is not None,
            self.calories is not None
        ])
    
    def get_updates(self) -> dict:
        """Get dictionary of non-None fields"""
        updates = {}
        if self.name is not None:
            updates['name'] = self.name
        if self.type is not None:
            updates['type'] = self.type
        if self.price is not None:
            updates['price'] = self.price
        if self.calories is not None:
            updates['calories'] = self.calories
        return updates
```

### DTO Mapping

```python
class DTOMapper:
    """Utility class for mapping between DTOs and POPOs"""
    
    @staticmethod
    def request_to_poco(dto: CreateMealRequestDTO) -> Meal:
        """Map request DTO to domain model"""
        return Meal(
            id=None,  # ID assigned by database
            name=dto.name,
            meal_type=dto.type,
            price=dto.price,
            calories=dto.calories
        )
    
    @staticmethod
    def poco_to_response(meal: Meal) -> MealResponseDTO:
        """Map domain model to response DTO"""
        return MealResponseDTO.from_meal(meal)
    
    @staticmethod
    def poco_list_to_response(meals: list[Meal], 
                             total: int, 
                             page: int, 
                             page_size: int) -> MealListResponseDTO:
        """Map list of domain models to list response DTO"""
        meal_dtos = [MealResponseDTO.from_meal(meal) for meal in meals]
        return MealListResponseDTO(meal_dtos, total, page, page_size)
```

---

## 5. DAO (Data Access Objects)

### What is DAO?

**Data Access Object** is a pattern that provides an abstract interface to a database or other persistence mechanism. DAOs:

- Encapsulate all database operations
- Handle CRUD (Create, Read, Update, Delete) operations
- Map database rows to domain objects (POPOs)
- Isolate the rest of the application from database-specific code

### DAO Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        DAO INTERFACE                             │
│                    (Abstract methods)                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ implements
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      CONCRETE DAO                                │
│              (SQL queries, database connection)                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ uses
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      DATABASE                                    │
└─────────────────────────────────────────────────────────────────┘
```

### DAO Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class IMealsDAO(ABC):
    """Interface for Meals Data Access Object"""
    
    @abstractmethod
    def create(self, meal: Meal) -> Meal:
        """Create a new meal in database"""
        pass
    
    @abstractmethod
    def find_by_id(self, meal_id: int) -> Optional[Meal]:
        """Find meal by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Meal]:
        """Get all meals"""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Meal]:
        """Find meals by name (partial match)"""
        pass
    
    @abstractmethod
    def find_by_type(self, meal_type: str) -> List[Meal]:
        """Find meals by type"""
        pass
    
    @abstractmethod
    def find_by_price_range(self, min_price: float, 
                           max_price: float) -> List[Meal]:
        """Find meals within price range"""
        pass
    
    @abstractmethod
    def update(self, meal: Meal) -> bool:
        """Update an existing meal"""
        pass
    
    @abstractmethod
    def delete(self, meal_id: int) -> bool:
        """Delete a meal"""
        pass
```

### Concrete DAO Implementation

```python
import sqlite3
from typing import List, Optional
from db import get_connection

class MealsDAO(IMealsDAO):
    """SQLite implementation of MealsDAO"""
    
    def __init__(self):
        self._init_table()
    
    def _init_table(self):
        """Create table if not exists"""
        query = '''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            calories INTEGER NOT NULL
        );
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    
    def create(self, meal: Meal) -> Meal:
        """Create a new meal"""
        query = '''
        INSERT INTO meals (name, type, price, calories)
        VALUES (?, ?, ?, ?)
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal.name, meal.type, 
                               meal.price, meal.calories))
        meal.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return meal
    
    def find_by_id(self, meal_id: int) -> Optional[Meal]:
        """Find meal by ID"""
        query = 'SELECT * FROM meals WHERE id = ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_meal(row)
        return None
    
    def find_all(self) -> List[Meal]:
        """Get all meals"""
        query = 'SELECT * FROM meals'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_meal(row) for row in rows]
    
    def find_by_name(self, name: str) -> List[Meal]:
        """Find meals by name (partial match)"""
        query = 'SELECT * FROM meals WHERE name LIKE ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (f'%{name}%',))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_meal(row) for row in rows]
    
    def find_by_type(self, meal_type: str) -> List[Meal]:
        """Find meals by type"""
        query = 'SELECT * FROM meals WHERE type = ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal_type,))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_meal(row) for row in rows]
    
    def find_by_price_range(self, min_price: float, 
                           max_price: float) -> List[Meal]:
        """Find meals within price range"""
        query = 'SELECT * FROM meals WHERE price BETWEEN ? AND ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (min_price, max_price))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_meal(row) for row in rows]
    
    def update(self, meal: Meal) -> bool:
        """Update an existing meal"""
        query = '''
        UPDATE meals 
        SET name = ?, type = ?, price = ?, calories = ?
        WHERE id = ?
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal.name, meal.type, 
                               meal.price, meal.calories, meal.id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0
    
    def delete(self, meal_id: int) -> bool:
        """Delete a meal"""
        query = 'DELETE FROM meals WHERE id = ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0
    
    def _row_to_meal(self, row: tuple) -> Meal:
        """Convert database row to Meal object"""
        return Meal(
            id=row[0],
            name=row[1],
            meal_type=row[2],
            price=row[3],
            calories=row[4]
        )
```

### DAO Factory Pattern

```python
class DAOFactory:
    """Factory for creating DAO instances"""
    
    @staticmethod
    def get_meals_dao() -> IMealsDAO:
        """Get MealsDAO instance"""
        return MealsDAO()
    
    # Can extend for other DAOs
    # @staticmethod
    # def get_users_dao() -> IUsersDAO:
    #     return UsersDAO()
```

---

## 6. PDBC (Python Database Connectivity)

### What is PDBC?

**PDBC** (Python Database Connectivity) refers to the layer that manages database connections and provides a unified interface for database operations. It's similar to JDBC in Java.

### Connection Management

```python
import sqlite3
from typing import ContextManager
from contextlib import contextmanager

class DatabaseConnection:
    """Manages database connections"""
    
    def __init__(self, db_path: str = 'jolt.db'):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self) -> ContextManager[sqlite3.Connection]:
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def get_cursor(self) -> ContextManager[sqlite3.Cursor]:
        """Context manager for database cursor"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise

# Singleton instance
db = DatabaseConnection()

# Usage
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    rows = cursor.fetchall()
```

### Connection Pool

```python
import sqlite3
from queue import Queue
from threading import Lock

class ConnectionPool:
    """Simple connection pool for SQLite"""
    
    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool = Queue(maxsize=pool_size)
        self.lock = Lock()
        
        # Initialize pool
        for _ in range(pool_size):
            self.pool.put(sqlite3.connect(db_path, check_same_thread=False))
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a connection from the pool"""
        return self.pool.get()
    
    def return_connection(self, conn: sqlite3.Connection):
        """Return a connection to the pool"""
        self.pool.put(conn)
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

# Usage
pool = ConnectionPool('jolt.db', pool_size=5)

conn = pool.get_connection()
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    rows = cursor.fetchall()
finally:
    pool.return_connection(conn)
```

### Transaction Management

```python
class TransactionManager:
    """Manages database transactions"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    @contextmanager
    def transaction(self):
        """Transaction context manager"""
        with self.db.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise

# Usage with DAO
class MealsDAO(IMealsDAO):
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        self.transaction = TransactionManager(db_connection)
    
    def create_with_related(self, meal: Meal, ingredients: list):
        """Create meal with ingredients in a transaction"""
        with self.transaction.transaction() as conn:
            # Create meal
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO meals (name, type, price, calories) VALUES (?, ?, ?, ?)",
                (meal.name, meal.type, meal.price, meal.calories)
            )
            meal_id = cursor.lastrowid
            
            # Create ingredients
            for ingredient in ingredients:
                cursor.execute(
                    "INSERT INTO ingredients (meal_id, name) VALUES (?, ?)",
                    (meal_id, ingredient)
                )
```

---

## 7. Service Layer

### What is the Service Layer?

The **Service Layer** contains business logic and orchestrates operations. It:

- Implements use cases
- Coordinates multiple DAOs
- Handles business rules
- Manages transactions
- Transforms DTOs to POPOs

### Service Example

```python
from typing import List, Optional
from datetime import datetime

class MealService:
    """Service layer for meal operations"""
    
    def __init__(self, meals_dao: IMealsDAO):
        self.meals_dao = meals_dao
    
    def create_meal(self, request_dto: CreateMealRequestDTO) -> MealResponseDTO:
        """Create a new meal"""
        # Validate input
        is_valid, error = request_dto.validate()
        if not is_valid:
            raise ValueError(error)
        
        # Convert DTO to POPO
        meal = DTOMapper.request_to_poco(request_dto)
        
        # Business logic
        if meal.price < 5:
            raise ValueError("Price too low for a meal")
        
        # Persist
        created_meal = self.meals_dao.create(meal)
        
        # Convert back to DTO
        return DTOMapper.poco_to_response(created_meal)
    
    def get_meal_by_id(self, meal_id: int) -> MealResponseDTO:
        """Get a meal by ID"""
        meal = self.meals_dao.find_by_id(meal_id)
        if not meal:
            raise ValueError(f"Meal with ID {meal_id} not found")
        return DTOMapper.poco_to_response(meal)
    
    def get_all_meals(self, page: int = 1, 
                     page_size: int = 10) -> MealListResponseDTO:
        """Get all meals with pagination"""
        meals = self.meals_dao.find_all()
        
        # Pagination logic
        start = (page - 1) * page_size
        end = start + page_size
        paginated_meals = meals[start:end]
        
        total = len(meals)
        return DTOMapper.poco_list_to_response(
            paginated_meals, total, page, page_size
        )
    
    def search_meals(self, name: str = None, 
                    meal_type: str = None,
                    min_price: float = None,
                    max_price: float = None) -> List[MealResponseDTO]:
        """Search meals with filters"""
        meals = []
        
        if name:
            meals = self.meals_dao.find_by_name(name)
        elif meal_type:
            meals = self.meals_dao.find_by_type(meal_type)
        elif min_price and max_price:
            meals = self.meals_dao.find_by_price_range(min_price, max_price)
        else:
            meals = self.meals_dao.find_all()
        
        # Additional business logic
        meals = [m for m in meals if m.price > 0]
        
        return [DTOMapper.poco_to_response(m) for m in meals]
    
    def update_meal(self, meal_id: int, 
                   update_dto: UpdateMealRequestDTO) -> MealResponseDTO:
        """Update a meal"""
        if not update_dto.has_updates():
            raise ValueError("No updates provided")
        
        meal = self.meals_dao.find_by_id(meal_id)
        if not meal:
            raise ValueError(f"Meal with ID {meal_id} not found")
        
        # Apply updates
        updates = update_dto.get_updates()
        for key, value in updates.items():
            if key == 'name':
                meal.name = value
            elif key == 'type':
                meal.type = value
            elif key == 'price':
                meal.price = value
            elif key == 'calories':
                meal.calories = value
        
        # Business validation
        if meal.price < 0:
            raise ValueError("Price cannot be negative")
        
        # Persist
        self.meals_dao.update(meal)
        
        return DTOMapper.poco_to_response(meal)
    
    def delete_meal(self, meal_id: int) -> bool:
        """Delete a meal"""
        meal = self.meals_dao.find_by_id(meal_id)
        if not meal:
            raise ValueError(f"Meal with ID {meal_id} not found")
        
        return self.meals_dao.delete(meal_id)
    
    def get_healthy_meals(self) -> List[MealResponseDTO]:
        """Get meals with business logic filter"""
        all_meals = self.meals_dao.find_all()
        healthy_meals = [m for m in all_meals if m.is_healthy()]
        return [DTOMapper.poco_to_response(m) for m in healthy_meals]
```

---

## 8. Controller Layer

### What is the Controller Layer?

The **Controller Layer** (also called Presentation Layer) handles HTTP requests and responses. It:

- Receives HTTP requests
- Validates request data
- Calls service layer
- Returns HTTP responses with appropriate status codes
- Handles errors

### Controller Example

```python
from flask import Blueprint, request, jsonify
from typing import Any

meals_blueprint = Blueprint('meals', __name__)

class MealsController:
    """Controller for meal endpoints"""
    
    def __init__(self, meal_service: MealService):
        self.service = meal_service

# Initialize controller with service
meals_dao = DAOFactory.get_meals_dao()
meal_service = MealService(meals_dao)
controller = MealsController(meal_service)

# Routes
@meals_blueprint.route('/meals', methods=['POST'])
def create_meal():
    """Create a new meal"""
    try:
        # Parse request
        data = request.get_json()
        request_dto = CreateMealRequestDTO.from_json(data)
        
        # Call service
        response_dto = controller.service.create_meal(request_dto)
        
        # Return response
        return jsonify(response_dto.to_json()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@meals_blueprint.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id: int):
    """Get a meal by ID"""
    try:
        response_dto = controller.service.get_meal_by_id(meal_id)
        return jsonify(response_dto.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@meals_blueprint.route('/meals', methods=['GET'])
def get_meals():
    """Get all meals with optional filters"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        name = request.args.get('name')
        meal_type = request.args.get('type')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Search if filters provided
        if name or meal_type or (min_price and max_price):
            meals = controller.service.search_meals(
                name=name,
                meal_type=meal_type,
                min_price=min_price,
                max_price=max_price
            )
            return jsonify([m.to_json() for m in meals]), 200
        
        # Otherwise get paginated list
        response_dto = controller.service.get_all_meals(page, page_size)
        return jsonify(response_dto.to_json()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@meals_blueprint.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id: int):
    """Update a meal"""
    try:
        data = request.get_json()
        update_dto = UpdateMealRequestDTO(
            name=data.get('name'),
            meal_type=data.get('type'),
            price=data.get('price'),
            calories=data.get('calories')
        )
        
        response_dto = controller.service.update_meal(meal_id, update_dto)
        return jsonify(response_dto.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@meals_blueprint.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id: int):
    """Delete a meal"""
    try:
        controller.service.delete_meal(meal_id)
        return jsonify({'message': 'Meal deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@meals_blueprint.route('/meals/healthy', methods=['GET'])
def get_healthy_meals():
    """Get healthy meals"""
    try:
        meals = controller.service.get_healthy_meals()
        return jsonify([m.to_json() for m in meals]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
```

---

## 9. Complete Example: Flask Meals API

### Project Structure

```
python-12-fully-structured-flask/
├── app.py                          # Flask app initialization
├── db.py                           # Database connection
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
├── POCO/                           # Domain models
│   ├── __init__.py
│   └── meal.py                     # Meal POPO
├── DTO/                            # Data Transfer Objects
│   ├── __init__.py
│   ├── meal_request_dto.py         # Request DTOs
│   └── meal_response_dto.py        # Response DTOs
├── DAO/                            # Data Access Objects
│   ├── __init__.py
│   ├── meals_dao.py                # Meals DAO implementation
│   └── dao_factory.py              # DAO factory
├── Service/                        # Service layer
│   ├── __init__.py
│   └── meal_service.py             # Meal business logic
├── Controller/                     # Controllers
│   ├── __init__.py
│   └── meals_controller.py         # Meal endpoints
├── Utils/                          # Utilities
│   ├── __init__.py
│   └── dto_mapper.py               # DTO mapping utilities
└── errors.py                       # Error handling
```

### Complete Implementation

See the refactored code in `/Users/hothaifa/workspace/DevSecOps-22/python/classcode/python-12-fully-structured-flask/` for the complete working example.

---

## 10. Best Practices

### 1. Layer Separation

```python
# ✅ GOOD - Controller delegates to service
@meals_blueprint.route('/meals', methods=['POST'])
def create_meal():
    data = request.get_json()
    dto = CreateMealRequestDTO.from_json(data)
    response = meal_service.create_meal(dto)
    return jsonify(response.to_json()), 201

# ❌ BAD - Controller has business logic
@meals_blueprint.route('/meals', methods=['POST'])
def create_meal():
    data = request.get_json()
    if data['price'] < 5:  # Business logic in controller!
        return jsonify({'error': 'Price too low'}), 400
    meals_dao.create(data)  # Direct DAO access!
    return jsonify(data), 201
```

### 2. DTO Validation

```python
# ✅ GOOD - Validate in DTO
class CreateMealRequestDTO:
    def validate(self) -> tuple[bool, str]:
        if not self.name:
            return False, "Name required"
        if self.price <= 0:
            return False, "Price must be positive"
        return True, ""

# ❌ BAD - No validation
class CreateMealRequestDTO:
    def __init__(self, name, price):
        self.name = name
        self.price = price
```

### 3. DAO Error Handling

```python
# ✅ GOOD - Handle database errors
def find_by_id(self, meal_id: int) -> Optional[Meal]:
    try:
        query = 'SELECT * FROM meals WHERE id = ?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (meal_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_meal(row) if row else None
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None

# ❌ BAD - No error handling
def find_by_id(self, meal_id: int) -> Optional[Meal]:
    query = 'SELECT * FROM meals WHERE id = ?'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (meal_id,))
    row = cursor.fetchone()
    conn.close()
    return self._row_to_meal(row) if row else None
```

### 4. Use Type Hints

```python
# ✅ GOOD - Type hints
def create(self, meal: Meal) -> Meal:
    pass

def find_by_id(self, meal_id: int) -> Optional[Meal]:
    pass

def find_all(self) -> List[Meal]:
    pass

# ❌ BAD - No type hints
def create(self, meal):
    pass

def find_by_id(self, meal_id):
    pass
```

### 5. Dependency Injection

```python
# ✅ GOOD - Inject dependencies
class MealService:
    def __init__(self, meals_dao: IMealsDAO):
        self.meals_dao = meals_dao

# ❌ BAD - Hard-coded dependencies
class MealService:
    def __init__(self):
        self.meals_dao = MealsDAO()  # Hard to test!
```

---

## 11. Comparison with Other Patterns

### Layered vs Clean Architecture

| Aspect | Layered Architecture | Clean Architecture |
|--------|---------------------|-------------------|
| **Focus** | Separation by technical concern | Separation by business concern |
| **Dependencies** | Upper depends on lower | Inner depends on outer |
| **Testing** | Each layer testable | Each component independently testable |
| **Complexity** | Simpler, easier to understand | More complex, better for large systems |

### DAO vs Repository Pattern

| Aspect | DAO | Repository |
|--------|-----|------------|
| **Scope** | Per-entity operations | Aggregate root operations |
| **Abstraction** | Table-focused | Domain-focused |
| **Methods** | CRUD per table | Business-meaningful operations |
| **Use Case** | Simple CRUD | Complex domain logic |

### DTO vs Domain Model

| Aspect | DTO | Domain Model |
|--------|-----|--------------|
| **Purpose** | Data transfer | Business logic |
| **Behavior** | Minimal | Rich with methods |
| **Location** | Boundaries | Core domain |
| **Persistence** | Not persisted | Persisted |

---

## Summary

### Key Concepts

| Concept | Purpose |
|---------|---------|
| **Layered Architecture** | Organize code into distinct layers with clear responsibilities |
| **POJO/POCO** | Simple domain objects with minimal dependencies |
| **DTO** | Transfer data between layers, hide internal structure |
| **DAO** | Encapsulate database operations |
| **PDBC** | Manage database connections |
| **Service Layer** | Implement business logic |
| **Controller Layer** | Handle HTTP requests/responses |

### Data Flow Summary

```
HTTP Request
    ↓
Controller (validates, calls service)
    ↓
Service (business logic, calls DAO)
    ↓
DAO (database operations)
    ↓
Database
    ↓
DAO (returns POPO)
    ↓
Service (transforms POPO to DTO)
    ↓
Controller (returns DTO as JSON)
    ↓
HTTP Response
```

### Benefits Recap

- **Maintainability**: Clear separation makes code easier to maintain
- **Testability**: Each layer can be tested independently
- **Scalability**: Layers can be scaled independently
- **Reusability**: Components can be reused across applications
- **Flexibility**: Easy to swap implementations (e.g., change database)

---

## Practice Exercises

1. **Add a new entity**: Implement User management with layered architecture
2. **Add filtering**: Implement advanced meal search with multiple filters
3. **Add caching**: Add a caching layer between Service and DAO
4. **Add logging**: Implement logging at each layer
5. **Add validation**: Implement comprehensive validation in DTOs

---

## Additional Resources

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Data Access Object Pattern](https://en.wikipedia.org/wiki/Data_access_object)
- [DTO Pattern](https://martinfowler.com/eaaCatalog/DataTransferObject.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
