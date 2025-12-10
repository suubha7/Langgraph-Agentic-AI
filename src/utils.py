from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from typing import Optional, Type, Any
from pydantic import BaseModel


class AWSLLM:
    def __init__(self, model: str = "amazon.nova-lite-v1:0"):
        """
        Initialize AWS Bedrock LLM wrapper.
        
        Args:
            model: The Bedrock model ID to use
        """
        self.model = model
        self.llm = None
    
    def _get_llm(self):
        """Lazy initialization of LLM to avoid unnecessary API calls."""
        if self.llm is None:
            self.llm = init_chat_model(
                model_provider="bedrock_converse",
                model=self.model
            )
        return self.llm
    
    def chat(
        self, 
        prompt: str, 
        schema: Optional[Type[BaseModel]] = None
    ) -> Any:
        """
        Send a chat message to the LLM.
        
        Args:
            prompt: The user prompt/question
            schema: Optional Pydantic BaseModel for structured output
            
        Returns:
            str if no schema provided, Pydantic model instance if schema provided
        """
        llm = self._get_llm()
        
        if schema is None:
            # Unstructured response
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        else:
            # Structured response
            structured_llm = llm.with_structured_output(schema)
            structured_output = structured_llm.invoke([HumanMessage(content=prompt)])
            return structured_output