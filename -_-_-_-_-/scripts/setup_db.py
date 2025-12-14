#!/usr/bin/env python3
"""
Database setup script for Pulse AI Assistant.
Creates tables, adds pgvector extension, and imports data.
"""
import os
import sys
import psycopg2
import pandas as pd
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.core.config import config

def create_tables(conn):
    """Create database tables."""
    sql = """
    -- Enable pgvector extension
    CREATE EXTENSION IF NOT EXISTS vector;
    
    -- Drop existing tables if they exist
    DROP TABLE IF EXISTS E CASCADE;
    DROP TABLE IF EXISTS N CASCADE;
    
    -- Create N (Nodes/Genes) table
    CREATE TABLE N (
        name TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        degree_layout INTEGER,
        stringdb_description TEXT,
        target_family TEXT,
        embedding vector(384)
    );
    
    -- Create E (Edges/Interactions) table
    CREATE TABLE E (
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
    
    -- Create indexes for better performance
    CREATE INDEX idx_n_display_name ON N(display_name);
    CREATE INDEX idx_n_family ON N(target_family);
    CREATE INDEX idx_n_degree ON N(degree_layout DESC);
    """
    
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("✅ Tables created successfully")

def import_data(conn, data_dir: Path):
    """Import data from CSV files."""
    # Import N table data
    n_path = data_dir / "raw" / "N_table_filtered.csv"
    if n_path.exists():
        df_n = pd.read_csv(n_path)
        # Rename columns to match our schema
        df_n = df_n.rename(columns={
            'degree.layout': 'degree_layout',
            'display name': 'display_name',
            'stringdb::description': 'stringdb_description',
            'target::family': 'target_family'
        })
        
        with conn.cursor() as cur:
            for _, row in df_n.iterrows():
                cur.execute("""
                    INSERT INTO N (name, display_name, degree_layout, stringdb_description, target_family)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """, (row['name'], row['display_name'], row['degree_layout'], 
                      row['stringdb_description'], row['target_family']))
        print(f"✅ Imported {len(df_n)} records to N table")
    
    # Import E table data
    e_path = data_dir / "raw" / "E_table_filtered.csv"
    if e_path.exists():
        df_e = pd.read_csv(e_path, sep=';')
        
        with conn.cursor() as cur:
            for _, row in df_e.iterrows():
                cur.execute("""
                    INSERT INTO E (
                        name, stringdb_coexpression, stringdb_cooccurrence,
                        stringdb_databases, stringdb_experiments, stringdb_fusion,
                        stringdb_neighborhood, stringdb_score, stringdb_textmining
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """, (row['name'], row['stringdb_coexpression'], row['stringdb_cooccurrence'],
                      row['stringdb_databases'], row['stringdb_experiments'], row['stringdb_fusion'],
                      row['stringdb_neighborhood'], row['stringdb_score'], row['stringdb_textmining']))
        print(f"✅ Imported {len(df_e)} records to E table")
    
    conn.commit()

def main():
    """Main setup function."""
    print("🚀 Setting up Pulse database...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(config.DB_URI)
        print("✅ Connected to database")
        
        # Create tables
        create_tables(conn)
        
        # Import data
        data_dir = Path(__file__).parent.parent / "data"
        import_data(conn, data_dir)
        
        # Verify data
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM N")
            n_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM E")
            e_count = cur.fetchone()[0]
        
        print(f"\n📊 Database setup complete!")
        print(f"   Genes (N table): {n_count} records")
        print(f"   Interactions (E table): {e_count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
