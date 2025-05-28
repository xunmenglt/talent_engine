import json
import httpx
from sseclient import SSEClient
from datetime import datetime
import os
import uuid
import requests

# 待处理的多个 query 请求

data_path="/opt/data/private/liuteng/code/szrcb/talent_engine/data/benchmark/eval.json"

with open(data_path,"r",encoding="utf-8") as f:
    items = json.load(f)
    
queries = [
    item["question"]
    for item in items
]

# 通用请求体固定部分
base_payload = {
    "history": [
        ["user", "哪些员工同时拥有日语能力和项目管理认证？"],
        ["assistant", "赵敏"]
    ],
    "question_score_threshold": 0.8,
    "sql_score_threshold": 0.5,
    "topk": 5,
    "is_planing": True,
    "sql_verfy_times": 2
}

# 接口地址
url = "http://localhost:8888/chat/sql_chat"

# 输出目录
output_dir = os.path.join(os.getcwd(),"data/sql_chat_outputs_0P5_qwen25-7b_comm_promt")
os.makedirs(output_dir, exist_ok=True)
headers = {
    "Accept": "text/event-stream"
}

# 遍历每个 query，分别发起 SSE 请求并保存响应
for idx, query in enumerate(queries):
    payload = base_payload.copy()
    payload["query"] = query

    print(f"[{idx + 1}/{len(queries)}] 正在处理 query: {query}")

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=(1000, 1000))
        # 一次性获取整个响应文本
        content = response.text
        filename = os.path.join(output_dir, f"question_{idx+1}.log")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已保存到: {filename}\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")
