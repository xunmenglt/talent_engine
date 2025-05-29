"""
样例构建
"""
import re
import json
from typing import List
from core.text2sql.base import SQLExampleData
from prompts import (GENERATE_NL_SQL_TASK_PROMPT,
                     GENERATE_NL_SQL_TASK_REF_SQL_PROMPT,
                     FIX_FAULTY_SQL_PROMPT,
                     ANSWER_USER_QUESTION_PROMPT,
                     GENERATE_SQL_PROMPT,
                     GENERATE_QUESTION_SKELETON_PROMPT,
                     PLAN_FORMULATION_PROMPT,
                     GENERATE_SQL_BY_EXAMPLE_PROMPT,
                     ANSWER_USER_QUESTION_ON_PLAN_PROMPT
                    )
from langchain_core.language_models.chat_models import BaseChatModel



# 解析模型输出
def parse_model_output(model_output):
    if not model_output:
        raise ValueError("Model output is empty.")
    # 正则表达式匹配模型输出中的SQL语句
    parrent="```json\s*\n*(.+?)\s*\n*```"  
    items=re.findall(parrent, model_output,re.DOTALL)
    if items and len(items)>0:
        json_data_str=items[-1]
    else:
        json_data_str=model_output
    try:
        json_data=json.loads(json_data_str)
        return json_data
    except Exception as e:
        return None
    
def generate_fixed_sql(sql_schema, sql_example_data,question,error_sql,error_message,llm,sql_client,try_times=1):
    while try_times>0:
        prompt=FIX_FAULTY_SQL_PROMPT.format(
            sql_schema=sql_schema,
            sql_example_data=sql_example_data,
            question=question,
            error_sql=error_sql,
            error_message=error_message
        )
        try:
            llm_result=llm.invoke(prompt).content
            res=parse_model_output(llm_result)
            if res:
                fixed_sql=res["fixed_sql"]
                if not fixed_sql:
                    continue
                is_success,execute_res=sql_client.execute_sql(fixed_sql)
                if is_success:
                    return fixed_sql,execute_res
                error_message=execute_res
                error_sql=fixed_sql
        finally:
            try_times-=1
    return None,None
        
# 生成样例代码
def generate_nl_sql_task(sql_schema,sql_example_data,reference_question,llm,sql_client)->SQLExampleData:
    end_res=None
    prompt=GENERATE_NL_SQL_TASK_PROMPT.format(
            sql_schema=sql_schema,
            sql_example_data=sql_example_data,
            reference_question=reference_question
    )
    llm_result=llm.invoke(
        prompt
    ).content
    res=parse_model_output(llm_result)
    if res is None:
        with open('./gener_log_error.jsonl','a+')as f:
            f.write(json.dumps({"question":reference_question,"model_response":llm_result,"executed":False,"is_valid":False,"error_message":"无法解析模型输出"},ensure_ascii=False))
            f.write("\n")
        return None
    # 判断生成的SQL语句是否有用
    sql=res["sql"]
    question=res["question"]
    is_success,execute_res=sql_client.execute_sql(sql)
    if is_success:
        res["sql_execute_res"]=execute_res
        end_res=res
    else:
        fixed_sql,fix_sql_execute_res=generate_fixed_sql(sql_schema, sql_example_data,question,sql,execute_res,llm,sql_client,try_times=2)
        if fixed_sql:
            res["sql"]=fixed_sql
            res["sql_execute_res"]=fix_sql_execute_res
            end_res=res
        else:
            with open('./gener_log_error.jsonl','a+')as f:
                f.write(json.dumps({"question":question,"model_response":llm_result,"executed":True,"is_valid":False,"error_message":execute_res},ensure_ascii=False))
                f.write("\n")
    if end_res:
        end_res=SQLExampleData(
                schamea=sql_schema,
                question=end_res["question"],
                query=end_res["sql"],
                tables=end_res["tables"],
                sql_exec_res=end_res["sql_execute_res"],
        )
    return end_res

# 生成样例（有sql参照版）  
def generate_nl_sql_ref_sql_task(sql_schema,sql_example_data,reference_question,reference_sql,llm,sql_client)->SQLExampleData:
    end_res=None
    prompt=GENERATE_NL_SQL_TASK_REF_SQL_PROMPT.format(
            sql_schema=sql_schema,
            sql_example_data=sql_example_data,
            reference_question=reference_question,
            reference_sql=reference_sql
    )
    llm_result=llm.invoke(
        prompt
    ).content
    res=parse_model_output(llm_result)
    if res is None:
        with open('./gener_log_error.jsonl','a+')as f:
            f.write(json.dumps({"question":reference_question,"model_response":llm_result,"executed":False,"is_valid":False,"error_message":"无法解析模型输出"},ensure_ascii=False))
            f.write("\n")
        return None
    # 判断生成的SQL语句是否有用
    sql=res["sql"]
    question=res["question"]
    is_success,execute_res=sql_client.execute_sql(sql)
    if is_success:
        res["sql_execute_res"]=execute_res
        end_res=res
    else:
        fixed_sql,fix_sql_execute_res=generate_fixed_sql(sql_schema, sql_example_data,question,sql,execute_res,llm,sql_client,try_times=2)
        if fixed_sql:
            res["sql"]=fixed_sql
            res["sql_execute_res"]=fix_sql_execute_res
            end_res=res
        else:
            with open('./gener_log_error.jsonl','a+')as f:
                f.write(json.dumps({"question":question,"model_response":llm_result,"executed":True,"is_valid":False,"error_message":execute_res},ensure_ascii=False))
                f.write("\n")
    if end_res:
        end_res=SQLExampleData(
                schamea=sql_schema,
                question=end_res["question"],
                query=end_res["sql"],
                tables=end_res["tables"],
                reference_question=reference_question,
                sql_exec_res=end_res["sql_execute_res"],
        )
    return end_res

