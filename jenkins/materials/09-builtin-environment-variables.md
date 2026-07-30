# Built-in Environment Variables in Jenkins

## Table of Contents
1. [What are Built-in Variables?](#what-are-built-in-variables)
2. [How to View All Available Variables](#how-to-view-all-available-variables)
3. [Core Build Variables](#core-build-variables)
4. [Git / SCM Variables](#git--scm-variables)
5. [Job & URL Variables](#job--url-variables)
6. [Node & Executor Variables](#node--executor-variables)
7. [Pipeline-Specific Variables (`currentBuild`)](#pipeline-specific-variables-currentbuild)
8. [Using Variables in Practice](#using-variables-in-practice)
9. [Complete Variable Reference Table](#complete-variable-reference-table)

---

## What are Built-in Variables?

Jenkins automatically injects a set of **environment variables** into every build. They are available:

- In shell steps as `$VARIABLE_NAME`
- In Groovy as `env.VARIABLE_NAME`
- In string interpolation as `${env.VARIABLE_NAME}`

These variables describe the current build context — job name, build number, SCM branch, node, and more.

---

## How to View All Available Variables

### In the Jenkins UI

Navigate to:
```
http://your-jenkins-url/env-vars.html/
```

This page lists **all** environment variables available on your Jenkins instance, including those added by installed plugins.

### In a Pipeline Step

```groovy
stage('Print All Env Vars') {
    steps {
        sh 'printenv | sort'
        // or in Groovy:
        script {
            env.each { name, value ->
                println "${name} = ${value}"
            }
        }
    }
}
```

---

## Core Build Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `BUILD_NUMBER` | Sequential build number | `42` |
| `BUILD_ID` | Same as BUILD_NUMBER | `42` |
| `BUILD_DISPLAY_NAME` | Display name of the build | `#42` |
| `BUILD_TAG` | Unique tag: `jenkins-{job}-{build}` | `jenkins-my-app-42` |
| `BUILD_URL` | Full URL to the build | `http://jenkins/job/my-app/42/` |
| `BUILD_RESULT` | Result of the build (set after post) | `SUCCESS`, `FAILURE` |
| `BUILD_TIMESTAMP` | Build start time (with plugin) | `2024-01-15_10-30-00` |

### Usage Examples

```groovy
pipeline {
    agent any
    stages {
        stage('Tag') {
            steps {
                echo "Build #${env.BUILD_NUMBER}"
                sh "docker tag myapp:latest myapp:${env.BUILD_TAG}"
                echo "View results: ${env.BUILD_URL}"
            }
        }
    }
}
```

---

## Git / SCM Variables

These are provided by the **Git plugin** when a Git repository is checked out.

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `GIT_COMMIT` | Full SHA of the current commit | `a1b2c3d4e5f6...` |
| `GIT_PREVIOUS_COMMIT` | SHA of the previous successful commit | `f1e2d3c4b5a6...` |
| `GIT_PREVIOUS_SUCCESSFUL_COMMIT` | SHA of last successful build's commit | `f1e2d3c4b5a6...` |
| `GIT_BRANCH` | Branch being built | `origin/main` |
| `GIT_LOCAL_BRANCH` | Local branch name | `main` |
| `GIT_URL` | Repository URL | `https://github.com/org/repo.git` |
| `GIT_URL_1` | First remote URL (for multiple remotes) | `https://github.com/...` |
| `GIT_COMMITTER_NAME` | Name of the committer | `John Doe` |
| `GIT_AUTHOR_NAME` | Name of the author | `Jane Doe` |
| `GIT_COMMITTER_EMAIL` | Committer email | `john@example.com` |
| `BRANCH_NAME` | Branch name (Multibranch pipelines) | `feature/login` |
| `CHANGE_ID` | Pull request number | `42` |
| `CHANGE_TITLE` | Pull request title | `Add login feature` |
| `CHANGE_AUTHOR` | PR author username | `johndoe` |
| `CHANGE_TARGET` | PR target branch | `main` |

### Usage Examples

```groovy
stage('Tag Docker Image') {
    steps {
        script {
            // Short commit SHA
            def shortSHA = env.GIT_COMMIT.take(8)
            env.IMAGE_TAG = "${env.BUILD_NUMBER}-${shortSHA}"
        }
        sh "docker build -t myapp:${env.IMAGE_TAG} ."
    }
}

stage('PR Info') {
    when { changeRequest() }
    steps {
        echo "PR #${env.CHANGE_ID}: ${env.CHANGE_TITLE}"
        echo "Author: ${env.CHANGE_AUTHOR}"
        echo "Merging: ${env.BRANCH_NAME} → ${env.CHANGE_TARGET}"
    }
}
```

---

## Job & URL Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `JOB_NAME` | Full job name including folder path | `my-folder/my-app` |
| `JOB_BASE_NAME` | Job name without folder prefix | `my-app` |
| `JOB_URL` | URL to the job page | `http://jenkins/job/my-app/` |
| `JENKINS_URL` | Base URL of Jenkins | `http://jenkins:8080/` |
| `JENKINS_HOME` | Jenkins home directory | `/var/jenkins_home` |

### Usage Examples

```groovy
stage('Notify') {
    steps {
        echo "Job: ${env.JOB_NAME}"
        echo "Jenkins: ${env.JENKINS_URL}"
        mail to: 'team@example.com',
             subject: "Build result for ${env.JOB_BASE_NAME}",
             body: "See: ${env.BUILD_URL}"
    }
}
```

---

## Node & Executor Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `NODE_NAME` | Name of the agent running the build | `linux-agent-01` |
| `NODE_LABELS` | Space-separated labels of the agent | `linux docker maven` |
| `EXECUTOR_NUMBER` | Executor slot number on the agent | `0`, `1`, `2` |
| `WORKSPACE` | Absolute path to the build workspace | `/home/jenkins/workspace/my-app` |

### Usage Examples

```groovy
stage('Debug Agent') {
    steps {
        echo "Running on node: ${env.NODE_NAME}"
        echo "Node labels: ${env.NODE_LABELS}"
        echo "Workspace: ${env.WORKSPACE}"
        echo "Executor: ${env.EXECUTOR_NUMBER}"
        sh "df -h ${env.WORKSPACE}"    // Check disk space in workspace
    }
}
```

---

## Pipeline-Specific Variables (`currentBuild`)

`currentBuild` is a Groovy object (not a shell variable) with read/write properties:

### Read Properties

```groovy
script {
    echo "Result: ${currentBuild.result}"
    echo "Duration: ${currentBuild.durationString}"
    echo "Display name: ${currentBuild.displayName}"
    echo "Description: ${currentBuild.description}"
    echo "Full project name: ${currentBuild.fullProjectName}"
    echo "Is building: ${currentBuild.isBuilding()}"
    echo "Number: ${currentBuild.number}"
    echo "Absolute URL: ${currentBuild.absoluteUrl}"

    // Access previous build
    def prev = currentBuild.previousBuild
    if (prev) {
        echo "Previous result: ${prev.result}"
    }
}
```

### Write Properties

```groovy
script {
    // Set a custom display name shown in Jenkins UI
    currentBuild.displayName = "#${env.BUILD_NUMBER} - myapp:${env.IMAGE_TAG}"

    // Set a description visible in build list
    currentBuild.description = "Deployed to ${params.TARGET_ENV} by ${env.BUILD_USER}"
}
```

### `currentBuild.result` Values

| Value | Meaning |
|-------|---------|
| `null` | Build still running |
| `SUCCESS` | Completed successfully |
| `UNSTABLE` | Completed but with test failures |
| `FAILURE` | Build failed |
| `ABORTED` | Manually cancelled |

### Marking a Build Unstable Programmatically

```groovy
stage('Test') {
    steps {
        script {
            def result = sh(script: 'npm test', returnStatus: true)
            if (result != 0) {
                currentBuild.result = 'UNSTABLE'
                echo 'Tests failed — marking build unstable'
            }
        }
    }
}
```

---

## Using Variables in Practice

### Build a Unique Docker Image Tag

```groovy
environment {
    IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(8)}"
}
```

### Construct Slack Message with Context

```groovy
post {
    failure {
        slackSend(
            color: 'danger',
            message: """
:x: *Build Failed*
*Job:* ${env.JOB_NAME}
*Build:* #${env.BUILD_NUMBER}
*Branch:* ${env.BRANCH_NAME}
*Commit:* ${env.GIT_COMMIT.take(8)}
*URL:* ${env.BUILD_URL}
            """.stripIndent()
        )
    }
}
```

### Skip Deploy if Only Documentation Changed

```groovy
stage('Check Changes') {
    steps {
        script {
            def changes = sh(
                script: "git diff --name-only ${env.GIT_PREVIOUS_COMMIT} ${env.GIT_COMMIT}",
                returnStdout: true
            ).trim()
            echo "Changed files:\n${changes}"

            if (changes.split('\n').every { it.startsWith('docs/') }) {
                currentBuild.result = 'SUCCESS'
                error('Only documentation changed — skipping build')
            }
        }
    }
}
```

### Dynamic Build Name Based on PR

```groovy
stage('Set Build Name') {
    steps {
        script {
            if (env.CHANGE_ID) {
                // This is a PR build
                currentBuild.displayName = "PR-${env.CHANGE_ID}: ${env.CHANGE_TITLE?.take(40)}"
            } else {
                currentBuild.displayName = "#${env.BUILD_NUMBER} | ${env.GIT_COMMIT.take(7)}"
            }
        }
    }
}
```

---

## Complete Variable Reference Table

```
CORE BUILD
─────────────────────────────────────────────────────────
BUILD_NUMBER                  Current build number
BUILD_ID                      Same as BUILD_NUMBER
BUILD_DISPLAY_NAME            Build display name (#42)
BUILD_TAG                     jenkins-{job}-{number}
BUILD_URL                     Full URL to this build
WORKSPACE                     Workspace directory path

SCM / GIT
─────────────────────────────────────────────────────────
GIT_COMMIT                    Full commit SHA
GIT_BRANCH                    Branch (origin/main)
GIT_LOCAL_BRANCH              Local branch name
GIT_URL                       Repository URL
GIT_AUTHOR_NAME               Commit author name
GIT_COMMITTER_EMAIL           Commit author email
GIT_PREVIOUS_COMMIT           Previous commit SHA
GIT_PREVIOUS_SUCCESSFUL_COMMIT Last success commit SHA

MULTIBRANCH / PULL REQUEST
─────────────────────────────────────────────────────────
BRANCH_NAME                   Branch or PR name
CHANGE_ID                     PR/MR number
CHANGE_TITLE                  PR title
CHANGE_AUTHOR                 PR author
CHANGE_TARGET                 Target branch for PR

JOB
─────────────────────────────────────────────────────────
JOB_NAME                      Full job path
JOB_BASE_NAME                 Job name only
JOB_URL                       URL to job page

JENKINS
─────────────────────────────────────────────────────────
JENKINS_URL                   Jenkins base URL
JENKINS_HOME                  Jenkins home directory

AGENT
─────────────────────────────────────────────────────────
NODE_NAME                     Agent name
NODE_LABELS                   Agent labels
EXECUTOR_NUMBER               Executor slot index
```

---

## Summary

- Built-in variables are automatically available — no need to declare them
- Access in Groovy via `env.VARIABLE_NAME` or `"${env.VARIABLE_NAME}"`
- Access in shell via `$VARIABLE_NAME` (single-quoted strings)
- `currentBuild` is a Groovy object for build metadata — not a shell variable
- Use `http://your-jenkins/env-vars.html` to discover all variables including plugin-added ones
- Combine `GIT_COMMIT`, `BUILD_NUMBER`, and `BRANCH_NAME` for unique, traceable image tags
