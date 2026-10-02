-- ============================================================
-- AGRIPAM — Penambahan Kolom September & Oktober
-- Jalankan di: Supabase Dashboard > SQL Editor
-- Project: https://wcocmwkccntmmtlofowe.supabase.co
-- ============================================================
-- Tujuan: Menambahkan kolom tk_september dan target_oktober 
-- ke tabel data_kebun_tk agar data tidak hilang (persistent)
-- ============================================================

ALTER TABLE data_kebun_tk
ADD COLUMN IF NOT EXISTS tk_september INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS target_oktober INT DEFAULT 0;

-- Verifikasi kolom berhasil ditambahkan
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'data_kebun_tk' 
  AND column_name IN ('tk_september', 'target_oktober');
