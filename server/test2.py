from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", base_url="https://api.vveai.com/v1",api_key="sk-uHVUAlU35OdVvwMe99D9D8D8D5Ce4f28921064D456D131E9")
response = embeddings.embed_documents(["test input"])
print(response)