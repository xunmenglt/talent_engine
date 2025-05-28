from functools import lru_cache
import importlib
from configs import logger


from langchain_community.document_loaders import UnstructuredFileLoader


def get_loader(name):
    try:
        if "Customized" in name:
            customized_document_loaders_module = importlib.import_module("core.indexing.loader")
            return getattr(customized_document_loaders_module, name)
        else:
            document_loaders_module = importlib.import_module("langchain.document_loaders")
            return getattr(document_loaders_module, name)
    except Exception as e:
        return UnstructuredFileLoader



