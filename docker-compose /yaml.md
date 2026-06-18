# Complete YAML Tutorial

## What is YAML?
YAML (YAML Ain't Markup Language) is a human-readable data serialization format commonly used for configuration files in DevOps tools like Docker Compose, Kubernetes, Ansible, and CI/CD pipelines.

---

## Basic Syntax Rules

1. **Indentation**: Use spaces (not tabs), typically 2 spaces
2. **Case-sensitive**: `Name` and `name` are different
3. **Colon + space**: Key-value pairs use `: ` (colon followed by space)
4. **Comments**: Start with `#`

---

## Data Types

### Strings
```yaml
# Strings (quotes optional for simple text)
name: John Doe
message: "Hello, World!"
path: '/usr/local/bin'
multiline: |
  This is a multiline
  string that preserves
  line breaks
folded: >
  This is a folded string
  that becomes a single line
```

### Numbers
```yaml
integer: 42
float: 3.14
scientific: 1.0e+5
hex: 0x1A
octal: 0o17
```

### Booleans
```yaml
enabled: true
disabled: false
yes_value: yes    # Also true
no_value: no      # Also false
```

### Null
```yaml
empty: null
also_empty: ~
```

---

## Collections

### Lists (Arrays)
```yaml
# Block style
fruits:
  - apple
  - banana
  - orange

# Inline style
colors: [red, green, blue]

# List of numbers
ports:
  - 80
  - 443
  - 8080
```

### Dictionaries (Maps)
```yaml
# Block style
person:
  name: John
  age: 30
  city: New York

# Inline style
coordinates: {x: 10, y: 20, z: 30}
```

### Nested Structures
```yaml
company:
  name: TechCorp
  employees:
    - name: Alice
      role: Developer
      skills:
        - Python
        - Docker
    - name: Bob
      role: DevOps
      skills:
        - Kubernetes
        - Terraform
```

---

## Advanced Features

### Anchors and Aliases (Reusability)
```yaml
# Define anchor with &
defaults: &default_settings
  timeout: 30
  retries: 3
  logging: true

# Reference with *
development:
  <<: *default_settings  # Merge anchor
  debug: true

production:
  <<: *default_settings
  debug: false
  timeout: 60  # Override
```

### Multiple Documents
```yaml
---
document: 1
name: first
---
document: 2
name: second
...
```

### Environment Variables (Docker Compose)
```yaml
services:
  app:
    environment:
      - DB_HOST=${DATABASE_HOST:-localhost}
      - DB_PORT=${DATABASE_PORT:-5432}
```

---

## Docker Compose Example

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    image: myapp:latest
    container_name: web-app
    ports:
      - "8080:80"
    environment:
      - NODE_ENV=production
      - API_KEY=${API_KEY}
    volumes:
      - ./app:/usr/src/app
      - app-data:/data
    networks:
      - frontend
      - backend
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend

volumes:
  app-data:
  postgres-data:
  redis-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

---

## Kubernetes Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.25
          ports:
            - containerPort: 80
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
            requests:
              memory: "64Mi"
              cpu: "250m"
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 3
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

---

## GitHub Actions Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t ${{ env.IMAGE_NAME }}:${{ github.sha }} .
      
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ${{ env.IMAGE_NAME }}:${{ github.sha }}
```

---

## Common Mistakes to Avoid

```yaml
# ❌ WRONG: Using tabs
services:
	web:    # Tab character - will cause error

# ✅ CORRECT: Using spaces
services:
  web:     # 2 spaces

# ❌ WRONG: Missing space after colon
name:value

# ✅ CORRECT: Space after colon
name: value

# ❌ WRONG: Inconsistent indentation
services:
  web:
   image: nginx  # 1 space
    ports:       # 2 spaces - inconsistent!

# ✅ CORRECT: Consistent indentation
services:
  web:
    image: nginx
    ports:
      - "80:80"

# ❌ WRONG: Special characters without quotes
password: p@ss:word!

# ✅ CORRECT: Quote special characters
password: "p@ss:word!"
```

---

## YAML Validation Tools

```bash
# Using Python
pip install pyyaml
python -c "import yaml; yaml.safe_load(open('file.yaml'))"

# Using yamllint
pip install yamllint
yamllint docker-compose.yaml

# Online validators
# - https://www.yamllint.com/
# - https://yamlvalidator.com/
```

---

## Quick Reference

| Type | Syntax |
|------|--------|
| String | `key: value` or `key: "value"` |
| Number | `count: 42` |
| Boolean | `enabled: true` |
| Null | `empty: null` or `empty: ~` |
| List | `- item` or `[a, b, c]` |
| Dictionary | `key: value` or `{a: 1, b: 2}` |
| Multiline | `\|` (literal) or `>` (folded) |
| Anchor | `&name` |
| Alias | `*name` |
| Merge | `<<: *name` |
| Comment | `# comment` |
