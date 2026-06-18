# Lab 10 - DaemonSets

## Objective

Practice deploying DaemonSets to run Pods on every node.

---

## Exercise 1 - Create a DaemonSet

Create a DaemonSet named `log-agent` with:
- Image: `busybox`
- Command: `sh -c "while true; do echo collecting logs from $(hostname); sleep 10; done"`
- Label: `app: log-agent`

Verify one Pod runs on each node:
```bash
kubectl get pods -o wide
kubectl get nodes
```

---

## Exercise 2 - DaemonSet with HostPath Volume

Create a DaemonSet named `node-monitor` that:
- Mounts `/var/log` from the host to `/host-logs` (readOnly)
- Image: `busybox`
- Command: lists files in `/host-logs` every 30 seconds

Check the logs of a Pod.

---

## Exercise 3 - Node Selector

Add a label to one of your nodes:
```bash
kubectl label node <node-name> disk=ssd
```

Create a DaemonSet named `ssd-agent` that only runs on nodes with `disk=ssd`.

Verify the Pod only runs on the labeled node.

---

## Exercise 4 - Update DaemonSet

Update the `log-agent` DaemonSet image to `busybox:1.36`.

- Watch the rolling update: `kubectl rollout status ds/log-agent`
- Verify all Pods are updated

---

## Exercise 5 - DaemonSet Rollback

Roll back the DaemonSet to the previous version:
```bash
kubectl rollout undo daemonset/log-agent
```

Verify.

---

## Exercise 6 - Cleanup

- Remove node labels
- Delete all DaemonSets created in this lab

---
