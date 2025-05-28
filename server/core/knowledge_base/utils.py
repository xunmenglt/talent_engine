import os
from pathlib import Path
from configs import settings
from core.indexing.loader import LOADER_MAPPING
from core.indexing.loader.utils import get_loader


def get_kb_path(knowledge_base_name: str):
    kb_root_path=settings.knowledge_base.base_storage_path
    if not os.path.isabs(kb_root_path):
        kb_root_path=os.path.join(os.getcwd(),kb_root_path)
    if not os.path.exists(kb_root_path):
        os.makedirs(kb_root_path,exist_ok=True)
    path=os.path.join(kb_root_path,knowledge_base_name)
    if not os.path.exists(path):
        os.makedirs(path,exist_ok=True)
    return path

def get_doc_path(knowledge_base_name: str):
    return os.path.join(get_kb_path(knowledge_base_name), "content")


def get_file_path(knowledge_base_name: str, doc_name: str):
    return os.path.join(get_doc_path(knowledge_base_name), doc_name)


class KnowledgeFile:
    def __init__(
            self,
            filename: str,
            knowledge_base_name: str,
    ):
        self.kb_name = knowledge_base_name
        self.filename = str(Path(filename).as_posix())
        self.ext = os.path.splitext(filename)[-1].lower()
        self.filepath = filename if os.path.exists(filename) else get_file_path(knowledge_base_name, filename)
        self.document_loader = self.get_document_loader()
        self.text_splitter = self.get_splitter()

    def get_document_loader(self):
        """根据文件名后缀自动选择Loader"""
        loader_name = ""
        for loader_cls, extensions in LOADER_MAPPING.items():
            if self.ext in extensions:
                loader_name = loader_cls; break
        return get_loader(loader_name)

    def get_splitter(self):
        # TODO: 待实现
        return None

    def file_exist(self):
        return os.path.isfile(self.filepath)

    def get_mtime(self):
        return os.path.getmtime(self.filepath)

    def get_size(self):
        return os.path.getsize(self.filepath)