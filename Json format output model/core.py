from langchain_openai import ChatOpenAI
import json
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

model = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    model = "qwen/qwen3.5-9b",
    api_key = "lm-studio"
)
input_paragraph = input("Enter para: ")

class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: str
    writers: str
    cast: str
    country_of_origin: Optional[str]
    runtime_minutes: int
    production_companies: List[str]
    plot_summary: str
    additional_details: Optional[str]
    rating: Optional[float]

parser = PydanticOutputParser(pydantic_object=Movie)

promp = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a movie information extraction assistant.

        Extract movie information from the user's paragraph.
        {format_instructions}
        """
    ),
    (
        "human",
        "{input_paragraph}"
    )
]) 

prompt = promp.format_messages(
    input_paragraph = input_paragraph,
    format_instructions = parser.get_format_instructions()
)

response = model.invoke(prompt)
movie_data = parser.parse(response.content)
print("Bot:", movie_data)