import json
import urllib.request

url = "http://localhost:3000/api/kebunTK"

# 1. Fetch Aceh region data
req_get = urllib.request.Request(f"{url}?region=Aceh", method="GET")
with urllib.request.urlopen(req_get) as response:
    data_before = json.loads(response.read().decode())

sample_kebun = data_before["data"][0]
kebun_id = sample_kebun["id"]
orig_juli = sample_kebun.get("tk_juli", 0)

print(f"Sample Kebun ID {kebun_id} ({sample_kebun['nama_kebun']}): Original TK Juli = {orig_juli}")

# 2. Perform edit via POST updateTK
payload = {
    "action": "updateTK",
    "region": "Aceh",
    "token": "valid_token",
    "edits": [
        {
            "id": kebun_id,
            "tk_juli": (orig_juli + 1) if orig_juli < sample_kebun.get("req_tk", 10) else 0
        }
    ]
}

data_bytes = json.dumps(payload).encode('utf-8')
req_post = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(req_post) as response:
    result_post = json.loads(response.read().decode())

print("POST Update Result:", result_post)

# 3. Verify read back from database
req_get_after = urllib.request.Request(f"{url}?region=Aceh", method="GET")
with urllib.request.urlopen(req_get_after) as response:
    data_after = json.loads(response.read().decode())

updated_kebun = next(k for k in data_after["data"] if k["id"] == kebun_id)
print(f"Verified Database Read-back: Kebun ID {kebun_id} TK Juli is now = {updated_kebun.get('tk_juli')}")

# 4. Revert edit back to original value
payload_revert = {
    "action": "updateTK",
    "region": "Aceh",
    "token": "valid_token",
    "edits": [
        {
            "id": kebun_id,
            "tk_juli": orig_juli
        }
    ]
}
data_revert = json.dumps(payload_revert).encode('utf-8')
req_revert = urllib.request.Request(url, data=data_revert, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req_revert) as response:
    res_revert = json.loads(response.read().decode())

print("Reverted sample data back to original state cleanly:", res_revert["success"])
