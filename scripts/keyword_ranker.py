import os
from langchain_community.chat_models import AzureChatOpenAI 
from typing import List, Dict
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()


# Initialize the AzureChatOpenAI instance
llm = "Your LLM"


class KeywordAnalysis(BaseModel):
    Keyword_Analysis: Dict[str, str] = Field(description="Keyword and their comparative study")

    def __str__(self):
        return f"Keyword Analysis: {self.Keyword_Analysis}"
    
parser = PydanticOutputParser(pydantic_object=KeywordAnalysis)


def keyword_study(keyword_list: List[str]) -> List[Dict[str, str]]:
    if not keyword_list:
        return "No keywords provided for analysis."

    results = []
    
    for keyword_string in keyword_list:
        prompt = PromptTemplate(
            template='''
            CONTEXT: You are a Search Engine Optimization (SEO) expert.
            
            ROLE: Analyze the given task and return the output as a single string.
            
            INPUT:
            Keyword List - {keyword_string}
            
            TASK: As an SEO Expert, analyze the given list of keywords and provide a comparative analysis of them on the basis of keyword difficulty, cost per click, and volume.
            
            GUIDELINES:
            1. Provide only the comparative analysis.
            2. Do not hallucinate.
            
            {format_instructions}
            ''',
            input_variables=["keyword_string"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        
        formatted_prompt = prompt.format(keyword_string=keyword_string)
        output = llm.invoke(formatted_prompt)  # Pass the prompt as a string

        # Extract the content of the AIMessage or other structured response
        if hasattr(output, 'content'):
            response_text = output.content  # If output is an AIMessage or similar with 'content' attribute
        else:
            response_text = str(output)  # Fallback if output is already a string or lacks 'content'

        # Parse the response text
        response = parser.parse(response_text)

        results.append(response.Keyword_Analysis)

    return results

# # Test the function
# my_list = ['movies based on true stories', 'filmmakers dealing with real-life events', 'vivid, enveloping film', 'movies that draw on history', 'top 10 movies based on a true story']
# answer = keyword_study(my_list)
# print(answer)
# print(type(answer))