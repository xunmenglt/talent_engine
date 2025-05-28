import json
import base64
from decimal import Decimal
from datetime import datetime, date, time
from typing import Any

def mysql_safe_convert(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

def mysql_result_to_json_safe(obj: Any) -> Any:
    """
    将 MySQL 查询结果中的特殊类型（Decimal、datetime、bytes等）
    转换为可被 json.dumps() 正确序列化的结构。
    支持递归处理嵌套 dict 和 list。
    """
    if isinstance(obj, dict):
        return {k: mysql_result_to_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [mysql_result_to_json_safe(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)  # 或 str(obj)，用于保留精度
    elif isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    else:
        return obj