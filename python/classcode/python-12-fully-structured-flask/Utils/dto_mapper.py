"""
DTO Mapper Utility
Handles mapping between DTOs and POPOs
"""
from typing import List
from POCO.meal import Meal
from DTO.meal_request_dto import CreateMealRequestDTO
from DTO.meal_response_dto import MealResponseDTO, MealListResponseDTO


class DTOMapper:
    """Utility class for mapping between DTOs and POPOs"""
    
    @staticmethod
    def request_to_poco(dto: CreateMealRequestDTO) -> Meal:
        """Map request DTO to domain model (POCO)"""
        return Meal(
            id=None,  # ID assigned by database
            name=dto.name,
            meal_type=dto.type,
            price=dto.price,
            calories=dto.calories
        )
    
    @staticmethod
    def poco_to_response(meal: Meal) -> MealResponseDTO:
        """Map domain model (POCO) to response DTO"""
        return MealResponseDTO.from_meal(meal)
    
    @staticmethod
    def poco_list_to_response(meals: List[Meal], 
                             total: int, 
                             page: int, 
                             page_size: int) -> MealListResponseDTO:
        """Map list of domain models to list response DTO"""
        meal_dtos = [MealResponseDTO.from_meal(meal) for meal in meals]
        return MealListResponseDTO(meal_dtos, total, page, page_size)
