"""
Quick test script to verify backend connection
"""
import requests

API_URL = "https://sentinel-ai-3yc8.onrender.com"

print("Testing Sentinel AI Backend...")
print(f"URL: {API_URL}")
print("-" * 50)

# Test 1: Health check
try:
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Text analysis
try:
    print("\n2. Testing text analysis...")
    response = requests.post(
        f"{API_URL}/analyze/text",
        json={"text": "You won $1000! Click here now!"},
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Verdict: {result.get('verdict')}")
        print(f"   Risk Score: {result.get('risk_score')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "-" * 50)
print("Test complete!")
