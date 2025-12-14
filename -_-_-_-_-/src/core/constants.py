"""
Constants and schema definitions for Pulse AI Assistant.
"""
DB_SCHEMA = """
PostgreSQL Database Schema:
1. N (Nodes/Genes table)
   - name (TEXT): Gene identifier (e.g., "9606.ENSP00000418960")
   - display_name (TEXT): Common gene name (e.g., "BRCA1", "TP53")
   - degree_layout (INTEGER): PRE-CALCULATED number of connections
   - stringdb_description (TEXT): Description of the gene function
   - target_family (TEXT): Protein family
   - embedding (VECTOR): Vector embedding of gene description (384 dimensions)

2. E (Edges/Interactions table)
   - name (TEXT): Interaction ID
   - stringdb_coexpression (FLOAT4)
   - stringdb_cooccurrence (FLOAT4)
   - stringdb_databases (FLOAT4)
   - stringdb_experiments (FLOAT4)
   - stringdb_fusion (FLOAT4)
   - stringdb_neighborhood (FLOAT4)
   - stringdb_score (FLOAT4): Reliability score
   - stringdb_textmining (FLOAT4)
"""

# Example queries for the bot to suggest
EXAMPLE_QUERIES = [
    "🔹 Что известно о гене TP53?",
    "🔹 К какому семейству белков относится ген INS?",
    "🔹 Сколько связей у гена EGFR?",
    "🔹 Назови топ-5 генов с наибольшим количеством связей.",
    "🔹 Какие гены связаны с репарацией ДНК?",
    "🔹 Найди гены из семейства киназ.",
]

# SQL templates for common queries
SQL_TEMPLATES = {
    "gene_info": "SELECT display_name, stringdb_description, target_family, degree_layout FROM N WHERE display_name = '{gene_name}'",
    "gene_connections": "SELECT degree_layout FROM N WHERE display_name = '{gene_name}'",
    "top_connected": "SELECT display_name, degree_layout FROM N ORDER BY degree_layout DESC LIMIT {limit}",
    "by_family": "SELECT display_name, target_family FROM N WHERE target_family = '{family}'",
}

# System prompts for LLM
SYSTEM_PROMPTS = {
    "sql_generator": """
    You are a professional SQL Data Analyst using PostgreSQL.
    
    Here is the database schema:
    {schema}
    
    Your task: Convert the user's question into a valid SQL query.
    
    RULES:
    1. Output ONLY the SQL query. Do not write markdown, code blocks (```), or explanations.
    2. Use only SELECT statements. Do not use INSERT, UPDATE, DELETE.
    3. If the question cannot be answered with the schema, return "SELECT 'Cannot answer';"
    4. Always answer in Russian.
    
    User question: {question}
    """,
    
    "response_formatter": """
    You are a helpful medical analyst assistant speaking Russian.
    
    User Question: "{question}"
    Database Raw Result: "{result}"
    
    Task: Formulate a concise and professional answer in Russian based strictly on the data provided.
    Do not invent facts. Keep it under 3 sentences if possible.
    """
}
