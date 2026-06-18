# Lab 02 - Services

## Objective

Practice exposing Pods using different Service types.

---

## Exercise 1 - Create a Deployment to Expose

Create a Deployment named `web-app` with:
- 3 replicas
- Image: `nginx`
- Label: `app: web`

---

## Exercise 2 - ClusterIP Service

Create a ClusterIP Service named `web-clusterip` that:
- Selects pods with label `app: web`
- Maps port 80 to targetPort 80

Verify with `kubectl get svc` and `kubectl describe svc web-clusterip`.

---

## Exercise 3 - Test ClusterIP Internally

- Create a temporary Pod: `kubectl run test --image=busybox --rm -it -- sh`
- From inside, run: `wget -qO- http://web-clusterip`
- Verify you get the nginx welcome page

---

## Exercise 4 - NodePort Service

Create a NodePort Service named `web-nodeport` that:
- Selects pods with label `app: web`
- Maps port 80 to targetPort 80
- Uses nodePort 30080

Access it using `<NodeIP>:30080`.

---

## Exercise 5 - LoadBalancer Service

Create a LoadBalancer Service named `web-lb` that:
- Selects pods with label `app: web`
- Maps port 80 to targetPort 80

Check the external IP with `kubectl get svc web-lb`.

> Note: On minikube, use `minikube service web-lb --url` to get the URL.

---

## Exercise 6 - Multi-Port Service

Create a Deployment named `multi-app` running an image that listens on ports 8080 and 8443.

Create a Service with two ports:
- `http`: port 80 → targetPort 8080
- `https`: port 443 → targetPort 8443

---

## Exercise 7 - Service DNS

- Create a Service named `backend-svc` in namespace `default`
- From a test Pod, verify you can reach it using:
  - `backend-svc`
  - `backend-svc.default`
  - `backend-svc.default.svc.cluster.local`

---

## Exercise 8 - Headless Service

Create a Headless Service (clusterIP: None) named `headless-svc` that selects your `web-app` pods.

- Run `nslookup headless-svc` from a test Pod
- Observe that it returns individual Pod IPs

---

## Exercise 9 - ExternalName Service

Create an ExternalName Service named `external-db` that points to `db.example.com`.

Describe the service and verify the externalName field.

---

## Exercise 10 - Cleanup

Delete all Services and Deployments created in this lab.

---
