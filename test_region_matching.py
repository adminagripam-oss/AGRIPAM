import json

with open(r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\data_kebun_tk.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Login region names from login.html select
login_regions = [
  'Aceh', 'Sumatera Utara 1', 'Sumatera Utara 2 Ex Torganda', 'Riau 1', 'Riau 2', 'Riau 3', 'Riau 4',
  'Bangka Belitung', 'Jambi', 'Sumatera Barat', 'Sumatera Selatan',
  'Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2',
  'Kalimantan Selatan 1', 'Kalimantan Selatan 2', 'Kalimantan Timur', 'Kalimantan Utara',
  'Kalimantan Tengah 1', 'Kalimantan Tengah 2', 'Kalimantan Tengah 3',
  'Sulawesi Tenggara', 'Sulawesi Tengah', 'Papua Selatan'
]

# Unique raw regions in data
excel_regions = sorted(list(set(item['region'] for item in data)))
print("Distinct regions in DATA KONTOL.xlsx JSON:", excel_regions)
print("-" * 70)

def norm(s):
    if not s: return ''
    s = s.upper().replace('REGIONAL ', '').replace('RO ', '').strip()
    if 'SUMUT 1' in s or 'SUMATERA UTARA 1' in s: return 'SUMUT 1'
    if 'SUMUT 2' in s or 'SUMATERA UTARA 2' in s or 'TORGANDA' in s: return 'SUMUT 2'
    if 'KALBAR 1A' in s or 'KALIMANTAN BARAT 1A' in s: return 'KALBAR 1A'
    if 'KALBAR 1B' in s or 'KALIMANTAN BARAT 1B' in s: return 'KALBAR 1B'
    if 'KALBAR 1' in s or 'KALIMANTAN BARAT 1' in s: return 'KALBAR 1'
    if 'KALBAR 2' in s or 'KALIMANTAN BARAT 2' in s: return 'KALBAR 2'
    if 'KALSEL 1' in s or 'KALIMANTAN SELATAN 1' in s: return 'KALSEL 1'
    if 'KALSEL 2' in s or 'KALIMANTAN SELATAN 2' in s: return 'KALSEL 2'
    if 'KALTARA' in s or 'KALIMANTAN UTARA' in s: return 'KALTARA'
    if 'KALTIM' in s or 'KALIMANTAN TIMUR' in s: return 'KALTIM'
    if 'KALTENG 1' in s or 'KALIMANTAN TENGAH 1' in s: return 'KALTENG 1'
    if 'KALTENG 2' in s or 'KALIMANTAN TENGAH 2' in s: return 'KALTENG 2'
    if 'KALTENG 3' in s or 'KALIMANTAN TENGAH 3' in s: return 'KALTENG 3'
    if 'BABEL' in s or 'BANGKA BELITUNG' in s: return 'BABEL'
    if 'SUMBAR' in s or 'SUMATERA BARAT' in s: return 'SUMBAR'
    if 'SUMSEL' in s or 'SUMATERA SELATAN' in s: return 'SUMSEL'
    if 'SULTENG' in s or 'SULAWESI TENGAH' in s: return 'SULTENG'
    if 'SULTRA' in s or 'SULAWESI TENGGARA' in s: return 'SULTRA'
    if 'PAPUA' in s: return 'PAPUA SELATAN'
    return s

total_matched = 0
for lr in login_regions:
    n_lr = norm(lr)
    matched = [item for item in data if norm(item['region']) == n_lr or (len(n_lr) > 3 and (n_lr in norm(item['region']) or norm(item['region']) in n_lr))]
    total_matched += len(matched)
    print(f"Login: \"{lr:<30}\" -> Norm: \"{n_lr:<15}\" -> Matches: {len(matched)} kebun")

print("-" * 70)
print(f"Total matched kebun entries: {total_matched} out of {len(data)}")

