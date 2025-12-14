# Data Directory

This directory contains all data for the Pulse AI Assistant.

## Structure
- `raw/` - Original, unprocessed data files (CSV, JSON, etc.)
- `processed/` - Processed data and generated embeddings
- `migrations/` - Database migration scripts

## Current Data
1. `N_table_filtered.csv` - Genes/nodes table with 50+ aging-related genes
2. `E_table_filtered.csv` - Interactions/edges table

## Next Steps
1. Run `scripts/setup_db.py` to import data into PostgreSQL
2. Run `scripts/generate_embeddings.py` to create vector embeddings
