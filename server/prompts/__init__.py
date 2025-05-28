from langchain_core.prompts.prompt import PromptTemplate
from prompts.data_augmentation_prompts import generate_nl_sql_task_prompt, fix_faulty_sql_prompt,generate_nl_sql_task_ref_sql_prompt
from prompts.sql_sceen_prompts import (answer_user_question_prompt,
                                       generate_sql_prompt,
                                       generate_sql_by_example_prompt,
                                       generate_question_skeleton_prompt,
                                       plan_formulation_prompt,
                                       answer_user_question_on_plan_prompt)

GENERATE_NL_SQL_TASK_PROMPT= PromptTemplate(
    input_variables=["sql_schema", "sql_example_data","reference_question"],
    template=generate_nl_sql_task_prompt,
    template_format="jinja2"
)

GENERATE_NL_SQL_TASK_REF_SQL_PROMPT= PromptTemplate(
    input_variables=["sql_schema", "sql_example_data","reference_question","reference_sql"],
    template=generate_nl_sql_task_ref_sql_prompt,
    template_format="jinja2"
)


FIX_FAULTY_SQL_PROMPT= PromptTemplate(
    input_variables=["sql_schema", "sql_example_data","question","error_sql","error_message"],
    template=fix_faulty_sql_prompt,
    template_format="jinja2"
)


ANSWER_USER_QUESTION_PROMPT= PromptTemplate(
    input_variables=["sql_schema", "question","sql_statement","sql_result"],
    template=answer_user_question_prompt,
    template_format="jinja2"
)

GENERATE_SQL_PROMPT= PromptTemplate(
    input_variables=["sql_schema","sql_example_data", "question"],
    template=generate_sql_prompt,
    template_format="jinja2"
)


GENERATE_SQL_BY_EXAMPLE_PROMPT= PromptTemplate(
    input_variables=["sql_schema","table_part_data","sql_example_input_output", "question"],
    template=generate_sql_by_example_prompt,
    template_format="jinja2"
)

GENERATE_QUESTION_SKELETON_PROMPT= PromptTemplate(
    input_variables=["sql_schema","question"],
    template=generate_question_skeleton_prompt,
    template_format="jinja2"
)

PLAN_FORMULATION_PROMPT= PromptTemplate(
    input_variables=["sql_schema","question"],
    template=plan_formulation_prompt,
    template_format="jinja2"
)

ANSWER_USER_QUESTION_ON_PLAN_PROMPT= PromptTemplate(
    input_variables=["sql_schema", "question","reference_question_answers"],
    template=answer_user_question_on_plan_prompt,
    template_format="jinja2"
)