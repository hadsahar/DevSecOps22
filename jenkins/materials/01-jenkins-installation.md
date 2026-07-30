# Jenkins Installation — Zero to Hero

## Table of Contents
1. [What is Jenkins?](#what-is-jenkins)
2. [Prerequisites](#prerequisites)
3. [Install Jenkins on Ubuntu](#install-jenkins-on-ubuntu)
4. [Install Jenkins via Docker](#install-jenkins-via-docker)
5. [Install Jenkins on Kubernetes](#install-jenkins-on-kubernetes)
6. [First-Time Setup Wizard](#first-time-setup-wizard)
7. [Verify Your Installation](#verify-your-installation)

---

## What is Jenkins?

Jenkins is an open-source automation server written in Java. It enables developers to build, test, and deploy software continuously. It is the most widely used CI/CD tool in the industry, with over 1,800 plugins covering everything from source control to cloud deployments.

---

## Prerequisites

| Requirement | Minimum |
|-------------|---------|
| RAM         | 256 MB (1 GB+ recommended) |
| Disk        | 10 GB free space |
| Java        | JDK 11 or 17 (Ubuntu install only) |
| OS          | Ubuntu 20.04/22.04, Docker 20+, K8s 1.22+ |

---

## Install Jenkins on Ubuntu

### Step 1 — Install Java

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-17-jre
java -version
```

### Step 2 — Add Jenkins Repository

```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

### Step 3 — Install Jenkins

```bash
sudo apt update
sudo apt install jenkins -y
```

### Step 4 — Start and Enable Jenkins

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
```

### Step 5 — Open Firewall (if UFW is active)

```bash
sudo ufw allow 8080
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### Step 6 — Get Initial Admin Password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Jenkins is now accessible at: **http://\<your-server-ip\>:8080**

### Useful Ubuntu Jenkins Commands

```bash
sudo systemctl start jenkins      # Start Jenkins
sudo systemctl stop jenkins       # Stop Jenkins
sudo systemctl restart jenkins    # Restart Jenkins
sudo systemctl status jenkins     # Check status
journalctl -u jenkins -f          # Follow logs
```

---

## Install Jenkins via Docker

Docker is the fastest way to get Jenkins running locally or on any server with Docker installed.

### Step 1 — Pull the Official Jenkins Image

```bash
docker pull jenkins/jenkins:lts-jdk17
```

### Step 2 — Create a Persistent Volume

```bash
docker volume create jenkins_home
```

### Step 3 — Run Jenkins Container

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --restart=unless-stopped \
  jenkins/jenkins:lts-jdk17
```

| Port  | Purpose |
|-------|---------|
| 8080  | Jenkins Web UI |
| 50000 | Jenkins agent inbound port (JNLP) |

### Step 4 — Get Initial Admin Password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 5 — Docker Compose (Recommended for Persistence)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    container_name: jenkins
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - JAVA_OPTS=-Djenkins.install.runSetupWizard=false

volumes:
  jenkins_home:
```

> **Note:** Mounting `/var/run/docker.sock` allows Jenkins to run Docker commands from within the container (Docker-in-Docker pattern).

```bash
docker-compose up -d
docker-compose logs -f jenkins
```

### Useful Docker Jenkins Commands

```bash
docker logs -f jenkins                    # Follow logs
docker exec -it jenkins bash              # Shell into container
docker stop jenkins                       # Stop
docker start jenkins                      # Start
docker rm -f jenkins                      # Remove container
docker volume rm jenkins_home             # Remove data (destructive!)
```

---

## Install Jenkins on Kubernetes

Running Jenkins on Kubernetes provides high availability, scalability, and dynamic agent provisioning.

### Step 1 — Create a Namespace

```bash
kubectl create namespace jenkins
```

### Step 2 — Create a Persistent Volume Claim

```yaml
# jenkins-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins-pvc
  namespace: jenkins
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

```bash
kubectl apply -f jenkins-pvc.yaml
```

### Step 3 — Create a Service Account with RBAC

```yaml
# jenkins-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: jenkins
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: jenkins
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/exec", "pods/log", "persistentvolumeclaims", "events"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jenkins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: jenkins
subjects:
  - kind: ServiceAccount
    name: jenkins
    namespace: jenkins
```

```bash
kubectl apply -f jenkins-rbac.yaml
```

### Step 4 — Create the Jenkins Deployment

```yaml
# jenkins-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
  namespace: jenkins
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      serviceAccountName: jenkins
      containers:
        - name: jenkins
          image: jenkins/jenkins:lts-jdk17
          ports:
            - containerPort: 8080
            - containerPort: 50000
          volumeMounts:
            - name: jenkins-storage
              mountPath: /var/jenkins_home
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
      volumes:
        - name: jenkins-storage
          persistentVolumeClaim:
            claimName: jenkins-pvc
```

```bash
kubectl apply -f jenkins-deployment.yaml
```

### Step 5 — Expose Jenkins with a Service

```yaml
# jenkins-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: jenkins
  namespace: jenkins
spec:
  type: NodePort
  selector:
    app: jenkins
  ports:
    - name: http
      port: 8080
      targetPort: 8080
      nodePort: 30080
    - name: jnlp
      port: 50000
      targetPort: 50000
```

```bash
kubectl apply -f jenkins-service.yaml
```

Access Jenkins at: **http://\<node-ip\>:30080**

### Step 6 — Get Initial Admin Password from Pod

```bash
kubectl get pods -n jenkins
kubectl exec -n jenkins <pod-name> -- cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 7 — Install Jenkins with Helm (Easiest K8s Method)

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update

helm install jenkins jenkins/jenkins \
  --namespace jenkins \
  --create-namespace \
  --set controller.serviceType=NodePort \
  --set controller.nodePort=30080 \
  --set persistence.size=10Gi
```

Get admin password after Helm install:

```bash
kubectl exec -n jenkins -it svc/jenkins -- /bin/cat /run/secrets/additional/chart-admin-password
```

---

## First-Time Setup Wizard

Once you access Jenkins at port 8080:

1. **Unlock Jenkins** — Paste the initial admin password
2. **Install Suggested Plugins** — Click "Install suggested plugins" (recommended for beginners)
3. **Create Admin User** — Set username, password, full name, and email
4. **Configure Jenkins URL** — Set the URL used by Jenkins (important for webhooks and email links)
5. **Start Using Jenkins!**

### Suggested Plugins Installed by Default
- Git
- Pipeline
- GitHub Integration
- Email Extension
- Credentials Binding
- SSH Agent
- Workspace Cleanup
- Build Timeout
- Timestamper

---

## Verify Your Installation

```bash
# Check the Jenkins version
curl -s http://localhost:8080/api/json?pretty=true \
  --user admin:<your-password> | grep version

# Check Jenkins is responding
curl -I http://localhost:8080/login
# Expected: HTTP/1.1 200 OK
```

### Health Check Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/login` | Web UI |
| `/api/json` | REST API |
| `/crumbIssuer/api/json` | CSRF token endpoint |
| `/metrics` | Prometheus metrics (if plugin installed) |

---

## Summary

| Method | Best For | Persistence |
|--------|----------|-------------|
| Ubuntu | Production VMs, bare metal | `/var/lib/jenkins` |
| Docker | Local dev, quick setup | Named volume |
| Docker Compose | Team dev environments | Named volume |
| Kubernetes | Production, scalable setups | PVC |
| Helm on K8s | Production with GitOps | PVC via values.yaml |
