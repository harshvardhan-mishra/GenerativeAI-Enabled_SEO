import os
from langchain_community.chat_models import AzureChatOpenAI 
from typing import List, Dict
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field, model_validator

load_dotenv()

# Initialize the AzureChatOpenAI instance
llm = "Your LLM"


class KeywordList(BaseModel):
    KeywordList: List[str] = Field(description="List of Keywords in the text")

    def __str__(self):
        return f"Keyword List: {self.KeywordList}"
    
parser = PydanticOutputParser(pydantic_object=KeywordList)



def possible_keywords(input_text):


    prompt = PromptTemplate(
    template='''
    
    CONTEXT: You are a Search Engine Optimization (SEO) expert.

    ROLE: Analyze the given task and return the output as a list of keyword phrases.

    TASK: You are provided with a text. As an SEO expert, analyze the text and identify various relevant keyword phrases on which SEO techniques could be applied.

    GUIDELINES:
    1. Only identify keywords that appear naturally in the text.
    2. Generate keywords as short, complete phrases that make sense in SEO context (e.g., “best marketing strategies,” “digital marketing tools”).
    3. Avoid hallucinations or invented keywords; stick to terms and phrases present in or directly relevant to the text.

    OUTPUT FORMAT:
    - List of keyword phrases.

\n{format_instructions}\n{query}\n

    
    \n{format_instructions}\n{query}\n''',
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    prompt_and_model = prompt | llm
    output = prompt_and_model.invoke({"query": input_text})
    # parser.invoke(output)
    response = parser.invoke(output)
    keyword_list = response.KeywordList
    return keyword_list