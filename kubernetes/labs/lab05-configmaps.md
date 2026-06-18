# Lab 05 - ConfigMaps

## Objective

Practice creating and using ConfigMaps to inject configuration into Pods.

---

## Exercise 1 - Create ConfigMap from Literals

Create a ConfigMap named `app-config` with:
- `APP_ENV=production`
- `APP_PORT=8080`
- `LOG_LEVEL=info`

Verify with `kubectl get cm app-config -o yaml`.

---

## Exercise 2 - Create ConfigMap from File

Create a file called `app.properties`:
```
database.host=db.example.com
database.port=5432
database.name=myapp
```

Create a ConfigMap named `file-config` from this file.

---

## Exercise 3 - Use ConfigMap as Environment Variables

Create a Pod named `env-pod` that uses `app-config` to inject all keys as environment variables using `envFrom`.

Exec into the Pod and verify the variables are set.

---

## Exercise 4 - Use Specific Keys

Create a Pod named `selective-env-pod` that only uses the `APP_ENV` key from `app-config` as an environment variable named `ENVIRONMENT`.

---

## Exercise 5 - Mount ConfigMap as Volume

Create a Pod named `vol-pod` that mounts `app-config` as a volume at `/etc/config`.

- Exec into the Pod
- List files in `/etc/config`
- Read the contents of each file

---

## Exercise 6 - ConfigMap with Nginx Config

Create a ConfigMap named `nginx-config` containing a custom `nginx.conf` that serves on port 8080.

Create a Pod that mounts this ConfigMap and uses it as the nginx configuration.

Verify nginx is running on port 8080.

---

## Exercise 7 - Update ConfigMap

Update the `app-config` ConfigMap to change `LOG_LEVEL` to `debug`.

- If mounted as volume: check if the file updates (may take ~30s)
- If used as env var: verify the Pod does NOT pick up the change (requires restart)

---

## Exercise 8 - ConfigMap in a Deployment

Create a Deployment named `config-deploy` with 3 replicas that uses `app-config` as environment variables.

Verify all Pods have the correct environment.

---

## Exercise 9 - Cleanup

Delete all ConfigMaps, Pods, and Deployments created in this lab.

---
