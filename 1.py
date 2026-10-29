from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

models = client.models.list()
model_id = models.data[0].id

print("__________________Welcome to the AI chat! Type '0' to exit__________________")
convo = [
    SystemMessage(content="You are a funny AI.")
]
while True:
    
    prompt = input("You: ")
    convo.append(HumanMessage(content=prompt))
    if prompt =="0":
        break
    response = client.chat.completions.create(
        model=model_id,
        messages=convo
    )
    convo.append(AIMessage(content=response.choices[0].message.content))
    print("Bot: ",response.choices[0].message.content)