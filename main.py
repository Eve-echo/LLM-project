from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
model = ChatOpenAI(
    base_url = "http://127.0.0.1:1234/v1",
    api_key= "lm-studio",
    model = "qwen/qwen3.5-9b"
)

print("__________________Welcome to the AI chat! Type '0' to exit__________________")

mode= ["happy", "sad", "angry", "funny"]

print("Enter a no. to select the AI modes : ")
x = int(input(""))

convo = [
    SystemMessage(content= f"You are a {mode[x]} AI. reply in short messages.")
]

while True:
    prompt = input("You: ")
    convo.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(convo)
    convo.append(AIMessage(response.content))
    print(response.content)
