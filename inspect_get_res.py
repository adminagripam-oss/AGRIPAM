import json
import urllib.request

url = "http://localhost:3000/api/kebunTK?region=Aceh"
req = urllib.request.Request(url, method="GET")
with urllib.request.urlopen(req) as response:
    res = json.loads(response.read().decode())

print("GET Response Keys:", res.keys())
if "kebunData" in res:
    print("Kebun count:", len(res["kebunData"]))
    print("Sample Kebun:", res["kebunData"][0])
