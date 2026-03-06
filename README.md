
# Kubernetes Job Processing System with KEDA

![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-Application-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![KEDA](https://img.shields.io/badge/KEDA-Event--Driven%20Autoscaling-FF6C37)
![Kustomize](https://img.shields.io/badge/Kustomize-Kubernetes%20Config-blue)

A **Kubernetes-based asynchronous job processing system** built using **Python, PostgreSQL, and KEDA autoscaling**.

This project demonstrates how to build a **scalable job queue architecture** where jobs are pushed into a database and processed asynchronously by multiple consumer workers.

The system uses **KEDA to automatically scale workers based on the number of pending jobs**.

---

# System Architecture



```
              +-------------------+
              |   Job Pusher      |
              |  (Python Service) |
              +---------+---------+
                        |
                        v
               +-------------------+
               |    PostgreSQL     |
               |   Job Queue DB    |
               |-------------------|
               | jobs              |
               | done_jobs         |
               +---------+---------+
                         |
            +------------+-------------+
            |                          |
            v                          v
   +---------------+          +---------------+
   | Job Consumer  |          | Job Consumer  |
   |   Pod #1      |          |   Pod #2      |
   +---------------+          +---------------+

                ^
                |
            +--------+
            |  KEDA  |
            +--------+
      Autoscaling based on
       number of jobs
```



# Workflow

1️⃣ **Job Pusher** continuously inserts jobs into PostgreSQL.

2️⃣ Jobs are stored inside the `jobs` table.

3️⃣ **Consumers poll the database** to fetch jobs.

4️⃣ Each consumer:
- Picks a job
- Processes it
- Moves it to `done_jobs`

5️⃣ **KEDA monitors the queue size**.

6️⃣ If the number of pending jobs increases, **KEDA scales the number of consumer pods automatically**.

---

# Technologies Used

| Technology | Purpose |
|------|------|
| Kubernetes | Container orchestration |
| Docker | Application containerization |
| Python | Pusher and consumer services |
| PostgreSQL | Persistent job queue |
| KEDA | Event-driven autoscaling |
| Kustomize | Kubernetes configuration management |

---

# Repository Structure

```

.
├── consumer
│   ├── consumer.py
│   ├── consumer.yaml
│   ├── job-consumer.yaml
│   └── kustomization.yaml
│
├── database
│   ├── db-init.yaml
│   ├── init.sql
│   ├── kustomization.yaml
│   ├── service.yaml
│   └── statefulset.yaml
│
├── keda
│   ├── kustomization.yaml
│   ├── scaler.yaml
│   ├── secret.yaml
│   └── trigger-auth.yaml
│
├── pusher
│   ├── kustomization.yaml
│   ├── pusher-cm.yaml
│   ├── pusher.py
│   └── pusher.yaml
│
├── ns.yaml
└── kustomization.yaml

````

---

# Kubernetes Components

| Component | Purpose |
|------|------|
| Namespace | Isolates project resources |
| StatefulSet | Runs PostgreSQL with persistent storage |
| Deployment | Runs job pushers and consumers |
| Service | Stable network endpoint for PostgreSQL |
| ConfigMap | Configuration management |
| Secret | Stores database credentials |
| KEDA ScaledObject | Enables autoscaling |

---

# Database Schema

### jobs

Stores pending jobs.

| Column | Description |
|------|-------------|
| id | Job ID |
| payload | Job data |
| created_at | Job creation time |

### done_jobs

Stores completed jobs.

| Column | Description |
|------|-------------|
| id | Job ID |
| completed_at | Job completion time |

---

# Deployment

## 1 Create Namespace

```bash
kubectl apply -f ns.yaml
````

## 2 Deploy Database

```bash
kubectl apply -k database/
```

## 3 Deploy Job Pusher

```bash
kubectl apply -k pusher/
```

## 4 Deploy Job Consumers

```bash
kubectl apply -k consumer/
```

## 5 Deploy KEDA Autoscaler

```bash
kubectl apply -k keda/
```

---

# Demo Commands

Check running pods:

```bash
kubectl get pods -n job-process
```

Watch autoscaling:

```bash
kubectl get hpa -w
```

Check job table:

```bash
kubectl exec -it postgres-0 -n job-process -- psql -U jobuser -d jobqueue
```

Query jobs:

```sql
SELECT * FROM jobs;
SELECT * FROM done_jobs;
```

---

# Autoscaling Behavior

KEDA scales consumers based on the number of pending jobs.

Example:

| Jobs in Queue | Consumer Pods |
| ------------- | ------------- |
| 0–10          | 1             |
| 50            | 5             |
| 100+          | 10            |

This ensures **efficient resource usage and high throughput**.

