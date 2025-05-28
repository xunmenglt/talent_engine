import os
import urllib
from pydantic import Json
from typing import List
from langchain_core.documents import Document

from fastapi import File, Form, Body, UploadFile

from server.utils import BaseResponse
from configs import settings
from configs import logger
from core.knowledge_base.utils import get_file_path, KnowledgeFile
from core.vectorstore.utils import get_vectorstore
from core.embedder.utils import get_embedding_model
from utils.thread import run_in_thread_pool
from core.chain.indexing import IndexingSqlDataChain



def validate_vectorstore_name(name: str) -> bool:
    # 检查是否包含预期外的字符或路径攻击关键字
    if "../" in name:
        return False
    return True


class KBServiceFactory:
    @staticmethod
    def _get_service(kb_name: str,
                    vector_store_type: str):
        embedding_model=get_embedding_model(
            settings.embeddings.model_name_or_path,
            settings.embeddings.model_engine,
            settings.embeddings.base_url,
            settings.embeddings.api_key
        )
        return get_vectorstore(kb_name, vector_store_type, embedding_model)

    @staticmethod
    def get_service():
        """从db中查询知识库信息，知识库名称和向量数据库类型"""
        vs_type=settings.vector_store.type
        kb_name=settings.knowledge_base.name
        return KBServiceFactory._get_service(kb_name, vs_type)


def create_knowledge_base() -> BaseResponse:
    # Create selected knowledge base
    knowledge_base_name=settings.knowledge_base.name
    if not validate_vectorstore_name(settings.knowledge_base.name):
        return BaseResponse(code=403, msg="Don't attack me")

    if knowledge_base_name is None or knowledge_base_name.strip() == "":
        return BaseResponse(code=404, msg="知识库名称不能为空，请重新填写知识库名称")

    """step 1. 校验知识库是否已存在"""
    kb = KBServiceFactory.get_service()
    if kb is not None:
        return BaseResponse(code=404, msg=f"已存在同名知识库 {knowledge_base_name}")
    try:
        # TODO 创建成功后知识库信息添加到数据库
        pass
    except Exception as e:
        msg = f"创建知识库出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
        return BaseResponse(code=500, msg=msg)

    return BaseResponse(code=200, msg=f"已新增知识库 {knowledge_base_name}")

def delete_knowledge_base() -> BaseResponse:
    # Delete selected knowledge base
    knowledge_base_name=settings.knowledge_base.name
    if not validate_vectorstore_name(knowledge_base_name):
        return BaseResponse(code=403, msg="Don't attack me")
    knowledge_base_name = urllib.parse.unquote(knowledge_base_name)
    kb = KBServiceFactory.get_service()
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")
    else:
        vs = kb  # 这里的kb指的是向量数据库
    try:
        vs.drop_vectorstore()
        return BaseResponse(code=200, msg=f"成功删除知识库 {knowledge_base_name}")
    except Exception as e:
        msg = f"删除知识库时出现意外： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
        return BaseResponse(code=500, msg=msg)


def clear_knowledge_base() -> BaseResponse:
    # Delete selected knowledge base
    knowledge_base_name=settings.knowledge_base.name
    if not validate_vectorstore_name(knowledge_base_name):
        return BaseResponse(code=403, msg="Don't attack me")
    knowledge_base_name = urllib.parse.unquote(knowledge_base_name)
    kb = KBServiceFactory.get_service()

    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")
    else:
        vs = kb  # 这里的kb指的是向量数据库
    try:
        vs.clear_vectorstore()
        return BaseResponse(code=200, msg=f"成功清空知识库 {knowledge_base_name}")
    except Exception as e:
        msg = f"清空知识库时出现意外： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
        return BaseResponse(code=500, msg=msg)


def _save_files_in_thread(files: List[UploadFile],
                          knowledge_base_name: str,
                          override: bool):
    """
    通过多线程将上传的文件保存到对应知识库目录内。
    生成器返回保存结果：{"code":200, "msg": "xxx", "data": {"knowledge_base_name":"xxx", "file_name": "xxx"}}
    """

    def save_file(file: UploadFile,
                  knowledge_base_name: str,
                  override: bool) -> dict:
        '''
        保存单个文件。
        '''
        filename = file.filename
        data = {"knowledge_base_name": knowledge_base_name, "file_name": filename}
        file_path = get_file_path(knowledge_base_name=knowledge_base_name, doc_name=filename)
        try:
            file_content = file.file.read()  # 读取上传文件的内容
            if (os.path.isfile(file_path)
                    and not override
                    and os.path.getsize(file_path) == len(file_content)
            ):
                file_status = f"文件 {filename} 已存在。"
                logger.warning(file_status)
                return dict(code=404, msg=file_status, data=data)

            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "wb") as f:
                f.write(file_content)
            return dict(code=200, msg=f"成功上传文件 {filename}", data=data)
        except Exception as e:
            msg = f"{filename} 文件上传失败，报错信息为: {e}"
            logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
            return dict(code=500, msg=msg, data=data)

    params = [{"file": file, "knowledge_base_name": knowledge_base_name, "override": override} for file in files]
    for result in run_in_thread_pool(save_file, params=params):
        yield result



def upload_docs(
        files: List[UploadFile] = File(..., description="上传文件，支持多文件"),
        override: bool = Form(True, description="覆盖已有文件")
) -> BaseResponse:
    """
    API接口：上传文件，并/或向量化
    """
    knowledge_base_name=settings.knowledge_base.name
    if not validate_vectorstore_name(knowledge_base_name):
        return BaseResponse(code=403, msg="Don't attack me")

    kb = KBServiceFactory.get_service()
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")

    failed_files = {}
    file_names = []

    # 先将上传的文件保存到磁盘
    for result in _save_files_in_thread(files,
                                        knowledge_base_name=knowledge_base_name,
                                        override=override):
        filename = result["data"]["file_name"]
        if result["code"] != 200:
            failed_files[filename] = result["msg"]
        if filename not in file_names:
            file_names.append(filename)

    # 对保存的文件进行向量化
    result = update_docs(
        knowledge_base_name=knowledge_base_name,
        file_names=file_names,
    )
    failed_files.update(result.data["failed_files"])

    return BaseResponse(code=200, msg="文件上传与向量化完成", data={"failed_files": failed_files})


def update_docs(
        knowledge_base_name: str = Body(..., description="知识库名称", examples=["samples"]),
        file_names: List[str] = Body(..., description="文件名称，支持多文件", examples=[["file_name1", "text.txt"]]),
) -> BaseResponse:
    """
    更新知识库文档
    TODO: 支持用户上传自定义的结构化文档
    """
    if not validate_vectorstore_name(knowledge_base_name):
        return BaseResponse(code=403, msg="Don't attack me")

    kb = KBServiceFactory.get_service()
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")
    else:
        vs = kb

    failed_files = {}
    kb_files = []

    # 生成需要加载docs的文件列表
    for file_name in file_names:
        try:
            kb_files.append(KnowledgeFile(filename=file_name, knowledge_base_name=knowledge_base_name))
        except Exception as e:
            msg = f"加载文档 {file_name} 时出错：{e}"
            logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e)
            failed_files[file_name] = msg

    indexing_chain = IndexingSqlDataChain(vectorstore=vs)
    failed_files = indexing_chain.chain(kb_files)

    return BaseResponse(code=200, msg=f"更新文档完成", data={"failed_files": failed_files})



