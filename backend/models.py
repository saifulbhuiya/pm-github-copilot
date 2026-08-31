from pydantic import BaseModel
from typing import Dict, List

class Card(BaseModel):
    id: str
    title: str
    details: str

class Column(BaseModel):
    id: str
    title: str
    cardIds: List[str]

class BoardData(BaseModel):
    columns: List[Column]
    cards: Dict[str, Card]

class CreateCardRequest(BaseModel):
    column_id: int
    title: str
    details: str = ""

class MoveCardRequest(BaseModel):
    column_id: int
    position: int

class RenameColumnRequest(BaseModel):
    title: str

class AIChatRequest(BaseModel):
    message: str

