#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_api():
    try:
        # Test root
        response = requests.get(f'{BASE_URL}/')
        print(f'Root endpoint: {response.status_code} - {response.json()}')

        # Create agent
        agent_data = {'name': 'David Lopez', 'brokerage': 'ABC Realty'}
        response = requests.post(f'{BASE_URL}/agents/', json=agent_data)
        print(f'Create agent: {response.status_code} - {response.json()}')

        # Create client
        client_data = {'name': 'Jane Smith', 'phone': '+15551234568', 'email': 'jane@example.com'}
        response = requests.post(f'{BASE_URL}/clients/', json=client_data)
        print(f'Create client: {response.status_code} - {response.json()}')

        # Test analysis
        analysis_data = {'transcript': 'The agent was very helpful and responsive.'}
        response = requests.post(f'{BASE_URL}/analyze', json=analysis_data)
        print(f'Analyze transcript: {response.status_code}')
        if response.status_code == 200:
            print(f'Analysis result: {response.json()}')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    test_api()