"""
DAO (Data Access Object) Layer
Handles all database operations for meals
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from POCO.meal import Meal
from db import get_connection


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
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Meal]:
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
        cursor.execute(query, (meal.name, meal.type, meal.price, meal.calories))
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
    
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Meal]:
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
        cursor.execute(query, (meal.name, meal.type, meal.price, meal.calories, meal.id))
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