from langchain_openai import ChatOpenAI
import json
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    model = "qwen/qwen3.5-9b",
    api_key = "lm-studio"
)
input_paragraph = input("Enter para: ")
schema = {
    "movie_title": None,
    "release_date": None,
    "release_year": None,
    "genres": [],
    "director": [],
    "writers": [],
    "cast": [],
    "original_language": None,
    "country_of_origin": [],
    "runtime_minutes": None,
    "production_companies": [],
    "plot_summary": None,
    "themes": [],
    "additional_details": [],
    "uncertainties": []
}

promp = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a movie information extraction assistant.

        Extract movie information from the user's paragraph.
        Use only information supported by the paragraph.
        Do not invent missing facts.
        Return valid JSON matching this schema:

        {schema}
        """
    ),
    (
        "human",
        "Analyze this movie paragraph:\n{input_paragraph}"
    )
]) 

prompt = promp.format_messages(
    input_paragraph = input_paragraph,
    schema = json.dumps(schema, indent=2)
)

response = model.invoke(prompt)
print("Bot:", response.content)