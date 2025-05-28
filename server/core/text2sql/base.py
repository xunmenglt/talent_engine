import json
from dataclasses import dataclass, field, asdict,fields
from typing import List, Optional, Tuple,Literal


@dataclass
class Question:
    text: str
    skeleton: Optional[str] = None  # 问题骨架，如“总共有多少_？”
    metadata: Optional[dict] = field(default_factory=dict)


@dataclass
class SQL:
    query: str
    skeleton: Optional[str] = None  # SQL骨架，如“SELECT count(*) FROM _”
    metadata: Optional[dict] = field(default_factory=dict)


@dataclass
class Sample:
    question: Question
    sql: SQL


@dataclass
class SQLExampleData:
    schamea:str # 数据库表结构
    question:str # 问题
    query:str # SQL语句
    tables:List[str] # 与问题相关的表名
    reference_question:Optional[str]=field(default=None) # 参考问题
    answer:Optional[str]=field(default=None) # 答案
    sql_exec_res:Optional[dict|str]=field(default=None)
    query_skeleton:Optional[str]=field(default=None) # SQL语句骨架
    question_skeleton:Optional[str]=field(default=None) # 答案骨架
    
    @staticmethod
    def from_dict(data: dict) -> "SQLExampleData":
        # 提取合法字段
        valid_fields = {f.name for f in fields(SQLExampleData)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return SQLExampleData(**filtered_data)
    
    def to_dict(self):
        return asdict(self)
    
@dataclass
class SQLExampleDataMetadata:
    file_path:str
    sql_data:SQLExampleData
    embedding_field:Literal["query","question"]=field(default="query")
    
    @staticmethod
    def from_dict(data: dict) -> "SQLExampleDataMetadata":
        # 手动反序列化嵌套结构
        sql_data = data.get("sql_data", {})
        if isinstance(sql_data, str):
            try:
                sql_data = json.loads(sql_data)
            except json.JSONDecodeError:
                sql_data=eval(sql_data)
        sql_data = SQLExampleData(**sql_data)
        return SQLExampleDataMetadata(
            file_path=data["file_path"],
            sql_data=sql_data,
            embedding_field=data.get("embedding_field", "query")
        )
    def to_dict(self):
        sql_data={}
        if self.sql_data is not None:
            sql_data=self.sql_data.to_dict()
        res=asdict(self)
        res['sql_data']=sql_data
        return res
    
    
@dataclass
class DBSchema:
    table_names_original: List[str]
    column_names_original: List[Tuple[int,str]]
    
    def to_dict(self):
        return asdict(self)