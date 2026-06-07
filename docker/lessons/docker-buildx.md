# Docker Buildx Tutorial

## What is Docker Buildx?

**Docker Buildx** is the extended build CLI plugin built on top of **BuildKit** — Docker's next-generation build engine. It replaces the legacy `docker build` command with enhanced features:

- Multi-platform image builds (e.g., `linux/amd64` + `linux/arm64` in one command)
- Faster builds via advanced caching (registry cache, S3, GitHub Actions cache)
- Build matrix (bake) for building many images at once
- Named builders with custom configurations
- Output control (load, push, tar, OCI layout)

```
docker buildx build → BuildKit daemon → Image(s) for one or more platforms
```

---

## Prerequisites

Buildx ships with Docker Desktop and Docker Engine ≥ 19.03.

```bash
# Verify buildx is available
docker buildx version

# Enable BuildKit globally (add to ~/.docker/daemon.json or set env)
export DOCKER_BUILDKIT=1
```

---

## 1. Builders (Instances)

A **builder** is a named BuildKit instance. You can have multiple builders with different configurations.

### List builders
```bash
docker buildx ls
```

```
NAME/NODE       DRIVER/ENDPOINT  STATUS   PLATFORMS
default *       docker
  default       default          running  linux/amd64, linux/arm64
mybuilder       docker-container
  mybuilder0    desktop-linux    running  linux/amd64, linux/arm64, linux/arm/v7
```

### Create a new builder
```bash
# Create a builder using the docker-container driver (recommended)
docker buildx create --name mybuilder --driver docker-container --bootstrap

# Set it as the active builder
docker buildx use mybuilder

# Inspect it
docker buildx inspect mybuilder --bootstrap
```

### Builder drivers

| Driver | Description |
|--------|-------------|
| `docker` | Uses the Docker daemon (default, limited features) |
| `docker-container` | Runs BuildKit in a container, full features |
| `kubernetes` | Runs BuildKit pods in Kubernetes |
| `remote` | Connects to a remote BuildKit daemon |

---

## 2. Basic Multi-Platform Build

```bash
# Build for a single platform (same as regular docker build)
docker buildx build --platform linux/amd64 -t myapp:1.0 --load .

# Build for multiple platforms and push to registry
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t myrepo/myapp:1.0 \
  --push \
  .
```

**`--load`** — load into local Docker image store (single platform only)  
**`--push`** — push directly to registry  
**`--output`** — custom output (see below)

---

## 3. Output Types

```bash
# Load into local daemon
docker buildx build --load -t myapp .

# Push to registry
docker buildx build --push -t myrepo/myapp:latest .

# Export as a tar archive
docker buildx build --output type=docker,dest=myapp.tar .

# Export as OCI layout directory
docker buildx build --output type=oci,dest=./oci-dir .

# Export as a local directory (useful for extracting build artifacts)
docker buildx build --output type=local,dest=./output .
```

---

## 4. Build Cache

### Inline cache (simplest)
```bash
# Build and inline the cache in the image
docker buildx build \
  --cache-to type=inline \
  --push \
  -t myrepo/myapp:latest .

# Later builds use it
docker buildx build \
  --cache-from type=registry,ref=myrepo/myapp:latest \
  --push \
  -t myrepo/myapp:latest .
```

### Registry cache (recommended for CI)
```bash
docker buildx build \
  --cache-from type=registry,ref=myrepo/myapp:buildcache \
  --cache-to   type=registry,ref=myrepo/myapp:buildcache,mode=max \
  --push \
  -t myrepo/myapp:latest .
```

`mode=max` caches all layers including intermediate ones (better cache hit rate).  
`mode=min` only caches the final image layers (default).

### GitHub Actions cache
```bash
docker buildx build \
  --cache-from type=gha \
  --cache-to   type=gha,mode=max \
  --push \
  -t myrepo/myapp:latest .
```

### Local filesystem cache
```bash
docker buildx build \
  --cache-from type=local,src=/tmp/buildcache \
  --cache-to   type=local,dest=/tmp/buildcache,mode=max \
  -t myapp .
```

---

## 5. Build Arguments and Secrets

```bash
# Build args
docker buildx build \
  --build-arg APP_VERSION=2.0.0 \
  --build-arg NODE_ENV=production \
  -t myapp:2.0 .

# Mount a secret (never baked into image layers)
docker buildx build \
  --secret id=mysecret,src=./secret.txt \
  -t myapp .
```

In the Dockerfile:
```dockerfile
RUN --mount=type=secret,id=mysecret \
    cat /run/secrets/mysecret && \
    pip install --extra-index-url $(cat /run/secrets/mysecret) -r requirements.txt
```

