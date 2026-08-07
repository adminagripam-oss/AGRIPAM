import json
import re

json_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\data_kebun_tk.json'
sql_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\supabase_setup_data_kebun_tk.sql'

with open(json_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

def clean_sql_str(val):
    if val is None:
        return 'NULL'
    s = str(val).replace("'", "''").strip()
    return f"'{s}'"

sql_lines = []
sql_lines.append("-- ============================================================================")
sql_lines.append("-- AGRIPAM - SUPABASE SQL EDITOR SCRIPT: DATA KEBUN TK PANEN")
sql_lines.append("-- Source Data: DATA KONTOL.xlsx (800 Entri Kebun 23 Regional + ADMIN)")
sql_lines.append("-- Cara Penggunaan:")
sql_lines.append("-- 1. Buka Supabase Dashboard Project Anda -> Menu 'SQL Editor'")
sql_lines.append("-- 2. Copy (Salin) seluruh isi kode SQL ini dan Paste di SQL Editor")
sql_lines.append("-- 3. Klik tombol 'Run' (Jalankan)")
sql_lines.append("-- ============================================================================\n")

sql_lines.append("-- 1. HAPUS TABEL LAMA JIKA ADA")
sql_lines.append("DROP TABLE IF EXISTS data_kebun_tk CASCADE;\n")

sql_lines.append("-- 2. BUAT STRUKTUR TABEL data_kebun_tk")
sql_lines.append("""CREATE TABLE data_kebun_tk (
    id INT PRIMARY KEY,
    cro VARCHAR(50),
    region VARCHAR(100) NOT NULL,
    region_raw VARCHAR(100),
    nama_kebun VARCHAR(255) NOT NULL,
    name_tag VARCHAR(100),
    luasan NUMERIC(10, 2) DEFAULT 0,
    req_tk INT DEFAULT 0,
    tk_mei INT DEFAULT 0,
    tk_juni INT DEFAULT 0,
    target_juli INT DEFAULT 0,
    target_agustus INT DEFAULT 0,
    tk_juli INT DEFAULT 0,
    tk_agustus INT DEFAULT 0,
    updated_by VARCHAR(100) DEFAULT 'SYSTEM',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);\n""")

sql_lines.append("-- 3. BUAT INDEX UNTUK PERFORMA QUERY CEPAT")
sql_lines.append("CREATE INDEX idx_data_kebun_tk_region ON data_kebun_tk(region);")
sql_lines.append("CREATE INDEX idx_data_kebun_tk_cro ON data_kebun_tk(cro);")
sql_lines.append("CREATE INDEX idx_data_kebun_tk_name_tag ON data_kebun_tk(name_tag);\n")

sql_lines.append("-- 4. AKTIFKAN ROW LEVEL SECURITY (RLS) & KEBIJAKAN AKSES PUBLIC")
sql_lines.append("ALTER TABLE data_kebun_tk ENABLE ROW LEVEL SECURITY;")
sql_lines.append("CREATE POLICY \"Allow public select on data_kebun_tk\" ON data_kebun_tk FOR SELECT USING (true);")
sql_lines.append("CREATE POLICY \"Allow public insert on data_kebun_tk\" ON data_kebun_tk FOR INSERT WITH CHECK (true);")
sql_lines.append("CREATE POLICY \"Allow public update on data_kebun_tk\" ON data_kebun_tk FOR UPDATE USING (true);\n")

sql_lines.append("-- 5. INSERT 800 DATA KEBUN DARI DATA KONTOL.xlsx")

# Batch inserts into chunks of 100
chunk_size = 100
for i in range(0, len(items), chunk_size):
    chunk = items[i:i + chunk_size]
    sql_lines.append(f"-- Batch Insert Data Kebun ({i + 1} s/d {i + len(chunk)})")
    sql_lines.append("INSERT INTO data_kebun_tk (id, cro, region, region_raw, nama_kebun, name_tag, luasan, req_tk, tk_mei, tk_juni, target_juli, target_agustus, tk_juli, tk_agustus, updated_by) VALUES")
    
    values_list = []
    for item in chunk:
        item_id = item.get('id', 0)
        cro = clean_sql_str(item.get('cro'))
        region = clean_sql_str(item.get('region'))
        region_raw = clean_sql_str(item.get('region_raw'))
        nama_kebun = clean_sql_str(item.get('nama_kebun'))
        name_tag = clean_sql_str(item.get('name_tag'))
        luasan = item.get('luasan', 0)
        req_tk = item.get('req_tk', 0)
        tk_mei = item.get('tk_mei', 0)
        tk_juni = item.get('tk_juni', 0)
        target_juli = item.get('target_juli', 0)
        target_agustus = item.get('target_agustus', 0)
        tk_juli = item.get('tk_juli', 0)
        tk_agustus = item.get('tk_agustus', 0)
        updated_by = clean_sql_str(item.get('updated_by', 'SYSTEM'))

        val_str = f"({item_id}, {cro}, {region}, {region_raw}, {nama_kebun}, {name_tag}, {luasan}, {req_tk}, {tk_mei}, {tk_juni}, {target_juli}, {target_agustus}, {tk_juli}, {tk_agustus}, {updated_by})"
        values_list.append(val_str)

    sql_lines.append(",\n".join(values_list) + ";\n")

sql_lines.append("-- ============================================================================")
sql_lines.append("-- SELESAI: 800 Data Kebun Berhasil Dibuat dan Di-seed ke Supabase!")
sql_lines.append("-- ============================================================================")

with open(sql_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(sql_lines))

print(f"SUCCESSFULLY GENERATED SUPABASE SQL EDITOR SCRIPT AT: {sql_path}")
print(f"Total SQL Lines: {len(sql_lines)}")
