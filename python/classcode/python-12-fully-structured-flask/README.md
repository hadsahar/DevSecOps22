# Flask Meals API - Layered Architecture Example

A fully structured Flask REST API demonstrating proper layered architecture with DAO, DTO, POCO, and PDBC patterns.

## Project Structure

```
python-12-fully-structured-flask/
├── app.py                          # Flask application entry point
├── db.py                           # PDBC - Database connection management
├── requirements.txt                # Python dependencies
├── POCO/                           # Domain Models (Plain Old Python Objects)
│   ├── __init__.py
│   └── meal.py                     # Meal domain model
├── DTO/                            # Data Transfer Objects
│   ├── __init__.py
│   ├── meal_request_dto.py         # Request DTOs (CreateMealRequestDTO, UpdateMealRequestDTO)
│   └── meal_response_dto.py        # Response DTOs (MealResponseDTO, MealListResponseDTO)
├── DAO/                            # Data Access Objects
│   ├── __init__.py
│   ├── meals_dao.py                # Meals DAO implementation with interface
│   └── dao_factory.py              # Factory for creating DAO instances
├── Service/                        # Service Layer (Business Logic)
│   ├── __init__.py
│   └── meal_service.py             # Meal business logic
├── Controller/                     # Controllers (Presentation Layer)
│   ├── __init__.py
│   └── meals_controller.py         # Meal API endpoints
├── Utils/                          # Utilities
│   ├── __init__.py
│   └── dto_mapper.py               # DTO to POCO mapping utilities
└── jolt.db                         # SQLite database
```

## Architecture Layers

### 1. Controller Layer (Presentation)
- **File**: `Controller/meals_controller.py`
- **Responsibility**: Handle HTTP requests/responses
- **Key Features**:
  - Parse incoming requests
  - Validate input
  - Call service layer
  - Return appropriate HTTP status codes

### 2. Service Layer (Business Logic)
- **File**: `Service/meal_service.py`
- **Responsibility**: Implement business rules
- **Key Features**:
  - Validate business rules
  - Orchestrate DAO operations
  - Transform DTOs to POCOs
  - Handle transactions

### 3. DAO Layer (Data Access)
- **File**: `DAO/meals_dao.py`
- **Responsibility**: Database operations
- **Key Features**:
  - CRUD operations
  - Map database rows to POCOs
  - Handle database connections
  - No business logic

### 4. POCO (Domain Models)
- **File**: `POCO/meal.py`
- **Responsibility**: Represent business entities
- **Key Features**:
  - Domain logic methods
  - Self-contained
  - No framework dependencies

### 5. DTO (Data Transfer Objects)
- **Files**: `DTO/meal_request_dto.py`, `DTO/meal_response_dto.py`
- **Responsibility**: Data transfer across layer boundaries
- **Key Features**:
  - Validation
  - Serialization/deserialization
  - Hide internal structure

### 6. PDBC (Database Connectivity)
- **File**: `db.py`
- **Responsibility**: Manage database connections
- **Key Features**:
  - Connection management
  - Context managers
  - Connection pooling (optional)

## API Endpoints

### Health Check
```
GET /ping
```

### Meals CRUD Operations

**Create Meal**
```
POST /meals
Content-Type: application/json

{
  "name": "Pasta",
  "type": "lunch",
  "price": 12.99,
  "calories": 450
}
```

**Get Meal by ID**
```
GET /meals/<id>
```

**Get All Meals (with pagination)**
```
GET /meals?page=1&page_size=10
```

**Search Meals**
```
GET /meals?name=Pasta
GET /meals?type=lunch
GET /meals?min_price=5&max_price=20
```

**Update Meal**
```
PUT /meals/<id>
Content-Type: application/json

{
  "name": "Updated Pasta",
  "price": 15.99
}
```

**Delete Meal**
```
DELETE /meals/<id>
```

**Get Healthy Meals**
```
GET /meals/healthy
```

## Data Flow

```
HTTP Request
    ↓
Controller (validates, calls service)
    ↓
Service (business logic, transforms DTO→POCO)
    ↓
DAO (database operations)
    ↓
Database
    ↓
DAO (returns POCO)
    ↓
Service (transforms POCO→DTO)
    ↓
Controller (returns DTO as JSON)
    ↓
HTTP Response
```

## Installation

```bash
cd python-12-fully-structured-flask
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5005`

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:5005/ping

# Create a meal
curl -X POST http://localhost:5005/meals \
  -H "Content-Type: application/json" \
  -d '{"name":"Pizza","type":"lunch","price":15.99,"calories":500}'

# Get all meals
curl http://localhost:5005/meals

# Get meal by ID
curl http://localhost:5005/meals/1

# Search by type
curl http://localhost:5005/meals?type=lunch

# Update meal
curl -X PUT http://localhost:5005/meals/1 \
  -H "Content-Type: application/json" \
  -d '{"price":18.99}'

# Delete meal
curl -X DELETE http://localhost:5005/meals/1

# Get healthy meals
curl http://localhost:5005/meals/healthy
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| **POCO** | `POCO/meal.py` - Domain model with business logic |
| **DTO** | `DTO/*.py` - Request/Response objects with validation |
| **DAO** | `DAO/meals_dao.py` - Database operations with interface |
| **PDBC** | `db.py` - Connection management |
| **Service** | `Service/meal_service.py` - Business logic orchestration |
| **Controller** | `Controller/meals_controller.py` - HTTP handling |
| **Factory** | `DAO/dao_factory.py` - Dependency injection |
| **Mapper** | `Utils/dto_mapper.py` - DTO↔POCO conversion |

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Each layer can be tested independently
3. **Maintainability**: Changes in one layer don't affect others
4. **Reusability**: Components can be reused across applications
5. **Scalability**: Layers can be scaled independently
6. **Flexibility**: Easy to swap implementations (e.g., change database)

## Related Documentation

See the comprehensive tutorial at:
`/Users/hothaifa/workspace/DevSecOps-22/python/lessons/13-layered-architecture-dao-poco-dto.md`
