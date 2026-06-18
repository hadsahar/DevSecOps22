# Lab 09 - StatefulSets

## Objective

Practice deploying stateful applications with stable identities and persistent storage.

---

## Exercise 1 - Create a Headless Service

Create a Headless Service named `mysql-headless` with:
- clusterIP: None
- Selector: `app: mysql`
- Port: 3306

---

## Exercise 2 - Create a StatefulSet

Create a StatefulSet named `mysql` with:
- serviceName: `mysql-headless`
- 3 replicas
- Image: `mysql:8.0`
- Env: `MYSQL_ROOT_PASSWORD=rootpass`
- volumeClaimTemplate: 5Gi, ReadWriteOnce

Verify Pods are created in order: mysql-0, mysql-1, mysql-2.

---

## Exercise 3 - Verify Stable Pod Names

- Delete `mysql-1`
- Watch the Pods: `kubectl get pods -w`
- Verify the new Pod is named `mysql-1` (same name)

---

## Exercise 4 - Verify Stable DNS

From a test Pod, resolve each StatefulSet Pod:

```bash
nslookup mysql-0.mysql-headless.default.svc.cluster.local
nslookup mysql-1.mysql-headless.default.svc.cluster.local
```

---

## Exercise 5 - Verify Persistent Storage

- Exec into `mysql-0` and create a database
- Delete `mysql-0`
- Wait for it to restart
- Verify the database still exists

---

## Exercise 6 - Scale StatefulSet

Scale to 5 replicas and observe the order of creation.

Scale down to 2 and observe the order of deletion (reverse).

---

## Exercise 7 - Check PVCs

```bash
kubectl get pvc
```

- Verify each Pod has its own PVC
- Note that PVCs are NOT deleted when Pods are deleted

---

## Exercise 8 - Cleanup

Delete the StatefulSet, Headless Service, and PVCs.

---
