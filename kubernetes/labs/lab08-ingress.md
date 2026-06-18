# Lab 08 - Ingress

## Objective

Practice configuring Ingress rules for HTTP routing.

---

## Prerequisites

Enable the Ingress addon:

```bash
# Minikube
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx
```

---

## Exercise 1 - Deploy Two Applications

Create two Deployments:
1. `frontend` with image `nginx` (3 replicas)
2. `backend` with image `httpd` (2 replicas)

Create a ClusterIP Service for each (port 80).

---

## Exercise 2 - Path-Based Routing

Create an Ingress named `path-ingress` with host `myapp.local`:
- `/` → frontend service
- `/api` → backend service

Add `myapp.local` to your `/etc/hosts` pointing to your cluster IP.

Test with curl:
```bash
curl http://myapp.local/
curl http://myapp.local/api
```

---

## Exercise 3 - Host-Based Routing

Create an Ingress named `host-ingress`:
- `frontend.local` → frontend service
- `backend.local` → backend service

Add both to `/etc/hosts` and test.

---

## Exercise 4 - TLS Ingress

- Generate a self-signed certificate for `secure.local`
- Create a TLS Secret named `tls-secret`
- Create an Ingress that uses TLS for `secure.local`

Test with:
```bash
curl -k https://secure.local
```

---

## Exercise 5 - Default Backend

Create an Ingress with a default backend that catches all unmatched requests.

Test by accessing a path that doesn't match any rule.

---

## Exercise 6 - Annotations

Create an Ingress with:
- Rewrite target annotation (`nginx.ingress.kubernetes.io/rewrite-target: /`)
- Path `/app` rewritten to `/` on the backend

Verify the rewrite works.

---

## Exercise 7 - Multiple Paths to Same Service

Create an Ingress that routes both `/v1` and `/v2` to the same backend service but different ports.

---

## Exercise 8 - Cleanup

Delete all Ingress resources, Services, and Deployments created in this lab.

---
