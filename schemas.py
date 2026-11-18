
from pydantic import BaseModel, Field
from typing import Literal

class CustomerSupportAnalysis(BaseModel):

    category: Literal[
        "order",
        "payment",
        "shipping",
        "return_refund",
        "product",
        "other"
    ] = Field(
        description="The main category of the customer's issue."
    )

    priority: Literal[
        "low",
        "medium",
        "high"
    ] = Field(
        description="How urgently the support team should handle this issue."
    )

    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ] = Field(
        description="The emotional tone expressed by the customer."
    )

    summary: str = Field(
        description="A short summary of the customer's issue."
    )

    required_action: str = Field(
        description="What the support team should do next."
    )

    suggested_reply: str = Field(
        description="A polite suggested response to the customer."
    )
