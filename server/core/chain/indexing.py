from dataclasses import dataclass
import os
import uuid
from typing import List, Union, Tuple, Dict

from langchain_core.documents import Document


from utils.thread import run_in_thread_pool
from configs import logger,nltk

from core.chain.base import BaseIndexingChain
from core.vectorstore.base import VectorStoreBase
from core.knowledge_base.utils import KnowledgeFile


@dataclass
class IndexingSqlDataChain(BaseIndexingChain):

    vectorstore: VectorStoreBase

    def load(self,
             file: KnowledgeFile,
             loader: None):
        """
        加载文件内容
        :param file:
        :param loader: 配置加载器，默认根据文件后缀名进行路由，也可指定
        :return:
        """
        if loader is None:
            loader_class = file.document_loader
        else:
            loader_class = loader
        file_path = file.filename if os.path.exists(file.filename) else file.filepath
        docs = loader_class(file_path).load()
        return docs

    def split(self,
              docs: List[Document],
              **kwargs):
        return docs

    def file2chunks(self, file, **kwargs) -> Tuple[bool, Tuple[KnowledgeFile, List[Document]]]:
        try:
            docs = self.load(file=file, loader=None)
            chunks = self.split(docs=docs, splitter=file.text_splitter)
            return True, (file, chunks)
        except Exception as e:
            msg = f"从文件 {file.filename} 加载文档时出错：{e}"
            logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
            return False, (file, msg)

    def store(self,
              file: KnowledgeFile,
              chunks: List[Document]):

        doc_infos = self.vectorstore.update_doc(file=file,
                                                docs=chunks)
        if doc_infos:
            return True
        return False

    def chain(self,
              files: List[Union[KnowledgeFile, Tuple[str, str], Dict]], ):
        """
        利用多线程批量将磁盘文件转化成langchain Document，并存储到向量数据库.
        :param files:
        :return: status, (kb_name, file_name, docs | error)
        """
        failed_files = {}
        kwargs_list = []
        for i, file in enumerate(files):
            kwargs = {"file": file}
            kwargs_list.append(kwargs)
        for status, result in run_in_thread_pool(func=self.file2chunks, params=kwargs_list):
            if status:
                file, chunks = result
                chunks = chunks
                self.store(file, chunks)
            else:
                file, error = result
                failed_files[file.filename] = error
        return failed_files




