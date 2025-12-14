from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from services.embed_service import embedder
from services.kb_service import get_collection
from utils.logger import log_info


def get_index():
    collection = get_collection()  
    vector_store = ChromaVectorStore(collection)

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embedder
    )


def index_document(doc_id, content, metadata):
    doc = Document(
        doc_id=doc_id,
        text=content,
        metadata=metadata
    )

    collection = get_collection()
    vector_store = ChromaVectorStore(collection)
    
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    VectorStoreIndex.from_documents(
        [doc],
        embed_model=embedder,
        storage_context=storage_context
    )