def generate_sql_direct(sql_schema,sql_example_data,question,llm,sql_client,re_try_times=1,re_try_verfy_times=2)->SQLExampleData:
    end_res=None
    prompt=GENERATE_SQL_PROMPT.format(
        sql_schema=sql_schema,
        sql_example_data=sql_example_data,
        question=question
    )
    res=None
    while re_try_times>0:
        try:
            llm_result=llm.invoke(
                prompt
            ).content
            res=parse_model_output(llm_result)
            if res:
                break
        except Exception as e:
            re_try_times-=1
    if res is None:
        return None
    # 判断生成的SQL语句是否有用
    sql=res["sql"]
    is_success,execute_res=sql_client.execute_sql(sql)
    if is_success:
        res["sql_execute_res"]=execute_res
        end_res=res
    else:
        fixed_sql,fix_sql_execute_res=generate_fixed_sql(sql_schema, sql_example_data,question,sql,execute_res,llm,sql_client,try_times=re_try_verfy_times)
        if fixed_sql:
            res["sql"]=fixed_sql
            res["sql_execute_res"]=fix_sql_execute_res
        end_res=res
    if end_res:
        end_res=SQLExampleData(
                schamea=sql_schema,
                question=question,
                query=end_res["sql"],
                tables=end_res["tables"],
                sql_exec_res=end_res["sql_execute_res"],
        )
    return end_res

def generate_sql_by_example_data(sql_schema,table_part_data,sql_example_input_output,question,llm,sql_client,re_try_times=1,re_try_verfy_times=2)->SQLExampleData:
    end_res=None
    prompt=GENERATE_SQL_BY_EXAMPLE_PROMPT.format(
        sql_schema=sql_schema,
        table_part_data=table_part_data,
        sql_example_input_output=sql_example_input_output,
        question=question
    )
    res=None
    while re_try_times>0:
        try:
            llm_result=llm.invoke(
                prompt
            ).content
            res=parse_model_output(llm_result)
            if res:
                break
        except Exception as e:
            re_try_times-=1
    if res is None:
        return None
    # 判断生成的SQL语句是否有用
    sql=res["sql"]
    is_success,execute_res=sql_client.execute_sql(sql)
    if is_success:
        res["sql_execute_res"]=execute_res
        end_res=res
    else:
        fixed_sql,fix_sql_execute_res=generate_fixed_sql(sql_schema, table_part_data,question,sql,execute_res,llm,sql_client,try_times=re_try_verfy_times)
        if fixed_sql:
            res["sql"]=fixed_sql
            res["sql_execute_res"]=fix_sql_execute_res
            end_res=res
    if end_res:
        end_res=SQLExampleData(
                schamea=sql_schema,
                question=question,
                query=end_res["sql"],
                tables=end_res["tables"],
                sql_exec_res=end_res["sql_execute_res"],
        )
    return end_res


def answer_user_question(sql_schema,question,sql_statement,sql_result,llm):
    prompt=ANSWER_USER_QUESTION_PROMPT.format(
        sql_schema=sql_schema,
        question=question,
        sql_statement=sql_statement,
        sql_result=sql_result
    )
    llm_result=llm.invoke(
        prompt
    ).content
    return llm_result

async def answer_user_question_with_refernce(sql_schema,question,reference_question_answers,llm:BaseChatModel):
    prompt=ANSWER_USER_QUESTION_ON_PLAN_PROMPT.format(
        sql_schema=sql_schema,
        question=question,
        reference_question_answers=reference_question_answers
    )
    response=llm.astream(prompt)
    async for chunk in response:
        yield chunk.content


def generate_question_skeletion(sql_schema,question,llm)->SQLExampleData:
    prompt=GENERATE_QUESTION_SKELETON_PROMPT.format(
            sql_schema=sql_schema,
            question=question,
    )
    llm_result=llm.invoke(
        prompt
    ).content
    res=parse_model_output(llm_result)
    if res is None:
        return None
    return res.get("question_skeleton",None)


def plan_formulation(sql_schema,question,llm)->List[str]:
    prompt=PLAN_FORMULATION_PROMPT.format(
            sql_schema=sql_schema,
            question=question,
    )
    llm_result=llm.invoke(
        prompt
    ).content
    res=parse_model_output(llm_result)
    if res is None:
        return [question]
    question_list=res.get("question_list",None)
    if question_list is None:
        return [question]
    return question_list




