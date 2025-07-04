"""Base agent class for all agents.
This class provides a base structure for all agents, including loading environment variables and initializing the language model.
"""
import os
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

class BaseAgent:
    def __init__(self,name):
        self.name=name
        load_dotenv()
        # self.model='deepseek-r1-distill-llama-70b'
        self.model='llama-3.3-70b-versatile'
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        self.llm=ChatGroq(
            model=self.model,
            temperature=0,
            max_tokens=600,
            max_retries=3
        )
        self.guardrails: list = []
    async def add_guardrail(self, guardrail):
        """Add a guardrail to the agent."""
        self.guardrails.append(guardrail)
    async def remove_guardrail(self, guardrail):
        """Remove a guardrail from the agent."""
        self.guardrails.remove(guardrail)
    async def get_guardrails(self):
        """Get the list of guardrails."""
        return self.guardrails
    async def set_guardrails(self, guardrails):
        """Set the list of guardrails."""
        self.guardrails = guardrails
    async def clear_guardrails(self):
        """Clear the list of guardrails."""
        self.guardrails = []
    async def get_name(self):
        """Get the name of the agent."""
        return self.name
    async def set_name(self, name):
        """Set the name of the agent."""
        self.name = name
    async def get_model(self):
        """Get the model of the agent."""
        return self.model
    async def set_model(self, model):
        """Set the model of the agent."""
        self.model = model
    async def get_llm(self):
        """Get the language model of the agent."""
        return self.llm
    async def set_llm(self, llm):
        """Set the language model of the agent."""
        self.llm = llm
      
        




    
        
        