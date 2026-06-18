# Lab 15 - Namespaces and Resource Quotas

## Objective

Practice using Namespaces for isolation and applying Resource Quotas.

---

## Exercise 1 - Create Namespaces

Create three namespaces:
- `development`
- `staging`
- `production`

Verify:
```bash
kubectl get namespaces
```

---

## Exercise 2 - Deploy to Specific Namespace

Create a Deployment named `web` with 2 replicas in the `development` namespace.

Verify:
```bash
kubectl get pods -n development
kubectl get pods -n staging        # should be empty
```

---

## Exercise 3 - Set Default Namespace

Set your default namespace to `development`:
```bash
kubectl config set-context --current --namespace=development
```

Now `kubectl get pods` should show the pods without `-n`.

---

## Exercise 4 - Cross-Namespace Communication

- Deploy an nginx service in `staging`
- From a Pod in `development`, access it via:
  ```
  curl http://web.staging.svc.cluster.local
  ```

---

## Exercise 5 - Resource Quota

Create a ResourceQuota in `development`:
- Max pods: 5
- Max CPU requests: 2
- Max memory requests: 2Gi

Try to create more pods than allowed and observe the error.

---

## Exercise 6 - LimitRange

Create a LimitRange in `development`:
- Default CPU limit: 200m
- Default memory limit: 256Mi
- Default CPU request: 100m
- Default memory request: 128Mi

Create a Pod without specifying resources and verify the defaults are applied.

---

## Exercise 7 - Namespace Labels

Add labels to namespaces:
```bash
kubectl label namespace development environment=dev
kubectl label namespace production environment=prod
```

List namespaces with labels:
```bash
kubectl get ns --show-labels
```

---

## Exercise 8 - Delete a Namespace

Delete the `staging` namespace:
```bash
kubectl delete namespace staging
```

Verify all resources inside it are gone.

---

## Exercise 9 - Cleanup

- Delete `development` and `production` namespaces
- Reset your default namespace to `default`

---
