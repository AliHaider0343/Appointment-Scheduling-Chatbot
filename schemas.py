from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Role(str, Enum):
    human = "human"
    ai = "ai"

class ChatHistoryEntry(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    question: str
    # chat_history: Optional[List[ChatHistoryEntry]] = []

class ChatResponse(BaseModel):
    answer: str