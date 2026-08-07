import json
import urllib.request

login_url = "http://localhost:3000/api/auth"
login_payload = json.dumps({"action": "login", "region": "Aceh", "password": "ROACEH"}).encode('utf-8')
login_req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(login_req) as resp:
    login_res = json.loads(resp.read().decode())

token = login_res["token"]

tk_url = f"http://localhost:3000/api/kebunTK?action=getKebun&region=Aceh&token={token}"
get_req = urllib.request.Request(tk_url, method="GET")

with urllib.request.urlopen(get_req) as resp:
    get_res = json.loads(resp.read().decode())

print("GET Kebun Response Keys:", get_res.keys())
