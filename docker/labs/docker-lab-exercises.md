---
layout: default
title: Docker lab1 - Practice Exercises [run command]
---

# Docker Lab Exercises

## Part 1: Docker Architecture

### Question 1

What is the main difference between a Docker image and a Docker container?

A) An image is a running instance, while a container is a template
B) An image is a read-only template, while a container is a runnable instance of an image
C) An image is used for storage, while a container is used for networking
D) There is no difference between them

---

### Question 2

Which component of Docker architecture is responsible for building, running, and distributing Docker containers?

A) Docker Registry
B) Docker Client
C) Docker Daemon
D) Docker Host

---

### Question 3

What is the purpose of the Docker Registry?

A) To manage container networking
B) To store and distribute Docker images
C) To run containers in the background
D) To provide a command-line interface for Docker

---

## Part 2: Hands-on Command Exercises

### Exercise 1: Pull and Run a Simple Image

**Task:** Pull the `hello-world` image from Docker Hub and run it.
**try to do it in one command once and in 2 sepereate commands one**

**Expected Output:** You should see a "Hello from Docker!" message.

---

### Exercise 2: Run a Container in Detached Mode

**Task:** Run an `nginx` container in detached mode with the name `web-server`.

**Verification:** Use `docker ps` to verify the container is running.

---

### Exercise 3: Interactive Container Access

**Task:** Run an `ubuntu` container interactively with a terminal and execute the command `echo "Hello from Ubuntu"` inside it.

---

### Exercise 4: Port Mapping

**Task:** Run an `nginx` container and map port 8080 on your host to port 80 in the container. Name it `my-nginx`.

**Verification:** Open your browser and visit `http://localhost:8080` to see the nginx welcome page.

---

### Exercise 5: Environment Variables

**Task:** Run a `postgres` database container with the following environment variables:

- `POSTGRES_PASSWORD=mysecretpassword`
- `POSTGRES_USER=myuser`
- `POSTGRES_DB=mydb`

Name the container `postgres-db`.
**Verification:** Use `docker ps` to verify the container is running.

### Exercise 6: Container Management

**Task:**

1. Run two `nginx` containers named `nginx-1` and `nginx-2` each one in a new port (8081 and 8082) and in background
2. List all running containers
3. Stop both containers
4. Remove both containers
5. Remove the nginx image

---

### Exercise 7: Multi-Port Web Application

**Task:**

1. Pull the `redis` image
2. Run a Redis container named `redis-cache` in detached mode
3. Run an `nginx` container named `web-app` that maps port 3000 (host) to port 80 (container)
4. Set an environment variable `ENV=production` on the nginx container
5. List all containers (including stopped ones)
6. Stop the redis container
7. Remove both containers
8. Remove both images

---

### Exercise 8: Network Connectivity with Busybox

**Task:**

1. Run an `nginx` container named `web-1` in detached mode
2. Run an `apache` (httpd) container named `web-2` in detached mode
3. Use a `busybox` container to ping both `web-1` and `web-2` containers to test network connectivity

**Hint:** You can run busybox interactively and use the `ping` command inside it. The container names can be used as hostnames if they're on the same Docker network.

**please note that you neeed to get the continaers ip's from the inspect command**
**Verification:** You should see ping responses from both containers.
