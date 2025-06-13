from pydantic import BaseModel
from typing import List, Dict

class MenuResponse(BaseModel):
    요일: List[str]
    메뉴1_한식: List[List[str]]
    메뉴2_일품: List[List[str]]

class OCRResponse(BaseModel):
    tables: List[MenuResponse]