import requests
import json

# Your Render backend URL
API_URL = "https://realtor-phone-call.onrender.com"

# Create agents
agents_data = [
    {"name": "Sarah Johnson", "brokerage": "Premier Realty"},
    {"name": "Michael Chen", "brokerage": "Luxury Homes Group"}
]

# Create clients
clients_data = [
    {"name": "Emily Rodriguez", "phone": "+14155551234", "email": "emily.r@email.com"},
    {"name": "David Thompson", "phone": "+14155555678", "email": "david.t@email.com"},
    {"name": "Jennifer Park", "phone": "+14155559012", "email": "jennifer.p@email.com"},
    {"name": "Robert Martinez", "phone": "+14155553456", "email": "robert.m@email.com"}
]

# Create agents
agent_ids = []
for agent_data in agents_data:
    response = requests.post(f"{API_URL}/agents/", json=agent_data)
    if response.status_code == 200:
        agent_ids.append(response.json()['id'])
        print(f"✅ Created agent: {agent_data['name']}")
    else:
        print(f"❌ Failed to create agent: {response.text}")

# Create clients
client_ids = []
for client_data in clients_data:
    response = requests.post(f"{API_URL}/clients/", json=client_data)
    if response.status_code == 200:
        client_ids.append(response.json()['id'])
        print(f"✅ Created client: {client_data['name']}")
    else:
        print(f"❌ Failed to create client: {response.text}")

# Create calls
calls_data = [
    {"client_id": client_ids[0], "agent_id": agent_ids[0], "twilio_sid": "CA_demo_1", "transcript": "The agent was amazing! Very professional and responsive."},
    {"client_id": client_ids[1], "agent_id": agent_ids[0], "twilio_sid": "CA_demo_2", "transcript": "Good service overall, but could have been more proactive."},
    {"client_id": client_ids[2], "agent_id": agent_ids[1], "twilio_sid": "CA_demo_3", "transcript": "Excellent experience! Made the whole process smooth and stress-free."},
    {"client_id": client_ids[3], "agent_id": agent_ids[1], "twilio_sid": "CA_demo_4", "transcript": "Agent was knowledgeable but communication could be better."}
]

call_ids = []
for call_data in calls_data:
    response = requests.post(f"{API_URL}/calls/", json=call_data)
    if response.status_code == 200:
        call_ids.append(response.json()['id'])
        print(f"✅ Created call for client {call_data['client_id']}")
    else:
        print(f"❌ Failed to create call: {response.text}")

# Create feedback
feedbacks_data = [
    {
        "client_id": client_ids[0], "agent_id": agent_ids[0], "call_id": call_ids[0],
        "sentiment": "Positive", "rating": 9.5,
        "summary": "Client praised agent for exceptional professionalism and responsiveness throughout the entire home buying process.",
        "action_items": json.dumps(["Continue maintaining high level of communication", "Share success story as testimonial"])
    },
    {
        "client_id": client_ids[1], "agent_id": agent_ids[0], "call_id": call_ids[1],
        "sentiment": "Neutral", "rating": 7.0,
        "summary": "Client satisfied with service but suggested more proactive updates during the transaction process.",
        "action_items": json.dumps(["Implement weekly status update calls", "Set up automated milestone notifications"])
    },
    {
        "client_id": client_ids[2], "agent_id": agent_ids[1], "call_id": call_ids[2],
        "sentiment": "Positive", "rating": 10.0,
        "summary": "Outstanding experience with agent who made the complex process feel effortless and manageable.",
        "action_items": json.dumps(["Request referral", "Feature in marketing materials"])
    },
    {
        "client_id": client_ids[3], "agent_id": agent_ids[1], "call_id": call_ids[3],
        "sentiment": "Neutral", "rating": 6.5,
        "summary": "Agent demonstrated strong market knowledge but response times to inquiries could be improved.",
        "action_items": json.dumps(["Review communication protocols", "Consider adding support staff"])
    }
]

for feedback_data in feedbacks_data:
    response = requests.post(f"{API_URL}/feedbacks/", json=feedback_data)
    if response.status_code == 200:
        print(f"✅ Created feedback for client {feedback_data['client_id']}")
    else:
        print(f"❌ Failed to create feedback: {response.text}")

print("\n🎉 Demo data setup complete!")
