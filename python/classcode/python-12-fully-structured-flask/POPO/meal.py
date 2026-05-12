"""
POCO (Plain Old Python Objects) - Domain Models
Represents the business entity in the system
"""
from typing import Optional


class Meal:
    """Domain model representing a meal"""
    
    def __init__(self, id: Optional[int], name: str, meal_type: str, 
                 price: float, calories: int):
        self.id = id
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    def calculate_calories_per_dollar(self) -> float:
        """Calculate calories per dollar - business logic"""
        if self.price > 0:
            return self.calories / self.price
        return 0
    
    def is_healthy(self) -> bool:
        """Determine if meal is healthy - business logic"""
        return self.calories < 500
    
    def __repr__(self):
        return f"Meal(id={self.id}, name='{self.name}', type='{self.type}', price=${self.price}, calories={self.calories})"
    
    def __eq__(self, other):
        if isinstance(other, Meal):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id) if self.id else hash(self.name)