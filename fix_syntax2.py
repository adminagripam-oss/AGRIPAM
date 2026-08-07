import os
import re

files_to_update = [
    'login.html',
    'loginPANDUAN.html',
    'table-modal-fullscreen.html',
    'admin.html',
    'admin-screenshot.html',
    'FORMAT_ESTIMASI_PANEN.html',
    'laporan_produksi.html',
    'rekap-cro-fullscreen.html'
]

def fix_in_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix: 'kalbar 1': 'Kalimantan Barat 1A', 'Kalimantan Barat 1B',
    # We want it to be:
    # 'kalbar 1a': 'Kalimantan Barat 1A', 'kalbar 1b': 'Kalimantan Barat 1B', 'kalbar 1': 'Kalimantan Barat 1A',
    
    content = re.sub(
        r"'kalbar 1':\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',",
        r"'kalbar 1a': 'Kalimantan Barat 1A', 'kalbar 1b': 'Kalimantan Barat 1B', 'kalbar 1': 'Kalimantan Barat 1A',",
        content
    )

    content = re.sub(
        r"'kalbar 1 ex duta palma':\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',",
        r"'kalbar 1 ex duta palma': 'Kalimantan Barat 1A',",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

for f in files_to_update:
    fix_in_file(f)
