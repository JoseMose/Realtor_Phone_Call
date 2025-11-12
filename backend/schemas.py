from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

class AgentBase(BaseModel):
    name: str
    brokerage: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int

    class Config:
        from_attributes = True

class CallBase(BaseModel):
    client_id: int
    agent_id: int
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    twilio_sid: Optional[str] = None

class CallCreate(CallBase):
    pass

class Call(CallBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    client_id: int
    agent_id: int
    call_id: int
    sentiment: str
    rating: Optional[float] = None
    summary: str
    action_items: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackSummary(BaseModel):
    client_name: str
    agent_name: str
    overall_sentiment: str
    rating_estimate: float
    summary: str
    action_items: List[str]

class AnalyzeRequest(BaseModel):
    transcript: str