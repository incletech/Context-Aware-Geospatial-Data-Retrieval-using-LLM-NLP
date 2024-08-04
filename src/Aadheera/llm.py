from ai71 import AI71 
import os
from typing import List, Optional, Dict, Any
from groq import Groq
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
class ClientInitializerLlm:
    def __init__(self):
        self.clients = {
            'ai71': self.init_ai71_client(),
            'groq':self.init_groq_client(),
            'together_ai':self.init_together_client()
        }

    def init_ai71_client(self):
        return AI71(
            api_key=os.getenv("AI71_API_KEY")
        )
    def init_groq_client(self):
        return Groq(
            api_key=os.getenv("groq_api")
        )
    def init_together_client(self):
        return Together(api_key=os.getenv("together_ai"))
    
    def get_client(self, client_name: str):
        return self.clients.get(client_name)

class LlmModel:
    def __init__(self, client, model: str, temperature: float, max_tokens: int):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @staticmethod
    def from_config(client_name: str, model: str, temperature: float, max_tokens: int):
        initializer = ClientInitializerLlm()
        client = initializer.get_client(client_name)
        if not client:
            raise ValueError(f"Client '{client_name}' not found.")
        return LlmModel(client, model, temperature, max_tokens)

    def _create_completion(self, messages: List[Dict[str, Any]], response_format: Optional[Dict[str, str]] = None, tools: Optional[List[Any]] = None):
        try:
            params = {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "messages": messages
            }
            if response_format:
                params["response_format"] = response_format
            if tools:
                params["tools"] = tools
                params["tool_choice"] = "auto"
            response = self.client.chat.completions.create(**params)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to create completion: {e}")

    def text_completion(self, messages: List[Dict[str, Any]]):
        return self._create_completion(messages)

    def json_completion(self, messages: List[Dict[str, Any]]):
        response_format = {"type": "json_object"}
        return self._create_completion(messages = messages,response_format= response_format)

    def function_calling(self, messages: List[Dict[str, Any]], tools):
        return self._create_completion(messages = messages, tools=tools)
