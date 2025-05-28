import os
import json
import sys

files=[
    "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek_01.sqldata",
    "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek_02.sqldata",
    "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek_03.sqldata",
    "/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek_04.sqldata"
]

new_file_path="/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/examples_deepseek.sqldata"

# 合并文件
with open(new_file_path, 'w') as outfile:
    items=[]
    items_map={}
    for file_path in files:
        with open(file_path) as infile:
            lines=infile.readlines()
            for line in lines:
                item = json.loads(line)
                items_map[item["question"]]=item

    for key, value in items_map.items():
        items.append(value)

    for item in items:
        outfile.write(json.dumps(item,ensure_ascii=False))
        outfile.write("\n")