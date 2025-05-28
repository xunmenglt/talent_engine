"""
测试数据构建
"""
import re
import json
import sys
import os
import tqdm
sys.path.append(os.getcwd())

from configs import settings
from core.llm.utils import get_llm
from database.connector.client import sql_client
from utils.thread import xthread,as_completed
from core.text2sql.base import SQLExampleData
from prompts.utils import generate_sql_direct,answer_user_question
from database.utils import mysql_result_to_json_safe
model_name=settings.llm.model_name
model_engine=settings.llm.model_engine
api_key=settings.llm.api_key
base_url=settings.llm.base_url
max_tokens=settings.llm.max_tokens
temperature=settings.llm.temperature

llm=get_llm(model_name, model_engine, api_key=api_key, base_url=base_url, max_tokens=max_tokens, temperature=temperature)

# 获取数据库表结构
sql_schema=sql_client.get_markdown_create_table_schema()

# 获取数据样例
sql_example_data=sql_client.get_markdown_table_example_data()



def create_nl_sql_task(sql_schema, sql_example_data, question, llm, sql_client):
    res:SQLExampleData=generate_sql_direct(sql_schema,sql_example_data,question,llm,sql_client,re_try_times=3,re_try_verfy_times=5)
    if res:
        res.sql_exec_res=sql_client.sql_result_to_markdown(mysql_result_to_json_safe(res.sql_exec_res))
        answer=answer_user_question(
            sql_schema,question,res.query,res.sql_exec_res,llm
        )
        return res.to_dict()|{"model_answer":answer}
    else:
        return None




if __name__ == '__main__':
    # 读取数据
    benchmark_data_path = "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/eval.json"
    example_data_save_path="/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/eval_deepseek_r1.sqldata"
    examples=[]
    with open(benchmark_data_path, "r",encoding="utf-8") as f:
        benchmark_data = json.load(f)
        pd=tqdm.tqdm(
            total=len(benchmark_data),
            desc="Generating SQL Task"
        )
        with xthread(worker_num=10) as pool:
            futures = [
                pool.submit(create_nl_sql_task, sql_schema, sql_example_data, item["question"], llm, sql_client)
                for item in benchmark_data
            ]
            for i, future in enumerate(futures):
                result: SQLExampleData = future.result()
                pd.update(1)
                if result:
                    examples.append(result | {"answer": benchmark_data[i]["answer"]})
        pd.close()
    with open(example_data_save_path,'w',encoding="utf-8") as f:
        for example in examples:
            json_data=mysql_result_to_json_safe(example)
            try:
                f.write(json.dumps(example,ensure_ascii=False))
            except:
                import pdb;pdb.set_trace()
            f.write("\n")
    with open(example_data_save_path+".json",'w',encoding="utf-8") as f:
        f.write(json.dumps(examples,ensure_ascii=False,indent=4))
    print("合成完毕...")







