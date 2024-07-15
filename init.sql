DROP TABLE IF EXISTS metadata;

CREATE TABLE metadata (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    file_type TEXT,
    file_size FLOAT DEFAULT 0.0,
    architecture TEXT,
    num_of_imports INTEGER DEFAULT 0,
    num_of_exports INTEGER DEFAULT 0,
    status TEXT,
    error TEXT,
    hash TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
