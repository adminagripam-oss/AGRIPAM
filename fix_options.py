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

def fix_in_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the typo <option value="Kalimantan Barat 1A">Kalimantan Barat 1B</option>
    content = re.sub(
        r'<option\s+value="Kalimantan Barat 1A"([^>]*)>Kalimantan Barat 1B</option>',
        r'<option value="Kalimantan Barat 1B"\g<1>>Kalimantan Barat 1B</option>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

for f in files_to_update:
    fix_in_file(f)
