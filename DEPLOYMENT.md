# Deployment Instructions - Realtor Feedback System

## 🚀 Backend Deployment (Render)

### Step 1: Push to GitHub
```bash
cd "/Users/josephesfandiari/Realtor Phone Call App"
git init
git add .
git commit -m "Initial commit - Realtor Feedback System"
```

Create a new repository on GitHub, then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/realtor-feedback.git
git push -u origin main
```

### Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `realtor-feedback-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. Add Environment Variables (in Render dashboard):
   - `OPENAI_API_KEY`: your OpenAI key
   - `TWILIO_ACCOUNT_SID`: your Twilio SID
   - `TWILIO_AUTH_TOKEN`: your Twilio token
   - `TWILIO_PHONE_NUMBER`: your Twilio number
   - `WEBHOOK_BASE_URL`: https://realtor-feedback-api.onrender.com (will be your Render URL)

6. Click "Create Web Service"
7. Copy your Render URL (e.g., `https://realtor-feedback-api.onrender.com`)

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Add Environment Variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://realtor-feedback-api.onrender.com` (your Render backend URL)

6. Click "Deploy"

---

## 📱 Update Twilio Webhook

After both deployments:

1. Go to Twilio Console
2. Update webhook URL in your config to point to Render:
   - Old: `https://[ngrok].ngrok-free.dev/webhook`
   - New: `https://realtor-feedback-api.onrender.com/webhook`

---

## ✅ Testing

1. Visit your Vercel URL (e.g., `https://realtor-feedback.vercel.app`)
2. Enter a phone number
3. Click "Trigger Test Call"
4. Answer the call and provide feedback
5. Wait 30 seconds and refresh - feedback should appear!

---

## 🎯 For Tomorrow's Presentation

**Frontend URL**: Your Vercel deployment URL  
**Backend API**: Your Render deployment URL  
**Live Demo**: Make a test call during presentation

**Key Features to Showcase**:
- ✅ Automated phone calls via Twilio
- ✅ AI transcription with OpenAI Whisper
- ✅ Sentiment analysis with GPT-3.5
- ✅ Real-time dashboard with charts
- ✅ Full CRUD API for clients/agents/feedback

---

## 🔧 Troubleshooting

**If backend fails to start on Render**:
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure requirements.txt has all dependencies

**If frontend can't connect**:
- Verify NEXT_PUBLIC_API_URL is set correctly
- Check CORS settings in backend allow your Vercel domain

**Database**:
- SQLite will work on Render (persists in `/opt/render/project/src`)
- For production, consider PostgreSQL (Render has free tier)

---

## 📝 Notes

- **Free Tier Limits**: 
  - Render: 750 hours/month, sleeps after 15 min inactivity
  - Vercel: Unlimited deployments
  
- **Cold Starts**: First request may take 30s if service was sleeping

- **Database**: Current SQLite setup works but consider PostgreSQL for production
