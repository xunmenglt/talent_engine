import os
from functools import lru_cache
from configs.configuration_wizard import ConfigWizard, configclass, configfield


@configclass
class VectorStoreConfig(ConfigWizard):
    """Configuration class for the Vector Store connection.
    """

    type: str = configfield(
        "type",
        default="chroma",  # supports pgvector, milvus
        help_txt="向量存储的类型",
    )

    name: str = configfield(
        "name",
        default="rag",
        help_txt="The name of vector store",
    )
    
    host: str = configfield(
        "host",
        default="",
        help_txt="运行Vector Store DB的机器的主机",
    )
    port: str = configfield(
        "port",
        default="",
        help_txt="运行Vector Store DB的机器的端口",
    )
    user: str = configfield(
        "user",
        default="",
        help_txt="运行Vector Store DB的机器的用户名",
    )
    password: str = configfield(
        "password",
        default="",
        help_txt="运行Vector Store DB的机器的密码",
    )
    
    kwargs: dict = configfield(
        "kwargs",
        default="",
        help_txt="向量数据库额外配置参数",
    )


@configclass
class LLMConfig(ConfigWizard):
    """Configuration class for the llm connection.
    """
    api_key: str = configfield(
        "api_key",
        default="sk-xxxxxxxxxx",
        help_txt="OPENAI API kEY.",
    )
    base_url: str = configfield(
        "base_url",
        default="https://www.gptapi.us",
        help_txt="OPENAI API BASE URL"
    )
    model_name: str = configfield(
        "model_name",
        default="",
        help_txt="托管模型的名称。",
    )
    temperature: float = configfield(
        "temperature",
        default=0.7,
        help_txt="托管模型Sampling temperature",
    )
    max_tokens:int=configfield(
        "max_tokens",
        default=1024,
        help_txt="Max tokens to generate",
    )
    model_engine: str = configfield(
        "model_engine",
        default="openai",
        help_txt="托管模型的引擎。",
    )


@configclass
class EmbeddingConfig(ConfigWizard):
    """Configuration class for the Embeddings.
    """

    model_name_or_path: str = configfield(
        "model_name_or_path",
        default="",
        help_txt="The name or local path of huggingface embedding model.",
    )
    model_engine: str = configfield(
        "model_engine",
        default="huggingface",
        help_txt="The server type of the hosted model. Allowed values are hugginface",
    )
    dimensions: int = configfield(
        "dimensions",
        default=1024,
        help_txt="The required dimensions of the embedding model. Currently utilized for vector DB indexing.",
    )
    device: str = configfield(
        "device",
        default="cpu",
        help_txt="Operation equipment",
    )
    base_url: str = configfield(
        "base_url",
        default="",
        help_txt="The url of the hosted model.",
    )
    api_key: str = configfield(
        "api_key",
        default="",
        help_txt="The api key of the hosted model.",
    )

@configclass
class RerankConfig(ConfigWizard):
    """Configuration class for the Rerank Model.
    """
    model_name_or_path: str = configfield(
        "model_name_or_path",
        default="bge-reranker-large",
        help_txt="The model name or local path of rerank model.",
    )
    type: str = configfield(
        "type",
        default="rank",
        help_txt="The type of the rerank model. Allowed values are {rank, llm}",
    )
    device: str = configfield(
        "device",
        default="cpu",
        help_txt="Operation equipment",
    )


@configclass
class ServerConfig(ConfigWizard):

    api_server_host: str = configfield(
        "api_server_host",
        default="127.0.0.1",
        help_txt="Api Server host",
    )

    api_server_port: int = configfield(
        "api_server_port",
        default=7861,
        help_txt="Api Server port",
    )


@configclass
class KnowledgeBaseConfig(ConfigWizard):
    """Configuration class for the knowledge base.
    """
    base_storage_path: str = configfield(
        "base_storage_path",
        default="data/knowledge_base",
        help_txt="存储地址",
    )

    name: str = configfield(
        "name",
        default="default",
        help_txt="知识库名称",
    )
    
@configclass
class DatabaseConfig(ConfigWizard):
    """Configuration class for SQL database connection (e.g., MySQL, PostgreSQL)."""

    db_type: str = configfield(
        "db_type",
        default="mysql",  # 可选值: mysql, postgres, sqlite...
        help_txt="数据库类型",
    )
    host: str = configfield(
        "host",
        default="localhost",
        help_txt="数据库主机地址",
    )
    port: int = configfield(
        "port",
        default=3306,
        help_txt="数据库端口号",
    )
    user: str = configfield(
        "user",
        default="root",
        help_txt="数据库用户名",
    )
    password: str = configfield(
        "password",
        default="password",
        help_txt="数据库密码",
    )
    database: str = configfield(
        "database",
        default="mydb",
        help_txt="数据库名称",
    )
    echo: bool = configfield(
        "echo",
        default=False,
        help_txt="是否打印SQL日志",
    )
    

@configclass
class SystemConfig(ConfigWizard):
    """Configuration class for the application."""

    vector_store: VectorStoreConfig = configfield(
        "vector_store",
        env=False,
        help_txt="The configuration of the vector db connection.",
        default=VectorStoreConfig(),
    )
    llm: LLMConfig = configfield(
        "llm",
        env=False,
        help_txt="The configuration for the server hosting the Large Language Models.",
        default=LLMConfig(),
    )
    embeddings: EmbeddingConfig = configfield(
        "embeddings",
        env=False,
        help_txt="The configuration of embedding model.",
        default=EmbeddingConfig(),
    )
    reranker: RerankConfig = configfield(
        "reranker",
        env=False,
        help_txt="The configuration of rerank model.",
        default=RerankConfig(),
    )
    server: ServerConfig = configfield(
        "server",
        env=False,
        help_txt="Server args.",
        default=ServerConfig(),
    )
    knowledge_base: KnowledgeBaseConfig=configfield(
        "knowledge_base",
        env=False,
        help_txt="knowledge base args.",
        default=KnowledgeBaseConfig(),
    )
    database: DatabaseConfig = configfield(
        "database",
        env=False,
        help_txt="数据库连接参数",
        default=DatabaseConfig(),
    )





@lru_cache
def get_config() -> "ConfigWizard":
    """Parse the application configuration."""
    config = SystemConfig.from_file(os.path.join(os.getcwd(),"configs/config.yaml"))
    if config:
        return config
    raise RuntimeError("Unable to find configuration.")


settings = get_config()
