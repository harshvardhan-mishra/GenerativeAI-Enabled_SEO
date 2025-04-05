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


class KeywordAttribute(BaseModel):
    keyword_attribute: List[Dict[str,Dict[str,str]]] = Field(description="List of keywords with their attributes and their values")

    def __str__(self):
        return (
            f"Keyword Difficulty: {self.keyword_attribute}")
    
parser = PydanticOutputParser(pydantic_object=KeywordAttribute)


def attributes_keyword(keyword_list: List[str]) -> List[Dict[str, str]]:
    if not keyword_list:
        return "No keywords provided for analysis."

    results = []
    
    for keyword_string in keyword_list:
        prompt = PromptTemplate(
            template='''
            CONTEXT: You are a Search Engine Optimization (SEO) expert.

            ROLE: Analyze the given list of keywords and extract the attributes for each keyword: difficulty, cost per click (CPC), and volume.

            INPUT:
            Keyword List - {keyword_string}

            TASK: For each keyword provided, analyze and assign a value (e.g., high, low or moderate) to the following attributes:
            1. Keyword Difficulty
            2. Cost per Click (CPC)
            3. Search Volume

            GUIDELINES:
            1. For each keyword, provide only the keyword itself along with each attribute and its assigned value (e.g., "Keyword: Difficulty - High, CPC - Low, Volume - High").
            2. Avoid assumptions and only provide information explicitly stated.
            3. If data is not available, then take default value of attributes as 'Low'

            
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

        results.append(response.keyword_attribute)

    return results

# # Test the function
# my_list = [{'movies based on true stories': "The keyword 'movies based on true stories' has a moderate keyword difficulty, a high cost per click, and a high volume."}, {'filmmakers dealing with real-life events': "The keyword 'filmmakers dealing with real-life events' has a moderate keyword difficulty, low cost per click, and low search volume."}, {'vivid': 'Keyword difficulty: Medium, Cost per click: High, Volume: Low', 'enveloping film': 'Keyword difficulty: High, Cost per click: Medium, Volume: High'}, {'movies that draw on history': 'The keyword difficulty is high due to the broad nature of the topic. The cost per click is moderate as it is a popular search term but not highly competitive. The volume is high due to the general interest in historical movies.'}, {'top 10 movies based on a true story': "The comparative analysis of the keyword 'top 10 movies based on a true story' shows a moderate keyword difficulty, high cost per click, and high volume."}]
# answer = attributes_keyword(my_list)
# print(answer)
# print(type(answer))