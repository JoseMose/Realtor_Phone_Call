'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isCalling, setIsCalling] = useState(false);
  const [callStatus, setCallStatus] = useState('');
  const [feedbackData, setFeedbackData] = useState<any[]>([]);
  const [agentRatings, setAgentRatings] = useState<any[]>([]);
  const [sentimentData, setSentimentData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchFeedbackData();
  }, []);

  const fetchFeedbackData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/feedbacks/`);
      const feedbacks = await response.json();
      
      // Fetch clients and agents to join the data
      const clientsResponse = await fetch(`${apiUrl}/clients/`);
      const clients = await clientsResponse.json();
      
      const agentsResponse = await fetch(`${apiUrl}/agents/`);
      const agents = await agentsResponse.json();
      
      // Join feedback with client and agent names
      const enrichedFeedback = feedbacks.map((feedback: any) => {
        const client = clients.find((c: any) => c.id === feedback.client_id);
        const agent = agents.find((a: any) => a.id === feedback.agent_id);
        return {
          ...feedback,
          client_name: client?.name || 'Unknown',
          agent_name: agent?.name || 'Unknown',
          action_items: feedback.action_items ? JSON.parse(feedback.action_items) : []
        };
      });
      
      setFeedbackData(enrichedFeedback);
      
      // Calculate agent ratings
      const agentRatingMap = new Map<number, { name: string, total: number, count: number }>();
      enrichedFeedback.forEach((feedback: any) => {
        if (feedback.rating != null && feedback.agent_id) {
          const existing = agentRatingMap.get(feedback.agent_id) || { name: feedback.agent_name, total: 0, count: 0 };
          existing.total += feedback.rating;
          existing.count += 1;
          agentRatingMap.set(feedback.agent_id, existing);
        }
      });
      
      const ratings = Array.from(agentRatingMap.values()).map(({ name, total, count }) => ({
        name,
        rating: Number((total / count).toFixed(2))
      }));
      setAgentRatings(ratings);
      
      // Calculate sentiment distribution
      const sentimentMap = new Map<string, number>();
      enrichedFeedback.forEach((feedback: any) => {
        const sentiment = feedback.sentiment || 'Neutral';
        sentimentMap.set(sentiment, (sentimentMap.get(sentiment) || 0) + 1);
      });
      
      const sentimentColors: { [key: string]: string } = {
        'Positive': '#00C49F',
        'Neutral': '#FFBB28',
        'Negative': '#FF8042'
      };
      
      const sentiments = Array.from(sentimentMap.entries()).map(([name, value]) => ({
        name,
        value,
        color: sentimentColors[name] || '#999999'
      }));
      setSentimentData(sentiments);
      
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching feedback data:', error);
      setIsLoading(false);
    }
  };

  const handleTestCall = async () => {
    if (!phoneNumber.trim()) {
      setCallStatus('Please enter a phone number');
      return;
    }

    setIsCalling(true);
    setCallStatus('Initiating call...');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/test-call`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          phone_number: phoneNumber
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        setCallStatus(`Call initiated! SID: ${data.call_sid}`);
        // Refresh feedback data after a delay to allow time for the call to complete
        setTimeout(() => {
          fetchFeedbackData();
        }, 30000); // Refresh after 30 seconds
      } else {
        setCallStatus(`Error: ${data.detail || 'Failed to initiate call'}`);
      }
    } catch (error) {
      setCallStatus('Error: Could not connect to backend');
    } finally {
      setIsCalling(false);
    }
  };

  return (
    <div className="min-h-screen bg-white p-8">
      <h1 className="text-3xl font-bold mb-8 text-black">Realtor Feedback Dashboard</h1>

      {isLoading ? (
        <div className="text-center py-8">
          <p className="text-black">Loading feedback data...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-semibold mb-4 text-black">Average Ratings by Agent</h2>
              {agentRatings.length > 0 ? (
                <BarChart width={400} height={300} data={agentRatings}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 10]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="rating" fill="#8884d8" />
                </BarChart>
              ) : (
                <p className="text-black">No agent ratings available yet.</p>
              )}
            </div>

            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-semibold mb-4 text-black">Sentiment Distribution</h2>
              {sentimentData.length > 0 ? (
                <PieChart width={400} height={300}>
                  <Pie
                    data={sentimentData}
                    cx={200}
                    cy={150}
                    labelLine={false}
                    label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              ) : (
                <p className="text-black">No sentiment data available yet.</p>
              )}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow border">
            <h2 className="text-xl font-semibold mb-4 text-black">Client Feedback</h2>
            {feedbackData.length > 0 ? (
              <div className="space-y-4">
                {feedbackData.map((feedback, index) => (
                  <div key={index} className="border p-4 rounded bg-gray-50">
                    <h3 className="font-semibold text-black">{feedback.client_name} - {feedback.agent_name}</h3>
                    <p className="text-sm text-black">
                      Sentiment: {feedback.sentiment} 
                      {feedback.rating != null && ` | Rating: ${feedback.rating}/10`}
                    </p>
                    <p className="mt-2 text-black">{feedback.summary}</p>
                    {feedback.action_items.length > 0 && (
                      <ul className="mt-2 list-disc list-inside">
                        {feedback.action_items.map((item: string, i: number) => (
                          <li key={i} className="text-sm text-black">{item}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-black">No feedback data available yet. Make a test call to see results here!</p>
            )}
          </div>
        </>
      )}

      <div className="mt-8 bg-white p-6 rounded-lg shadow border">
        <h2 className="text-xl font-semibold mb-4 text-black">Test Call Feature</h2>
        <p className="text-black mb-4">
          Enter your phone number to hear what the automated feedback call sounds like.
          The call will ask about your experience with a realtor.
        </p>
        <div className="flex gap-4 items-center">
          <input
            type="tel"
            placeholder="+17701234567"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            disabled={isCalling}
          />
          <button
            onClick={handleTestCall}
            disabled={isCalling}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isCalling ? 'Calling...' : 'Trigger Test Call'}
          </button>
        </div>
        {callStatus && (
          <p className={`mt-4 text-sm ${callStatus.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
            {callStatus}
          </p>
        )}
      </div>
    </div>
  );
}
