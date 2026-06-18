# Lab 04 - Deployments

## Objective

Practice creating Deployments, performing rolling updates, and rollbacks.

---

## Exercise 1 - Create a Deployment

Create a Deployment named `app-deploy` with:
- 3 replicas
- Image: `nginx:1.21`
- Labels: `app: myapp`

Verify the Deployment, ReplicaSet, and Pods are created.

---

## Exercise 2 - Check Rollout Status

```bash
kubectl rollout status deployment/app-deploy
```

Check the revision history:

```bash
kubectl rollout history deployment/app-deploy
```

---

## Exercise 3 - Rolling Update

Update the image to `nginx:1.22`:

```bash
kubectl set image deployment/app-deploy nginx=nginx:1.22
```

- Watch the rollout: `kubectl rollout status deployment/app-deploy`
- Check that a new ReplicaSet was created: `kubectl get rs`
- Verify Pods are running the new image

---

## Exercise 4 - Rollback

Roll back to the previous version:

```bash
kubectl rollout undo deployment/app-deploy
```

- Verify the image is back to `nginx:1.21`
- Check the rollout history

---

## Exercise 5 - Rollback to Specific Revision

- Update the image to `nginx:1.23`
- Update again to `nginx:1.24`
- Roll back to revision 1:

```bash
kubectl rollout undo deployment/app-deploy --to-revision=1
```

---

## Exercise 6 - Scaling

Scale the Deployment to 6 replicas, then down to 2.

Verify at each step.

---

## Exercise 7 - Recreate Strategy

Create a new Deployment named `recreate-deploy` with:
- Strategy type: `Recreate`
- 3 replicas, image: `nginx:1.21`

Update the image and observe that all old Pods are killed before new ones start.

---

## Exercise 8 - RollingUpdate with maxSurge and maxUnavailable

Create a Deployment named `controlled-deploy` with:
- 5 replicas
- Strategy: RollingUpdate
- maxSurge: 1
- maxUnavailable: 0

Update the image and observe how Pods are replaced one at a time (zero downtime).

---

## Exercise 9 - Pause and Resume

- Pause the Deployment: `kubectl rollout pause deployment/app-deploy`
- Update the image
- Verify no rollout happens
- Resume: `kubectl rollout resume deployment/app-deploy`

---

## Exercise 10 - Cleanup

Delete all Deployments created in this lab and verify no Pods remain.

---
