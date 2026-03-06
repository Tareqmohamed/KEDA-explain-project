import psycopg2
import time
import random
import os

DB_CONFIG = {
    "host": "postgres.job-processing.svc.cluster.local",
    "database": "jobqueue",
    "user": "jobuser",
    "password": "jobpass123"
}

pod_name = os.getenv('HOSTNAME', 'unknown')
print(f"Job Consumer {pod_name} started")

while True:
    try:
        # Create new connection for each iteration
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Fetch and lock a job
                cur.execute("""
                    DELETE FROM jobs
                    WHERE id = (
                        SELECT id FROM jobs
                        ORDER BY created_at
                        LIMIT 1
                        FOR UPDATE SKIP LOCKED
                    )
                    RETURNING id, payload
                """)

                job = cur.fetchone()

                if job:
                    job_id, payload = job
                    print(f"[{pod_name}] Processing job {job_id}: {payload}")

                    # Simulate random processing time (2-10 seconds)
                    process_time = random.uniform(2, 10)
                    time.sleep(process_time)

                    # Mark as done
                    cur.execute(
                        "INSERT INTO done_jobs (id) VALUES (%s)", (job_id,))
                    conn.commit()
                    print(
                        f"[{pod_name}] Completed job {job_id} in {process_time:.2f}s")
                else:
                    time.sleep(1)

    except Exception as e:
        print(f"[{pod_name}] Error: {e}")
        time.sleep(2)