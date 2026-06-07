# Dockerfile Tutorial

## What is a Dockerfile?

A **Dockerfile** is a plain-text script containing a series of instructions that Docker uses to automatically build an image. Each instruction creates a new layer in the image.

```
Dockerfile → docker build → Image → docker run → Container
```

---

## Dockerfile Instruction Reference

| Instruction   | Purpose                                              |
|---------------|------------------------------------------------------|
| `FROM`        | Base image to build upon                             |
| `RUN`         | Execute a command during build                       |
| `COPY`        | Copy files from host into image                      |
| `ADD`         | Like COPY but also handles URLs and tar extraction   |
| `WORKDIR`     | Set working directory inside the container           |
| `ENV`         | Set environment variables                            |
| `ARG`         | Build-time variable (not available at runtime)       |
| `EXPOSE`      | Document the port the container listens on           |
| `CMD`         | Default command to run when container starts         |
| `ENTRYPOINT`  | Fixed executable; CMD becomes its arguments          |
| `VOLUME`      | Declare a mount point                                |
| `USER`        | Set the user to run subsequent instructions          |
| `LABEL`       | Add metadata key-value pairs                         |
| `HEALTHCHECK` | Define a health-check command                        |
| `ONBUILD`     | Trigger instruction for child images                 |
| `STOPSIGNAL`  | Signal sent to stop the container                    |

---

## 1. FROM — Choosing a Base Image

```dockerfile
# Always start with FROM
FROM ubuntu:22.04

# Use a specific digest for reproducibility
FROM node:20-alpine

# Scratch — empty base (for compiled binaries)
FROM scratch
```

**Best practice:** prefer `-alpine` or `-slim` variants to keep images small.

---

## 2. RUN — Execute Commands

```dockerfile
FROM ubuntu:22.04

# Each RUN creates a new layer — chain commands to reduce layers
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
```

Two forms:
```dockerfile
# Shell form (uses /bin/sh -c)
RUN echo "hello"

# Exec form (no shell, safer for entrypoints)
RUN ["apt-get", "install", "-y", "curl"]
```

---

## 3. COPY and ADD

```dockerfile
FROM node:20-alpine
WORKDIR /app

# COPY <src-on-host> <dest-in-image>
COPY package*.json ./
COPY src/ ./src/

# ADD can unpack tarballs and fetch URLs (prefer COPY for local files)
ADD https://example.com/config.tar.gz /etc/myapp/
ADD archive.tar.gz /opt/
```

**Rule of thumb:** use `COPY` unless you specifically need `ADD`'s extra features.

---

## 4. WORKDIR

```dockerfile
FROM python:3.12-slim
WORKDIR /app          # creates /app if it doesn't exist

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

`WORKDIR` affects all subsequent `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions.

---

## 5. ENV and ARG

```dockerfile
FROM node:20-alpine

# ARG — available only at build time
ARG APP_VERSION=1.0.0

# ENV — available at build time AND runtime
ENV NODE_ENV=production \
    PORT=3000 \
    APP_VER=${APP_VERSION}

RUN echo "Building version $APP_VER"
```

Pass ARG at build time:
```bash
docker build --build-arg APP_VERSION=2.5.1 -t myapp .
```

---

## 6. EXPOSE

```dockerfile
FROM nginx:alpine
EXPOSE 80
EXPOSE 443
```

`EXPOSE` is **documentation only** — it does not publish the port. Use `-p` with `docker run` to actually publish:
```bash
docker run -p 8080:80 mynginx
```

---

## 7. CMD and ENTRYPOINT

| | `CMD` | `ENTRYPOINT` |
|---|---|---|
| Overridable at runtime? | Yes (`docker run image cmd`) | Partially (use `--entrypoint`) |
| Main purpose | Default arguments | Fixed executable |

```dockerfile
# CMD only — easily overridden
FROM ubuntu:22.04
CMD ["echo", "Hello World"]

# ENTRYPOINT + CMD — CMD provides default arguments
FROM ubuntu:22.04
ENTRYPOINT ["ping"]
CMD ["localhost"]
# docker run myimage          → ping localhost
# docker run myimage 8.8.8.8  → ping 8.8.8.8
```

---

## 8. USER — Non-Root Security

```dockerfile
FROM node:20-alpine
WORKDIR /app

COPY --chown=node:node . .
RUN npm ci --only=production

# Drop from root to node user
USER node

CMD ["node", "server.js"]
```

---

## 9. HEALTHCHECK

```dockerfile
FROM nginx:alpine

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

Check status:
```bash
docker inspect --format='{{.State.Health.Status}}' <container>
```

---

## 10. LABEL

```dockerfile
FROM python:3.12-slim

LABEL maintainer="devteam@example.com" \
      version="1.0" \
      description="My Python microservice"
```

---

## 11. VOLUME

```dockerfile
FROM postgres:16
VOLUME /var/lib/postgresql/data   # data survives container removal
```

---

## Full Example 1 — Node.js REST API

```dockerfile
# ── Stage: builder ──────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Stage: production ───────────────────────────────────────
FROM node:20-alpine AS production

ARG APP_VERSION=1.0.0
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

LABEL version="${APP_VERSION}" maintainer="devops@example.com"

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost:3000/health || exit 1

USER node
CMD ["node", "dist/index.js"]
```

Build and run:
```bash
docker build --build-arg APP_VERSION=2.0.0 -t myapi:2.0.0 .
docker run -d -p 3000:3000 --name api myapi:2.0.0
```

---

## Full Example 2 — Python Flask App

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 5000

HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## Full Example 3 — Go Binary (Multi-stage, tiny final image)

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server ./cmd/server

# Final stage — scratch (0 MB base)
FROM scratch

COPY --from=builder /build/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
ENTRYPOINT ["/server"]
```

Final image is only a few MB!

---

## Full Example 4 — Static Website with Nginx

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Multi-Stage Builds

Multi-stage builds let you use multiple `FROM` statements. Only the final stage ends up in the image.

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Benefits:
- Build tools stay out of the production image
- Dramatically smaller images
- Better security surface

---

## .dockerignore

Always create a `.dockerignore` alongside your `Dockerfile`:

```
node_modules/
.git/
.env
*.log
dist/
__pycache__/
.DS_Store
Dockerfile*
README.md
.dockerignore
```

This prevents large or sensitive files from being sent to the build context.

---

## Layer Caching Best Practices

```dockerfile
# ✅ GOOD — copy dependency files first, install, then copy source
COPY package*.json ./
RUN npm ci
COPY . .

# ❌ BAD — copying everything invalidates cache on any file change
COPY . .
RUN npm ci
```

Docker re-uses a cached layer if nothing above it changed. Put things that change rarely near the top.

---

## Common Build Commands

```bash
# Build with tag
docker build -t myapp:1.0 .

# Build with a different Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg ENV=production -t myapp .

# Build with no cache
docker build --no-cache -t myapp .

# View image layers
docker history myapp:1.0

# Inspect image metadata
docker inspect myapp:1.0

# Remove dangling images
docker image prune
```

---