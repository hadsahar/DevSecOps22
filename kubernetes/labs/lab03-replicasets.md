# Lab 03 - ReplicaSets

## Objective

Practice creating and managing ReplicaSets to maintain Pod replicas.

---

## Exercise 1 - Create a ReplicaSet

Create a ReplicaSet named `nginx-rs` with:
- 3 replicas
- Image: `nginx:1.21`
- Label selector: `app: nginx`

Verify all 3 Pods are running.

---

## Exercise 2 - Examine Pod Names

- List all Pods created by the ReplicaSet
- Notice the naming pattern: `nginx-rs-<random>`
- Describe the ReplicaSet and check the events

---

## Exercise 3 - Self-Healing

Delete one of the Pods manually:

```bash
kubectl delete pod <pod-name>
```

- Watch the Pods: `kubectl get pods -w`
- Verify that a new Pod is created automatically

---

## Exercise 4 - Scale Up

Scale the ReplicaSet to 5 replicas:

```bash
kubectl scale rs nginx-rs --replicas=5
```

Verify 5 Pods are running.

---

## Exercise 5 - Scale Down

Scale the ReplicaSet to 2 replicas.

- Which Pods get terminated?
- Verify only 2 Pods remain

---

## Exercise 6 - Label Mismatch

Create a standalone Pod with label `app: nginx` (matching the ReplicaSet selector).

- What happens to the extra Pod?
- Explain why

---

## Exercise 7 - Update Image (Limitation)

Update the ReplicaSet YAML to use `nginx:1.22`.

- Apply the change
- Check if existing Pods get the new image
- Delete one Pod and check the new Pod's image

> This demonstrates why Deployments are preferred over ReplicaSets.

---

## Exercise 8 - Delete ReplicaSet

Delete the ReplicaSet:

```bash
kubectl delete rs nginx-rs
```

- What happens to the Pods?
- Try deleting with `--cascade=orphan` and observe the difference

---
