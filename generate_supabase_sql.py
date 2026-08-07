import json

with open(r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\data_kebun_tk.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sql_header = """-- ============================================================
-- AGRI-PAM — Tabel Database Supabase: data_kebun_tk
-- Menyimpan Data Kebun & Realisasi TK Panen (Kolom I Juli & Kolom J Agustus)
-- Jalankan kode SQL ini di Supabase Dashboard -> SQL Editor
-- ============================================================

-- 1. Buat Tabel data_kebun_tk
CREATE TABLE IF NOT EXISTS data_kebun_tk (
  id              BIGSERIAL PRIMARY KEY,
  cro             VARCHAR(50),
  region          VARCHAR(100) NOT NULL,
  nama_kebun      TEXT NOT NULL,
  name_tag        VARCHAR(100),
  luasan          NUMERIC(10,2) DEFAULT 0,
  req_tk          NUMERIC(10,2) DEFAULT 0,
  tk_mei          NUMERIC(10,2) DEFAULT 0,
  tk_juni         NUMERIC(10,2) DEFAULT 0,
  tk_juli         NUMERIC(10,2) DEFAULT 0,  -- Kolom I (Red - Editable)
  tk_agustus      NUMERIC(10,2) DEFAULT 0,  -- Kolom J (Red - Editable)
  target_juli     NUMERIC(10,2) DEFAULT 0,  -- Kolom K (Yellow)
  target_agustus  NUMERIC(10,2) DEFAULT 0,  -- Kolom L (Yellow)
  updated_by      VARCHAR(100),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_kebun_tag_region UNIQUE (name_tag, region, nama_kebun)
);

-- 2. Buat Indeks Performa
CREATE INDEX IF NOT EXISTS idx_kebun_region ON data_kebun_tk(region);
CREATE INDEX IF NOT EXISTS idx_kebun_cro    ON data_kebun_tk(cro);

-- 3. Aktifkan Row Level Security (RLS)
ALTER TABLE data_kebun_tk ENABLE ROW LEVEL SECURITY;

-- 4. Policy RLS (Blokir Akses Publik, Hanya Backend / service_role yang diizinkan)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'data_kebun_tk' AND policyname = 'block_public'
    ) THEN
        CREATE POLICY "block_public" ON data_kebun_tk FOR ALL USING (false);
    END IF;
END
$$;

-- 5. SEED DATA (800 Akun Kebun dari DATA KONTOL.xlsx)
"""

def esc(val):
    if val is None: return "NULL"
    s = str(val).replace("'", "''")
    return f"'{s}'"

values_list = []
for item in data:
    cro = esc(item.get('cro'))
    region = esc(item.get('region'))
    nama_kebun = esc(item.get('nama_kebun'))
    name_tag = esc(item.get('name_tag'))
    luas = item.get('luasan', 0) or 0
    req = item.get('req_tk', 0) or 0
    mei = item.get('tk_mei', 0) or 0
    juni = item.get('tk_juni', 0) or 0
    juli = item.get('tk_juli', 0) or 0
    ags = item.get('tk_agustus', 0) or 0
    tgt_juli = item.get('target_juli', 0) or 0
    tgt_ags = item.get('target_agustus', 0) or 0
    
    val_str = f"({cro}, {region}, {nama_kebun}, {name_tag}, {luas}, {req}, {mei}, {juni}, {juli}, {ags}, {tgt_juli}, {tgt_ags})"
    values_list.append(val_str)

# Chunk insert statements into batches of 100 to avoid SQL query size limits
insert_statements = []
chunk_size = 100
for i in range(0, len(values_list), chunk_size):
    chunk = values_list[i:i + chunk_size]
    stmt = "INSERT INTO data_kebun_tk (cro, region, nama_kebun, name_tag, luasan, req_tk, tk_mei, tk_juni, tk_juli, tk_agustus, target_juli, target_agustus) VALUES\n  " + ",\n  ".join(chunk) + "\nON CONFLICT (name_tag, region, nama_kebun) DO NOTHING;\n"
    insert_statements.append(stmt)

full_sql = sql_header + "\n" + "\n".join(insert_statements)

out_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\supabase\setup_kebun_tk_table.sql'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_sql)

print(f"Generated {out_path} with {len(values_list)} seed rows.")

