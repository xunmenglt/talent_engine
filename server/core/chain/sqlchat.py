import asyncio
import uuid
from dataclasses import dataclass,field
from typing import (
    Union,
    List,
    Optional,
    Tuple,
    Any
)

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from core.chain.base import BaseRetrievalChain
from configs import logger,settings
from core.vectorstore.base import VectorStoreBase
from server.messages import (AsyncMessageStream,
                             Message,
                             StartMessage,
                             QuestionParsingMessage,
                             PlanFormulationMessage,
                             SimilarQuestionRetrievalMessage,
                             PreGeneratedSqlMessage,
                             SqlSimilarityMatchMessage,
                             QuestionSkeletonMessage,
                             TipMessage,
                             ErrorMessage,
                             RealSqlBuildMessage,
                             SqlExecutionResultMessage,
                             EndMessage,
                             FinalModelAnswerMessage
                            )
from langchain_core.language_models.chat_models import BaseChatModel
from database.connector.client import SQLDatabaseClient
from prompts.utils import plan_formulation,generate_question_skeletion,generate_sql_direct,generate_sql_by_example_data,answer_user_question_with_refernce
from core.text2sql.base import SQLExampleDataMetadata,SQLExampleData
from core.text2sql.utils import jaccard_similarity,sql2skeleton,question2skeleton


