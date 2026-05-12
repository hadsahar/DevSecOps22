"""
Data Transfer Objects for Meal Responses
Used for outgoing API responses
"""
from typing import List
from POCO.meal import Meal


class MealResponseDTO:
    """DTO for single meal response"""
    
    def __init__(self, id: int, name: str, meal_type: str, price: float, calories: int):
        self.id = id
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    @classmethod
    def from_meal(cls, meal: Meal) -> 'MealResponseDTO':
        """Create DTO from domain model (POCO)"""
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
    """DTO for list of meals with pagination metadata"""
    
    def __init__(self, meals: List[MealResponseDTO], total: int, page: int, page_size: int):
        self.meals = meals
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    def to_json(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            'data': [meal.to_json() for meal in self.meals],
            'meta': {
                'total': self.total,
                'page': self.page,
                'page_size': self.page_size,
                'total_pages': self.total_pages
            }
        }
