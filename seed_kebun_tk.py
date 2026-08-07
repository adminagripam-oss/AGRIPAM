import zipfile
import xml.etree.ElementTree as ET
import json
import os

xlsx_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\DATA KONTOL.xlsx'
out_json_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\data_kebun_tk.json'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
        ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        for si in tree.findall('.//s:si', ns):
            t_elems = si.findall('.//s:t', ns)
            text = "".join([t.text or "" for t in t_elems])
            shared_strings.append(text)

    s_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    def to_num(val):
        if val is None or val == '-' or val == 'Tidak Ditemukan':
            return 0.0
        try:
            return round(float(val), 2)
        except:
            return 0.0

    kebun_list = []
    item_id = 1

    for row in s_tree.findall('.//s:row', ns):
        r_idx = int(row.attrib['r'])
        if r_idx == 1: continue # Skip header
        
        row_dict = {}
        for c in row.findall('./s:c', ns):
            col_ref = c.attrib['r']
            col_letter = "".join([char for char in col_ref if char.isalpha()])
            t_type = c.attrib.get('t')
            v_elem = c.find('./s:v', ns)
            val = v_elem.text if v_elem is not None else None
            if t_type == 's' and val is not None:
                val = shared_strings[int(val)]
            row_dict[col_letter] = val

        cro = (row_dict.get('A') or '').strip()
        reg_raw = (row_dict.get('B') or '').strip()
        nama_kebun = (row_dict.get('C') or '').strip()
        name_tag = (row_dict.get('D') or '').strip()

        if not reg_raw or not nama_kebun:
            continue

        # Clean region string (remove "Regional " prefix for matching)
        reg_clean = reg_raw.replace("Regional ", "").strip()

        kebun_item = {
            "id": item_id,
            "cro": cro,
            "region_raw": reg_raw,
            "region": reg_clean,
            "nama_kebun": nama_kebun,
            "name_tag": name_tag,
            "luasan": to_num(row_dict.get('E')),
            "req_tk": to_num(row_dict.get('F')),
            "tk_mei": to_num(row_dict.get('G')),
            "tk_juni": to_num(row_dict.get('H')),
            "tk_juli": to_num(row_dict.get('I')),       # Kolom I (Red)
            "tk_agustus": to_num(row_dict.get('J')),    # Kolom J (Red)
            "target_juli": to_num(row_dict.get('K')),   # Kolom K (Yellow)
            "target_agustus": to_num(row_dict.get('L')),# Kolom L (Yellow)
            "updated_by": None,
            "updated_at": None
        }

        kebun_list.append(kebun_item)
        item_id += 1

    print(f"Total extracted kebun entries: {len(kebun_list)}")
    with open(out_json_path, 'w', encoding='utf-8') as f:
        json.dump(kebun_list, f, indent=2, ensure_ascii=False)

    print(f"Saved to {out_json_path}")

