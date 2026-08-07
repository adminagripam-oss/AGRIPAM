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

    # Fix { region: 'Kalimantan Barat 1A', 'Kalimantan Barat 1B', tonase: 612.8, color: '#d97706' }
    content = re.sub(
        r"\{\s*region:\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',\s*tonase:\s*612\.8,\s*color:\s*'#d97706'\s*\},",
        r"{ region: 'Kalimantan Barat 1A', tonase: 306.4, color: '#d97706' }, { region: 'Kalimantan Barat 1B', tonase: 306.4, color: '#fbbf24' },",
        content
    )

    # Fix { rank: 3, region: 'Kalimantan Barat 1A', 'Kalimantan Barat 1B', tonase: 612.8, pct: 68 }
    content = re.sub(
        r"\{\s*rank:\s*3,\s*region:\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',\s*tonase:\s*612\.8,\s*pct:\s*68\s*\},",
        r"{ rank: 3, region: 'Kalimantan Barat 1A', tonase: 306.4, pct: 68 }, { rank: 4, region: 'Kalimantan Barat 1B', tonase: 306.4, pct: 68 },",
        content
    )

    # Fix { rank: 3, region: 'Kalimantan Barat 1A', 'Kalimantan Barat 1B', restan: 718.3, pct: 58 }
    content = re.sub(
        r"\{\s*rank:\s*3,\s*region:\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',\s*restan:\s*718\.3,\s*pct:\s*58\s*\},",
        r"{ rank: 3, region: 'Kalimantan Barat 1A', restan: 359.1, pct: 58 }, { rank: 4, region: 'Kalimantan Barat 1B', restan: 359.2, pct: 58 },",
        content
    )
    
    # Are there any other occurrences of "'Kalimantan Barat 1A', 'Kalimantan Barat 1B'," inside objects?
    content = re.sub(
        r"region:\s*'Kalimantan Barat 1A',\s*'Kalimantan Barat 1B',",
        r"region: 'Kalimantan Barat 1A',",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed syntax in {filepath}")

for f in files_to_update:
    fix_in_file(f)
