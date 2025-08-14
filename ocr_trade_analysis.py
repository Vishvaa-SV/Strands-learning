# ocr_trade_analysis.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def extract_trade_text(image_path: str):
    """
    Upload screenshot path, return extracted text.
    """
    return await falcon_tools.extract_trade_text_from_image(image_path)

# Initialize agent with OCR tool
model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[extract_trade_text])

# Test query
query = "Extract text from screenshot at 'sample_trade.png'"
result = agent(query)
print(result)
