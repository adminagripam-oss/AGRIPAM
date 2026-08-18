-- ============================================================================
-- AGRIPAM - TAMBAH KOLOM BARU KE TABEL data_kebun_tk
-- Jalankan di Supabase Dashboard -> SQL Editor
-- Script ini AMAN dijalankan berkali-kali (IF NOT EXISTS)
-- ============================================================================

-- Tambah kolom tk_agustus (Ketersediaan TK Agustus)
ALTER TABLE data_kebun_tk ADD COLUMN IF NOT EXISTS tk_agustus INT DEFAULT 0;

-- Tambah kolom tk_juli (Ketersediaan TK Juli)
ALTER TABLE data_kebun_tk ADD COLUMN IF NOT EXISTS tk_juli INT DEFAULT 0;

-- Tambah kolom target_september (Rencana Pemenuhan September)
ALTER TABLE data_kebun_tk ADD COLUMN IF NOT EXISTS target_september INT DEFAULT 0;

-- Verifikasi: Tampilkan 5 baris pertama untuk memastikan kolom ada
SELECT id, nama_kebun, tk_juni, tk_juli, tk_agustus, target_juli, target_agustus, target_september
FROM data_kebun_tk
LIMIT 5;
