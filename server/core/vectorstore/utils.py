from functools import lru_cache

from configs import logger

from core.vectorstore.base import VectorStoreBase
from core.vectorstore import ChromaVectorStore


# @lru_cache
def get_vectorstore(knowledge_base_name,
                    vs_type,
                    embed_model) -> VectorStoreBase:
    """Get the vectorstore"""
    logger.info(f"Using {vs_type} as db to create vectorstore")
    if vs_type == "chroma":
        vectorstore = ChromaVectorStore(embedding_model=embed_model,
                                        collection_name=knowledge_base_name)
    else:
        raise ValueError(f"{vs_type} vector database is not supported")
    logger.info("Vector store created")
    return vectorstore


def get_default_vectorstore() -> VectorStoreBase:
    from configs import settings
    from core.embedder.utils import get_default_embedding_model
    embedding_model = get_default_embedding_model()
    vs_type=settings.vector_store.type
    kb_name=settings.knowledge_base.name
    return get_vectorstore(kb_name,
                           vs_type,
                           embedding_model)


# vector_store = get_vectorstore(settings.vector_store.name,
#                                settings.vector_store.type,
#                                embedding_model)


