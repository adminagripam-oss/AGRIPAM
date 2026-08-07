# -*- coding: utf-8 -*-
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

def replace_in_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace <option> tags
    content = re.sub(
        r'(<option\s+value="Kalimantan Barat 1"[^>]*>)\s*Kalimantan Barat 1\s*(</option>)',
        r'\g<1>Kalimantan Barat 1A\g<2>\n' +
        r'\g<1>'.replace('"Kalimantan Barat 1"', '"Kalimantan Barat 1B"') + r'Kalimantan Barat 1B\g<2>',
        content
    )

    # 2. Replace array list: "Kalimantan Barat 1", "Kalimantan Barat 2"
    content = re.sub(
        r'"Kalimantan Barat 1"(?=\s*,)',
        r'"Kalimantan Barat 1A", "Kalimantan Barat 1B"',
        content
    )
    content = re.sub(
        r"'Kalimantan Barat 1'(?=\s*,)",
        r"'Kalimantan Barat 1A', 'Kalimantan Barat 1B'",
        content
    )
    
    # 3. Handle specific keys in dictionaries
    content = re.sub(
        r'"Kalimantan Barat 1":\s*77956\s*,',
        r'"Kalimantan Barat 1A": 38978, "Kalimantan Barat 1B": 38978,',
        content
    )
    content = re.sub(
        r'"Kalimantan Barat 1":\s*2800\s*,',
        r'"Kalimantan Barat 1A": 1400, "Kalimantan Barat 1B": 1400,',
        content
    )

    # laporan_produksi.html replacements
    content = re.sub(
        r"\{\s*region:\s*'Kalimantan Barat 1',\s*tonase:\s*612\.8,\s*color:\s*'#d97706'\s*\},",
        r"{ region: 'Kalimantan Barat 1A', tonase: 306.4, color: '#d97706' }, { region: 'Kalimantan Barat 1B', tonase: 306.4, color: '#fbbf24' },",
        content
    )
    content = re.sub(
        r"\{\s*rank:\s*3,\s*region:\s*'Kalimantan Barat 1',\s*tonase:\s*612\.8,\s*pct:\s*68\s*\},",
        r"{ rank: 3, region: 'Kalimantan Barat 1A', tonase: 306.4, pct: 68 }, { rank: 4, region: 'Kalimantan Barat 1B', tonase: 306.4, pct: 68 },",
        content
    )
    content = re.sub(
        r"\{\s*rank:\s*3,\s*region:\s*'Kalimantan Barat 1',\s*restan:\s*718\.3,\s*pct:\s*58\s*\},",
        r"{ rank: 3, region: 'Kalimantan Barat 1A', restan: 359.1, pct: 58 }, { rank: 4, region: 'Kalimantan Barat 1B', restan: 359.2, pct: 58 },",
        content
    )
    
    content = re.sub(
        r"\{\s*region:\s*'Kalimantan Barat 1',\s*shortLabel:\s*'Kalbar 1',\s*estimasi:\s*900,\s*realisasi:\s*613,\s*restan:\s*718\.3,\s*tonase:\s*612\.8,\s*color:\s*'#d97706'\s*\},",
        r"{ region: 'Kalimantan Barat 1A', shortLabel: 'Kalbar 1A', estimasi: 450, realisasi: 306, restan: 359, tonase: 306.4, color: '#d97706' }, { region: 'Kalimantan Barat 1B', shortLabel: 'Kalbar 1B', estimasi: 450, realisasi: 307, restan: 359, tonase: 306.4, color: '#fbbf24' },",
        content
    )
    
    content = re.sub(
        r"'Kalimantan Barat 1':\s*\{\s*shortLabel:\s*'Kalbar 1',\s*color:\s*'#d97706'\s*\},",
        r"'Kalimantan Barat 1A': { shortLabel: 'Kalbar 1A', color: '#d97706' }, 'Kalimantan Barat 1B': { shortLabel: 'Kalbar 1B', color: '#fbbf24' },",
        content
    )

    content = re.sub(
        r"'kalbar 1':\s*'Kalimantan Barat 1',",
        r"'kalbar 1a': 'Kalimantan Barat 1A', 'kalbar 1b': 'Kalimantan Barat 1B', 'kalbar 1': 'Kalimantan Barat 1A',",
        content
    )
    
    content = re.sub(
        r"'kalbar 1 ex duta palma':\s*'Kalimantan Barat 1',",
        r"'kalbar 1 ex duta palma': 'Kalimantan Barat 1A',",
        content
    )

    content = re.sub(
        r'\{\s*label:\s*"Kalbar 1 Ex Duta Palma",\s*regionKey:\s*"Kalimantan Barat 1",\s*excelKey:\s*"Kalbar 1",\s*luas:\s*77955\.99,\s*target:\s*1750,\s*type:\s*"detail"\s*\},',
        r'{ label: "Kalbar 1A Ex Duta Palma", regionKey: "Kalimantan Barat 1A", excelKey: "Kalbar 1A", luas: 38978, target: 875, type: "detail" }, { label: "Kalbar 1B", regionKey: "Kalimantan Barat 1B", excelKey: "Kalbar 1B", luas: 38978, target: 875, type: "detail" },',
        content
    )

    content = re.sub(
        r'"Kalimantan Barat 1"(?!A|B)',
        r'"Kalimantan Barat 1A"',
        content
    )
    content = re.sub(
        r"'Kalimantan Barat 1'(?!A|B)",
        r"'Kalimantan Barat 1A'",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

for f in files_to_update:
    replace_in_file(f)
