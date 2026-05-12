"""
Data Transfer Objects for Meal Requests
Used for incoming API requests
"""
from typing import Optional


class CreateMealRequestDTO:
    """DTO for creating a new meal"""
    
    def __init__(self, name: str, meal_type: str, price: float, calories: int):
        self.name = name
        self.type = meal_type
        self.price = price
        self.calories = calories
    
    def validate(self) -> tuple[bool, str]:
        """Validate request data"""
        if not self.name or len(self.name) > 100:
            return False, "Name must be 1-100 characters"
        if self.type not in ['breakfast', 'lunch', 'dinner', 'snack']:
            return False, "Invalid meal type. Must be: breakfast, lunch, dinner, or snack"
        if self.price <= 0 or self.price > 1000:
            return False, "Price must be between 0 and 1000"
        if self.calories <= 0 or self.calories > 5000:
            return False, "Calories must be between 0 and 5000"
        return True, ""
    
    @classmethod
    def from_json(cls, json_data: dict) -> 'CreateMealRequestDTO':
        """Create DTO from JSON request body"""
        return cls(
            name=json_data['name'],
            meal_type=json_data['type'],
            price=float(json_data['price']),
            calories=int(json_data['calories'])
        )


class UpdateMealRequestDTO:
    """DTO for updating a meal (all fields optional)"""
    
    def __init__(self, name: Optional[str] = None, meal_type: Optional[str] = None,
                 price: Optional[float] = None, calories: Optional[int] = None):
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
    
    @classmethod
    def from_json(cls, json_data: dict) -> 'UpdateMealRequestDTO':
        """Create DTO from JSON request body"""
        return cls(
            name=json_data.get('name'),
            meal_type=json_data.get('type'),
            price=json_data.get('price'),
            calories=json_data.get('calories')
        )
