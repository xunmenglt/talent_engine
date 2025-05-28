from functools import lru_cache
import importlib
from configs import logger

from core.retriever.reranker import Reranker


@lru_cache()
def get_reranker(model_name_or_path: str,
                 reranker_type: str):

    logger.info(f"Loading {model_name_or_path} as model reranker")
    if reranker_type == "rank":
        reranker = Reranker(model_name_or_path)

    return reranker