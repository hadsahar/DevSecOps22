# Lab 14 - RBAC

## Objective

Practice configuring Role-Based Access Control to restrict permissions.

---

## Exercise 1 - Create a Namespace

Create a namespace named `dev-team`.

---

## Exercise 2 - Create a ServiceAccount

Create a ServiceAccount named `developer` in namespace `dev-team`.

---

## Exercise 3 - Create a Role

Create a Role named `pod-reader` in namespace `dev-team` that allows:
- Resources: pods
- Verbs: get, list, watch

---

## Exercise 4 - Create a RoleBinding

Create a RoleBinding named `developer-pod-reader` that binds:
- Role: `pod-reader`
- Subject: ServiceAccount `developer` in namespace `dev-team`

---

## Exercise 5 - Test Permissions

Test what the ServiceAccount can do:

```bash
kubectl auth can-i get pods --as=system:serviceaccount:dev-team:developer -n dev-team
kubectl auth can-i create pods --as=system:serviceaccount:dev-team:developer -n dev-team
kubectl auth can-i delete pods --as=system:serviceaccount:dev-team:developer -n dev-team
```

Expected: only `get` returns yes.

---

## Exercise 6 - Expand the Role

Update the Role to also allow:
- Resources: pods, services, deployments
- Verbs: get, list, watch, create

Test again with `kubectl auth can-i`.

---

## Exercise 7 - ClusterRole

Create a ClusterRole named `node-viewer` that allows:
- Resources: nodes
- Verbs: get, list

Create a ClusterRoleBinding to bind it to the `developer` ServiceAccount.

Test:
```bash
kubectl auth can-i list nodes --as=system:serviceaccount:dev-team:developer
```

---

## Exercise 8 - Deny Test

Verify the ServiceAccount CANNOT:
- Delete deployments
- Access secrets
- Create namespaces

---

## Exercise 9 - Use ServiceAccount in a Pod

Create a Pod in `dev-team` that uses the `developer` ServiceAccount.

Exec into the Pod and try to list pods using the mounted token:
```bash
curl -s --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  https://kubernetes.default.svc/api/v1/namespaces/dev-team/pods
```

---

## Exercise 10 - Cleanup

Delete namespace `dev-team` (removes all resources inside).

---
