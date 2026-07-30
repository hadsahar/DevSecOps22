# Jenkins Architecture and Nodes

## Table of Contents
1. [Jenkins Architecture Overview](#jenkins-architecture-overview)
2. [Controller (Master) Node](#controller-master-node)
3. [Agent (Worker) Nodes](#agent-worker-nodes)
4. [Controller-Agent Communication](#controller-agent-communication)
5. [Node Types](#node-types)
6. [Adding a Permanent Agent Node](#adding-a-permanent-agent-node)
7. [Node Labels and Executors](#node-labels-and-executors)
8. [Distributed Builds — How It Works](#distributed-builds--how-it-works)
9. [Monitoring Nodes](#monitoring-nodes)

---

## Jenkins Architecture Overview

Jenkins follows a **Controller-Agent (Master-Worker)** architecture. The Controller manages the configuration, scheduling, and UI, while Agents execute the actual build jobs.

```
┌─────────────────────────────────────────────────────────┐
│                    JENKINS CONTROLLER                    │
│                                                         │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  Web UI     │  │  REST API│  │  Job Scheduler     │  │
│  └─────────────┘  └──────────┘  └───────────────────┘  │
│  ┌─────────────────────────────────────────────────┐   │
│  │             Plugin Manager                       │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Credentials & Config Store               │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │ SSH / JNLP / WebSocket
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼─────┐  ┌────────▼──────┐
│   Agent: Linux│  │  Agent: Win  │  │  Agent: Docker│
│  (ssh-agent)  │  │  (JNLP)      │  │  (Pod/DinD)   │
└───────────────┘  └──────────────┘  └───────────────┘
```

---

## Controller (Master) Node

The **Controller** is the central brain of Jenkins. It never runs build jobs directly in production — it only orchestrates.

### Responsibilities
- Stores all job configurations in `$JENKINS_HOME`
- Serves the Web UI (port 8080)
- Provides the REST API
- Manages credentials, secrets, and plugins
- Schedules jobs to agents based on labels
- Collects and displays build results
- Manages the build queue

### JENKINS_HOME Directory Structure

```
/var/jenkins_home/
├── config.xml              # Main Jenkins config
├── credentials.xml         # Credentials store
├── jobs/                   # All job definitions
│   └── my-job/
│       ├── config.xml
│       └── builds/
├── nodes/                  # Agent node configs
├── plugins/                # Installed plugins
├── secrets/                # Encrypted secrets
│   └── initialAdminPassword
├── logs/                   # Jenkins logs
└── workspace/              # Build workspaces (built-in node only)
```

> **Best Practice:** Never run builds on the Controller node in production. Go to **Manage Jenkins → Nodes → Built-In Node → Configure** and set **Number of executors = 0**.

---

## Agent (Worker) Nodes

Agents are machines (physical, virtual, container, or cloud-based) that execute the actual build steps delegated by the Controller.

### What Lives on an Agent
- Jenkins agent JAR (`agent.jar`)
- Workspace for each job it runs
- Tools like JDK, Maven, npm, Docker
- Outbound network connection back to Controller

### Agent Requirements
- Java (JDK 11 or 17)
- Network access to the Controller on port 50000 (JNLP) or 22 (SSH)
- Sufficient disk and RAM for builds

---

## Controller-Agent Communication

Jenkins supports three connection protocols:

### 1. SSH (Recommended for Linux Agents)
- Controller initiates an SSH connection to the agent machine
- Requires: SSH server on agent, SSH credentials in Jenkins
- Port: 22

```
Controller ──SSH:22──► Agent
```

### 2. JNLP / Inbound Agent (Recommended for Windows / Firewalled Agents)
- Agent initiates connection to the Controller
- Requires: Port 50000 open on Controller
- Agent runs: `java -jar agent.jar -jnlpUrl http://<controller>:50000/...`

```
Agent ──TCP:50000──► Controller
```

### 3. WebSocket (Modern Alternative to JNLP)
- Agent connects to Controller via WebSocket over port 443/80
- Ideal when only HTTP/S ports are open (cloud environments)

```
Agent ──WSS:443──► Controller (via /wsagents/)
```

---

## Node Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Built-in Node** | The Controller itself | Never use for builds in prod |
| **Permanent Agent** | Static VM or bare metal | Long-lived, always-on agents |
| **Cloud Agent (Docker)** | Container spun up per build | Ephemeral, clean environments |
| **Cloud Agent (Kubernetes)** | Pod spun up per build | Scalable, cloud-native builds |
| **EC2 Agent** | AWS EC2 instance provisioned on demand | Cost-effective scaling |

---

## Adding a Permanent Agent Node

### Step 1 — Prepare the Agent Machine

```bash
# On the agent machine (Ubuntu)
sudo apt update
sudo apt install -y openjdk-17-jre
sudo useradd -m -s /bin/bash jenkins
sudo mkdir -p /home/jenkins/agent
sudo chown jenkins:jenkins /home/jenkins/agent
```

### Step 2 — Create SSH Key on Controller

```bash
# On the Jenkins controller
ssh-keygen -t rsa -b 4096 -C "jenkins-agent" -f ~/.ssh/jenkins_agent_key
cat ~/.ssh/jenkins_agent_key.pub
```

Copy the public key to the agent:

```bash
# On the agent machine
sudo -u jenkins mkdir -p /home/jenkins/.ssh
echo "<public-key-content>" >> /home/jenkins/.ssh/authorized_keys
chmod 700 /home/jenkins/.ssh
chmod 600 /home/jenkins/.ssh/authorized_keys
```

### Step 3 — Add SSH Credential in Jenkins

1. Go to **Manage Jenkins → Credentials → System → Global credentials**
2. Click **Add Credentials**
3. Kind: **SSH Username with private key**
4. ID: `agent-ssh-key`
5. Username: `jenkins`
6. Private Key: paste content of `~/.ssh/jenkins_agent_key`

### Step 4 — Register the Node in Jenkins

1. Go to **Manage Jenkins → Nodes → New Node**
2. Name: `linux-agent-01`
3. Type: **Permanent Agent**
4. Configure:
   - **Remote root directory:** `/home/jenkins/agent`
   - **Labels:** `linux docker maven`
   - **Launch method:** Launch agents via SSH
   - **Host:** `<agent-ip>`
   - **Credentials:** `agent-ssh-key`
   - **Host Key Verification Strategy:** Known hosts file (or Non verifying for dev)

### Step 5 — Save and Connect

Click **Save**, then **Launch Agent**. You should see "Agent successfully connected and online."

---

## Node Labels and Executors

### Labels
Labels allow you to **target specific agents** for specific jobs.

```groovy
// Pipeline using a label
pipeline {
    agent { label 'linux && docker' }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
    }
}
```

Common label conventions:
- `linux`, `windows`, `macos`
- `docker`, `kubernetes`
- `maven`, `nodejs`, `python`
- `high-memory`, `gpu`
- `prod`, `staging`, `dev`

### Executors
Each node has a configurable number of **executors** — the number of concurrent jobs it can run.

| Node Type | Recommended Executors |
|-----------|----------------------|
| Controller | 0 (never run builds) |
| Small Agent (2 CPU) | 2 |
| Medium Agent (8 CPU) | 4-6 |
| Large Agent (16 CPU) | 8-12 |
| Docker/K8s Agent | 1 (ephemeral) |

> **Rule:** Set executors to (CPU cores) or (CPU cores × 1.5) for I/O heavy workloads.

---

## Distributed Builds — How It Works

```
Developer pushes code
        │
        ▼
   Git Webhook ──► Jenkins Controller
                        │
              Checks build queue
                        │
          Finds available agent matching label
                        │
              Sends job to Agent
                        │
         Agent clones repo & runs stages
                        │
         Results sent back to Controller
                        │
       Controller stores artifacts & reports
```

### Workspace Isolation
Each agent maintains its own workspace per job:

```
/home/jenkins/agent/workspace/
├── job-frontend/
├── job-backend/
└── job-integration-tests/
```

---

## Monitoring Nodes

### Via Web UI
Go to **Manage Jenkins → Nodes** to see:
- Online/offline status
- Number of executors in use
- Build queue per node
- Disk space, temp space usage

### Via Script Console
Go to **Manage Jenkins → Script Console**:

```groovy
// List all nodes and their status
Jenkins.instance.nodes.each { node ->
    println "Node: ${node.name} | Online: ${node.toComputer().isOnline()}"
}
```

### Checking Agent Logs

```bash
# On the agent machine
tail -f /home/jenkins/agent/remoting.log

# In Docker agent
docker logs jenkins-agent -f
```

### Key Metrics to Monitor
- **Response time** between Controller and Agent
- **Disk space** on agent workspace
- **Executor utilization** (idle vs. busy)
- **Queue wait time** (if agents are insufficient)

---

## Summary

| Component | Role |
|-----------|------|
| **Controller** | Orchestration, UI, config, scheduling |
| **Agent** | Executes builds, tests, deployments |
| **JNLP/SSH** | Communication protocol |
| **Labels** | Route jobs to the right agents |
| **Executors** | Concurrency slots per agent |
| **Workspace** | Per-job isolated build directory on agent |
