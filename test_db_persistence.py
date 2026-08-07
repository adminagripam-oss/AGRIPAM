import json
import urllib.request

# 1. Login as Aceh to get valid token
login_url = "http://localhost:3000/api/auth"
login_payload = json.dumps({"action": "login", "region": "Aceh", "password": "ROACEH"}).encode('utf-8')
login_req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(login_req) as resp:
    login_res = json.loads(resp.read().decode())

token = login_res["token"]

# 2. GET Kebun TK Data for Aceh with action=getKebun
tk_url = f"http://localhost:3000/api/kebunTK?action=getKebun&region=Aceh&token={token}"
get_req = urllib.request.Request(tk_url, method="GET")

with urllib.request.urlopen(get_req) as resp:
    get_res = json.loads(resp.read().decode())

kebun_list = get_res["data"]
# Select kebun with req_tk > 0
sample_kebun = next(k for k in kebun_list if k.get("req_tk", 0) > 0)
kebun_id = sample_kebun["id"]
orig_juli = sample_kebun.get("tk_juli", 0)
req_tk = sample_kebun.get("req_tk", 0)

test_new_val = min(3, req_tk)

print(f"Testing Kebun ID {kebun_id} ({sample_kebun['nama_kebun']}): Req TK = {req_tk}, Original TK Juli = {orig_juli}, Updating to = {test_new_val}")

# 3. POST Edit Update
edit_url = "http://localhost:3000/api/kebunTK"
edit_payload = json.dumps({
    "action": "updateTK",
    "region": "Aceh",
    "token": token,
    "edits": [
        {
            "id": kebun_id,
            "tk_juli": test_new_val
        }
    ]
}).encode('utf-8')

edit_req = urllib.request.Request(edit_url, data=edit_payload, headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(edit_req) as resp:
    edit_res = json.loads(resp.read().decode())

print("POST Edit Update Response:", edit_res)

# 4. Verify Database Persistence Read-Back
with urllib.request.urlopen(get_req) as resp:
    read_back_res = json.loads(resp.read().decode())

updated_kebun = next(k for k in read_back_res["data"] if k["id"] == kebun_id)
print(f"Verified Database Persistence Read-Back: Kebun ID {kebun_id} TK Juli is now = {updated_kebun.get('tk_juli')}")

assert updated_kebun.get('tk_juli') == test_new_val, "Database Persistence Test Failed!"

# 5. Revert back to original value
revert_payload = json.dumps({
    "action": "updateTK",
    "region": "Aceh",
    "token": token,
    "edits": [
        {
            "id": kebun_id,
            "tk_juli": orig_juli
        }
    ]
}).encode('utf-8')

revert_req = urllib.request.Request(edit_url, data=revert_payload, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(revert_req) as resp:
    revert_res = json.loads(resp.read().decode())

print("Clean Revert Status:", revert_res["success"])
print("\n>>> DATABASE PERSISTENCE END-TO-END VERIFICATION FULLY PASSED! <<<")
