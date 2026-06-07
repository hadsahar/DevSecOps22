# Docker Volumes and Bind Mounts

## Storage in Docker — Overview

By default, container file systems are ephemeral — data written inside a container is **lost** when the container is removed. Docker provides three ways to persist or share data:

| Type | Managed by | Location | Best for |
|------|-----------|----------|---------|
| **Volume** | Docker | `/var/lib/docker/volumes/` | Persisting data, sharing between containers |
| **Bind Mount** | User | Anywhere on host | Dev workflows, config injection |
| **tmpfs Mount** | Kernel | RAM only | Sensitive data, fast temp storage |

```
Host filesystem
├── /var/lib/docker/volumes/myvolume/_data   ← Docker Volume
├── /home/user/myproject                     ← Bind Mount source
└── RAM                                      ← tmpfs
         ↕               ↕              ↕
      Container        Container      Container
```

---

## Part 1 — Docker Volumes

### What is a Volume?

A Docker-managed directory on the host. Docker handles its lifecycle independently of containers. Volumes survive container removal and can be shared across multiple containers.

---

### Creating and Managing Volumes

```bash
# Create a named volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect a volume (see mount point, driver, etc.)
docker volume inspect mydata

# Remove a specific volume
docker volume rm mydata

# Remove all unused volumes (not mounted to any container)
docker volume prune

# Remove volumes along with containers
docker rm -v mycontainer
```

---

### Using Volumes with docker run

```bash
# Mount named volume → /data inside container
docker run -d \
  --name mycontainer \
  -v mydata:/data \
  ubuntu:22.04 \
  bash -c "while true; do date >> /data/time.log; sleep 5; done"

# Short flag: -v <volume-name>:<container-path>
# Long flag:  --mount type=volume,source=mydata,target=/data

# Read-only volume
docker run -d \
  -v mydata:/data:ro \
  nginx:alpine
```

### --mount syntax (recommended, explicit)

```bash
docker run -d \
  --name postgres \
  --mount type=volume,source=pgdata,target=/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:16
```

---

### Real-World Volume Examples

#### PostgreSQL with persistent data
```bash
docker volume create pgdata

docker run -d \
  --name postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

Stop and remove the container — the database persists in `pgdata`:
```bash
docker stop postgres && docker rm postgres
# Data still lives in pgdata volume
docker run -d --name postgres2 -v pgdata:/var/lib/postgresql/data postgres:16
```

#### MySQL with persistent data
```bash
docker volume create mysqldata

docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=myapp \
  -v mysqldata:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
```

#### MongoDB
```bash
docker run -d \
  --name mongo \
  -v mongodata:/data/db \
  -p 27017:27017 \
  mongo:7
```

---

### Sharing a Volume Between Containers

```bash
docker volume create shared

# Writer container
docker run -d --name writer \
  -v shared:/data \
  ubuntu bash -c "while true; do echo \$(date) >> /data/log.txt; sleep 2; done"

# Reader container
docker run --rm --name reader \
  -v shared:/data:ro \
  ubuntu tail -f /data/log.txt
```

---

### Backing Up and Restoring Volumes

```bash
# Backup: run a helper container that tars the volume contents
docker run --rm \
  -v mydata:/source:ro \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/mydata-backup.tar.gz -C /source .

# Restore: extract tar into the volume
docker run --rm \
  -v mydata:/target \
  -v $(pwd):/backup \
  ubuntu \
  tar xzf /backup/mydata-backup.tar.gz -C /target
```

---

### Volume Drivers

```bash
# Default local driver
docker volume create --driver local myvolume

# NFS volume (shared storage across hosts)
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/nfs/shared \
  nfsvolume

# Use a third-party driver (e.g. rexray for cloud storage)
docker volume create --driver rexray/ebs myebsvol
```

---

## Part 2 — Bind Mounts

### What is a Bind Mount?

A bind mount maps a **specific path on the host** directly into the container. Changes on either side are immediately reflected on the other.

```bash
# Syntax
docker run -v /host/path:/container/path image

# --mount syntax
docker run --mount type=bind,source=/host/path,target=/container/path image
```

---

### Common Bind Mount Patterns

#### Development hot-reload (Node.js)
```bash
docker run -d \
  --name nodedev \
  -v $(pwd):/app \
  -w /app \
  -p 3000:3000 \
  node:20-alpine \
  sh -c "npm install && npm run dev"
```

Edit files on your host → changes reflect instantly inside the container.

#### Development hot-reload (Python Flask)
```bash
docker run -d \
  --name flaskdev \
  -v $(pwd):/app \
  -w /app \
  -p 5000:5000 \
  -e FLASK_ENV=development \
  python:3.12-slim \
  sh -c "pip install flask && flask run --host=0.0.0.0"
