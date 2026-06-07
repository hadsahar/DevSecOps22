# Docker Networking

## Overview

Docker networking lets containers communicate with each other, with the host, and with the outside world. Docker provides a pluggable networking subsystem powered by **network drivers**.

```
                     Internet
                        │
                   ┌────┴────┐
                   │  Host   │
                   │ Network │
                   └────┬────┘
                        │ (port publish -p)
              ┌─────────┴──────────┐
              │   Docker Engine    │
    ┌─────────┼────────────────────┼─────────┐
    │         │                    │         │
 bridge0    overlay0            host net   none
    │         │                             │
  ctr-A    ctr-B/C                        ctr-D
```

---

## Network Drivers

| Driver | Description |
|--------|-------------|
| `bridge` | Default. Isolated virtual switch on the host (single host) |
| `host` | Container shares the host's network namespace directly |
| `none` | No networking — fully isolated |
| `overlay` | Multi-host networking (Docker Swarm / Kubernetes) |
| `macvlan` | Container gets its own MAC/IP on the physical network |
| `ipvlan` | Like macvlan but shares the host MAC address |
| `network plugins` | Third-party (Weave, Calico, Cilium, etc.) |

---

## Part 1 — Bridge Networks

### Default bridge (`bridge`)

Every container not explicitly assigned a network joins `bridge`. Containers communicate by IP only (no DNS).

```bash
# Run two containers on default bridge
docker run -d --name c1 alpine sleep 3600
docker run -d --name c2 alpine sleep 3600

# c2 can reach c1 only by IP (no hostname DNS on default bridge)
docker inspect c1 | grep IPAddress
docker exec c2 ping 172.17.0.2
```

### User-defined bridge (recommended)

User-defined bridges provide **automatic DNS resolution** by container name.

```bash
# Create a custom network
docker network create mynet

# Attach containers to it
docker run -d --name db --network mynet postgres:16
docker run -d --name api --network mynet myapi:latest

# api can reach db by hostname "db" — DNS works!
docker exec api ping db
docker exec api curl http://db:5432
```

---

### Network Commands Reference

```bash
# List networks
docker network ls

# Create a network
docker network create mynet
docker network create --driver bridge --subnet 192.168.100.0/24 mynet

# Inspect a network
docker network inspect mynet

# Connect a running container to a network
docker network connect mynet mycontainer

# Disconnect a container from a network
docker network disconnect mynet mycontainer

# Remove a network
docker network rm mynet

# Remove all unused networks
docker network prune
```

---

### Bridge Network Options

```bash
docker network create \
  --driver bridge \
  --subnet 10.10.0.0/16 \
  --gateway 10.10.0.1 \
  --ip-range 10.10.1.0/24 \
  --opt com.docker.network.bridge.name=mydocker0 \
  mynet

# Assign a static IP to a container
docker run -d \
  --name webapp \
  --network mynet \
  --ip 10.10.1.50 \
  nginx:alpine
```

---

## Part 2 — Host Network

The container bypasses Docker's virtual networking and uses the **host's network stack** directly. No port publishing needed — the container's ports are the host's ports.

```bash
docker run -d \
  --name nginxhost \
  --network host \
  nginx:alpine

# Port 80 is directly accessible on the host — no -p needed
curl http://localhost:80
```

**Use cases:** performance-sensitive workloads, monitoring agents that need to see all network interfaces.

**Limitation:** only works on Linux. On Docker Desktop (Mac/Windows), host network does NOT mean the macOS host — it means the Linux VM.

---

## Part 3 — None Network

No network interfaces except loopback. The container is fully isolated.

```bash
docker run --rm \
  --network none \
  alpine \
  ip addr
# Output: only lo (127.0.0.1)

# Cannot reach anything
docker run --rm --network none alpine ping google.com
# ping: bad address 'google.com'
```

Use case: batch jobs, data processing that must not make external network calls.

---

## Part 4 — Port Publishing

Expose container ports to the host or external world:

```bash
# Publish container port 80 → host port 8080
docker run -d -p 8080:80 nginx:alpine

# Bind to specific host interface
docker run -d -p 127.0.0.1:8080:80 nginx:alpine   # localhost only
docker run -d -p 0.0.0.0:8080:80 nginx:alpine      # all interfaces

# Publish all EXPOSEd ports to random host ports
docker run -d -P nginx:alpine

# View port mappings
docker port mycontainer
docker ps  # shows published ports
```

### UDP ports
```bash
docker run -d -p 5353:5353/udp myapp
```

---

## Part 5 — Container DNS and Name Resolution

```bash
# Custom DNS server
docker run --dns 8.8.8.8 --dns 1.1.1.1 alpine nslookup google.com

# Add entries to /etc/hosts
docker run --add-host db.internal:192.168.1.50 alpine

# Set hostname
docker run --hostname myapp.internal alpine hostname

# DNS search domains
docker run --dns-search example.com alpine
```

On a **user-defined bridge**, Docker runs an embedded DNS server at `127.0.0.11`:
```bash
docker exec mycontainer cat /etc/resolv.conf
# nameserver 127.0.0.11
# options ndots:0
```

---

## Part 6 — Overlay Networks (Multi-Host / Swarm)

Overlay networks stretch across multiple Docker hosts. Required for Docker Swarm services.

```bash
# Initialize Swarm
docker swarm init --advertise-addr 192.168.1.10

# Create an overlay network
docker network create \
  --driver overlay \
  --attachable \
  --subnet 10.20.0.0/16 \
  myoverlay

# Deploy a stack using the overlay network
docker service create \
  --name web \
  --network myoverlay \
  --replicas 3 \
  -p 80:80 \
  nginx:alpine
```

Containers on different hosts joined to the same overlay network communicate as if on the same LAN.

