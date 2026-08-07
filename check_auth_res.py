import json
import urllib.request

login_url = "http://localhost:3000/api/auth"
login_payload = json.dumps({"action": "login", "region": "Aceh", "password": "ROACEH"}).encode('utf-8')
login_req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(login_req) as resp:
    res = json.loads(resp.read().decode())

print("Auth response:", res)
