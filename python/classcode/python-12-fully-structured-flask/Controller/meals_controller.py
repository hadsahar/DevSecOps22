"""
Controller Layer
Handles HTTP requests and responses
"""
from flask import Blueprint, request, jsonify
from Service.meal_service import MealService
from DTO.meal_request_dto import CreateMealRequestDTO, UpdateMealRequestDTO
from DAO.dao_factory import DAOFactory

# Create Blueprint
meals_blueprint = Blueprint('meals', __name__)

# Initialize dependencies
meals_dao = DAOFactory.get_meals_dao()
meal_service = MealService(meals_dao)


@meals_blueprint.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint"""
    return jsonify({'message': 'pong'}), 200


@meals_blueprint.route('/meals', methods=['POST'])
def create_meal():
    """Create a new meal"""
    try:
        # Parse request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        request_dto = CreateMealRequestDTO.from_json(data)
        
        # Call service
        response_dto = meal_service.create_meal(request_dto)
        
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
        response_dto = meal_service.get_meal_by_id(meal_id)
        return jsonify(response_dto.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@meals_blueprint.route('/meals', methods=['GET'])
def get_meals():
    """Get all meals with optional filters and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        name = request.args.get('name')
        meal_type = request.args.get('type')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Search if filters provided
        if name or meal_type or (min_price is not None and max_price is not None):
            meals = meal_service.search_meals(
                name=name,
                meal_type=meal_type,
                min_price=min_price,
                max_price=max_price
            )
            return jsonify([m.to_json() for m in meals]), 200
        
        # Otherwise get paginated list
        response_dto = meal_service.get_all_meals(page, page_size)
        return jsonify(response_dto.to_json()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@meals_blueprint.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id: int):
    """Update a meal"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        update_dto = UpdateMealRequestDTO.from_json(data)
        
        response_dto = meal_service.update_meal(meal_id, update_dto)
        return jsonify(response_dto.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@meals_blueprint.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id: int):
    """Delete a meal"""
    try:
        meal_service.delete_meal(meal_id)
        return jsonify({'message': f'Meal {meal_id} deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@meals_blueprint.route('/meals/healthy', methods=['GET'])
def get_healthy_meals():
    """Get healthy meals (business logic example)"""
    try:
        meals = meal_service.get_healthy_meals()
        return jsonify([m.to_json() for m in meals]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
