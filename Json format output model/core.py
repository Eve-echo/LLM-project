from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    model = "qwen/qwen3.5-9b",
    api_key = "lm-studio"
)

