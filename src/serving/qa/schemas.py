"""
This scrips hold all pydantic model
"""
from pydantic import BaseModel


class Question(BaseModel):
    text: str
