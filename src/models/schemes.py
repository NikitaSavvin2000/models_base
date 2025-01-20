from pydantic import BaseModel
from typing import Dict

class SaveModelRequest(BaseModel):
    pipeline: Dict[str, str]
    metrics: Dict[str, float]
    name: str
    lag: int
    point_per_call: int
    description: str


