# Lab 13 - NetworkPolicy

## Objective

Practice restricting Pod-to-Pod traffic using NetworkPolicies.

---

## Prerequisites

Ensure your cluster uses a CNI that supports NetworkPolicies (Calico, Cilium, Weave).

On minikube with Calico:
```bash
minikube start --cni=calico
```

---

## Exercise 1 - Setup Test Environment

Create three Deployments in namespace `netpol-lab`:
1. `frontend` (image: nginx, label: `role=frontend`)
2. `backend` (image: nginx, label: `role=backend`)
3. `database` (image: nginx, label: `role=database`)

Create a ClusterIP Service for each.

Verify all Pods can communicate with each other.

---

## Exercise 2 - Deny All Ingress

Create a NetworkPolicy that denies all ingress traffic to all Pods in `netpol-lab`.

Test: from `frontend`, try to curl `backend` — it should fail.

---

## Exercise 3 - Allow Frontend to Backend

Create a NetworkPolicy that allows `frontend` Pods to access `backend` Pods on port 80.

Test:
- frontend → backend: should work
- frontend → database: should fail
- database → backend: should fail

---

## Exercise 4 - Allow Backend to Database

Create a NetworkPolicy that allows `backend` Pods to access `database` Pods on port 80.

Test:
- backend → database: should work
- frontend → database: should fail

---

## Exercise 5 - Deny All Egress

Create a NetworkPolicy that denies all egress from `database` Pods.

Test: from `database`, try to curl anything — should fail.

---

## Exercise 6 - Allow DNS Egress

Update the database NetworkPolicy to allow egress to DNS (port 53 UDP/TCP).

Test: DNS should work now, but HTTP to other services still blocked.

---

## Exercise 7 - Allow Traffic from Specific Namespace

Create a namespace `monitoring` with label `purpose=monitoring`.

Create a NetworkPolicy that allows Pods from `monitoring` namespace to access `backend`.

Test from a Pod in `monitoring`.

---

## Exercise 8 - Cleanup

Delete the namespace `netpol-lab` (this deletes everything inside it).

---
