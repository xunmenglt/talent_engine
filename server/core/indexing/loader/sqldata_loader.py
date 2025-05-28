# -*- coding:UTF-8 -*-
import json
import os
import re
from typing import Iterator, List,Optional,Literal
from dataclasses import dataclass,field,asdict
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
import tqdm
from core.text2sql.base import SQLExampleData,SQLExampleDataMetadata,DBSchema
from database.connector.client import sql_client
from core.text2sql.utils import sql2skeleton,question2skeleton
from core.llm.utils import get_default_llm
from utils.thread import xthread,as_completed

class CustomizedSQLDataLoader(BaseLoader):
    def __init__(self,file_path:str,encoding:str="utf-8",is_create_question_skeleton=True,is_create_query_skeleton=True,**kwargs):
        self.file_path=file_path
        self.encoding=encoding
        self.is_create_question_skeleton=is_create_question_skeleton
        self.is_create_query_skeleton=is_create_query_skeleton
        self.verify_prams()
        self._init_db_schema()
        
    
    def _init_db_schema(self):
        schema_info=sql_client.get_schema_info()
        table_names_original=[table.table_name for table in schema_info]
        column_names_original=[]
        index=0
        for table in schema_info:
            for column_info in table.columns:
                column_names_original.append((index,column_info[0]))
                index+=1
        self.db_schema=DBSchema(table_names_original=table_names_original,column_names_original=column_names_original)
    
    def verify_prams(self):
        if not os.path.exists(self.file_path):
            raise ValueError(f"文件路径不存在: {self.file_path}")
        # 获取文件后缀
        suffix = os.path.splitext(self.file_path)[1]
        if suffix != ".sqldata":
            raise ValueError(f"文件格式错误: {suffix}, 应该为sqldata")
        
    def create_question_skeleton(self,question:str)->str:
        if not self.is_create_question_skeleton:
            return question
        llm=get_default_llm()
        masked_question=question2skeleton(question,sql_client.get_markdown_create_table_schema(),llm)
        return masked_question
    
    def create_query_skeleton(self,query:str)->str:
        if not self.is_create_query_skeleton:
            return query
        query=sql2skeleton(query,self.db_schema.to_dict())
        return query
        
    def create_skeleton(self,sql_data:SQLExampleData):
        sql_data.question_skeleton=self.create_question_skeleton(sql_data.question)
        sql_data.query_skeleton=self.create_query_skeleton(sql_data.query)
    def load(self) -> List[Document]:
        documents=[]
        with open(self.file_path,'r',encoding=self.encoding) as fp:
            print("正在加载sqldata文件...")
            contents=fp.readlines()
            def process_content(content):
                json_data=json.loads(content)
                sql_data=SQLExampleData.from_dict(json_data)
                self.create_skeleton(sql_data)
                query_meta_data=SQLExampleDataMetadata(file_path=self.file_path,sql_data=sql_data,embedding_field="query")
                question_meta_data=SQLExampleDataMetadata(file_path=self.file_path,sql_data=sql_data,embedding_field="question")
                # documents.append(
                #     Document(page_content=sql_data.query_skeleton,metadata=query_meta_data.to_dict())
                # )
                documents.append(
                    Document(page_content=sql_data.question_skeleton,metadata=question_meta_data.to_dict())
                )
            # 构建并发任务
            future_list = []
            with xthread(worker_num=10) as pool:
                for content in contents:
                    future_list.append(pool.submit(process_content, content))
            pd=tqdm.tqdm(total=len(future_list),desc="sqldata数据处理中")
            for future in as_completed(future_list):
                pd.update(1)               
        return documents


    def lazy_load(self) -> Iterator[Document]:
        with open(self.file_path, 'r', encoding=self.encoding) as fp:
            print("正在懒加载 sqldata 文件...")
            for line in fp:
                if not line.strip():
                    continue
                try:
                    json_data = json.loads(line)
                    sql_data = SQLExampleData(**json_data)
                    self.create_skeleton(sql_data)

                    # 构建元数据对象
                    query_meta = SQLExampleDataMetadata(file_path=self.file_path, sql_data=sql_data, embedding_field="query")
                    question_meta = SQLExampleDataMetadata(file_path=self.file_path, sql_data=sql_data, embedding_field="question")

                    # yield query skeleton 文档
                    yield Document(page_content=sql_data.query_skeleton or sql_data.query, metadata=query_meta.to_dict())

                    # yield question skeleton 文档
                    yield Document(page_content=sql_data.question_skeleton or sql_data.question, metadata=question_meta.to_dict())

                except json.JSONDecodeError as e:
                    print(f"[跳过无效行] JSON 解码失败: {e}")
