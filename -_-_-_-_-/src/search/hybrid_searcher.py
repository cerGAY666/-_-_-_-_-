"""
Hybrid search combining vector and SQL search.
"""
from typing import List, Dict, Any
from src.database.connection import DatabaseConnection

class HybridSearcher:
    """Combines vector semantic search with SQL filtering."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform hybrid search:
        1. Vector search for semantic similarity
        2. SQL filtering for exact criteria
        """
        # TODO: Implement vector search when embeddings are ready
        # For now, fall back to SQL-based search
        
        # Extract potential gene names from query
        gene_names = self._extract_gene_names(query)
        
        if gene_names:
            # Search for specific genes
            results = []
            for gene in gene_names:
                sql = f"""
                SELECT display_name, stringdb_description, target_family, degree_layout
                FROM N WHERE display_name ILIKE '%{gene}%'
                LIMIT 5
                """
                try:
                    rows = self.db.execute_query(sql)
                    for row in rows:
                        results.append({
                            "display_name": row[0],
                            "description": row[1],
                            "family": row[2],
                            "connections": row[3]
                        })
                except:
                    continue
            return results
        
        return []
    
    def _extract_gene_names(self, query: str) -> List[str]:
        """Simple gene name extraction (to be improved)."""
        common_genes = [
            "TP53", "BRCA1", "BRCA2", "EGFR", "ATM", "CHEK2", 
            "SIRT6", "ERCC1", "RAD50", "BLM", "FANCD2"
        ]
        
        found = []
        query_upper = query.upper()
        for gene in common_genes:
            if gene in query_upper:
                found.append(gene)
        
        return found