@dataclass
class SQLChatChain(BaseRetrievalChain):

    vectorstore: Optional[VectorStoreBase]
    llm: BaseChatModel
    sql_client: SQLDatabaseClient
    retrievers: List[BaseRetriever] = None
    top_k: int = 5
    question_score_threshold: Union[None, float] = 0.0
    sql_score_threshold: Union[None, float] = 0.85
    is_split_question: bool = False
    sql_verfy_times: int = 2
    message_stream:AsyncMessageStream=field(default_factory=AsyncMessageStream)
    uuid: str = field(default_factory=lambda: uuid.uuid4().hex)
    
    def post_retrieval(self, query: str, results: List[Document]):
        pass

    async def pre_retrieval(self, query: str):
        await self.put_message(QuestionParsingMessage(id=self.uuid))
        queries = []
        await self.put_message(TipMessage(id=self.uuid,content="开始制定计划"))
        if not self.is_split_question:
            queries.append(query)
        else:
            queries = await asyncio.to_thread(plan_formulation,self.sql_client.get_markdown_create_table_schema(),query,self.llm)
        await self.put_message(PlanFormulationMessage(id=self.uuid,content=PlanFormulationMessage.PlanFormationContent(plan_list=queries)))
        return queries

    async def retrieval(self, query: str) -> List[SQLExampleDataMetadata]:
        example_metadata_list=[]
        if self.vectorstore:
            docs = await asyncio.to_thread(self.vectorstore.search_docs,
                                            query,
                                            self.top_k,
                                            self.question_score_threshold)
            example_metadata_list=[SQLExampleDataMetadata.from_dict(doc[0].metadata) for doc in docs ]
        return example_metadata_list

    
    async def sql_skeleton_filter(self, example_sql_datas: List[SQLExampleDataMetadata], sql: str):
        sql_sekeleton=sql2skeleton(sql=sql,db_schema=self.sql_client.get_db_schema().to_dict())
        fileter_result=[(jaccard_similarity(sql_sekeleton,example_sql_data.sql_data.query_skeleton),example_sql_data) for example_sql_data in example_sql_datas ] 
        fileter_result.sort(key=lambda x:x[0],reverse=True)
        res=[]
        for score,fileter_item in fileter_result:
            if score>=self.sql_score_threshold:
                res.append(fileter_item)
        return res
    
    async def pre_create_sql(self, question: str)->SQLExampleData:
        res=await asyncio.to_thread(generate_sql_direct,
                                    self.sql_client.get_markdown_create_table_schema(),
                                    self.sql_client.get_markdown_table_example_data(),
                                    question,
                                    self.llm,
                                    self.sql_client,
                                    1,
                                    self.sql_verfy_times
                                    )
        return res
   
    async def put_message(self, message: Message):
        await self.message_stream.put(message)
        
    async def create_question_seketon(self, question: str):
        question_seketon=await asyncio.to_thread(question2skeleton,self.sql_client.get_markdown_create_table_schema(),question,self.llm)
        if not question_seketon:
            return question
        return question_seketon
    
    def create_input_output_from_sql_example_data(self,example_sql_datas: List[SQLExampleDataMetadata])->str:
        examples=[]
        for idx,example_sql_data in enumerate(example_sql_datas):
            example_str=f"- 样例{idx+1}\n-- 用户问题: {example_sql_data.sql_data.question}\n-- SQL语句: {example_sql_data.sql_data.query}"
            examples.append(example_str)
        if not examples:
            return "暂无相关样例数据"
        return "\n\n".join(examples)
    
    async def create_real_sql(self, question: str, example_sql_datas: List[SQLExampleDataMetadata])->SQLExampleData:
        sql_example_input_output=self.create_input_output_from_sql_example_data(example_sql_datas)
        res:SQLExampleData=await asyncio.to_thread(generate_sql_by_example_data,
                                self.sql_client.get_markdown_create_table_schema(),
                                self.sql_client.get_markdown_table_example_data(),
                                sql_example_input_output,
                                question,
                                self.llm,
                                self.sql_client,
                                1,
                                self.sql_verfy_times
                                )
        return res

    
    async def sql_check(self, sql: str)->Tuple[str,Any]:
        flag,res=await asyncio.to_thread(self.sql_client.execute_sql,sql)
        if flag:
            return sql,self.sql_client.sql_result_to_markdown(res)
        else:
            return sql,"SQL语句执行异常"
        
    async def model_reply(self, question: str, sql_exec_res_list: List[Tuple[str,str,str]]):
        reference_question_answers="\n\n".join([
            f"- 子问题{idx+1}: {sql_exec_res[0]}\n-- 子问题{idx+1}的SQL语句: {sql_exec_res[1]}\n-- 子问题{idx+1}的SQL语句执行结果: {sql_exec_res[2]}"
            for idx,sql_exec_res in enumerate(sql_exec_res_list)
        ])
        
        response_stream=answer_user_question_with_refernce(self.sql_client.get_markdown_create_table_schema(),
                                           question,
                                           reference_question_answers,
                                           llm=self.llm
        )
        answer=""
        async for response in response_stream:
            answer+=response
            await self.put_message(FinalModelAnswerMessage(id=self.uuid,
                                                           content=FinalModelAnswerMessage.FinalModelAnswerContent(
                                                               final_answer=answer,
                                                               chunk=response
                                                           )))
    
    async def achain(self, question: str):
        query=question
        await self.put_message(StartMessage(id=self.uuid))
        questions = await self.pre_retrieval(question)
        sql_exec_res_list=[]
        for idx, question in enumerate(questions):
            # 相似问题检索结果
            await self.put_message(TipMessage(id=self.uuid,content="问题骨架构建"))
            question_seketon=await self.create_question_seketon(question)
            await self.put_message(QuestionSkeletonMessage(id=self.uuid,
                                                     content=QuestionSkeletonMessage.QuestionSkeletonContent(question_skeleton=question_seketon),
                                                     question_index=idx))
            await self.put_message(TipMessage(id=self.uuid,content="相似问检索"))
            example_sql_datas = await self.retrieval(question_seketon)
            await self.put_message(SimilarQuestionRetrievalMessage(id=self.uuid,
                                                             content=SimilarQuestionRetrievalMessage.SimilarQuestionRetrievalContent(similar_docs=example_sql_datas),
                                                             question_index=idx))
            
            await self.put_message(TipMessage(id=self.uuid,content="预生成SQL"))
            # 预生成SQL语句为question
            sql_data= await self.pre_create_sql(question)
            if sql_data is None:
                await self.put_message(ErrorMessage(id=self.uuid,content="预生成SQL失败"))
                continue
            sql=sql_data.query
            await self.put_message(PreGeneratedSqlMessage(id=self.uuid,
                                                    content=PreGeneratedSqlMessage.PreGeneratedSqlContent(sql_data=sql_data),
                                                    question_index=idx))
            # SQL骨架相似度过滤
            await self.put_message(TipMessage(id=self.uuid,content="SQL骨架相似度过滤"))
            example_sql_datas= await self.sql_skeleton_filter(example_sql_datas, sql)
            await self.put_message(SqlSimilarityMatchMessage(id=self.uuid,
                                                       content=SqlSimilarityMatchMessage.SqlSimilarityMatchContent(similar_docs=example_sql_datas),
                                                       question_index=idx))
            # 模型构建真实SQL结果
            await self.put_message(TipMessage(id=self.uuid,content="真实SQL构建"))
            sql_example_data= await self.create_real_sql(question,example_sql_datas)
            if sql_example_data is None:
                await self.put_message(ErrorMessage(id=self.uuid,content="真实SQL构建失败"))
                continue
            else:
                await self.put_message(RealSqlBuildMessage(id=self.uuid,content=RealSqlBuildMessage.RealSqlBuildContent(sql_data=sql_example_data),question_index=idx))
            # sql校验，校验里面有重写
            await self.put_message(TipMessage(id=self.uuid,content="SQL语句校验"))
            sql,exec_res=await self.sql_check(sql)
            await self.put_message(SqlExecutionResultMessage(id=self.uuid,content=SqlExecutionResultMessage.SqlExecutionResultContent(sql=sql,exec_res=exec_res),question_index=idx))
            sql_exec_res_list.append((question,sql,exec_res))

        # 模型回复结果
        await self.model_reply(query, sql_exec_res_list)
        await self.put_message(EndMessage(id=self.uuid))
        # 对话结束
        await self.message_stream.end()





