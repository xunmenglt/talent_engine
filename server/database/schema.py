from dataclasses import dataclass
from typing import List, Tuple,Optional


@dataclass
class TableSchema:
    table_name: str
    columns: List[Tuple[str, str]]                 # e.g., [("id", "INT"), ("name", "VARCHAR")]
    create_sql: str                                # 原始建表语句
    example_rows: Optional[List[dict]] = None      # 原始样例数据（前两行）

    def example_to_markdown(self) -> str:
        """
        将样例数据转换为 markdown 表格格式，适合文档或 CLI 展示。
        """
        if not self.example_rows:
            return "_(表中无数据)_"

        headers = list(self.example_rows[0].keys())
        md = "| " + " | ".join(headers) + " |"
        sep = "| " + " | ".join(["---"] * len(headers)) + " |"
        lines = [md, sep]
        if len(self.example_rows)<=1:
            lines.append("_表中无数据_")
        else:
            for row in self.example_rows:
                values = [str(row.get(h, "")) for h in headers]
                lines.append("| " + " | ".join(values) + " |")
        return "\n".join(lines)
