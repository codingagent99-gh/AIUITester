from pydantic import BaseModel
from typing import Optional, List

class StepResult(BaseModel):
    step: str
    status: str
    error: Optional[str]

class TestReport(BaseModel):
    test_name: str
    steps: List[StepResult]
    final_status: str