### SSH agent forwarding
```bash
docker buildx build \
  --ssh default=$SSH_AUTH_SOCK \
  -t myapp .
```

In the Dockerfile:
```dockerfile
RUN --mount=type=ssh \
    git clone git@github.com:private/repo.git
```

---

## 6. RUN --mount cache (BuildKit feature)

Speed up builds by caching package manager directories:

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./

# Cache npm modules between builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .
CMD ["node", "server.js"]
```

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .

# Cache pip downloads between builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .
```

```dockerfile
FROM golang:1.22-alpine

WORKDIR /build
COPY go.mod go.sum ./

# Cache Go module downloads
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    go build -o server .
```

---

## 7. Bake — Build Matrix

**`docker buildx bake`** builds multiple images at once from a `docker-bake.hcl` (or JSON/Compose) file.

### docker-bake.hcl example

```hcl
# docker-bake.hcl

variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "myrepo"
}

group "default" {
  targets = ["api", "worker", "frontend"]
}

target "api" {
  context    = "./services/api"
  dockerfile = "Dockerfile"
  tags       = ["${REGISTRY}/api:${TAG}"]
  platforms  = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=registry,ref=${REGISTRY}/api:buildcache"]
  cache-to   = ["type=registry,ref=${REGISTRY}/api:buildcache,mode=max"]
}

target "worker" {
  context    = "./services/worker"
  tags       = ["${REGISTRY}/worker:${TAG}"]
  platforms  = ["linux/amd64", "linux/arm64"]
}

target "frontend" {
  context    = "./frontend"
  tags       = ["${REGISTRY}/frontend:${TAG}"]
  platforms  = ["linux/amd64"]
  args = {
    NODE_ENV = "production"
  }
}
```

```bash
# Build all targets in the default group
docker buildx bake --push

# Build a specific target
docker buildx bake api --push

# Override variables
docker buildx bake --set "*.tags=${REGISTRY}/myapp:v2" --push

# Preview what would be built (dry run)
docker buildx bake --print
```

### docker-compose.yml as bake file
```bash
docker buildx bake -f docker-compose.yml --push
```

---

## 8. Multi-Platform Setup with QEMU

To build `arm64` on an `amd64` host you need QEMU emulation:

```bash
# Install QEMU (one-time setup)
docker run --privileged --rm tonistiigi/binfmt --install all

# Create a multi-platform builder
docker buildx create \
  --name multiplatform \
  --driver docker-container \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --bootstrap

docker buildx use multiplatform

# Verify supported platforms
docker buildx inspect --bootstrap
```

---

## 9. Full CI/CD Example (GitHub Actions)

```yaml
# .github/workflows/docker-publish.yml
name: Build and Push

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myrepo/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 10. Inspecting Multi-Platform Images

```bash
# View manifest list (all platform variants)
docker buildx imagetools inspect myrepo/myapp:latest

# Create and annotate a manifest list manually
docker buildx imagetools create \
  --tag myrepo/myapp:latest \
  myrepo/myapp:amd64 \
  myrepo/myapp:arm64
```

---

## 11. Useful Buildx Commands Cheat Sheet

```bash
# ── Builders ────────────────────────────────────────────────
docker buildx ls                                  # list builders
docker buildx create --name mybuilder --bootstrap # create builder
docker buildx use mybuilder                       # set active builder
docker buildx inspect mybuilder                   # inspect builder
docker buildx rm mybuilder                        # remove builder

# ── Building ────────────────────────────────────────────────
docker buildx build -t myapp .                    # basic build
docker buildx build --platform linux/amd64,linux/arm64 --push -t myrepo/myapp .
docker buildx build --no-cache -t myapp .         # skip cache
docker buildx build --progress plain -t myapp .   # verbose output

# ── Cache ───────────────────────────────────────────────────
docker buildx prune                               # remove build cache
docker buildx prune --filter until=24h            # remove cache older than 24h
docker buildx du                                  # disk usage of build cache

# ── Bake ────────────────────────────────────────────────────
docker buildx bake --print                        # dry run / preview
docker buildx bake --push                         # build all and push
docker buildx bake api worker                     # build specific targets
```

---

## Quick-Reference: Legacy vs Buildx

| Feature | `docker build` | `docker buildx build` |
|---|---|---|
| Multi-platform | No | Yes |
| BuildKit cache mounts | Limited | Full |
| Registry cache | No | Yes |
| Bake / matrix builds | No | Yes |
| Build secrets | No | Yes |
| SSH forwarding | No | Yes |
| OCI output | No | Yes |