```

#### Inject a config file
```bash
docker run -d \
  --name nginx \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  -p 80:80 \
  nginx:alpine
```

#### Mount host logs directory
```bash
docker run -d \
  --name myapp \
  -v /var/log/myapp:/app/logs \
  myapp:latest
```

#### Pass SSH keys into a build container
```bash
docker run --rm \
  -v ~/.ssh:/root/.ssh:ro \
  alpine sh -c "ssh -T git@github.com"
```

---

### Read-Only Bind Mounts

```bash
# :ro prevents the container from writing to the host path
docker run -d \
  -v $(pwd)/config:/etc/myapp/config:ro \
  myapp:latest
```

---

### Bind Mount vs Volume: Key Differences

| | Bind Mount | Volume |
|---|---|---|
| Path | Explicit host path | Docker-managed |
| Portability | Low (host-specific) | High |
| Performance | Native | Native (local driver) |
| Permissions | Host controls | Docker controls |
| Backups | Manual | `docker volume` commands |
| Use in production | Rare | Recommended |
| Use in development | Common (hot-reload) | Uncommon |

---

## Part 3 — tmpfs Mounts

Stored in the host's **RAM**, never written to disk. Useful for temporary, sensitive data.

```bash
docker run -d \
  --name myapp \
  --mount type=tmpfs,target=/tmp,tmpfs-size=100m \
  myapp:latest

# Short syntax
docker run -d \
  --tmpfs /tmp:size=100m \
  myapp:latest
```

Use cases:
- Session tokens, API keys used at runtime
- Fast temporary file storage
- Secrets that must never touch disk

---

## Part 4 — Volumes in Docker Compose

### Named volumes
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### Bind mounts in Compose (dev)
```yaml
services:
  api:
    build: ./api
    volumes:
      - ./api:/app           # bind mount — hot reload
      - /app/node_modules    # anonymous volume — keep container's node_modules
    ports:
      - "3000:3000"

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
```

### External volumes (pre-created)
```yaml
volumes:
  pgdata:
    external: true   # must exist before compose up
```

### NFS volume in Compose
```yaml
volumes:
  nfsdata:
    driver: local
    driver_opts:
      type: nfs
      o: "addr=192.168.1.100,rw"
      device: ":/nfs/shared"
```

---

## Part 5 — Volume Lifecycle in Compose

```bash
# Start with volumes created automatically
docker compose up -d

# Stop but keep volumes
docker compose down

# Stop and REMOVE named volumes
docker compose down -v

# View volumes created by compose
docker volume ls | grep projectname
```

---

## Full Example — Full-Stack App with Volumes

```yaml
# docker-compose.yml
services:
  app:
    build: .
    volumes:
      - ./src:/app/src           # bind: hot-reload source
      - uploads:/app/uploads     # volume: user uploaded files
    ports:
      - "3000:3000"
    depends_on:
      - db
      - cache

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"

  cache:
    image: redis:7-alpine
    volumes:
      - redisdata:/data
    command: redis-server --appendonly yes

  backup:
    image: ubuntu:22.04
    volumes:
      - pgdata:/source:ro
      - ./backups:/backups
    command: >
      bash -c "
        while true; do
          tar czf /backups/pg-\$(date +%Y%m%d-%H%M%S).tar.gz -C /source .;
          sleep 86400;
        done
      "

volumes:
  pgdata:
  redisdata:
  uploads:
```

---

## Cheat Sheet

```bash
# ── Volumes ─────────────────────────────────────────────────
docker volume create mydata
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune

# ── Run with volume ──────────────────────────────────────────
docker run -v mydata:/data image
docker run --mount type=volume,source=mydata,target=/data image
docker run -v mydata:/data:ro image           # read-only

# ── Run with bind mount ──────────────────────────────────────
docker run -v $(pwd):/app image
docker run --mount type=bind,source=$(pwd),target=/app image
docker run -v $(pwd)/config.yml:/etc/app/config.yml:ro image

# ── tmpfs ────────────────────────────────────────────────────
docker run --tmpfs /tmp:size=50m image
docker run --mount type=tmpfs,target=/tmp,tmpfs-size=50m image

# ── Backup / Restore ─────────────────────────────────────────
# Backup
docker run --rm -v mydata:/src:ro -v $(pwd):/out ubuntu tar czf /out/backup.tar.gz -C /src .
# Restore
docker run --rm -v mydata:/dst -v $(pwd):/out ubuntu tar xzf /out/backup.tar.gz -C /dst
```
