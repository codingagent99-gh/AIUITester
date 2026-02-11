from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class StepResult(BaseModel):
    step: Dict[str, Any]  # Changed from str to Dict
    status: str  # "success", "failed", "skipped"
    error: Optional[str] = None
    screenshot: Optional[str] = None
    data: Optional[Any] = None

class TestReport(BaseModel):
    test_name: str
    status: str
    steps: List[StepResult]
    summary: str
    timestamp: str