---

## Part 7 — Macvlan Network

Assigns a real MAC address to each container, making it appear as a physical device on the network.

```bash
docker network create \
  --driver macvlan \
  --subnet 192.168.1.0/24 \
  --gateway 192.168.1.1 \
  --opt parent=eth0 \
  mymacvlan

docker run -d \
  --name iot-device \
  --network mymacvlan \
  --ip 192.168.1.200 \
  alpine sleep 3600
```

The container gets IP `192.168.1.200` and is directly reachable from the physical LAN — no port publishing needed.

---

## Part 8 — Networks in Docker Compose

### Default network

Compose automatically creates a default network for the project. All services join it and can reach each other by service name.

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"

  api:
    build: ./api
    # web can reach api at http://api:3000

  db:
    image: postgres:16
    # api can reach db at postgres://db:5432
```

### Custom networks
```yaml
services:
  frontend:
    image: nginx:alpine
    networks:
      - frontend-net

  api:
    build: ./api
    networks:
      - frontend-net   # can talk to frontend
      - backend-net    # can talk to db

  db:
    image: postgres:16
    networks:
      - backend-net    # isolated from frontend

networks:
  frontend-net:
  backend-net:
    internal: true    # no external internet access
```

### Network isolation pattern (3-tier)
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - dmz

  api:
    build: ./api
    networks:
      - dmz
      - internal

  worker:
    build: ./worker
    networks:
      - internal      # no public internet exposure

  db:
    image: postgres:16
    networks:
      - internal

  redis:
    image: redis:7-alpine
    networks:
      - internal

networks:
  dmz:
  internal:
    internal: true
```

### External network (pre-existing)
```yaml
networks:
  shared:
    external: true    # created outside compose — must exist
```

---

## Part 9 — Network Inspection and Debugging

```bash
# Inspect network details
docker network inspect bridge

# See which networks a container is connected to
docker inspect --format='{{json .NetworkSettings.Networks}}' mycontainer | python3 -m json.tool

# Exec into a container for network debugging
docker exec -it mycontainer sh

# Check connectivity from inside a container
ping db
curl http://api:3000/health
nc -zv db 5432

# View routing table inside container
ip route
ip addr

# DNS lookup
nslookup api
dig api

# Network stats
docker stats mycontainer
```

### Temporary debug container attached to a network
```bash
docker run --rm -it \
  --network mynet \
  --name debugger \
  nicolaka/netshoot \
  bash

# Inside netshoot — has curl, dig, ping, tcpdump, nmap, etc.
ping api
tcpdump -i eth0 port 3000
nmap -p 1-1024 db
```

---

## Part 10 — Full Example — Microservices with Network Segmentation

```yaml
# docker-compose.yml
services:
  traefik:
    image: traefik:v3.0
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - public

  frontend:
    build: ./frontend
    labels:
      - "traefik.http.routers.frontend.rule=Host(`example.com`)"
    networks:
      - public
      - app

  api:
    build: ./api
    labels:
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"
    environment:
      DATABASE_URL: postgres://admin:secret@db:5432/myapp
      REDIS_URL: redis://cache:6379
    networks:
      - public
      - app
      - data

  worker:
    build: ./worker
    environment:
      DATABASE_URL: postgres://admin:secret@db:5432/myapp
      REDIS_URL: redis://cache:6379
    networks:
      - data    # no public access at all

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - data

  cache:
    image: redis:7-alpine
    volumes:
      - redisdata:/data
    networks:
      - data

networks:
  public:
  app:
  data:
    internal: true    # db and cache cannot reach internet

volumes:
  pgdata:
  redisdata:
```

Network segmentation:
- `traefik` and user traffic → `public`
- Application services ↔ `app`
- Sensitive data stores → `data` (internal, no internet)
- `worker` only has access to `data` network

---

## Part 11 — iptables and Docker

Docker automatically manages `iptables` rules to handle:
- Container NAT (masquerade outbound traffic)
- Port publishing
- Network isolation between Docker networks

```bash
# View Docker's iptables chains
sudo iptables -L DOCKER -n -v
sudo iptables -t nat -L DOCKER -n -v
```

**Never manually delete Docker's iptables rules** — use `docker network` commands instead.

---

## Networking Cheat Sheet

```bash
# ── Networks ─────────────────────────────────────────────────
docker network ls
docker network create mynet
docker network create --driver bridge --subnet 10.0.0.0/24 mynet
docker network inspect mynet
docker network connect mynet container1
docker network disconnect mynet container1
docker network rm mynet
docker network prune

# ── Port publishing ──────────────────────────────────────────
docker run -p 8080:80 nginx               # host:container
docker run -p 127.0.0.1:8080:80 nginx     # bind to localhost only
docker run -P nginx                        # publish all exposed ports
docker port mycontainer                    # show port mappings

# ── DNS / resolution ─────────────────────────────────────────
docker run --dns 8.8.8.8 alpine
docker run --add-host myhost:1.2.3.4 alpine
docker run --hostname myapp alpine

# ── Debugging ────────────────────────────────────────────────
docker run --rm -it --network mynet nicolaka/netshoot bash
docker exec mycontainer ping othercontainer
docker exec mycontainer curl http://service:port/health
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container
```

---

## Summary: When to Use What

| Scenario | Use |
|----------|-----|
| Containers on same host talking to each other | User-defined bridge |
| Development with docker compose | Default compose network or named networks |
| Maximum network performance on Linux | `--network host` |
| Fully isolated container (no network) | `--network none` |
| Multi-host / Swarm services | Overlay network |
| Container needs a real IP on the LAN | Macvlan |
| Expose service to public internet | Port publishing (`-p`) |
| Hide database from the internet | Internal network |
