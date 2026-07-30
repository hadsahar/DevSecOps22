# Jenkins Plugins and Freestyle Jobs

## Table of Contents
1. [What are Plugins?](#what-are-plugins)
2. [Managing Plugins](#managing-plugins)
3. [Essential Plugins List](#essential-plugins-list)
4. [Installing Plugins via CLI](#installing-plugins-via-cli)
5. [What is a Freestyle Job?](#what-is-a-freestyle-job)
6. [Creating a Freestyle Job — Step by Step](#creating-a-freestyle-job--step-by-step)
7. [Freestyle Job Configuration Deep Dive](#freestyle-job-configuration-deep-dive)
8. [Freestyle vs Pipeline Jobs](#freestyle-vs-pipeline-jobs)
9. [Chaining Freestyle Jobs](#chaining-freestyle-jobs)

---

## What are Plugins?

Jenkins ships with minimal functionality. **Plugins** extend Jenkins with integrations for:
- Source control (Git, SVN, Bitbucket)
- Build tools (Maven, Gradle, npm)
- Testing (JUnit, SonarQube, OWASP)
- Deployment (Docker, Kubernetes, AWS, Azure)
- Notifications (Slack, Email, PagerDuty)
- Security (LDAP, OAuth, Role-based access)

There are over **1,800+ plugins** in the Jenkins Plugin Registry.

---

## Managing Plugins

### Via Web UI

1. Go to **Manage Jenkins → Plugins**
2. Four tabs:
   - **Updates** — Available updates for installed plugins
   - **Available Plugins** — Search and install new plugins
   - **Installed Plugins** — View and uninstall
   - **Advanced** — Upload a `.hpi` plugin file manually

### Plugin Update Best Practices
- Keep plugins updated regularly (security patches)
- Test plugin updates in a dev Jenkins instance first
- Read the plugin changelog before updating
- Back up `$JENKINS_HOME` before major plugin updates

```bash
# Back up Jenkins before plugin updates
sudo systemctl stop jenkins
sudo tar -czvf jenkins-backup-$(date +%Y%m%d).tar.gz /var/lib/jenkins
sudo systemctl start jenkins
```

---

## Essential Plugins List

### Source Control
| Plugin | Purpose |
|--------|---------|
| **Git** | Git integration, checkout, polling |
| **GitHub** | GitHub webhooks, PR status |
| **GitLab** | GitLab CI/CD integration |
| **Bitbucket** | Bitbucket webhooks |
| **Multibranch Scan Webhook Trigger** | Trigger multibranch scans |

### Pipeline & Job
| Plugin | Purpose |
|--------|---------|
| **Pipeline** | Core declarative pipeline support |
| **Pipeline: Stage View** | Visual stage view in UI |
| **Blue Ocean** | Modern pipeline UI |
| **Job DSL** | Define jobs as code (Groovy) |
| **Build Timeout** | Kill stuck builds |
| **Workspace Cleanup** | Clean workspace before/after build |
| **Timestamper** | Add timestamps to console output |
| **AnsiColor** | Colored console output |

### Build Tools
| Plugin | Purpose |
|--------|---------|
| **Maven Integration** | Maven builds |
| **Gradle** | Gradle builds |
| **NodeJS** | Node.js builds |
| **Docker Pipeline** | Docker in pipeline steps |
| **Docker** | Docker build/publish |

### Testing & Quality
| Plugin | Purpose |
|--------|---------|
| **JUnit** | Publish test results |
| **HTML Publisher** | Publish HTML reports |
| **SonarQube Scanner** | Code quality analysis |
| **OWASP Dependency-Check** | Security vulnerability scan |
| **Cobertura** | Code coverage |
| **JaCoCo** | Java code coverage |

### Credentials & Security
| Plugin | Purpose |
|--------|---------|
| **Credentials** | Store and manage secrets |
| **Credentials Binding** | Inject credentials into builds |
| **SSH Agent** | SSH keys in pipeline |
| **HashiCorp Vault** | Vault secret integration |
| **AWS Credentials** | AWS key management |

### Notifications
| Plugin | Purpose |
|--------|---------|
| **Email Extension (mailer)** | Configurable email notifications |
| **Slack Notification** | Slack messages |
| **MS Teams Notification** | Microsoft Teams |

### Cloud & Deployment
| Plugin | Purpose |
|--------|---------|
| **Kubernetes** | K8s dynamic agents |
| **Amazon EC2** | EC2 dynamic agents |
| **AWS Steps** | AWS CLI in pipeline |
| **Helm** | Helm chart deployments |

---

## Installing Plugins via CLI

### Using Jenkins CLI Tool

```bash
# Download Jenkins CLI
curl -O http://localhost:8080/jnlpJars/jenkins-cli.jar

# Install a plugin
java -jar jenkins-cli.jar \
  -s http://localhost:8080 \
  -auth admin:your-password \
  install-plugin git pipeline-stage-view blueocean

# Restart after install
java -jar jenkins-cli.jar \
  -s http://localhost:8080 \
  -auth admin:your-password \
  safe-restart
```

### Via Dockerfile (Pre-installed Plugins)

```dockerfile
FROM jenkins/jenkins:lts-jdk17

# Install plugins during image build
RUN jenkins-plugin-cli --plugins \
  git \
  pipeline-stage-view \
  blueocean \
  slack \
  docker-workflow \
  kubernetes \
  credentials-binding
```

### Via plugins.txt File

Create `plugins.txt`:

```
git:latest
workflow-aggregator:latest
blueocean:latest
slack:latest
docker-workflow:latest
kubernetes:latest
credentials-binding:latest
```

```dockerfile
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt
```

---

## What is a Freestyle Job?

A **Freestyle Job** (also called a Freestyle Project) is Jenkins' original job type. It is configured entirely through the Web UI — no code required. It is good for:

- Simple build tasks
- Beginners learning Jenkins
- Running shell scripts or batch commands
- Jobs that don't need complex logic

> **Note:** For anything beyond simple builds, Pipelines (Jenkinsfile) are strongly preferred.

---

## Creating a Freestyle Job — Step by Step

### Step 1 — Create New Job

1. Click **New Item** on the Jenkins dashboard
2. Enter a job name (e.g., `build-my-app`)
3. Select **Freestyle project**
4. Click **OK**

### Step 2 — General Settings

- **Description:** Write what this job does
- **Discard old builds:** ✅ Check this to save disk
  - Strategy: Log Rotation
  - Days to keep builds: `14`
  - Max # of builds to keep: `10`
- **GitHub project:** Add your repo URL (if using GitHub plugin)

### Step 3 — Source Code Management

Select **Git**:

```
Repository URL: https://github.com/org/repo.git
Credentials:    github-token (select from dropdown)
Branch:         */main
```

For polling, additional refspecs can be added for pull requests.

### Step 4 — Build Triggers

| Trigger | Description |
|---------|-------------|
| **Build periodically** | Cron-style schedule `H/15 * * * *` |
| **Poll SCM** | Check repo for changes `H/5 * * * *` |
| **GitHub hook trigger** | Trigger on webhook push event |
| **Build after other jobs** | Job chaining |
| **Trigger remotely** | Trigger via URL with token |

Example cron syntax:
```
H/15 * * * *    # Every 15 minutes
0 8 * * 1-5     # Monday-Friday at 8:00 AM
H 2 * * *       # Every day at ~2 AM (H avoids thundering herd)
```

### Step 5 — Build Environment

Useful options:
- **Delete workspace before build starts** — Clean builds
- **Add timestamps to console output** — Requires Timestamper plugin
- **Use secret text(s) or file(s)** — Inject credentials
- **Set build name** — `${BUILD_NUMBER}-${GIT_BRANCH}`

### Step 6 — Build Steps

Click **Add build step**:

#### Execute Shell (Linux/Mac)
```bash
#!/bin/bash
set -e
echo "Building application..."
mvn clean package -DskipTests
echo "Build complete. Artifact: $(ls target/*.jar)"
```

#### Execute Windows Batch Command
```batch
echo Building...
mvn clean package
```

#### Invoke Maven Top-Level Targets
- Goals: `clean test package`
- POM: `pom.xml`

#### Execute Gradle Script
- Tasks: `clean build test`

### Step 7 — Post-Build Actions

Click **Add post-build action**:

| Action | Use Case |
|--------|---------|
| **Archive artifacts** | Save build outputs |
| **Publish JUnit test results** | Show test reports |
| **Send build artifacts over SSH** | Deploy to server |
| **Email notification** | Notify on failure |
| **Slack notifications** | Team alerts |
| **Trigger other jobs** | Build chains |

**Archive Artifacts example:**
```
Files to archive: target/*.jar, target/*.war
```

**JUnit results:**
```
Test report XMLs: **/target/surefire-reports/*.xml
```

---

## Freestyle Job Configuration Deep Dive

### Full Example: Java Maven Freestyle Job

```
General:
  Name: build-java-app
  Description: Build and test the Java backend service
  Discard old builds: 10 builds max

Source Code Management:
  Git:
    URL: https://github.com/myorg/java-app.git
    Credentials: github-token
    Branch: */main

Build Triggers:
  ✅ GitHub hook trigger for GITScm polling

Build Environment:
  ✅ Delete workspace before build starts
  ✅ Add timestamps to the console output

Build Steps:
  1. Execute shell:
     mvn --version
  2. Invoke Maven:
     Goals: clean test package
     POM: pom.xml

Post-Build Actions:
  1. Publish JUnit test results:
     XML: **/target/surefire-reports/*.xml
  2. Archive Artifacts:
     Files: target/*.jar
  3. Email notification:
     Recipients: dev-team@company.com
     Send email for every unstable build
```

---

## Freestyle vs Pipeline Jobs

| Feature | Freestyle | Pipeline |
|---------|-----------|----------|
| **Configuration** | UI-based | Code (Jenkinsfile) |
| **Version control** | No | Yes (Git) |
| **Complex logic** | Limited | Full Groovy |
| **Parallel stages** | No | Yes |
| **Code review** | No | Yes |
| **Reusability** | Low | High (shared libs) |
| **Visibility** | Basic | Stage view, BlueOcean |
| **Best for** | Simple tasks | Real CI/CD pipelines |

> **Rule of thumb:** Use Freestyle for quick one-off tasks or demos. Use Pipelines for everything else.

---

## Chaining Freestyle Jobs

You can create a build pipeline by chaining Freestyle jobs together.

### Method 1: Post-Build Trigger

In Job A → Post-Build Actions → **Trigger other projects**:
```
Projects to build: job-b, job-c
Trigger only if build is stable: ✅
```

### Method 2: Job Dependency in Build Trigger

In Job B → Build Triggers → **Build after other projects are built**:
```
Projects to watch: job-a
Trigger only if build is stable: ✅
```

### Visual Chain

```
job-checkout ──► job-build ──► job-test ──► job-deploy
     │                │             │             │
  Git clone      mvn package     JUnit test    SSH deploy
```

> **Note:** Build Pipeline Plugin or Delivery Pipeline Plugin can visualize these chains. However, a single Declarative Pipeline is almost always a better approach.

---

## Summary

- **Plugins** are the backbone of Jenkins' extensibility — install and manage them from the Plugin Manager
- Keep **essential plugins** updated; use `Dockerfile` or `plugins.txt` to codify your plugin set
- **Freestyle jobs** are UI-configured, good for simple tasks but don't scale well
- Use **Post-Build Actions** for test reporting, artifact archiving, and notifications
- Chain Freestyle jobs for simple sequences, but prefer **Pipeline** for complex workflows
