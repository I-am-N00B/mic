from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Painting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    title: str
    artist: str
    year: int
    description: Optional[str] = None