from pydantic import BaseModel
from typing import List


class Recommendation(BaseModel):

    name: str
    url: str
    attributes: list
    reason: str


class ChatResponse(BaseModel):

    response: str
    recommendations: List[Recommendation]