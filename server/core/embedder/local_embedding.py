from typing import List
import torch

from langchain_core.embeddings import Embeddings

from langchain_community.embeddings import (
    HuggingFaceEmbeddings,
    HuggingFaceBgeEmbeddings
)

from configs import logger


class LocalEmbeddings(Embeddings):

    def __init__(self,
                 model_name_or_path: str,
                 model_engine: str = "huggingface"):
        self.model_name_or_path = model_name_or_path
        self.model_engine = model_engine

        self._init_embedding_model()

    def _init_embedding_model(self):
        model_kwargs = {"device": "cpu"}
        if torch.cuda.is_available():
            model_kwargs["device"] = "cuda"
        encode_kwargs = {"normalize_embeddings": True}

        logger.info(f"Using {self.model_engine} as model engine to load embeddings")
        if self.model_engine == "huggingface":
            func_class = HuggingFaceBgeEmbeddings if any(
                [key_word in self.model_name_or_path for key_word in ["bge", "Chuxin"]]) \
                else HuggingFaceEmbeddings
            hf_embeddings = func_class(
                model_name=self.model_name_or_path,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )
            self.embeddings = hf_embeddings
        else:
            pass

    def embed_documents(self, docs: List[str]):
        return self.embeddings.embed_documents(docs)

    def embed_query(self, query: str):
        return self.embeddings.embed_query(query)

