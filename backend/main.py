from fastapi import FastAPI, Depends, HTTPException, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Client, Agent, Feedback, Call
from schemas import Client as ClientSchema, ClientCreate, Agent as AgentSchema, AgentCreate, Feedback as FeedbackSchema, FeedbackCreate, Call as CallSchema, CallCreate, AnalyzeRequest
from typing import List
from ai_service import analyze_feedback, transcribe_audio
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse
from config import settings
import json

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Realtor Feedback API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://*.vercel.app",  # Allow Vercel preview deployments
        "*"  # Allow all origins for demo (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

twilio_client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_twiml(client_name, brokerage, agent_name):
    response = VoiceResponse()
    response.say("This call may be recorded and analyzed for quality purposes.")
    response.say(f"Hi {client_name}, this is an automated follow-up from {brokerage}. How was your experience working with {agent_name}?")
    response.record(timeout=5, playBeep=True, recordingStatusCallback=f'{settings.webhook_base_url}/webhook', recordingStatusCallbackMethod='POST')
    response.say("Thank you for your feedback.")
    response.say("What did you like most about the experience?")
    response.record(timeout=5, playBeep=True, recordingStatusCallback=f'{settings.webhook_base_url}/webhook', recordingStatusCallbackMethod='POST')
    response.say("Thank you for your feedback.")
    response.say("Is there anything that could have been better?")
    response.record(timeout=5, playBeep=True, recordingStatusCallback=f'{settings.webhook_base_url}/webhook', recordingStatusCallbackMethod='POST')
    response.say("Thank you so much for your time and valuable feedback. We really appreciate you sharing your experience with us. Have a great day!")
    response.hangup()
    return str(response)

@app.get("/")
def read_root():
    return {"message": "Realtor Feedback API"}

# Clients
@app.post("/clients/", response_model=ClientSchema)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=List[ClientSchema])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientSchema)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Agents
@app.post("/agents/", response_model=AgentSchema)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.get("/agents/", response_model=List[AgentSchema])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

# Feedbacks
@app.post("/feedbacks/", response_model=FeedbackSchema)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/feedbacks/", response_model=List[FeedbackSchema])
def read_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).offset(skip).limit(limit).all()
    return feedbacks

# Calls
@app.post("/calls/", response_model=CallSchema)
def create_call(call: CallCreate, db: Session = Depends(get_db)):
    db_call = Call(**call.dict())
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

@app.get("/calls/", response_model=List[CallSchema])
def read_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    calls = db.query(Call).offset(skip).limit(limit).all()
    return calls

@app.post("/test-call")
async def test_call(phone_number: str = Form(...), db: Session = Depends(get_db)):
    try:
        # Validate and format phone number
        phone_number = phone_number.strip()
        if not phone_number.startswith('+'):
            # Assume US number if no country code
            phone_number = f'+1{phone_number}'
        
        print(f"Attempting to call: {phone_number}")
        
        # For testing, use the first agent in the database
        agent = db.query(Agent).first()
        if not agent:
            # Create a default agent if none exists
            agent = Agent(name="Test Agent", brokerage="Test Realty")
            db.add(agent)
            db.commit()
            db.refresh(agent)
        
        # Check if client already exists, otherwise create a test client
        client = db.query(Client).filter(Client.phone == phone_number).first()
        if not client:
            client = Client(name="Sara", phone=phone_number)
            db.add(client)
            db.commit()
            db.refresh(client)
        
        twiml = generate_twiml(client.name, agent.brokerage, agent.name)
        
        print("Creating Twilio call...")
        call = twilio_client.calls.create(
            to=phone_number,
            from_=settings.twilio_phone_number,
            twiml=twiml
        )
        
        # Store the call in our database
        db_call = Call(
            client_id=client.id,
            agent_id=agent.id,
            twilio_sid=call.sid
        )
        db.add(db_call)
        db.commit()
        
        return {"call_sid": call.sid, "message": f"Test call initiated to {phone_number}"}
        
    except Exception as e:
        print(f"Test call error: {e}")
        db.rollback()
        return {"error": str(e), "message": "Failed to initiate call"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    return analyze_feedback(request.transcript)

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Log all form data for debugging
        form_data = await request.form()
        print(f"Webhook form data: {dict(form_data)}")

        recording_url = form_data.get("RecordingUrl")
        call_sid = form_data.get("CallSid")

        print(f"Webhook received - CallSid: {call_sid}, RecordingUrl: {recording_url}")

        if not recording_url or not call_sid:
            print("Missing recording_url or call_sid")
            response = VoiceResponse()
            response.hangup()
            return Response(content=str(response), media_type="application/xml")

        # Transcribe the audio
        transcript = transcribe_audio(recording_url)
        print(f"Transcript: {transcript}")

        if transcript.startswith("Error:"):
            print(f"Transcription failed: {transcript}")
            response = VoiceResponse()
            response.hangup()
            return Response(content=str(response), media_type="application/xml")

        # Find the call in database
        call = db.query(Call).filter(Call.twilio_sid == call_sid).first()
        if not call:
            print(f"Call not found for sid: {call_sid}")
            response = VoiceResponse()
            response.hangup()
            return Response(content=str(response), media_type="application/xml")

        # Update call with transcript
        call.transcript = transcript
        call.recording_url = recording_url

        # Analyze the feedback
        analysis = analyze_feedback(transcript)
        print(f"Analysis: {analysis}")

        # Create feedback record
        feedback = Feedback(
            client_id=call.client_id,
            agent_id=call.agent_id,
            call_id=call.id,
            sentiment=analysis["overall_sentiment"],
            rating=analysis["rating_estimate"],
            summary=analysis["summary"],
            action_items=json.dumps(analysis["action_items"])
        )
        db.add(feedback)
        db.commit()

        print("Feedback processed successfully")
        # Return empty TwiML to continue the call
        response = VoiceResponse()
        return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        print(f"Webhook error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        response = VoiceResponse()
        response.hangup()
        return Response(content=str(response), media_type="application/xml")