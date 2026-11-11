-- Storage for scraped records and CRM sync tracking (SQLite locally).

CREATE TABLE IF NOT EXISTS scraped_records (
    record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT,
    price        REAL,
    rating       INTEGER,
    availability TEXT,
    product_url  TEXT UNIQUE,
    first_seen   TEXT,
    last_seen    TEXT
);

CREATE TABLE IF NOT EXISTS sync_history (
    sync_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_time       TEXT,
    records_synced  INTEGER,
    new_records     INTEGER,
    updated_records INTEGER,
    sync_status     TEXT,
    error_message   TEXT
);

CREATE TABLE IF NOT EXISTS duplicate_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    product_url   TEXT,
    title         TEXT,
    detected_time TEXT
);
