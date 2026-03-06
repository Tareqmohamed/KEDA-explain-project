import psycopg2
import time
import random
import string

DB_CONFIG = {
    "host": "postgres.job-processing.svc.cluster.local",
    "database": "jobqueue",
    "user": "jobuser",
    "password": "jobpass123"
}

print("Job Pusher started")

while True:
    try:
        # Create new connection for each job
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                payload = ''.join(random.choices(string.ascii_letters, k=20))
                cur.execute(
                    "INSERT INTO jobs (payload) VALUES (%s)", (payload,))
                conn.commit()
                print(f"Pushed job with payload: {payload}")

        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)