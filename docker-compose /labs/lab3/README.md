# Exercise 3: Full-Stack Application (React + Flask + PostgreSQL)

## Overview
This exercise demonstrates how to deploy a complete full-stack application using Docker Compose with:
- **React Frontend**: Modern web application with responsive UI
- **Flask Backend**: RESTful API server with database integration
- **PostgreSQL Database**: Relational database for structured data storage

## Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   React     │    │   Flask     │    │ PostgreSQL  │
│  Frontend   │◄──►│   Backend   │◄──►│  Database   │
│  (Port 3000)│    │ (Port 5000) │    │ (Port 5432) │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Quick Start

### 1. Start all services
```bash
docker-compose up -d
```

### 2. Verify services are running
```bash
docker-compose ps
```

### 3. Access the application
- **React Frontend**: http://localhost:3000
- **Flask Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000
- **PostgreSQL Database**: localhost:5432

### 4. Generate sample data (optional)
```bash
cd data-generator
pip install -r requirements.txt
python generate_postgres_data.py
```

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `POSTGRES_DB` | PostgreSQL database name | `appdb` |
| `POSTGRES_USER` | PostgreSQL username | `appuser` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `apppassword123` |
| `DATABASE_URL` | Database connection URL | `postgresql://appuser:apppassword123@postgres:5432/appdb` |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Flask debug mode | `True` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-here-change-in-production` |
| `BACKEND_URL` | Backend URL | `http://localhost:5000` |
| `REACT_APP_API_URL` | API URL for React | `http://localhost:5000` |
| `REACT_APP_TITLE` | Application title | `Full-Stack Docker App` |

## Volumes

| Volume | Purpose | Mount Point |
|--------|---------|-------------|
| `postgres_data` | Persistent PostgreSQL data storage | `/var/lib/postgresql/data` |
| `./backend` | Backend development code | `/app` |
| `./frontend` | Frontend development code | `/app` |

## Network Configuration

All services communicate over a dedicated bridge network:
- **Network Name**: `app-network`
- **Driver**: `bridge`

## Port Mappings

| Service | Container Port | Host Port |
|---------|----------------|-----------|
| PostgreSQL | 5432 | 5432 |
| Flask Backend | 5000 | 5000 |
| React Frontend | 3000 | 3000 |

## API Endpoints

### Health & Status
- `GET /` - API information
- `GET /health` - Health check with database status
- `GET /api/stats` - Database statistics

### Users
- `GET /api/users` - Get all users (paginated)
- `GET /api/users/<id>` - Get specific user

### Products
- `GET /api/products` - Get all products (paginated, filterable)
- `GET /api/products/<id>` - Get specific product

### Orders
- `GET /api/orders` - Get all orders (paginated, filterable)
- `POST /api/orders` - Create new order

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `first_name`, `last_name` - User's name
- `age`, `city`, `country` - Demographic information
- `bio` - User biography
- `is_active` - Account status
- `registration_date`, `last_login` - Timestamps

### Products Table
- `id` - Primary key
- `product_id` - Unique product identifier
- `name` - Product name
- `description` - Product description
- `category` - Product category
- `price`, `currency` - Pricing information
- `stock` - Inventory count
- `sku` - Stock keeping unit
- `brand` - Product brand
- `weight`, `dimensions` - Physical specifications
- `images` - Product images (JSON array)
- `tags` - Product tags
- `rating`, `reviews` - Customer feedback

### Orders Table
- `id` - Primary key
- `order_id` - Unique order identifier
- `user_id` - Foreign key to users
- `total_amount`, `currency` - Order total
- `status` - Order status (pending, processing, shipped, delivered, cancelled)
- `shipping_address` - Delivery address (JSON)
- `payment_method` - Payment type
- `order_date`, `shipping_date`, `delivery_date` - Order timestamps

## Development Features

### Hot Reload
- **Flask Backend**: Auto-reloads on code changes
- **React Frontend**: Hot module replacement for fast development

### Health Checks
- All containers include health checks
- Database connectivity monitoring
- Automatic service recovery

### Development Volumes
- Source code mounted for live editing
- Dependencies cached in containers
- No need to rebuild on code changes

## Useful Commands

### View logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs postgres
docker-compose logs backend
docker-compose logs frontend
```

### Execute commands in containers
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U appuser -d appdb

# Connect to Flask backend shell
docker-compose exec backend python

# Access React container
docker-compose exec frontend sh
```

### Database operations
```bash
# Connect to database
docker-compose exec postgres psql -U appuser -d appdb

# View tables
\dt

# View schema
\dt app_schema.*

# Query users
SELECT * FROM app_schema.users LIMIT 5;

# Query products
SELECT * FROM app_schema.products LIMIT 5;
```

### Development workflow
```bash
# Rebuild services after major changes
docker-compose up --build -d

# Stop services
docker-compose down

# Stop services and remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Clean up unused resources
docker system prune
```

## Frontend Features

### Dashboard
- Real-time statistics display
- Data tables for users, products, and orders
- Responsive design with Bootstrap
- Auto-refresh functionality

### UI Components
- Navigation bar with application title
- Statistics cards with counts
- Data tables with pagination
- Status badges and indicators
- Refresh button for data updates

## Backend Features

### RESTful API
- JSON responses with proper status codes
- Error handling and logging
- Database connection pooling
- CORS support for frontend integration

### Data Validation
- Input validation using Marshmallow schemas
- Proper error responses
- Database constraint handling

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check if PostgreSQL is running: `docker-compose ps`
   - Verify environment variables in `.env` file
   - Check database logs: `docker-compose logs postgres`

2. **Frontend can't connect to backend**
   - Verify API URL in `.env` file
   - Check backend logs: `docker-compose logs backend`
   - Ensure both services are on the same network

3. **Port conflicts**
   - Change port mappings in `docker-compose.yml`
   - Kill processes using ports: `lsof -ti:3000 | xargs kill -9`

4. **Build errors**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild services: `docker-compose up --build`

### Health Checks

```bash
# Check service health
docker-compose ps

# Check backend health
curl http://localhost:5000/health

# Check frontend
curl http://localhost:3000

# Check database connectivity
docker-compose exec postgres pg_isready -U appuser -d appdb
```

## Learning Objectives

After completing this exercise, you will understand:
- Full-stack application architecture
- Container orchestration with Docker Compose
- Database integration and migrations
- API development with Flask
- Frontend development with React
- Environment variable management
- Persistent data storage
- Development vs production configurations
- Health monitoring and logging

## Next Steps

1. Explore the React frontend interface
2. Test API endpoints with curl or Postman
3. Examine the database schema and data
4. Modify the data generator scripts
5. Add new features to the application
6. Experiment with different database queries
7. Try deploying to different environments
