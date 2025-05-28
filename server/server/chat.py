import asyncio
import os
from fastapi import Body
from typing import List, Tuple
from sse_starlette.sse import EventSourceResponse,ServerSentEvent
import json
from server.knowledge import KBServiceFactory
from server.utils import BaseResponse
from core.chain.sqlchat import SQLChatChain
from core.vectorstore.utils import get_default_vectorstore
from core.embedder.utils import  get_default_embedding_model
from core.llm.utils import get_default_llm
from configs import settings
from database.connector.client import sql_client
from database.utils import mysql_safe_convert
from configs import logger


async def sql_chat(
                query: str = Body(..., description="用户输入", examples=["找出既会钢琴演奏又擅长围棋的员工"]),
                history: List[Tuple[str, str]] = Body(
                    [],
                    description="历史对话",
                    examples=[[("user", "哪些员工同时拥有日语能力和项目管理认证？"),
                                ("assistant", "赵敏")]]
                ),
                question_score_threshold: float = Body(0.0, description="问题相似度阈值"),
                sql_score_threshold: float = Body(0.85, description="sql相似度阈值"),
                topk: int = Body(5, description="检索召回的相似度文档数量"),
                is_planing: bool = Body(False, description="是否是计划任务"),
                sql_verfy_times: int = Body(2, description="sql验证次数")
            ):
    kb = KBServiceFactory.get_service()
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {settings.knowledge_base.name}")
    vector_store = get_default_vectorstore()
    # 知识库召回上下文
    chat_chain = SQLChatChain(
        vectorstore=vector_store,
        llm=get_default_llm(),
        sql_client=sql_client,
        retrievers=[],
        top_k=topk,
        question_score_threshold=question_score_threshold,
        sql_score_threshold=sql_score_threshold,
        is_split_question=is_planing,
        sql_verfy_times=sql_verfy_times
    )
    # 启动 achain 为后台任务
    task=asyncio.create_task(chat_chain.achain(question=query))
    async def iterator():
        message_stream=chat_chain.message_stream
        async for message in message_stream:
            result=message.to_dict()
            logger.info(f"[MESSAGE]:\n{json.dumps(result,ensure_ascii=False,indent=4,default=mysql_safe_convert)}")
            yield ServerSentEvent(data=json.dumps(result, ensure_ascii=False,default=mysql_safe_convert))
    # 注册断开连接时的钩子
    async def close_connection():
        logger.info("Client disconnected. Cancelling achain task...")
        task.cancel()
    return EventSourceResponse(iterator(),background=close_connection)



async def sql_chat_bf(
                query: str = Body(..., description="用户输入", examples=["找出既会钢琴演奏又擅长围棋的员工"]),
                history: List[Tuple[str, str]] = Body(
                    [],
                    description="历史对话",
                    examples=[[("user", "哪些员工同时拥有日语能力和项目管理认证？"),
                                ("assistant", "赵敏")]]
                ),
                question_score_threshold: float = Body(0.0, description="问题相似度阈值"),
                sql_score_threshold: float = Body(0.85, description="sql相似度阈值"),
                topk: int = Body(5, description="检索召回的相似度文档数量"),
                is_planing: bool = Body(False, description="是否是计划任务"),
                sql_verfy_times: int = Body(2, description="sql验证次数")
            ):

    async def iterator():
        with open(os.path.join(os.getcwd(), "test.txt"), "r", encoding="utf-8") as f:
            lines=f.readlines()
        for line in lines:
            if line and line.strip().startswith("data: "):
                data_str = line.strip()[6:]  # 去掉前缀 'data: '
                # 正确方式：直接用 json.loads，而不是 eval
                result = json.loads(data_str)
            logger.info(f"[MESSAGE]:{json.dumps(result,ensure_ascii=False,indent=4,default=mysql_safe_convert)}")
            yield ServerSentEvent(data=json.dumps(result, ensure_ascii=False,default=mysql_safe_convert))
    # 注册断开连接时的钩子
    async def close_connection():
        logger.info("Client disconnected. Cancelling achain task...")
    return EventSourceResponse(iterator(),background=close_connection)