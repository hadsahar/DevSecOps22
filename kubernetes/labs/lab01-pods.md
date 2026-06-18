# Lab 01 - Pods

## Objective

Practice creating, managing, and troubleshooting Pods in Kubernetes.

---

## Exercise 1 - Create a Simple Pod

Create a Pod named `nginx-pod` running the `nginx:latest` image.

- Expose port 80
- Verify the Pod is running with `kubectl get pods`
- Describe the Pod and find its IP address

---

## Exercise 2 - Pod with Custom Labels

Create a Pod named `labeled-pod` with the following labels:
- `app: web`
- `environment: dev`
- `team: backend`

Verify the labels using `kubectl get pods --show-labels`.

---

## Exercise 3 - Multi-Container Pod

Create a Pod named `multi-pod` with two containers:
1. `web` container running `nginx`
2. `logger` container running `busybox` with command: `sh -c "while true; do echo logging...; sleep 5; done"`

- View logs from each container separately
- Exec into the `web` container

---

## Exercise 4 - Pod with Environment Variables

Create a Pod named `env-pod` running `busybox` with the following environment variables:
- `APP_NAME=myapp`
- `APP_VERSION=1.0`
- `ENV=production`

The container command should print all environment variables and sleep.

---

## Exercise 5 - Pod with Resource Limits

Create a Pod named `resource-pod` running `nginx` with:
- CPU request: 100m
- CPU limit: 200m
- Memory request: 64Mi
- Memory limit: 128Mi

Describe the Pod to confirm resources are set.

---

## Exercise 6 - Pod with a Volume

Create a Pod named `volume-pod` running `nginx` with:
- An `emptyDir` volume named `shared-data`
- Mount it at `/usr/share/nginx/html`
- Exec into the pod and create an `index.html` file

---

## Exercise 7 - Init Container

Create a Pod named `init-pod` with:
- An init container that creates a file `/work-dir/ready.txt`
- A main container that checks if the file exists and prints "Ready!"
- Use a shared `emptyDir` volume

---

## Exercise 8 - Pod Troubleshooting

Create a Pod named `broken-pod` with image `nginx:nonexistent`.

- Check the Pod status
- Describe the Pod to find the error
- Fix the image and reapply

---

## Exercise 9 - Liveness Probe

Create a Pod named `liveness-pod` running `busybox` with:
- Command: `sh -c "touch /tmp/healthy; sleep 30; rm /tmp/healthy; sleep 600"`
- A liveness probe that checks if `/tmp/healthy` exists using `exec`
- Watch what happens after 30 seconds

---

## Exercise 10 - Delete and Cleanup

- List all running pods
- Delete all pods you created in this lab
- Verify no pods remain

---
