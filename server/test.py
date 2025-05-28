from core.text2sql.utils import sql2skeleton

# 示例数据库schema
db_schema = {
    "table_names_original": ["employee_records"],
    "column_names_original": [
        (0, "employee_id"),
        (0, "department"),
        (0, "salary")
    ]
}

sql = """
SELECT department
FROM employee_records
GROUP BY department
HAVING AVG(salary) > 50000;
"""

print(sql2skeleton(sql, db_schema))

from database.connector.client import sql_client

schema_info=sql_client.get_schema_info()
for schema in schema_info:
    res=schema.example_to_markdown()
    print(res)
    print("-"*100)
