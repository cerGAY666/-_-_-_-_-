# 📊 **GenNet AI: Semantic Search Engine for Genetic Networks**

**AI-powered conversational assistant for analyzing aging-related gene networks using hybrid vector + SQL search.**

---

## 🎯 **Project Overview**

GenNet AI is a research prototype that bridges the gap between biological experts and complex genetic network analysis tools. The system allows researchers to interact with genetic networks through natural language queries, transforming static network visualizations into interactive knowledge models.

**Core Innovation:** Hybrid architecture combining traditional SQL queries with semantic vector search using gene description embeddings.

---

## 🧬 **Data Structure**

### **PostgreSQL Database Schema**
```
N (Nodes/Genes table):
- display_name (TEXT): Common gene name (e.g., "BRCA1", "TP53")
- degree_layout (INTEGER): Pre-calculated number of connections
- stringdb_description (TEXT): Gene function description
- target_family (TEXT): Protein family

E (Edges/Interactions table):
- name (TEXT): Interaction ID
- stringdb_coexpression, stringdb_score, etc. (FLOAT4): Interaction metrics
```

**Sample Genes in Network:** TP53, BRCA1, ATM, CHEK2, ERCC1, RAD50, SIRT6 (total 50+ aging-related genes)

---

## 🏗️ **Current Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │───▶│   Python Bot    │───▶│  LM Studio     │
│    Interface    │    │  (giga_gen.py)  │    │ (GigaChat LLM) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                               │
┌─────────────────┐    ┌─────────────────┐    │
│   Researcher    │◀───│   Formatted     │◀───┤
│   Natural Query │    │   Response      │    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                               │
                                         ┌─────────────────┐
                                         │   PostgreSQL    │
                                         │   Database      │
                                         └─────────────────┘
