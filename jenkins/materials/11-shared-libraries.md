# Jenkins Shared Libraries

## Table of Contents
1. [What are Shared Libraries?](#what-are-shared-libraries)
2. [Repository Structure](#repository-structure)
3. [Configure a Shared Library in Jenkins](#configure-a-shared-library-in-jenkins)
4. [Vars — Global Variables and Steps](#vars--global-variables-and-steps)
5. [src — Groovy Classes](#src--groovy-classes)
6. [resources — Static Files](#resources--static-files)
7. [Loading a Shared Library in a Pipeline](#loading-a-shared-library-in-a-pipeline)
8. [Dynamic Library Loading](#dynamic-library-loading)
9. [Testing Shared Libraries](#testing-shared-libraries)
10. [Complete Real-World Example](#complete-real-world-example)

---

## What are Shared Libraries?

Shared Libraries let you **extract reusable pipeline code** into a central Git repository. Instead of copy-pasting the same stages across dozens of Jenkinsfiles, you write the logic once and call it everywhere.

### Problems They Solve

- Duplicated pipeline code across many repos
- Inconsistent CI/CD standards across teams
- Difficult to update shared logic (must edit every Jenkinsfile)
- No unit testing for pipeline code

### Benefits

- **DRY** — Write once, reuse everywhere
- **Centralized updates** — Fix a bug in one place, all pipelines benefit
- **Standardization** — Enforce company-wide CI/CD practices
- **Testable** — Write unit tests for your pipeline logic

---

## Repository Structure

A Shared Library is a Git repository with this exact structure:

```
jenkins-shared-library/
├── vars/                       # Global callable steps
│   ├── buildDockerImage.groovy
│   ├── deployToKubernetes.groovy
│   ├── notifySlack.groovy
│   └── runMavenBuild.groovy
├── src/                        # Groovy classes (helper code)
│   └── com/
│       └── example/
│           ├── Docker.groovy
│           ├── Kubernetes.groovy
│           └── Utils.groovy
├── resources/                  # Static files (scripts, configs)
│   ├── scripts/
│   │   └── deploy.sh
│   └── config/
│       └── sonar.properties
└── README.md
```

| Directory | Purpose |
|-----------|---------|
| `vars/` | Each `.groovy` file becomes a global step callable from pipelines |
| `src/` | Regular Groovy classes — helpers, utilities, abstractions |
| `resources/` | Static files accessible via `libraryResource()` |

---

## Configure a Shared Library in Jenkins

### Global Configuration (All Pipelines)

1. Go to **Manage Jenkins → System**
2. Scroll to **Global Pipeline Libraries**
3. Click **Add**

```
Name:               company-pipeline-lib
Default version:    main
Load implicitly:    false   (or true to auto-load in every pipeline)
Retrieval method:   Modern SCM
  Source Code Management: Git
    Project Repository: https://github.com/myorg/jenkins-shared-library.git
    Credentials: github-token
```

### Per-Folder Configuration

In a Folder (multi-branch folder), configure a library that applies only to pipelines inside that folder:

1. Open the Folder
2. Click **Configure → Pipeline Libraries**
3. Add the library as above

---

## Vars — Global Variables and Steps

Each `.groovy` file in `vars/` becomes a callable step. The filename is the step name.

### Simple Step — `vars/sayHello.groovy`

```groovy
def call(String name = 'World') {
    echo "Hello, ${name}!"
}
```

Usage in Jenkinsfile:
```groovy
sayHello()
sayHello('Jenkins')
```

### Step that Runs Shell — `vars/runMavenBuild.groovy`

```groovy
def call(Map config = [:]) {
    def goals  = config.get('goals', 'clean package')
    def profile = config.get('profile', '')
    def args    = profile ? "-P${profile}" : ''

    sh "mvn ${goals} ${args} -B --no-transfer-progress"
}
```

Usage:
```groovy
runMavenBuild goals: 'clean test package', profile: 'integration'
```

### Docker Build Step — `vars/buildDockerImage.groovy`

```groovy
def call(Map config) {
    def imageName = config.image
    def tag       = config.get('tag', env.BUILD_NUMBER)
    def dockerfile = config.get('dockerfile', 'Dockerfile')
    def buildArgs = config.get('buildArgs', '')

    echo "Building Docker image: ${imageName}:${tag}"

    sh "docker build -t ${imageName}:${tag} -f ${dockerfile} ${buildArgs} ."
    sh "docker tag ${imageName}:${tag} ${imageName}:latest"

    return "${imageName}:${tag}"
}
```

Usage:
```groovy
def tag = buildDockerImage image: 'myorg/myapp', tag: env.BUILD_NUMBER
```

### Slack Notification Step — `vars/notifySlack.groovy`

```groovy
def call(String status, String channel = '#ci-builds') {
    def color = [
        'SUCCESS'  : 'good',
        'FAILURE'  : 'danger',
        'UNSTABLE' : 'warning',
        'ABORTED'  : '#808080'
    ].get(status, '#808080')

    def icon = [
        'SUCCESS'  : ':white_check_mark:',
        'FAILURE'  : ':x:',
        'UNSTABLE' : ':warning:',
        'ABORTED'  : ':no_entry_sign:'
    ].get(status, ':grey_question:')

    def message = """
${icon} *${env.JOB_NAME}* #${env.BUILD_NUMBER}
*Status:* ${status}
*Branch:* ${env.BRANCH_NAME ?: 'N/A'}
*Duration:* ${currentBuild.durationString}
*URL:* ${env.BUILD_URL}
    """.stripIndent().trim()

    slackSend channel: channel, color: color, message: message
}
```

Usage:
```groovy
post {
    success { notifySlack('SUCCESS') }
    failure { notifySlack('FAILURE', '#alerts') }
}
```

### Full Pipeline Step — `vars/standardPipeline.groovy`

This is the most powerful pattern — a complete pipeline as a shared step:

```groovy
def call(Map config) {
    def imageName = config.image
    def deployEnv = config.get('deployEnv', 'staging')
    def helmChart = config.get('helmChart', './helm')
    def runTests  = config.get('runTests', true)

    pipeline {
        agent any

        stages {
            stage('Checkout') {
                steps { checkout scm }
            }

            stage('Test') {
                when { expression { return runTests } }
                steps {
                    sh 'mvn test'
                }
                post {
                    always { junit '**/target/surefire-reports/*.xml' }
                }
            }

            stage('Build Docker') {
                steps {
                    sh "docker build -t ${imageName}:${env.BUILD_NUMBER} ."
                    sh "docker push ${imageName}:${env.BUILD_NUMBER}"
                }
            }

            stage('Deploy') {
                steps {
                    sh "helm upgrade --install myapp ${helmChart} --set image.tag=${env.BUILD_NUMBER}"
                }
            }
        }

        post {
            success { notifySlack('SUCCESS') }
            failure { notifySlack('FAILURE') }
        }
    }
}
```

Usage in any Jenkinsfile:
```groovy
@Library('company-pipeline-lib') _

standardPipeline(
    image:     'myorg/my-service',
    deployEnv: 'staging',
    runTests:  true
)
```

---

## src — Groovy Classes

Use `src/` for complex helper logic that benefits from OOP and proper unit testing.

### `src/com/example/Docker.groovy`

```groovy
package com.example

class Docker implements Serializable {
    private def script

    Docker(def script) {
        this.script = script
    }

    def build(String image, String tag, String dockerfile = 'Dockerfile') {
        script.sh "docker build -t ${image}:${tag} -f ${dockerfile} ."
    }

    def push(String image, String tag, String registry = '') {
        def fullName = registry ? "${registry}/${image}:${tag}" : "${image}:${tag}"
        script.sh "docker tag ${image}:${tag} ${fullName}"
        script.sh "docker push ${fullName}"
    }

    def cleanup(String image, String tag) {
        script.sh "docker rmi ${image}:${tag} || true"
    }
}
```

Usage in `vars/` or Jenkinsfile:

```groovy
import com.example.Docker

def docker = new Docker(this)
docker.build('myapp', env.BUILD_NUMBER)
docker.push('myapp', env.BUILD_NUMBER, 'registry.example.com')
```

### `src/com/example/Utils.groovy`

```groovy
package com.example

class Utils implements Serializable {
    private def script

    Utils(def script) {
        this.script = script
    }

    String getShortCommit() {
        return script.sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }

    String buildImageTag() {
        return "${script.env.BUILD_NUMBER}-${getShortCommit()}"
    }

    boolean isMainBranch() {
        return script.env.BRANCH_NAME == 'main'
    }

    Map getEnvironmentConfig(String env) {
        def configs = [
            dev:        [ns: 'development', replicas: 1],
            staging:    [ns: 'staging',     replicas: 2],
            production: [ns: 'production',  replicas: 5]
        ]
        return configs[env] ?: configs['dev']
    }
}
```

---

## resources — Static Files

Store shell scripts, config templates, or any static file under `resources/`.

### `resources/scripts/healthcheck.sh`

```bash
#!/bin/bash
set -e
URL="${1}"
MAX_RETRIES=10
WAIT=5

for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf "${URL}/health" > /dev/null; then
        echo "Health check passed"
        exit 0
    fi
    echo "Attempt ${i}/${MAX_RETRIES} — waiting ${WAIT}s..."
    sleep $WAIT
done

echo "Health check failed after ${MAX_RETRIES} attempts"
exit 1
```

Access in a pipeline step:

```groovy
// In vars/runHealthCheck.groovy
def call(String url) {
    def script = libraryResource('scripts/healthcheck.sh')
    writeFile file: 'healthcheck.sh', text: script
    sh "chmod +x healthcheck.sh && ./healthcheck.sh ${url}"
}
```

---

## Loading a Shared Library in a Pipeline

### Annotation (Pre-configured library)

```groovy
@Library('company-pipeline-lib') _   // _ imports everything

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                runMavenBuild goals: 'clean package'
            }
        }
    }
    post {
        always { notifySlack(currentBuild.result ?: 'SUCCESS') }
    }
}
```

### Specific Version

```groovy
@Library('company-pipeline-lib@v1.2.0') _   // Pin to a tag
@Library('company-pipeline-lib@feature/new-docker') _  // Use a branch
```

### Multiple Libraries

```groovy
@Library(['company-pipeline-lib@main', 'security-lib@v2.0']) _
```

---

## Dynamic Library Loading

Load a library programmatically within a pipeline:

```groovy
pipeline {
    agent any
    stages {
        stage('Load Library') {
            steps {
                script {
                    def lib = library(
                        identifier: 'company-pipeline-lib@main',
                        retriever: modernSCM([
                            $class: 'GitSCMSource',
                            remote: 'https://github.com/myorg/jenkins-shared-library.git',
                            credentialsId: 'github-token'
                        ])
                    )
                }
            }
        }
    }
}
```

---

## Testing Shared Libraries

Use **Jenkins Spock** or **Jenkins Pipeline Unit** to test your library locally.

### Add to `build.gradle`

```groovy
dependencies {
    testImplementation 'com.lesfurets:jenkins-pipeline-unit:1.19'
    testImplementation 'org.spockframework:spock-core:2.3-groovy-3.0'
}
```

### Test Example

```groovy
// test/vars/NotifySlackTest.groovy
import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.Before
import org.junit.Test

class NotifySlackTest extends BasePipelineTest {
    def notifySlack

    @Before
    void setUp() {
        super.setUp()
        notifySlack = loadScript('vars/notifySlack.groovy')
    }

    @Test
    void 'should call slackSend with good color on SUCCESS'() {
        binding.setVariable('env', [JOB_NAME: 'test-job', BUILD_NUMBER: '1', BUILD_URL: 'http://url'])
        binding.setVariable('currentBuild', [durationString: '1 min'])

        notifySlack('SUCCESS')

        assert helper.callStack.find { it.methodName == 'slackSend' }
    }
}
```

---

## Complete Real-World Example

### Shared Library: `vars/mavenPipeline.groovy`

```groovy
def call(Map config) {
    def image      = config.image ?: error('image is required')
    def registry   = config.get('registry', 'registry.example.com')
    def helmChart  = config.get('helmChart', './helm')
    def namespace  = config.get('namespace', 'staging')
    def testGoals  = config.get('testGoals', 'test')

    pipeline {
        agent {
            kubernetes {
                yaml """
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
                      - name: docker
                        image: docker:24-dind
                        securityContext:
                          privileged: true
                      - name: helm
                        image: alpine/helm:3.13.0
                        command: ["sleep"]
                        args: ["infinity"]
                """
            }
        }

        environment {
            TAG = "${env.BUILD_NUMBER}"
            FULL_IMAGE = "${registry}/${image}:${env.BUILD_NUMBER}"
        }

        stages {
            stage('Build') {
                steps {
                    container('maven') {
                        sh 'mvn clean package -DskipTests -B'
                    }
                }
            }

            stage('Test') {
                steps {
                    container('maven') {
                        sh "mvn ${testGoals} -B"
                    }
                }
                post {
                    always {
                        junit '**/target/surefire-reports/*.xml'
                    }
                }
            }

            stage('Docker Build & Push') {
                steps {
                    container('docker') {
                        withCredentials([usernamePassword(
                            credentialsId: 'registry-creds',
                            usernameVariable: 'REG_USER',
                            passwordVariable: 'REG_PASS'
                        )]) {
                            sh "docker build -t ${FULL_IMAGE} ."
                            sh "docker login -u $REG_USER -p $REG_PASS ${registry}"
                            sh "docker push ${FULL_IMAGE}"
                        }
                    }
                }
            }

            stage('Deploy') {
                when { branch 'main' }
                steps {
                    container('helm') {
                        withKubeConfig([credentialsId: "${namespace}-kubeconfig"]) {
                            sh """
                                helm upgrade --install ${image} ${helmChart} \
                                    --namespace ${namespace} \
                                    --set image.repository=${registry}/${image} \
                                    --set image.tag=${TAG}
                            """
                        }
                    }
                }
            }
        }

        post {
            success { notifySlack('SUCCESS') }
            failure { notifySlack('FAILURE') }
            cleanup { cleanWs() }
        }
    }
}
```

### Consuming Jenkinsfile (any team's repo)

```groovy
@Library('company-pipeline-lib@main') _

mavenPipeline(
    image:     'payments-service',
    registry:  'registry.example.com',
    helmChart: './helm',
    namespace: 'staging',
    testGoals: 'verify'
)
```

This single line replaces 100+ lines of duplicated pipeline code.

---

## Summary

| Component | Location | Purpose |
|-----------|----------|---------|
| Global step | `vars/myStep.groovy` | Callable from any pipeline |
| Helper class | `src/com/org/MyClass.groovy` | OOP logic, unit-testable |
| Static file | `resources/scripts/run.sh` | Shell scripts, config files |
| `@Library` annotation | Top of Jenkinsfile | Load the shared library |
| `libraryResource()` | Inside a step | Read a file from `resources/` |
| `library()` call | Dynamic loading | Load at runtime with parameters |
