"""
Repsonsible for summarizing text using a language model.
This module provides a class to summarize text using a language model. It loads the summarization prompt from a file and uses the language model to generate a summary.
"""

import os 
from src.utils.agents.Base_agent import BaseAgent
import aiofiles
from langchain_core.prompts import ChatPromptTemplate
from src.constants.paths import PROMPT_FILE_PATHS
import asyncio
from src.utils.helper.helper import get_json_response


class Summarizer(BaseAgent):
    
    def __init__(self):
        super.__init__("Text Summarizer")
        self.prompt=PROMPT_FILE_PATHS['Summarize']
        self.summarizer=self.llm

    
    
    async def load_prompt(self,filepath):
        """ Asynchronously reads and returns the summarization prompt from the prompts file"""
        try:
            async with aiofiles.open(filepath,'r',encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            print((f'Error loading prompt for summarizer agent : {e}'))
            return ""



    async def generate_summary(self,text):
        text_prompt=await self.load_prompt(self.prompt)
        messages=[
            ("system",text_prompt
            ),
            (
                "Human","Help me in summarizing this text:{text}"
            )
        ]
        prompt=ChatPromptTemplate.from_messages(messages)
        chain=prompt | self.summarizer

        try:

            ai_message=await asyncio.to_thread(
                chain.invoke,
                {
                    "text":text
                }
                )
            return get_json_response(ai_message.content)
        
        except Exception as e:
            print(f"could not perform summarization , Error : {e}")

