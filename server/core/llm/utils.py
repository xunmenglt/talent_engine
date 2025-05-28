from functools import lru_cache
from langchain_openai.chat_models import ChatOpenAI
from configs import settings

@lru_cache
def get_llm(model_name, model_engine, **kwargs):
    if model_engine == "openai":
        api_key = kwargs.get("api_key",None)
        base_url=kwargs.get("base_url",None)
        max_tokens=kwargs.get("max_tokens",512)
        temperature=kwargs.get("temperature",0.7)
        if api_key and base_url:
            model = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                base_url=base_url,
                api_key=api_key,
                max_tokens=max_tokens
            )
        
        else:
            raise ValueError(f"please provide valid openai api key when using openai model engine! ")
    else:
        raise ValueError(f"{model_engine} is not supported! ")
    return model


def get_default_llm():
    model_name=settings.llm.model_name
    model_engine=settings.llm.model_engine
    api_key=settings.llm.api_key
    base_url=settings.llm.base_url
    max_tokens=settings.llm.max_tokens
    temperature=settings.llm.temperature
    llm=get_llm(model_name, model_engine, api_key=api_key, base_url=base_url, max_tokens=max_tokens, temperature=temperature)
    
    return llm

