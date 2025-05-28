from fastapi import FastAPI
import uvicorn
from server.utils import BaseResponse, ListResponse
from server.knowledge import (
    create_knowledge_base,
    delete_knowledge_base,
    clear_knowledge_base,
    upload_docs,
)

from server.chat import sql_chat,sql_chat_bf

VERSION = "v1.0"


def create_app(run_mode: str = None):
    app = FastAPI(
        title="Talent Engine API Server",
        version=VERSION
    )
    mount_app_routes(app, run_mode=run_mode)
    return app


def mount_app_routes(app: FastAPI, run_mode: str = None):

    # 知识库相关
    app.post("/knowledge_base/create_knowledge_base",
             tags=["Knowledge Base Management"],
             response_model=BaseResponse,
             summary="创建知识库"
             )(create_knowledge_base)
    app.post("/knowledge_base/delete_knowledge_base",
             tags=["Knowledge Base Management"],
             response_model=BaseResponse,
             summary="删除知识库"
             )(delete_knowledge_base)
    app.post("/knowledge_base/clear_knowledge_base",
             tags=["Knowledge Base Management"],
             response_model=BaseResponse,
             summary="清空知识库"
             )(clear_knowledge_base)
    app.post("/knowledge_base/upload_docs",
             tags=["Knowledge Base Management"],
             response_model=BaseResponse,
             summary="上传文件到知识库，并/或进行向量化"
             )(upload_docs)

    # 对话接口
    app.post("/chat/sql_chat",
             tags=["Chat"],
             summary="数据库对话对话")(sql_chat)
    
    app.post("/chat/sql_chat_bf",
            tags=["Chat"],
            summary="数据库对话对话")(sql_chat_bf)


def run_api(host, port, **kwargs):
    app = create_app()
    if kwargs.get("ssl_keyfile") and kwargs.get("ssl_certfile"):
        uvicorn.run(app,
                    host=host,
                    port=port,
                    ssl_keyfile=kwargs.get("ssl_keyfile"),
                    ssl_certfile=kwargs.get("ssl_certfile"),
                    )
    else:
        uvicorn.run(app,
                    host=host,
                    port=port)
