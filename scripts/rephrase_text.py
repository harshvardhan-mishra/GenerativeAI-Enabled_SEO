import os
from langchain_community.chat_models import AzureChatOpenAI 
from dotenv import load_dotenv

load_dotenv()

# Initialize the AzureChatOpenAI instance
llm = "Your LLM"

def new_text(text,keyword):
    paragraphs = text.split("\n\n")  # Split by double newlines to separate paragraphs
    rephrased_paragraphs = []

    for paragraph in paragraphs:
        prompt = f'''
        CONTEXT: You are a Search Engine Optimization (SEO) expert.

        ROLE: Analyze the given task and return the output as a single string.

        INPUT:
        paragraph - {paragraph}
        keyword - {keyword}

        TASK: Rephrase the paragraph to make the keyword prominent while preserving its context.

        GUIDELINES:
        1. Retain the paragraph structure in the output.
        2. Use the keyword naturally and prominently within this paragraph.
        3. Do not include anything else as part of the respose

        OUTPUT FORMAT: New paragraph
        '''
        response = llm.invoke(prompt)
        rephrased_paragraph = response.content.strip()
        rephrased_paragraphs.append(rephrased_paragraph)

    
    return "\n\n".join(rephrased_paragraphs)