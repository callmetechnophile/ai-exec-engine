import urllib.request
import json
import time
import ssl

url = "https://66.33.22.230/api/advance-research"
payload = {
    "query": "remote controlled car",
    "components": [],
    "budget": 1000,
    "complexity": "Medium",
    "time": "1 Month"
}

data = json.dumps(payload).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "Host": "ai-exec-engine-production.up.railway.app"
}

req = urllib.request.Request(url, data=data, headers=headers)
context = ssl._create_unverified_context()

try:
    print("Sending POST request to:", url)
    start = time.time()
    with urllib.request.urlopen(req, timeout=120, context=context) as response:
        print("Status:", response.status)
        res_data = response.read().decode("utf-8")
        print("Response:", res_data[:500] + "..." if len(res_data) > 500 else res_data)
        print(f"Time taken: {time.time() - start:.2f}s")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print("Error body:", e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {str(e)}")
