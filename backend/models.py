from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, index=True)

    calls = relationship("Call", back_populates="client")
    feedbacks = relationship("Feedback", back_populates="client")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brokerage = Column(String)

    calls = relationship("Call", back_populates="agent")
    feedbacks = relationship("Feedback", back_populates="agent")

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    recording_url = Column(String)
    transcript = Column(Text)
    twilio_sid = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="calls")
    agent = relationship("Agent", back_populates="calls")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    call_id = Column(Integer, ForeignKey("calls.id"))
    sentiment = Column(String)
    rating = Column(Float)
    summary = Column(Text)
    action_items = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="feedbacks")
    agent = relationship("Agent", back_populates="feedbacks")