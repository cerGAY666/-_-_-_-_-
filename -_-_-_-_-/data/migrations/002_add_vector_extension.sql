-- Ensure pgvector extension is enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column if it doesn't exist
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'n' AND column_name = 'embedding') THEN
        ALTER TABLE N ADD COLUMN embedding vector(384);
    END IF;
END $$;

-- Create index for vector search
CREATE INDEX IF NOT EXISTS idx_n_embedding ON N 
USING ivfflat (embedding vector_cosine_ops);
