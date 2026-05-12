"""
DAO Factory Pattern
Factory for creating DAO instances
"""
from DAO.meals_dao import IMealsDAO, MealsDAO


class DAOFactory:
    """Factory for creating DAO instances"""
    
    @staticmethod
    def get_meals_dao() -> IMealsDAO:
        """Get MealsDAO instance"""
        return MealsDAO()
