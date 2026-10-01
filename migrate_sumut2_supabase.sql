-- ============================================================
-- AGRIPAM — Migrasi Region "Sumatera Utara 2 Ex Torganda" -> "Sumut 2"
-- Jalankan di: Supabase Dashboard > SQL Editor
-- Project: https://wcocmwkccntmmtlofowe.supabase.co
-- ============================================================
-- PENTING: Jalankan seksi PRE-FLIGHT dulu (baris 1-50) untuk
-- melihat berapa baris yang akan terpengaruh sebelum UPDATE.
-- ============================================================


-- ============================================================
-- PRE-FLIGHT: Cek berapa baris yang akan diupdate per tabel
-- ============================================================

SELECT
  'data_kebun_tk'    AS tabel, COUNT(*) AS baris_akan_diupdate
FROM data_kebun_tk
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'data_estimasi', COUNT(*)
FROM data_estimasi
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'database_input', COUNT(*)
FROM database_input
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'database_palmops', COUNT(*)
FROM database_palmops
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'regions (login)', COUNT(*)
FROM regions
WHERE region_name ILIKE '%Torganda%' OR region_name ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'sesi_aktif', COUNT(*)
FROM sesi_aktif
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'audit_log', COUNT(*)
FROM audit_log
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%';


-- ============================================================
-- MIGRASI: Jalankan blok UPDATE berikut setelah pre-flight
-- ============================================================

-- 1. data_kebun_tk — update region + region_raw
UPDATE data_kebun_tk
SET
  region     = 'Sumut 2',
  region_raw = 'Regional Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';

-- 2. data_estimasi
UPDATE data_estimasi
SET region = 'Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';

-- 3. database_input — realisasi tonase harian
UPDATE database_input
SET region = 'Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';

-- 4. database_palmops — data realisasi PalmOps
UPDATE database_palmops
SET region = 'Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';

-- 5. regions — tabel credential login (kolom region_name, bukan region)
UPDATE regions
SET region_name = 'Sumut 2'
WHERE region_name ILIKE '%Torganda%'
   OR region_name ILIKE '%Sumatera Utara 2%';

-- 6. sesi_aktif — log sesi login historis
UPDATE sesi_aktif
SET region = 'Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';

-- 7. audit_log — log aktivitas sistem
UPDATE audit_log
SET region = 'Sumut 2'
WHERE region ILIKE '%Torganda%'
   OR region ILIKE '%Sumatera Utara 2%';


-- ============================================================
-- VERIFIKASI: Jalankan setelah semua UPDATE selesai
-- Semua kolom "sisa_nama_lama" harus bernilai 0
-- ============================================================

SELECT
  'data_kebun_tk'    AS tabel, COUNT(*) AS sisa_nama_lama
FROM data_kebun_tk
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'data_estimasi', COUNT(*)
FROM data_estimasi
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'database_input', COUNT(*)
FROM database_input
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'database_palmops', COUNT(*)
FROM database_palmops
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'regions (login)', COUNT(*)
FROM regions
WHERE region_name ILIKE '%Torganda%' OR region_name ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'sesi_aktif', COUNT(*)
FROM sesi_aktif
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%'

UNION ALL

SELECT
  'audit_log', COUNT(*)
FROM audit_log
WHERE region ILIKE '%Torganda%' OR region ILIKE '%Sumatera Utara 2%';
