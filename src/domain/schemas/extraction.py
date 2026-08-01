from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class AIExtractionSchema(BaseModel):
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0 representing how well the request was understood.")
    title: str = Field(..., description="The title of the task in Persian.")
    description: str = Field(..., description="The detailed description of the task in Persian.")
    originalTranscript: str = Field(..., description="The original Persian transcript text.")
    assignedDeveloper: Optional[str] = Field(None, description="The name or alias of the developer assigned to this task.")
    priority: Optional[str] = Field(None, description="The priority of the task. Should be one of: Low, Medium, High, Urgent.")
    deadline: Optional[date] = Field(None, description="The deadline for the task in YYYY-MM-DD format.")
    estimatedDays: Optional[int] = Field(None, description="The estimated number of days to complete the task.")
    labels: Optional[List[str]] = Field(default_factory=list, description="A list of tags or labels relevant to the task (e.g. Frontend, API, Bug).")
    subtasks: Optional[List[str]] = Field(default_factory=list, description="A list of smaller subtasks if the manager mentioned any.")
    acceptanceCriteria: Optional[List[str]] = Field(default_factory=list, description="A list of conditions that must be met for the task to be accepted.")
    questions: Optional[List[str]] = Field(default_factory=list, description="A list of clarification questions if the request is ambiguous.")
