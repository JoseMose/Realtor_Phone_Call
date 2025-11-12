# Realtor Feedback System

An AI-powered automated phone feedback system for real estate agents, built with Next.js, FastAPI, Twilio, and OpenAI.

## Features

- 🤖 **Automated Phone Calls**: Twilio-powered calls to collect client feedback
- 🎤 **AI Transcription**: OpenAI Whisper converts speech to text
- 🧠 **Sentiment Analysis**: GPT-3.5 analyzes feedback and extracts insights
- 📊 **Live Dashboard**: Real-time charts showing agent ratings and sentiment
- 📱 **Test Call Feature**: Easy demo functionality for presentations

## Tech Stack

**Frontend**:
- Next.js 15
- React with TypeScript
- Tailwind CSS
- Recharts for visualizations

**Backend**:
- FastAPI (Python)
- SQLAlchemy ORM with SQLite
- OpenAI API (Whisper + GPT-3.5)
- Twilio Voice API

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.13+
- OpenAI API key
- Twilio account with phone number

### Local Development

1. **Clone and setup backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

2. **Setup frontend**:
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev
```

3. **Start ngrok** (for Twilio webhooks):
```bash
ngrok http 8000
# Update WEBHOOK_BASE_URL in backend/.env with ngrok URL
```

4. Visit `http://localhost:3000`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions to Vercel + Render.

## Demo

1. Enter phone number in dashboard
2. Click "Trigger Test Call"
3. Answer automated questions
4. View transcribed feedback with AI analysis

## API Endpoints

- `POST /test-call` - Initiate feedback call
- `POST /webhook` - Twilio recording callback
- `GET /feedbacks` - List all feedback
- `GET /clients` - List all clients
- `GET /agents` - List all agents

## License

MIT

## Features

- Automated calling using Twilio Voice API
- AI conversation flow with natural language processing
- Sentiment analysis and feedback summarization using OpenAI GPT
- Dashboard for viewing analytics and client feedback
- Secure storage with encryption

## Tech Stack

- Frontend: Next.js + Tailwind CSS + Recharts
- Backend: FastAPI (Python) + PostgreSQL + SQLAlchemy
- AI: OpenAI GPT-4 for analysis, Whisper for transcription
- Voice: Twilio Voice API

## Setup

### Backend

1. cd backend
2. source venv/bin/activate
3. Create .env file with:
   ```
   OPENAI_API_KEY=your_openai_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```
4. uvicorn main:app --reload

### Frontend

1. cd frontend
2. npm install
3. npm run dev

## API Endpoints

- GET / - Root
- POST /clients/ - Create client
- GET /clients/ - List clients
- POST /agents/ - Create agent
- GET /agents/ - List agents
- POST /feedbacks/ - Create feedback
- GET /feedbacks/ - List feedbacks
- POST /calls/ - Create call
- GET /calls/ - List calls

## Prototype

The dashboard displays mock data with charts and feedback summaries.

To implement the full phone call flow:
1. Set up Twilio account and get credentials
2. Configure webhook for call recording
3. Implement transcription with Whisper
4. Analyze transcript with GPT
5. Store results in database

## Security

- Voice calls disclose recording
- Data encrypted in storage
- Recordings deleted after 30 days