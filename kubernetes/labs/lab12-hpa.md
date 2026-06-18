# Lab 12 - HorizontalPodAutoscaler (HPA)

## Objective

Practice auto-scaling Pods based on resource metrics.

---

## Prerequisites

Install Metrics Server:
```bash
# Minikube
minikube addons enable metrics-server

# Or manually
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Verify:
```bash
kubectl top nodes
kubectl top pods
```

---

## Exercise 1 - Deploy an Application with Resource Requests

Create a Deployment named `load-app` with:
- Image: `k8s.gcr.io/hpa-example` (or `nginx`)
- 1 replica
- CPU request: 100m
- CPU limit: 200m

Create a ClusterIP Service for it on port 80.

---

## Exercise 2 - Create HPA

Create an HPA for `load-app`:
- Min replicas: 1
- Max replicas: 10
- Target CPU utilization: 50%

```bash
kubectl autoscale deployment load-app --cpu-percent=50 --min=1 --max=10
```

Verify:
```bash
kubectl get hpa
```

---

## Exercise 3 - Generate Load

From another terminal, generate load:
```bash
kubectl run load-gen --image=busybox --rm -it -- sh -c "while true; do wget -q -O- http://load-app; done"
```

Watch the HPA:
```bash
kubectl get hpa -w
```

Observe Pods scaling up.

---

## Exercise 4 - Stop Load

Stop the load generator and watch the HPA scale down.

Note: scale-down takes ~5 minutes by default.

---

## Exercise 5 - HPA from YAML

Create an HPA from YAML with:
- Target: `load-app`
- Min: 2, Max: 8
- CPU: 60%
- Memory: 80%

Apply and verify.

---

## Exercise 6 - Check HPA Details

```bash
kubectl describe hpa load-app
```

Identify:
- Current vs target CPU
- Number of replicas
- Scaling events

---

## Exercise 7 - Cleanup

Delete the HPA, Deployment, Service, and load generator.

---
