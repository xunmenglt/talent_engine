import os
import json
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from typing import Dict, List, Any, Tuple
from sqlalchemy.orm import sessionmaker
from configs import settings

def build_engine() -> Engine:
    db_type=settings.database.db_type
    user=settings.database.user
    password=settings.database.password
    host=settings.database.host
    port=settings.database.port
    database=settings.database.database
    
    # 构造 SQLAlchemy URL
    if db_type == "mysql":
        return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4&collation=utf8mb4_unicode_ci",json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False))
    elif db_type == "postgres":
        return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False))
    elif db_type == "sqlite":
        db_path=os.path.join(os.getcwd(),"data",database)
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path),exist_ok= True)
        return create_engine(f"sqlite:///{db_path}",json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False))
    else:
        raise ValueError(f"不支持的数据库类型: {db_type}")

engine=build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


