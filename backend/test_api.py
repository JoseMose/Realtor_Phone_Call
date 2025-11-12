#!/usr/bin/env python3
import requests
import time

# Wait for server to start
time.sleep(2)

try:
    # Test root endpoint
    response = requests.get('http://127.0.0.1:8000/')
    print(f"Root endpoint: {response.status_code} - {response.json()}")

    # Test test-call endpoint
    response = requests.post(
        'http://127.0.0.1:8000/test-call',
        data={'phone_number': '+1234567890'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    print(f"Test-call endpoint: {response.status_code} - {response.json()}")

except Exception as e:
    print(f"Error: {e}")