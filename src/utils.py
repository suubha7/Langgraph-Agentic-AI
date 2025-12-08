from bytez import Bytez
from dotenv import load_dotenv
import os

load_dotenv()

def llm_model():
    """
    Docstring for llm_model
    """
    key = os.getenv("BYTEZ_API_KEY")
    sdk = Bytez(key)

    
    return sdk.model("google/flan-t5-xl")

   