```

### **Current Pipeline (Text-to-SQL):**
1. User asks question in Telegram
2. LLM converts question to SQL using RAG prompts
3. SQL executes against PostgreSQL
4. Results formatted and returned

**Example Query Flow:**
- ❓ "Сколько связей у гена TP53?"
- 🤖 Generated SQL: `SELECT degree_layout FROM N WHERE display_name = 'TP53';`
- 📊 Result: `[(12,)]`
- 💬 Response: "Ген TP53 имеет 12 связей в сети."

---

## 🔧 **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | GigaChat3-10B-A1.8B (local via LM Studio) | Query interpretation & SQL generation |
| **Database** | PostgreSQL + psycopg2 | Structured gene data storage |
| **Bot Framework** | Telebot (Python) | Telegram interface |
| **Vector Search** | *Planned: pgvector + SentenceTransformers* | Semantic search |
| **Development** | Python 3.10, PyCharm | Core implementation |

---

## 🚨 **Current Limitations**

### **1. Weak Local LLM**
- GigaChat has limited parameters (10B)
- Poor SQL generation for complex queries
- Not fine-tuned for biological terminology

### **2. No Semantic Understanding**
- Only exact string matching in SQL queries
- Can't find "tumor suppressor gene" when searching for TP53
- Misses connections based on function rather than name

### **3. Rigid Query Structure**
- Limited to predefined SQL schema
- Cannot discover implicit relationships
- No similarity-based recommendations

---

## 🎯 **Planned Enhancement: Vector Database Integration**

### **Problem Vector Search Solves:**
- ✅ Semantic similarity: "Find genes related to DNA repair" → ERCC1, XPA, BRCA1
- ✅ Typos and synonyms: "TP35" → TP53
- ✅ Functional grouping: "Telomere maintenance genes" → TERF1, TERF2, POT1

### **Implementation Plan:**

#### **Phase 1: Embedding Generation**
```python
# Generate embeddings for gene descriptions
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Local, 80MB
text = f"Gene {gene_name}. Family: {family}. Description: {description}"
embedding = model.encode(text)  # 384-dimensional vector
```

#### **Phase 2: Database Extension**
```sql
-- Add vector support to PostgreSQL
CREATE EXTENSION vector;
ALTER TABLE N ADD COLUMN embedding vector(384);
CREATE INDEX ON N USING ivfflat (embedding vector_cosine_ops);
```

#### **Phase 3: Hybrid Search Pipeline**
```
NEW WORKFLOW:
1. User Question → "Find DNA repair genes with many connections"
2. Generate question embedding
3. Vector Search → Find similar genes by description
4. SQL Filter → Filter by degree_layout > threshold
5. LLM Synthesis → Generate natural language response
```

#### **Phase 4: Enhanced RAG Prompt**
```python
NEW_SYSTEM_PROMPT = """
You analyze genetic networks. First, here are semantically relevant genes:
{vector_search_results}

Now, use SQL to filter/sort these genes as needed.
Focus on: {user_question}
"""
```

---

## 📈 **Expected Outcomes**

### **Before vs After Comparison:**

| Aspect | Current (SQL-only) | Future (Hybrid Search) |
|--------|-------------------|------------------------|
| **"Find tumor suppressors"** | Returns nothing | Returns TP53, CDKN2A, BRCA1 |
| **Query Flexibility** | Exact names only | Natural language, typos OK |
| **Discovery Potential** | Low (exact matches) | High (semantic similarity) |
| **Researcher Experience** | Requires precise terminology | Conversational, intuitive |

### **Quantitative Metrics to Track:**
- Query success rate improvement
- Reduction in "no results found" responses
- Time to find relevant genes
- User satisfaction scores

---

## 🗓️ **Development Roadmap**

### **Week 1-2: Foundation**
- [x] Existing code analysis (`giga_gen.py`)
- [x] Database schema understanding
- [ ] pgvector installation and testing
- [ ] SentenceTransformers local model setup

### **Week 3-4: Implementation**
- [ ] Embedding generation script
- [ ] Database migration (add vector columns)
- [ ] Hybrid search prototype
- [ ] Updated RAG prompts

### **Week 5-6: Integration & Testing**
- [ ] Integrate vector search into main bot
- [ ] A/B testing: SQL-only vs Hybrid
- [ ] Performance optimization
- [ ] Documentation

---

## 🔬 **Research Context**

This project addresses key challenges in **systems biology** and **gerontology**:
- **Big Data Gap:** Exponential growth of biomedical data vs limited analysis tools
- **Expert-AI Barrier:** Biologists without programming skills can't access network analysis
- **Semantic Disconnect:** Current tools miss functional relationships between genes
- **Data Sovereignty:** Local deployment ensures bioethical compliance (Helsinki Declaration)

**Key Insight from Thesis:** "Integration of graph analysis and vector semantic search under local LLM control creates an interface capable of revealing implicit functional relationships in aging mechanisms."

---

## 🎓 **Team & Resources**

### **Core Team:**
- **David Ozerov** - System architecture, LLM integration
- **Sergey Barabanov** - Vector database implementation (current focus)

### **Files Provided:**
```
├── giga_gen.py              # Main bot implementation
├── N_table_filtered.csv     # Genes/nodes data
├── E_table_filtered.csv     # Interactions/edges data
└── Озеров_полный_тезис.docx # Research thesis (context)
```

### **Immediate Next Steps:**
1. **Sergey:** Install pgvector, test embedding generation
2. **David:** Prepare test queries for comparison
3. **Both:** Design hybrid search API interface

---

## 💡 **Key Technical Decisions**

1. **Local-First Approach:** All components (LLM, embeddings) run locally for data privacy
2. **PostgreSQL + pgvector:** Avoids complexity of separate vector DB (Weaviate, Pinecone)
3. **SentenceTransformers:** Lightweight, specialized for semantic similarity (vs OpenAI embeddings)
4. **Gradual Integration:** Maintain existing SQL functionality while adding vector search

---

## 📚 **Learning Points**

For Sergey to master:
1. **Embeddings Theory:** How text converts to vectors, cosine similarity
2. **Vector Databases:** Nearest neighbor search, indexing strategies
3. **Hybrid Search:** Combining semantic + structured filtering
4. **RAG Enhancement:** Context enrichment with search results

---

## 🎯 **Success Criteria**

The enhancement will be successful when:
1. Users can find genes by function, not just exact names
2. Query success rate increases by ≥40%
3. System suggests relevant genes even with vague queries
4. All processing remains local (no external API calls)

---

**Project Status:** ✅ Core Text-to-SQL implemented | 🔄 Vector integration in progress

*"Transforming genetic networks from data archives into interactive knowledge models"*
