"""
Service Layer
Contains business logic and orchestrates operations
"""
from typing import List, Optional
from DAO.meals_dao import IMealsDAO
from DTO.meal_request_dto import CreateMealRequestDTO, UpdateMealRequestDTO
from DTO.meal_response_dto import MealResponseDTO, MealListResponseDTO
from Utils.dto_mapper import DTOMapper


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
            raise ValueError("Price too low for a meal (minimum $5)")
        
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
    
    def search_meals(self, name: Optional[str] = None, 
                    meal_type: Optional[str] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None) -> List[MealResponseDTO]:
        """Search meals with filters"""
        meals = []
        
        if name:
            meals = self.meals_dao.find_by_name(name)
        elif meal_type:
            meals = self.meals_dao.find_by_type(meal_type)
        elif min_price is not None and max_price is not None:
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
