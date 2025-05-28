from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Tuple,Union
from database.session import session_scope
from dataclasses import dataclass
from database.schema import TableSchema
from core.text2sql.base import DBSchema



class SQLDatabaseClient:
    """封装数据库 schema 查询和 SQL 执行逻辑"""

    def __init__(self,session_scope):
        self._session_scope = session_scope
        self.schema_info=None
        self.db_schema=None
    def get_schema_info(self) -> List[TableSchema]:
        """
        获取数据库中所有表结构、建表语句及原始样例数据（前两行）
        """
        if self.schema_info is not None:
            return self.schema_info
        with self._session_scope() as session:
            inspector = inspect(session.bind)
            result: List[TableSchema] = []

            for table_name in inspector.get_table_names():
                # 1. 字段信息
                columns = inspector.get_columns(table_name)
                col_info = [(col["name"], str(col["type"])) for col in columns]

                # 2. 建表语句
                try:
                    row = session.execute(text(f"SHOW CREATE TABLE {table_name}")).fetchone()
                    create_sql = row[1] if row else "-- 无法获取建表语句"
                except Exception as e:
                    create_sql = f"-- 获取建表语句失败: {e}"

                # 3. 样例数据
                try:
                    rows = session.execute(text(f"SELECT * FROM {table_name} LIMIT 10")).fetchall()
                    example_rows = [dict(r._mapping) for r in rows]
                except Exception as e:
                    example_rows = [{"error": f"获取失败: {e}"}]

                # 4. 构建返回对象
                result.append(TableSchema(
                    table_name=table_name,
                    columns=col_info,
                    create_sql=create_sql,
                    example_rows=example_rows
                ))
            self.schema_info=result
            return result


    def get_db_schema(self):
        if self.db_schema is not None:
            return self.db_schema
        schema_info=self.get_schema_info()
        table_names_original=[table.table_name for table in schema_info]
        column_names_original=[]
        index=0
        for table in schema_info:
            for column_info in table.columns:
                column_names_original.append((index,column_info[0]))
                index+=1
        self.db_schema=DBSchema(table_names_original=table_names_original,column_names_original=column_names_original)
        return self.db_schema
    def execute_sql(self, sql: str) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        执行 SQL 语句并返回执行状态和结果或错误信息。
        :param sql: 任意 SELECT 类型 SQL 查询
        :return: (是否成功, 成功时为查询结果列表，失败时为错误信息字符串)
        """
        try:
            with self._session_scope() as session:
                result = session.execute(text(sql))
                rows = [dict(row._mapping) for row in result]
                return True, rows
        except Exception as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)


    def sql_result_to_markdown(self,rows: List[Dict[str, Any]]) -> str:
        """
        将 SQL 查询结果转换为 Markdown 表格。
        :param rows: 每行结果为一个字典（来自 execute_sql）
        :return: Markdown 格式的表格字符串
        """
        if not rows:
            return "查询结果为空。"

        # 提取表头
        headers = list(rows[0].keys())
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

        # 构建数据行
        data_rows = ["| " + " | ".join(str(row.get(col, "")) for col in headers) + " |" for row in rows]

        return "\n".join([header_row, separator_row] + data_rows)

    def get_markdown_create_table_schema(self)->str:
        """
        获取数据库中所有表结构、建表语句及原始样例数据（前两行）
        """
        table_schemas = self.get_schema_info()
        return "\n\n".join([table_schema.create_sql for table_schema in table_schemas])

    def get_markdown_table_example_data(self)->str:
        """
        获取数据库中所有表结构、建表语句及原始样例数据（前两行）
        """
        table_schemas = self.get_schema_info()
        # 获取数据样例
        examples=[]
        for table_schema in table_schemas:
            example=f"- 表名:{table_schema.table_name}\n-- 表数据样例:\n```markdown\n{table_schema.example_to_markdown()}```\n---------"
            examples.append(example)
        sql_example_data="\n\n".join(examples)
        return sql_example_data



sql_client=SQLDatabaseClient(session_scope=session_scope)
