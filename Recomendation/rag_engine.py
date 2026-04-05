"""
rag_engine.py — Retrieval-Augmented Generation with Pinecone

Embeds career knowledge documents into Pinecone vector DB.
At query time, retrieves the most relevant chunks to ground LLM responses.

Setup:
    pip install pinecone-client sentence-transformers

Environment variables:
    PINECONE_API_KEY=your-key-here
    PINECONE_INDEX=career-counsellor
"""

import os
import sys
import json
import hashlib
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ── Try importing optional dependencies ───────────────────────────────
try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class RetrievedChunk:
    id: str
    text: str
    category: str
    domain: str
    score: float


class RAGEngine:
    """
    Pinecone-backed RAG engine for career counselling knowledge retrieval.

    Flow:
        1. ingest() — embed all knowledge base docs and upsert into Pinecone
        2. retrieve() — embed a query and fetch top-k similar chunks
        3. format_context() — format chunks into LLM prompt context
    """

    INDEX_NAME = "career-counsellor"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # 384-dim, fast, accurate enough
    EMBEDDING_DIM = 384

    def __init__(self):
        self.pinecone_client = None
        self.index = None
        self.embedder = None
        self._fallback_docs = []   # in-memory fallback if Pinecone unavailable
        self._initialized = False

    def initialize(self) -> bool:
        """Connect to Pinecone and load embedding model. Returns True if successful."""
        # ── Load embedding model ──────────────────────────────────────
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print("📦 Loading sentence-transformers embedding model...")
            self.embedder = SentenceTransformer(self.EMBEDDING_MODEL)
            print(f"   ✅ Embedder ready: {self.EMBEDDING_MODEL}")
        else:
            print("⚠️  sentence-transformers not installed. Using fallback keyword retrieval.")

        # ── Connect to Pinecone ───────────────────────────────────────
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("⚠️  PINECONE_API_KEY not set. Using in-memory fallback retrieval.")
            self._load_fallback()
            self._initialized = True
            return False

        if not PINECONE_AVAILABLE:
            print("⚠️  pinecone-client not installed. Using fallback.")
            self._load_fallback()
            self._initialized = True
            return False

        try:
            self.pinecone_client = Pinecone(api_key=api_key)

            # Create index if it doesn't exist
            existing = [idx.name for idx in self.pinecone_client.list_indexes()]
            if self.INDEX_NAME not in existing:
                print(f"📝 Creating Pinecone index: {self.INDEX_NAME}")
                self.pinecone_client.create_index(
                    name=self.INDEX_NAME,
                    dimension=self.EMBEDDING_DIM,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                print("   ✅ Index created")

            self.index = self.pinecone_client.Index(self.INDEX_NAME)
            stats = self.index.describe_index_stats()
            print(f"   ✅ Pinecone connected | Vectors: {stats.total_vector_count}")
            self._initialized = True
            return True

        except Exception as e:
            print(f"⚠️  Pinecone connection failed: {e}")
            print("   Falling back to in-memory retrieval.")
            self._load_fallback()
            self._initialized = True
            return False

    def _load_fallback(self):
        """Load knowledge base into memory for keyword-based fallback retrieval."""
        try:
            from Recomendation.data.rag_knowledge_base import RAG_DOCUMENTS
            self._fallback_docs = RAG_DOCUMENTS
            print(f"   📚 Loaded {len(self._fallback_docs)} docs into memory fallback")
        except ImportError:
            print("   ⚠️  Could not load RAG_DOCUMENTS")
            self._fallback_docs = []

    def ingest(self, documents: Optional[List[Dict]] = None) -> int:
        """
        Embed and upsert all knowledge base documents into Pinecone.
        Returns number of documents ingested.
        """
        if documents is None:
            try:
                from Recomendation.data.rag_knowledge_base import RAG_DOCUMENTS
                documents = RAG_DOCUMENTS
            except ImportError:
                print("❌ Could not import RAG_DOCUMENTS")
                return 0

        if not self.index or not self.embedder:
            print("⚠️  Cannot ingest — Pinecone or embedder not available")
            return 0

        print(f"📥 Ingesting {len(documents)} documents into Pinecone...")
        vectors = []

        for doc in documents:
            text = doc["text"]
            embedding = self.embedder.encode(text).tolist()
            vectors.append({
                "id": doc["id"],
                "values": embedding,
                "metadata": {
                    "text": text[:1000],   # Pinecone metadata limit
                    "category": doc.get("category", "general"),
                    "domain": doc.get("domain", "all"),
                }
            })

        # Batch upsert (Pinecone recommends batches of 100)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
            print(f"   Upserted batch {i // batch_size + 1}/{(len(vectors) - 1) // batch_size + 1}")

        print(f"✅ Ingested {len(documents)} documents")
        return len(documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        domain_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve top-k most relevant chunks for a given query.
        Falls back to keyword search if Pinecone unavailable.
        """
        if not self._initialized:
            self.initialize()

        # ── Pinecone retrieval ────────────────────────────────────────
        if self.index and self.embedder:
            return self._pinecone_retrieve(query, top_k, domain_filter)

        # ── Fallback: keyword retrieval ───────────────────────────────
        return self._keyword_retrieve(query, top_k, domain_filter)

    def _pinecone_retrieve(self, query: str, top_k: int, domain_filter: Optional[str]) -> List[RetrievedChunk]:
        """Vector similarity search via Pinecone."""
        query_embedding = self.embedder.encode(query).tolist()

        filter_dict = None
        if domain_filter:
            filter_dict = {
                "$or": [
                    {"domain": {"$eq": domain_filter}},
                    {"domain": {"$eq": "all"}}
                ]
            }

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )

        chunks = []
        for match in results.matches:
            chunks.append(RetrievedChunk(
                id=match.id,
                text=match.metadata.get("text", ""),
                category=match.metadata.get("category", "general"),
                domain=match.metadata.get("domain", "all"),
                score=match.score
            ))
        return chunks

    def _keyword_retrieve(self, query: str, top_k: int, domain_filter: Optional[str]) -> List[RetrievedChunk]:
        """Simple keyword overlap retrieval for fallback."""
        query_words = set(query.lower().split())
        scored = []

        for doc in self._fallback_docs:
            # Domain filter
            if domain_filter and doc.get("domain") not in [domain_filter, "all"]:
                continue

            doc_words = set(doc["text"].lower().split())
            overlap = len(query_words & doc_words)
            # Boost if domain matches
            if domain_filter and doc.get("domain") == domain_filter:
                overlap *= 2

            if overlap > 0:
                scored.append((overlap, doc))

        scored.sort(key=lambda x: x[0], reverse=True)

        chunks = []
        for score, doc in scored[:top_k]:
            chunks.append(RetrievedChunk(
                id=doc["id"],
                text=doc["text"],
                category=doc.get("category", "general"),
                domain=doc.get("domain", "all"),
                score=float(score) / max(1, len(query_words))
            ))
        return chunks

    def format_context(self, chunks: List[RetrievedChunk]) -> str:
        """Format retrieved chunks into a context string for the LLM prompt."""
        if not chunks:
            return "No specific knowledge retrieved — rely on general training."

        context_parts = ["RETRIEVED KNOWLEDGE BASE CONTEXT:"]
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"\n[Source {i} | Category: {chunk.category} | Domain: {chunk.domain} | Relevance: {chunk.score:.2f}]"
                f"\n{chunk.text}"
            )
        return "\n".join(context_parts)

    def get_stats(self) -> Dict:
        """Return index statistics."""
        if self.index:
            stats = self.index.describe_index_stats()
            return {
                "backend": "pinecone",
                "total_vectors": stats.total_vector_count,
                "index_name": self.INDEX_NAME,
                "embedding_model": self.EMBEDDING_MODEL
            }
        return {
            "backend": "in-memory fallback",
            "total_docs": len(self._fallback_docs),
            "embedding_model": "keyword-based"
        }