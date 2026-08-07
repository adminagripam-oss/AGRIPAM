import urllib.request
import json

url = "https://wcocmwkccntmmtlofowe.supabase.co/rest/v1/data_kebun_tk?select=*"

req = urllib.request.Request(url)
req.add_header("apikey", "sb_secret_vjLgbKDiOGGCw8GGfLb53Q_a2Rr8jp0")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"SUCCESS! Retrieved {len(data)} rows directly from Supabase Cloud data_kebun_tk table!")
        if len(data) > 0:
            print("First row sample:", data[0])
except Exception as e:
    print(f"Supabase REST query result: {e}")
