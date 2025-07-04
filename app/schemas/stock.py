from pydantic import BaseModel
from typing import List, Optional

# This model represents the data structure for each indicator data point
class IndicatorData(BaseModel):
    date: str
    value: Optional[float]

# This model represents the response structure for technical indicators
class IndicatorResponse(BaseModel):
    symbol: str
    indicator: str
    data: List[IndicatorData]
