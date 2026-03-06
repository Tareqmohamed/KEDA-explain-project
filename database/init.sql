CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    payload TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS done_jobs (
    id INTEGER PRIMARY KEY,
    completed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs (created_at);