# Jenkins Agents — Docker, Kubernetes, and Nodes

## Table of Contents
1. [Why Use Agents?](#why-use-agents)
2. [Static (Permanent) Node Agents](#static-permanent-node-agents)
3. [Docker Agents](#docker-agents)
4. [Docker Compose for Multi-Container Tests](#docker-compose-for-multi-container-tests)
5. [Kubernetes Pod Agents](#kubernetes-pod-agents)
6. [Multi-Container Kubernetes Pods](#multi-container-kubernetes-pods)
7. [Agent Templates and Reuse](#agent-templates-and-reuse)
8. [Choosing the Right Agent Type](#choosing-the-right-agent-type)
9. [Complete Pipeline with Mixed Agents](#complete-pipeline-with-mixed-agents)

---

## Why Use Agents?

Agents allow you to:
- **Isolate build environments** — each build gets a clean, reproducible environment
- **Scale horizontally** — spin up agents on demand (Kubernetes/Docker)
- **Use specialized machines** — GPU agents, Windows agents, high-memory agents
- **Parallelize builds** — multiple agents run jobs concurrently
- **Prevent contamination** — dependencies from one build don't affect another

---

## Static (Permanent) Node Agents

Static agents are persistent machines registered in Jenkins. They are always online and ready.

### When to Use
- Long-running tools that are slow to install
- Agents with special hardware (GPU, HSM)
- Windows build agents
- Agents with persistent caches (Maven, npm)

### Agent Declaration in Pipeline

```groovy
// Run entire pipeline on a specific label
pipeline {
    agent { label 'linux && maven' }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

### Per-Stage Agent with Static Node

```groovy
pipeline {
    agent none

    stages {
        stage('Build on Linux') {
            agent { label 'linux' }
            steps {
                sh 'make build'
                stash name: 'binary', includes: 'bin/app'
            }
        }

        stage('Test on Windows') {
            agent { label 'windows' }
            steps {
                unstash 'binary'
                bat 'run-tests.bat'
            }
        }
    }
}
```

### Adding a Node via SSH

```bash
# On agent machine
sudo useradd -m -s /bin/bash jenkins
sudo mkdir -p /home/jenkins/agent
sudo chown jenkins:jenkins /home/jenkins/agent
sudo apt install -y openjdk-17-jre

# On controller — generate key
ssh-keygen -t ed25519 -C "jenkins-agent" -f ~/.ssh/jenkins_agent_key -N ""
# Copy public key to agent
ssh-copy-id -i ~/.ssh/jenkins_agent_key.pub jenkins@<agent-ip>
```

In Jenkins UI: **Manage Jenkins → Nodes → New Node**

---

## Docker Agents

Docker agents run each pipeline (or stage) inside a Docker container. The container is created at build start and destroyed at build end.

### Prerequisites
- Docker installed on the agent/controller
- Jenkins user in `docker` group: `sudo usermod -aG docker jenkins`
- **Docker Pipeline** plugin installed

### Simple Docker Agent

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
        }
    }

    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

### Docker Agent with Options

```groovy
pipeline {
    agent {
        docker {
            image  'maven:3.9-eclipse-temurin-17'
            args   '-v $HOME/.m2:/root/.m2 --memory=2g'
            label  'docker-host'
            registryUrl 'https://registry.example.com'
            registryCredentialsId 'registry-creds'
        }
    }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

| Option | Description |
|--------|-------------|
| `image` | Docker image to use |
| `args` | Extra `docker run` arguments |
| `label` | Which Jenkins agent runs Docker |
| `registryUrl` | Private registry URL |
| `registryCredentialsId` | Credentials for private registry |

### Per-Stage Docker Agents

```groovy
pipeline {
    agent none

    stages {
        stage('Build (Java)') {
            agent {
                docker { image 'maven:3.9-eclipse-temurin-17' }
            }
            steps {
                sh 'mvn clean package'
                stash name: 'jar', includes: 'target/*.jar'
            }
        }

        stage('Build (Node)') {
            agent {
                docker { image 'node:18-alpine' }
            }
            steps {
                sh 'npm ci && npm run build'
                stash name: 'frontend', includes: 'dist/**'
            }
        }

        stage('Package Docker Image') {
            agent { label 'docker-host' }
            steps {
                unstash 'jar'
                unstash 'frontend'
                sh "docker build -t myapp:${env.BUILD_NUMBER} ."
            }
        }
    }
}
```

### Custom Dockerfile as Agent

```groovy
pipeline {
    agent {
        dockerfile {
            filename   'Dockerfile.build'
            dir        'ci'
            args       '-v /var/run/docker.sock:/var/run/docker.sock'
            label      'docker-host'
        }
    }

    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
    }
}
```

`ci/Dockerfile.build`:
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    maven \
    nodejs \
    npm \
    docker.io \
    && rm -rf /var/lib/apt/lists/*
```

---

## Docker Compose for Multi-Container Tests

Use Docker Compose to start dependent services (database, cache, etc.) during tests:

```groovy
stage('Integration Tests') {
    agent { label 'docker-host' }
    steps {
        sh 'docker-compose -f docker-compose.test.yml up -d'
        sleep 15   // Wait for services to be healthy
        sh 'npm run test:integration'
    }
    post {
        always {
            sh 'docker-compose -f docker-compose.test.yml down --volumes || true'
        }
    }
}
```

`docker-compose.test.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DB_URL=postgres://postgres:password@db:5432/testdb
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: testdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

---

## Kubernetes Pod Agents

The **Kubernetes plugin** provisions a Pod as a Jenkins agent on demand. The pod is created when the build starts and deleted when it ends.

### Prerequisites
- **Kubernetes plugin** installed
- Jenkins configured with K8s cluster access: **Manage Jenkins → Clouds → Kubernetes**

### Minimal Kubernetes Agent

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: jnlp
                    image: jenkins/inbound-agent:latest
                  - name: maven
                    image: maven:3.9-eclipse-temurin-17
                    command: ["sleep"]
                    args: ["infinity"]
            '''
        }
    }

    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package'
                }
            }
        }
    }
}
```

### Full Kubernetes Agent with Resources and Volumes

```groovy
pipeline {
    agent {
        kubernetes {
            label       'k8s-agent'
            defaultContainer 'build'
            yaml '''
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    app: jenkins-agent
                spec:
                  serviceAccountName: jenkins
                  containers:
                  - name: jnlp
                    image: jenkins/inbound-agent:latest
                    resources:
                      requests:
                        memory: "256Mi"
                        cpu: "100m"

                  - name: build
                    image: maven:3.9-eclipse-temurin-17
                    command: ["sleep"]
                    args: ["infinity"]
                    resources:
                      requests:
                        memory: "1Gi"
                        cpu: "500m"
                      limits:
                        memory: "2Gi"
                        cpu: "1000m"
                    volumeMounts:
                    - name: m2-cache
                      mountPath: /root/.m2

                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run/docker.sock

                  volumes:
                  - name: m2-cache
                    persistentVolumeClaim:
                      claimName: maven-cache-pvc
                  - name: docker-socket
                    hostPath:
                      path: /var/run/docker.sock
            '''
        }
    }

    stages {
        stage('Build') {
            steps {
                container('build') {
                    sh 'mvn clean package -DskipTests'
                }
            }
        }

        stage('Test') {
            steps {
                container('build') {
                    sh 'mvn test'
                }
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                container('docker') {
                    sh "docker build -t myapp:${env.BUILD_NUMBER} ."
                }
            }
        }
    }
}
```

---

## Multi-Container Kubernetes Pods

Use different containers in different stages of the same pipeline:

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: jnlp
                    image: jenkins/inbound-agent:latest
                  - name: node
                    image: node:18-alpine
                    command: ["sleep"]
                    args: ["infinity"]
                  - name: sonar
                    image: sonarsource/sonar-scanner-cli:latest
                    command: ["sleep"]
                    args: ["infinity"]
                  - name: helm
                    image: alpine/helm:3.13.0
                    command: ["sleep"]
                    args: ["infinity"]
            '''
        }
    }

    stages {
        stage('Install & Build') {
            steps {
                container('node') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
            }
        }

        stage('Test') {
            steps {
                container('node') {
                    sh 'npm test -- --coverage'
                }
            }
        }

        stage('Code Quality') {
            steps {
                container('sonar') {
                    withSonarQubeEnv('SonarQube') {
                        sh 'sonar-scanner'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                container('helm') {
                    withKubeConfig([credentialsId: 'k8s-prod']) {
                        sh "helm upgrade --install myapp ./helm --set image.tag=${env.BUILD_NUMBER}"
                    }
                }
            }
        }
    }
}
```

---

## Agent Templates and Reuse

### Define Reusable Pod Templates

Configure pod templates in **Manage Jenkins → Clouds → Kubernetes → Pod Templates** so pipelines can reference them by label:

```groovy
// Reference a pre-configured pod template by label
pipeline {
    agent { label 'maven-pod' }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

### Inline Pod Template with `podTemplate()`

```groovy
def podYaml = '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: python
        image: python:3.11-slim
        command: ["sleep"]
        args: ["infinity"]
'''

pipeline {
    agent {
        kubernetes {
            yaml podYaml
            defaultContainer 'python'
        }
    }

    stages {
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
    }
}
```

---

## Choosing the Right Agent Type

| Agent Type | Pros | Cons | Best For |
|------------|------|------|---------|
| **Static Node** | Fast startup, persistent cache | Manual management, scaling | Specialized hardware, Windows |
| **Docker Container** | Clean, reproducible, fast | Requires Docker daemon | Most CI builds |
| **Kubernetes Pod** | Auto-scale, cloud-native | K8s complexity | Cloud environments, large teams |
| **EC2 (Cloud)** | On-demand, cost-effective | Slow startup (2-5 min) | Cost-sensitive workloads |

---

## Complete Pipeline with Mixed Agents

```groovy
pipeline {
    agent none

    environment {
        APP_NAME = 'my-service'
        REGISTRY = 'registry.example.com'
    }

    stages {
        stage('Build & Test') {
            agent {
                kubernetes {
                    yaml '''
                        apiVersion: v1
                        kind: Pod
                        spec:
                          containers:
                          - name: jnlp
                            image: jenkins/inbound-agent:latest
                          - name: maven
                            image: maven:3.9-eclipse-temurin-17
                            command: ["sleep"]
                            args: ["infinity"]
                    '''
                    defaultContainer 'maven'
                }
            }
            steps {
                sh 'mvn clean package'
                stash name: 'artifacts', includes: 'target/*.jar'
            }
            post {
                always { junit '**/target/surefire-reports/*.xml' }
            }
        }

        stage('Docker Build & Push') {
            agent { label 'docker-host' }
            steps {
                unstash 'artifacts'
                sh "docker build -t ${REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER} ."
                withCredentials([usernamePassword(
                    credentialsId: 'registry-creds',
                    usernameVariable: 'REG_USER',
                    passwordVariable: 'REG_PASS'
                )]) {
                    sh "docker login -u $REG_USER -p $REG_PASS ${REGISTRY}"
                    sh "docker push ${REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy') {
            agent {
                kubernetes {
                    yaml '''
                        apiVersion: v1
                        kind: Pod
                        spec:
                          containers:
                          - name: jnlp
                            image: jenkins/inbound-agent:latest
                          - name: helm
                            image: alpine/helm:3.13.0
                            command: ["sleep"]
                            args: ["infinity"]
                    '''
                    defaultContainer 'helm'
                }
            }
            steps {
                withKubeConfig([credentialsId: 'k8s-staging']) {
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace staging \
                            --set image.tag=${env.BUILD_NUMBER}
                    """
                }
            }
        }
    }
}
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| `agent any` | Run on any available agent |
| `agent { label '...' }` | Target specific node by label |
| `agent { docker { image '...' } }` | Run inside a Docker container |
| `agent { dockerfile { ... } }` | Build and use a custom Dockerfile |
| `agent { kubernetes { yaml '...' } }` | Run in a K8s pod (ephemeral) |
| `container('name')` | Switch between containers in a K8s pod |
| `stash` / `unstash` | Pass files between agents in different stages |
| `agent none` + per-stage agents | Use different environments per stage |
