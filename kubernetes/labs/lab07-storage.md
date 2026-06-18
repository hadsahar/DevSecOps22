# Lab 07 - Storage (PV, PVC, StorageClass)

## Objective

Practice creating PersistentVolumes, PersistentVolumeClaims, and using StorageClasses.

---

## Exercise 1 - Create a PersistentVolume

Create a PV named `my-pv` with:
- Capacity: 5Gi
- Access mode: ReadWriteOnce
- Reclaim policy: Retain
- HostPath: `/mnt/data`

Verify with `kubectl get pv`.

---

## Exercise 2 - Create a PersistentVolumeClaim

Create a PVC named `my-pvc` that requests:
- 3Gi storage
- Access mode: ReadWriteOnce

- Check if it binds to `my-pv`
- Verify with `kubectl get pvc`

---

## Exercise 3 - Use PVC in a Pod

Create a Pod named `storage-pod` running `nginx` that:
- Mounts `my-pvc` at `/usr/share/nginx/html`

Exec into the Pod and create a file. Delete the Pod and create a new one with the same PVC — verify the file persists.

---

## Exercise 4 - PV and PVC Size Mismatch

Create a PV with 2Gi and a PVC requesting 5Gi.

- What happens to the PVC?
- Check its status

---

## Exercise 5 - List StorageClasses

```bash
kubectl get storageclass
```

Identify the default StorageClass in your cluster.

---

## Exercise 6 - Dynamic Provisioning

Create a PVC named `dynamic-pvc` with:
- StorageClassName matching your default SC
- Request: 1Gi

Verify that a PV is automatically created and bound.

---

## Exercise 7 - PVC in a Deployment

Create a Deployment named `db-deploy` with 1 replica running `mysql:8.0`:
- Mount a PVC at `/var/lib/mysql`
- Set env `MYSQL_ROOT_PASSWORD` from a Secret

Verify the database persists across Pod restarts.

---

## Exercise 8 - Reclaim Policy Test

- Delete the PVC from Exercise 2
- Check the PV status (should be `Released` with Retain policy)
- Manually delete the PV

---

## Exercise 9 - Cleanup

Delete all PVs, PVCs, Pods, and Deployments created in this lab.

---
