# Lab 06 - Secrets

## Objective

Practice creating and using Secrets to manage sensitive data in Kubernetes.

---

## Exercise 1 - Create Secret from Literals

Create a Secret named `db-credentials` with:
- `username=admin`
- `password=supersecret123`

Verify with `kubectl get secret db-credentials -o yaml`.

---

## Exercise 2 - Decode Secret

Get the Secret and decode the base64 values:

```bash
kubectl get secret db-credentials -o jsonpath='{.data.username}' | base64 -d
kubectl get secret db-credentials -o jsonpath='{.data.password}' | base64 -d
```

---

## Exercise 3 - Create Secret from YAML (stringData)

Create a Secret named `api-secret` using YAML with `stringData`:
- `API_KEY=abc123xyz`
- `API_SECRET=my-super-secret`

Apply and verify the data is encoded automatically.

---

## Exercise 4 - Use Secret as Environment Variables

Create a Pod named `secret-env-pod` running `busybox` that:
- Sets `DB_USER` from `db-credentials` key `username`
- Sets `DB_PASS` from `db-credentials` key `password`

Exec into the Pod and print the variables.

---

## Exercise 5 - Use Secret as Volume

Create a Pod named `secret-vol-pod` that mounts `db-credentials` at `/etc/secrets`.

- Exec into the Pod
- List and read files in `/etc/secrets`
- Verify the files contain the decoded values

---

## Exercise 6 - Docker Registry Secret

Create a docker-registry secret named `regcred` with:
- Server: `https://index.docker.io/v1/`
- Username: `myuser`
- Password: `mypass`

Use it in a Pod's `imagePullSecrets`.

---

## Exercise 7 - TLS Secret

Generate a self-signed certificate:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=myapp.local"
```

Create a TLS Secret named `tls-secret` from the cert and key.

Verify with `kubectl describe secret tls-secret`.

---

## Exercise 8 - Secret in a Deployment

Create a Deployment named `secret-deploy` with 3 replicas that uses `db-credentials` as environment variables.

Verify all Pods have the correct values.

---

## Exercise 9 - Cleanup

Delete all Secrets, Pods, and Deployments created in this lab.

---
