import urllib.request
import json
import urllib.parse

regional_accounts = [
    ("Aceh", "ROACEH"),
    ("Sumatera Utara 1", "ROSUMUT1"),
    ("Sumatera Utara 2 Ex Torganda", "ROSUMUT2"),
    ("Riau 1", "RORiau1"),
    ("Riau 2", "RORiau2"),
    ("Riau 3", "RORiau3"),
    ("Riau 4", "RORiau4"),
    ("Bangka Belitung", "ROBabel"),
    ("Jambi", "ROJ4mb1"),
    ("Sumatera Barat", "ROSumbar"),
    ("Sumatera Selatan", "ROSumsel"),
    ("Kalimantan Barat 1A", "ROKalbar1a"),
    ("Kalimantan Barat 1B", "ROKalbar1B"),
    ("Kalimantan Barat 2", "ROKalbar2"),
    ("Kalimantan Selatan 1", "ROKalsel1"),
    ("Kalimantan Selatan 2", "ROKalsel2"),
    ("Kalimantan Timur", "ROKaltim"),
    ("Kalimantan Utara", "ROKalut"),
    ("Kalimantan Tengah 1", "ROKalteng1"),
    ("Kalimantan Tengah 2", "ROKalteng2"),
    ("Kalimantan Tengah 3", "ROKalteng3"),
    ("Sulawesi Tenggara", "ROSultra"),
    ("Sulawesi Tengah", "ROSulteng"),
    ("ADMIN", "TANAMAN")
]

base_url = "http://localhost:3000"

print("=" * 80)
print(f"{'REGION LOGIN':<30} | {'AUTH STATUS':<12} | {'KEBUN COUNT':<12} | {'KEBUN REGION SAMPLE'}")
print("=" * 80)

total_verified = 0

for region, password in regional_accounts:
    # 1. Test Login
    auth_data = json.dumps({"action": "login", "region": region, "password": password}).encode('utf-8')
    auth_req = urllib.request.Request(f"{base_url}/api/auth", data=auth_data, headers={'Content-Type': 'application/json'})
    
    auth_status = "FAILED"
    token = None
    try:
        with urllib.request.urlopen(auth_req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            if res_json.get('success'):
                auth_status = "SUCCESS"
                token = res_json.get('token')
    except Exception as e:
        auth_status = f"ERROR: {e}"

    # 2. Test TK Panen Data Retrieval
    kebun_url = f"{base_url}/api/kebunTK?action=getKebun&region={urllib.parse.quote(region)}"
    kebun_count = 0
    sample_region = "-"
    try:
        with urllib.request.urlopen(kebun_url) as response:
            kebun_json = json.loads(response.read().decode('utf-8'))
            if kebun_json.get('success'):
                kebun_count = kebun_json.get('totalEntries', 0)
                data = kebun_json.get('data', [])
                if data:
                    sample_region = data[0].get('region', '-')
    except Exception as e:
        sample_region = f"ERROR: {e}"

    print(f"{region:<30} | {auth_status:<12} | {kebun_count:<12} | {sample_region}")
    if auth_status == "SUCCESS" and kebun_count > 0:
        total_verified += 1

print("=" * 80)
print(f"VERIFICATION SUMMARY: {total_verified} / {len(regional_accounts)} Regional Accounts Verified Successfully!")
