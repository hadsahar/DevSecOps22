# Docker Compose Tutorial

## What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.

---

## Basic docker-compose.yml Structure

```yaml
version: '3.8'                    # Compose file format version

services:                         # Define your containers
  web:                            # Service name (container name prefix)
    image: nginx:latest           # Docker image to use
    container_name: my-nginx      # Custom container name (optional)
    ports:                        # Port mapping host:container
      - "8080:80"
    environment:                  # Environment variables
      - NODE_ENV=production
    volumes:                      # Mount volumes
      - ./html:/usr/share/nginx/html
    networks:                     # Connect to networks
      - frontend
    depends_on:                   # Start order dependency
      - db
    restart: always               # Restart policy

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - frontend

volumes:                          # Named volumes declaration
  db_data:

networks:                         # Custom networks declaration
  frontend:
    driver: bridge
```

---

## Line-by-Line Explanation

| Line | Explanation |
|------|-------------|
| `version: '3.8'` | Specifies Compose file format (determines available features) |
| `services:` | Root key for defining all containers |
| `web:` | Service name - used for DNS resolution between containers |
| `image:` | Docker image to pull from registry |
| `container_name:` | Override default naming (project_service_1) |
| `ports:` | Expose ports - `"HOST:CONTAINER"` format |
| `environment:` | Set env vars (list or key-value format) |
| `volumes:` | Mount host paths or named volumes |
| `networks:` | Attach service to specific networks |
| `depends_on:` | Control startup order (not readiness) |
| `restart:` | Container restart policy |

---

## Version Differences

| Version | Docker Engine | Key Features |
|---------|---------------|--------------|
| `2.x` | 1.10.0+ | Single host, `depends_on` conditions |
| `3.x` | 1.13.0+ | Swarm mode support, deploy configs |
| `3.8` | 19.03.0+ | Latest stable, most features |
| No version | 20.10.0+ | Compose Specification (recommended) |

### Modern Approach (No Version)
```yaml
# Compose Specification - no version needed
services:
  app:
    image: myapp:latest
```

---

## Volume Types

### 1. Named Volumes (Recommended for Data)
```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data    # Named volume

volumes:
  db_data:                                   # Declaration required
    driver: local
```

### 2. Bind Mounts (Development)
```yaml
services:
  app:
    volumes:
      - ./src:/app/src                       # Host path:Container path
      - ./config:/app/config:ro              # :ro = read-only
```

### 3. Anonymous Volumes
```yaml
services:
  app:
    volumes:
      - /app/node_modules                    # Anonymous (not recommended)
```

### Volume Comparison

| Type | Use Case | Persistence | Portability |
|------|----------|-------------|-------------|
| Named | Production data | ✅ Persists | ✅ Portable |
| Bind Mount | Development | ✅ Persists | ❌ Host-dependent |
| Anonymous | Temporary | ❌ Lost on remove | ❌ Not portable |

---

## Network Types

```yaml
networks:
  frontend:
    driver: bridge              # Default - isolated network
  
  backend:
    driver: bridge
    internal: true              # No external access
  
  existing:
    external: true              # Use pre-existing network
    name: my-external-network
```

---

## Production Best Practices

### Production-Ready docker-compose.prod.yml

```yaml
services:
  app:
    image: myapp:${APP_VERSION:-latest}     # Use versioned tags
    container_name: myapp-prod
    
    # Resource Limits
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
      replicas: 3                           # Multiple instances
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    
    # Security
    read_only: true                         # Read-only filesystem
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"                       # Non-root user
    
    # Health Check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    # Environment (use secrets, not plain text)
    env_file:
      - .env.prod
    secrets:
      - db_password
    
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine               # Use alpine for smaller size
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          memory: 2G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      app:
        condition: service_healthy          # Wait for health check
    networks:
      - frontend

# Secrets from files
secrets:
  db_password:
    file: ./secrets/db_password.txt

# Named volumes with backup-friendly config
volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true                          # Isolated from external
```

---

## Best Practices Checklist

### ✅ Security
- [ ] Use specific image tags, not `latest`
- [ ] Run as non-root user
- [ ] Use secrets for sensitive data
- [ ] Set `read_only: true` where possible
- [ ] Use `no-new-privileges`

### ✅ Reliability
- [ ] Define health checks
- [ ] Set resource limits
- [ ] Configure restart policies
- [ ] Use `depends_on` with conditions

### ✅ Performance
- [ ] Use alpine-based images
- [ ] Set memory/CPU limits
- [ ] Configure logging limits

### ✅ Data Management
- [ ] Use named volumes for persistence
- [ ] Bind mounts only for development
- [ ] Regular volume backups

### ✅ Networking
- [ ] Use internal networks for backend
- [ ] Separate frontend/backend networks
- [ ] Don't expose unnecessary ports

---

## Common Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Scale service
docker compose up -d --scale app=3

# Use production file
docker compose -f docker-compose.prod.yml up -d

# Rebuild images
docker compose build --no-cache

# View running services
docker compose ps

# Execute command in container
docker compose exec app sh
```

---

## File Structure for Projects

```
project/
├── docker-compose.yml          # Base/development config
├── docker-compose.prod.yml     # Production overrides
├── docker-compose.override.yml # Local dev overrides (auto-loaded)
├── .env                        # Environment variables
├── .env.prod                   # Production env vars
├── secrets/
│   └── db_password.txt
├── nginx/
│   └── nginx.conf
└── app/
    └── Dockerfile
```

### Override Example
```bash
# Development (uses docker-compose.yml + docker-compose.override.yml)
docker compose up -d

# Production (explicit files)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
