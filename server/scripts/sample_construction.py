"""
样例构建
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
from prompts.utils import generate_nl_sql_task,generate_nl_sql_ref_sql_task
from database.utils import mysql_result_to_json_safe,mysql_safe_convert

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






if __name__ == '__main__':
    # 读取数据
    benchmark_data_path = "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/eval_deepseek.sqldata.json"
    example_data_save_path="/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek_04.sqldata"
    question_enhance_times=10
    examples=[]
    with open(benchmark_data_path, "r",encoding="utf-8") as f:
        benchmark_data = json.load(f)
        pd=tqdm.tqdm(
            total=len(benchmark_data)*question_enhance_times,
            desc="Generating NL SQL Task"
        )
        for i,item in enumerate(benchmark_data):
            with xthread(worker_num=10) as pool:
                futures = []
                for j in range(question_enhance_times):
                    task=pool.submit(generate_nl_sql_ref_sql_task, sql_schema, sql_example_data, item["question"],item['true_query'], llm, sql_client)
                    futures.append(task)
                j=0
                for future in as_completed(futures):
                    result:SQLExampleData = future.result()
                    pd.update(1)
                    if result and result.sql_exec_res and len(result.sql_exec_res)>0:
                        examples.append(result.to_dict() | {"row_id":i*question_enhance_times + j})
                    j+=1
        pd.close()
    with open(example_data_save_path,'w',encoding="utf-8") as f:
        for example in examples:
            json_data=mysql_result_to_json_safe(example)
            try:
                f.write(json.dumps(example,ensure_ascii=False,default=mysql_safe_convert))
            except:
                import pdb;pdb.set_trace()
            f.write("\n")
    examples=mysql_result_to_json_safe(examples)
    with open(example_data_save_path+".json",'w',encoding="utf-8") as f:
        f.write(json.dumps(examples,ensure_ascii=False,indent=4,default=mysql_safe_convert))
    print("合成完毕...")







