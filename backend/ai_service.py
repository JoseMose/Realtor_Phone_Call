import os
import json
import requests
from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.openai_api_key)

def analyze_feedback(transcript: str) -> dict:
    prompt = f"""
    Analyze the following conversation transcript from a real estate client feedback call.

    Transcript: {transcript}

    Extract the following in JSON format:
    {{
      "overall_sentiment": "Positive/Negative/Neutral",
      "rating_estimate": number between 1-10,
      "summary": "Brief summary of the feedback",
      "action_items": ["list", "of", "action", "items"]
    }}

    Return only the JSON.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result_text = response.choices[0].message.content.strip()
    # Assume it's JSON
    try:
        result = json.loads(result_text)
        return result
    except:
        return {
            "overall_sentiment": "Neutral",
            "rating_estimate": 5,
            "summary": "Analysis failed",
            "action_items": []
        }

def transcribe_audio(audio_url: str) -> str:
    try:
        print(f"Downloading audio from: {audio_url}")
        
        # Extract recording SID from URL
        # URL format: https://api.twilio.com/2010-04-01/Accounts/AC.../Recordings/RE...
        recording_sid = audio_url.split('/')[-1]
        
        # Use Twilio client to fetch recording
        from twilio.rest import Client
        twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        recording = twilio_client.recordings(recording_sid).fetch()
        
        # Get the recording content
        # recording.uri is a relative path, need to make it a full URL
        full_uri = f"https://api.twilio.com{recording.uri.replace('.json', '')}"
        audio_response = requests.get(full_uri, auth=(settings.twilio_account_sid, settings.twilio_auth_token))
        audio_response.raise_for_status()

        # Use a unique temp file to avoid race conditions
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_response.content)
            temp_filename = temp_file.name

        try:
            with open(temp_filename, "rb") as f:
                transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
            return transcript.text
        finally:
            os.remove(temp_filename)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Error: Could not transcribe audio"