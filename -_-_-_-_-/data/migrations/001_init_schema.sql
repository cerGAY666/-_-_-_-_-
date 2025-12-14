-- Initial database schema for Pulse
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS N (
    name TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    degree_layout INTEGER,
    stringdb_description TEXT,
    target_family TEXT,
    embedding vector(384)
);

CREATE TABLE IF NOT EXISTS E (
    name TEXT PRIMARY KEY,
    stringdb_coexpression FLOAT4,
    stringdb_cooccurrence FLOAT4,
    stringdb_databases FLOAT4,
    stringdb_experiments FLOAT4,
    stringdb_fusion FLOAT4,
    stringdb_neighborhood FLOAT4,
    stringdb_score FLOAT4,
    stringdb_textmining FLOAT4
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_n_display_name ON N(display_name);
CREATE INDEX IF NOT EXISTS idx_n_family ON N(target_family);
CREATE INDEX IF NOT EXISTS idx_n_degree ON N(degree_layout DESC);
