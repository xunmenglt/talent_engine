import asyncio
import json
from asyncio import Queue
from typing import Any, AsyncIterator,Union,Optional,List
from core.text2sql.base import SQLExampleDataMetadata,SQLExampleData
from enum import Enum
from dataclasses import dataclass,field
from typing import Any

from enum import Enum

class MessageType(Enum):
    ERROR = -2
    END = -1
    START = 0
    PARSING_USER_QUERY = 1
    PLAN_FORMULATION = 2
    SIMILAR_QUESTION_RETRIEVAL = 3
    PREGENERATED_SQL = 4
    SQL_SIMILARITY_MATCH = 5
    SQL_GENERATED_BY_MODEL = 6
    SQL_VALIDATION = 7
    SQL_REWRITING = 8
    SQL_EXECUTION_RESULT = 9
    FINAL_MODEL_ANSWER = 10
    TIP = 11
    QUESTION_SKELETON = 12

    def description(self) -> str:
        return {
            -1: "程序结束消息",
            -2: "异常信息",
            0: "程序开始消息",
            1: "问题解析",
            2: "计划制定",
            3: "相似问题检索",
            4: "预生成SQL语句结果",
            5: "SQL相似度匹配结果",
            6: "真实SQL构建结果",
            7: "SQL校验",
            8: "SQL重写",
            9: "SQL执行结果",
            10: "最终模型回答结果",
            11: "提示消息",
            12: "问题骨架"
        }[self.value]


@dataclass
class MessageContent:
    def to_dict(self) -> dict:
        raise NotImplementedError


@dataclass
class Message:
    id: str
    type: MessageType
    content: Optional[Union[str, MessageContent]] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "content": self.content if (isinstance(self.content, str) or self.content is None) else self.content.to_dict(),
        }


@dataclass
class QuestionItemMessage(Message):
    question_index: int = -1


@dataclass
class StartMessage(Message):
    type: MessageType = field(default=MessageType.START)
    content: Optional[Union[str, MessageContent]] = None


@dataclass
class EndMessage(Message):
    type: MessageType = field(default=MessageType.END)
    content: Optional[Union[str, MessageContent]] = None


@dataclass
class TipMessage(Message):
    type: MessageType = field(default=MessageType.TIP)
    content: str = ""


@dataclass
class ErrorMessage(Message):
    type: MessageType = field(default=MessageType.ERROR)
    content: str = ""


@dataclass
class QuestionParsingMessage(Message):
    type: MessageType = field(default=MessageType.PARSING_USER_QUERY)
    content: Optional[Union[str, MessageContent]] = None


@dataclass
class PlanFormulationMessage(QuestionItemMessage):
    @dataclass
    class PlanFormationContent(MessageContent):
        plan_list: List[str]

        def to_dict(self) -> dict:
            return {"plan_list": self.plan_list}

    type: MessageType = field(default=MessageType.PLAN_FORMULATION)
    content: PlanFormationContent = None


@dataclass
class SimilarQuestionRetrievalMessage(QuestionItemMessage):
    @dataclass
    class SimilarQuestionRetrievalContent(MessageContent):
        similar_docs: List

        def to_dict(self) -> dict:
            return {"similar_docs": [doc.to_dict() for doc in self.similar_docs]}

    type: MessageType = field(default=MessageType.SIMILAR_QUESTION_RETRIEVAL)
    content: SimilarQuestionRetrievalContent = None


@dataclass
class PreGeneratedSqlMessage(QuestionItemMessage):
    @dataclass
    class PreGeneratedSqlContent(MessageContent):
        sql_data: any

        def to_dict(self) -> dict:
            return {"sql": self.sql_data.to_dict()}

    type: MessageType = field(default=MessageType.PREGENERATED_SQL)
    content: PreGeneratedSqlContent = None


@dataclass
class SqlSimilarityMatchMessage(QuestionItemMessage):
    @dataclass
    class SqlSimilarityMatchContent(MessageContent):
        similar_docs: List

        def to_dict(self) -> dict:
            return {"similar_docs": [doc.to_dict() for doc in self.similar_docs]}

    type: MessageType = field(default=MessageType.SQL_SIMILARITY_MATCH)
    content: SqlSimilarityMatchContent = None


@dataclass
class QuestionSkeletonMessage(QuestionItemMessage):
    @dataclass
    class QuestionSkeletonContent(MessageContent):
        question_skeleton: str

        def to_dict(self) -> dict:
            return {"question_skeleton": self.question_skeleton}

    type: MessageType = field(default=MessageType.QUESTION_SKELETON)
    content: QuestionSkeletonContent = None


@dataclass
class RealSqlBuildMessage(QuestionItemMessage):
    @dataclass
    class RealSqlBuildContent(MessageContent):
        sql_data: any

        def to_dict(self) -> dict:
            return {"sql": self.sql_data.to_dict()}

    type: MessageType = field(default=MessageType.SQL_GENERATED_BY_MODEL)
    content: RealSqlBuildContent = None


@dataclass
class SqlExecutionResultMessage(QuestionItemMessage):
    @dataclass
    class SqlExecutionResultContent(MessageContent):
        sql: str
        exec_res: str

        def to_dict(self) -> dict:
            return {"sql": self.sql, "exec_res": self.exec_res}

    type: MessageType = field(default=MessageType.SQL_EXECUTION_RESULT)
    content: SqlExecutionResultContent = None


@dataclass
class FinalModelAnswerMessage(Message):
    @dataclass
    class FinalModelAnswerContent(MessageContent):
        final_answer: str
        chunk: str

        def to_dict(self) -> dict:
            return {"final_answer": self.final_answer, "chunk": self.chunk}

    type: MessageType = field(default=MessageType.FINAL_MODEL_ANSWER)
    content: FinalModelAnswerContent = None

class EndOfStream:
    """专用结束信号对象"""
    pass


class AsyncMessageStream:
    def __init__(self):
        self.queue: Queue = Queue()
        self._closed: bool = False
        self._eos = EndOfStream()

    async def put(self, item: Any):
        """
        向队列中放入一个消息对象。
        如果流已终止，则抛出异常。
        """
        if self._closed:
            raise RuntimeError("Cannot put into a closed AsyncQueueStream")
        await self.queue.put(item)

    async def end(self):
        """
        结束当前队列流，触发消费者停止。
        """
        if not self._closed:
            self._closed = True
            await self.queue.put(self._eos)

    def __aiter__(self) -> AsyncIterator[Any]:
        """
        支持 async for 消费消息
        """
        return self

    async def __anext__(self) -> Any:
        """
        消费队列中的下一个消息
        """
        item = await self.queue.get()
        if isinstance(item, EndOfStream):
            raise StopAsyncIteration
        return item
