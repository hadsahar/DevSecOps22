# Lab 11 - Jobs and CronJobs

## Objective

Practice creating Jobs for one-time tasks and CronJobs for scheduled tasks.

---

## Exercise 1 - Simple Job

Create a Job named `hello-job` that:
- Runs `busybox`
- Command: `echo "Hello from Kubernetes Job!"`

Check the Job status and view the logs.

---

## Exercise 2 - Job with Multiple Completions

Create a Job named `batch-job` with:
- completions: 5
- parallelism: 2
- Command: `sh -c "echo Processing task; sleep 3"`

Watch the Pods and observe parallel execution.

---

## Exercise 3 - Job Failure and Backoff

Create a Job named `failing-job` with:
- Command: `sh -c "exit 1"` (always fails)
- backoffLimit: 3

Watch and verify it retries 3 times then stops.

---

## Exercise 4 - Job with TTL

Create a Job named `ttl-job` with:
- `ttlSecondsAfterFinished: 30`
- Command: `echo "Done"`

Verify the Job is automatically deleted after 30 seconds.

---

## Exercise 5 - CronJob (Every Minute)

Create a CronJob named `minute-job` that:
- Runs every minute: `*/1 * * * *`
- Command: `echo "Tick at $(date)"`

Wait 3 minutes, then check:
```bash
kubectl get cronjobs
kubectl get jobs
kubectl get pods
```

---

## Exercise 6 - CronJob History

Create a CronJob with:
- `successfulJobsHistoryLimit: 2`
- `failedJobsHistoryLimit: 1`

Let it run several times and verify old Jobs are cleaned up.

---

## Exercise 7 - CronJob Concurrency Policy

Create a CronJob named `slow-job` that:
- Runs every minute
- Takes 90 seconds to complete
- concurrencyPolicy: `Forbid`

Verify that overlapping executions are skipped.

---

## Exercise 8 - Suspend a CronJob

Suspend the CronJob:
```bash
kubectl patch cronjob minute-job -p '{"spec":{"suspend":true}}'
```

Verify no new Jobs are created. Resume it and verify it runs again.

---

## Exercise 9 - Cleanup

Delete all Jobs and CronJobs created in this lab.

---
