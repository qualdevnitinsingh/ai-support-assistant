
import os

from pathlib import Path
from dotenv import load_dotenv
from google import genai
from schemas import CustomerSupportAnalysis
from typing import Optional, Tuple

# 1. Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


# 2. Read API key
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")


# 3. Create AI client
client = genai.Client(api_key=api_key)


# 4. Define AI instructions
SYSTEM_INSTRUCTION = """
You are a professional customer support assistant
for an online jewellery store.

Your responsibilities:
1. Help customers with orders, payments, shipping,
   returns, refunds and product questions.
2. Communicate politely, professionally and clearly.
3. Keep responses helpful and easy to understand.
4. If information is missing, ask the customer
   for the required details.
5. Never invent order status, payment status,
   shipping details or refund information.
6. Never claim that you checked an order or
   company system unless that information was
   actually provided to you.
7. If a question is unrelated to customer support,
   politely explain your role and redirect the customer.
"""


# 6. Reusable analyzer function

def analyze_customer_message(
    customer_message: str,
    previous_interaction_id: Optional[str] = None
) -> Tuple[CustomerSupportAnalysis, str, Optional[object]]:

    if not customer_message.strip():
        raise ValueError("Customer message cannot be empty")

    interaction = client.interactions.create(
        model=os.environ.get("GEMINI_API_MODEL"),

        # Continue the previous conversation when an ID exists
        previous_interaction_id=previous_interaction_id,

        # Instructions must be supplied on each interaction
        system_instruction=SYSTEM_INSTRUCTION,

        # Current customer message
        input=customer_message,

        # Maintain our structured JSON response
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": CustomerSupportAnalysis.model_json_schema()
        }
    )

    output_text = interaction.output_text

    if not output_text:
        raise ValueError("Gemini returned an empty response")

    analysis = CustomerSupportAnalysis.model_validate_json(
        output_text
    )

    usage = getattr(interaction, "usage", None)

    # Return both the analysis and the interaction ID
    return analysis, interaction.id, usage


def count_prompt_tokens(customer_message: str) -> int:

    if not customer_message.strip():
        raise ValueError("Customer message cannot be empty")

    # Combine our system instructions and customer message
    text_to_count = f"""
    {SYSTEM_INSTRUCTION}

    Customer message:
    {customer_message}
    """

    # Ask Gemini to count the tokens
    count_response = client.models.count_tokens(
        model=os.environ.get("GEMINI_API_MODEL"),
        contents=text_to_count
    )

    return count_response.total_tokens
