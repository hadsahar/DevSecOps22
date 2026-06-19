# Exercise 1: MongoDB + Mongo Express

## Overview
This exercise demonstrates how to set up a MongoDB database with a web-based admin interface using Docker Compose.

## Architecture
- **MongoDB**: NoSQL database server
- **Mongo Express**: Web-based MongoDB administration interface
- **Data Generator**: Python script to populate database with sample data

## Quick Start

### 1. Start the services
```bash
docker-compose up -d
```

### 2. Verify services are running
```bash
docker-compose ps
```

### 3. Access the services
- **MongoDB**: `mongodb://admin:securepassword123@localhost:27017/`
- **Mongo Express**: http://localhost:8081
  - Username: `admin`
  - Password: `admin123`

### 4. Generate sample data (optional)
```bash
cd data-generator
pip install -r requirements.txt
python generate_mongo_data.py
```

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `MONGO_INITDB_ROOT_USERNAME` | MongoDB root username | `admin` |
| `MONGO_INITDB_ROOT_PASSWORD` | MongoDB root password | `securepassword123` |
| `MONGO_INITDB_DATABASE` | Initial database to create | `testdb` |
| `ME_CONFIG_MONGODB_ADMINUSERNAME` | Mongo Express admin username | `admin` |
| `ME_CONFIG_MONGODB_ADMINPASSWORD` | Mongo Express admin password | `securepassword123` |
| `ME_CONFIG_MONGODB_URL` | MongoDB connection URL | `mongodb://admin:securepassword123@mongo:27017/` |
| `ME_CONFIG_BASICAUTH_USERNAME` | Mongo Express web UI username | `admin` |
| `ME_CONFIG_BASICAUTH_PASSWORD` | Mongo Express web UI password | `admin123` |

## Volumes

| Volume | Purpose | Mount Point |
|--------|---------|-------------|
| `mongo_data` | Persistent MongoDB data storage | `/data/db` |
| `mongo_config` | MongoDB configuration storage | `/data/configdb` |
| `./mongo-init.js` | Database initialization script | `/docker-entrypoint-initdb.d/mongo-init.js` |

## Network Configuration

The services communicate over a dedicated bridge network:
- **Network Name**: `mongo-network`
- **Driver**: `bridge`

## Port Mappings

| Service | Container Port | Host Port |
|---------|----------------|-----------|
| MongoDB | 27017 | 27017 |
| Mongo Express | 8081 | 8081 |

## Useful Commands

### View logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs mongo
docker-compose logs mongo-express
```

### Execute commands in containers
```bash
# Connect to MongoDB shell
docker-compose exec mongo mongosh -u admin -p securepassword123 --authenticationDatabase admin

# View container processes
docker-compose exec mongo ps
```

### Stop and remove services
```bash
# Stop services
docker-compose down

# Stop services and remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Rebuild and restart
docker-compose up --build -d
```

## Troubleshooting

### Common Issues

1. **Mongo Express can't connect to MongoDB**
   - Check if MongoDB is running: `docker-compose ps`
   - Verify environment variables in `.env` file
   - Check logs: `docker-compose logs mongo-express`

2. **Port already in use**
   - Change port mapping in `docker-compose.yml`
   - Kill process using the port: `lsof -ti:27017 | xargs kill -9`

3. **Authentication failed**
   - Verify username/password in `.env` file
   - Check MongoDB logs for initialization errors

### Health Checks

```bash
# Check if MongoDB is responding
docker-compose exec mongo mongosh --eval "db.adminCommand('ismaster')"

# Check network connectivity
docker-compose exec mongo-express ping mongo
```
