-- ============================================================
-- AGRI-PAM — Supabase PostgreSQL Schema
-- Jalankan file ini sekali di Supabase SQL Editor
-- Project: https://wcocmwkccntmmtlofowe.supabase.co
-- ============================================================

-- 1. Aktifkan ekstensi pgcrypto untuk hashing password
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================
-- 2. TABEL: regions (Master data region & password)
-- ============================================================
CREATE TABLE IF NOT EXISTS regions (
  id            SERIAL PRIMARY KEY,
  region_name   VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_active     BOOLEAN DEFAULT TRUE,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 3. TABEL: database_input (Realisasi tonase harian per jam)
-- ============================================================
CREATE TABLE IF NOT EXISTS database_input (
  id          BIGSERIAL PRIMARY KEY,
  tanggal     DATE NOT NULL,
  region      VARCHAR(100) NOT NULL,
  jam         VARCHAR(10) NOT NULL,
  tonase      NUMERIC(10,2) NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_input_tanggal        ON database_input(tanggal);
CREATE INDEX IF NOT EXISTS idx_input_region         ON database_input(region);
CREATE INDEX IF NOT EXISTS idx_input_tanggal_region ON database_input(tanggal, region);

-- ============================================================
-- 4. TABEL: data_estimasi (Estimasi panen harian)
-- ============================================================
CREATE TABLE IF NOT EXISTS data_estimasi (
  id                  BIGSERIAL PRIMARY KEY,
  waktu_input         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  tanggal             DATE NOT NULL,
  region              VARCHAR(100) NOT NULL,
  restan_lalu         NUMERIC(15,2) DEFAULT 0,
  luas_panen_ha       NUMERIC(10,2) NOT NULL,
  tk_panen_hk         NUMERIC(10,2) NOT NULL,
  estimasi_panen_kg   NUMERIC(15,2) NOT NULL,
  output_panen        NUMERIC(10,2) DEFAULT 0,
  estimasi_kirim_kg   NUMERIC(15,2) NOT NULL,
  estimasi_restan_kg  NUMERIC(15,2) NOT NULL,
  CONSTRAINT unique_estimasi_tanggal_region UNIQUE (tanggal, region)
);

CREATE INDEX IF NOT EXISTS idx_estimasi_tanggal ON data_estimasi(tanggal);
CREATE INDEX IF NOT EXISTS idx_estimasi_region  ON data_estimasi(region);

-- ============================================================
-- 5. TABEL: sesi_aktif (Log sesi login pengguna)
-- ============================================================
CREATE TABLE IF NOT EXISTS sesi_aktif (
  id          BIGSERIAL PRIMARY KEY,
  region      VARCHAR(100) NOT NULL,
  token       TEXT NOT NULL,
  login_time  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expiry      TIMESTAMPTZ NOT NULL,
  status      VARCHAR(20) DEFAULT 'Aktif'
                CHECK (status IN ('Aktif', 'Logout', 'Expired')),
  ip_address  VARCHAR(100),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sesi_token  ON sesi_aktif(token);
CREATE INDEX IF NOT EXISTS idx_sesi_region ON sesi_aktif(region);
CREATE INDEX IF NOT EXISTS idx_sesi_status ON sesi_aktif(status);

-- ============================================================
-- 6. TABEL: rate_limit (Pembatas percobaan login)
-- ============================================================
CREATE TABLE IF NOT EXISTS rate_limit (
  id           SERIAL PRIMARY KEY,
  region       VARCHAR(100) UNIQUE NOT NULL,
  attempts     INTEGER DEFAULT 0,
  window_start TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 7. TABEL: audit_log (Log aktivitas sistem)
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_log (
  id         BIGSERIAL PRIMARY KEY,
  region     VARCHAR(100) NOT NULL,
  action     VARCHAR(50) NOT NULL,
  detail     TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_region  ON audit_log(region);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);

-- ============================================================
-- 8. ROW LEVEL SECURITY
-- Hanya service_role (backend API) yang bisa akses.
-- Anon key / publik diblokir sepenuhnya.
-- ============================================================
ALTER TABLE regions       ENABLE ROW LEVEL SECURITY;
ALTER TABLE database_input ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_estimasi  ENABLE ROW LEVEL SECURITY;
ALTER TABLE sesi_aktif     ENABLE ROW LEVEL SECURITY;
ALTER TABLE rate_limit     ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log      ENABLE ROW LEVEL SECURITY;

-- Blokir semua akses publik (service_role otomatis bypass RLS)
CREATE POLICY "block_public" ON regions        FOR ALL USING (false);
CREATE POLICY "block_public" ON database_input FOR ALL USING (false);
CREATE POLICY "block_public" ON data_estimasi  FOR ALL USING (false);
CREATE POLICY "block_public" ON sesi_aktif     FOR ALL USING (false);
CREATE POLICY "block_public" ON rate_limit     FOR ALL USING (false);
CREATE POLICY "block_public" ON audit_log      FOR ALL USING (false);

-- ============================================================
-- 9. SEED DATA: Master Region & Password (bcrypt via pgcrypto)
-- Password di-hash dengan Blowfish (cost factor 10)
-- ============================================================
INSERT INTO regions (region_name, password_hash) VALUES
  ('Aceh',                        crypt('ROACEH',      gen_salt('bf', 10))),
  ('Sumatera Utara 1',            crypt('ROSUMUT1',    gen_salt('bf', 10))),
  ('Sumatera Utara 2 Ex Torganda',crypt('ROSUMUT2',    gen_salt('bf', 10))),
  ('Riau 1',                      crypt('RORiau1',     gen_salt('bf', 10))),
  ('Riau 2',                      crypt('RORiau2',     gen_salt('bf', 10))),
  ('Riau 3',                      crypt('RORiau3',     gen_salt('bf', 10))),
  ('Riau 4',                      crypt('RORiau4',     gen_salt('bf', 10))),
  ('Bangka Belitung',             crypt('ROBabel',     gen_salt('bf', 10))),
  ('Jambi',                       crypt('ROJ4mb1',     gen_salt('bf', 10))),
  ('Sumatera Barat',              crypt('ROSumbar',    gen_salt('bf', 10))),
  ('Sumatera Selatan',            crypt('ROSumsel',    gen_salt('bf', 10))),
  ('Kalimantan Barat 1A',         crypt('ROKalbar1a',  gen_salt('bf', 10))),
  ('Kalimantan Barat 1B',         crypt('ROKalbar1B',  gen_salt('bf', 10))),
  ('Kalimantan Barat 2',          crypt('ROKalbar2',   gen_salt('bf', 10))),
  ('Kalimantan Selatan 1',        crypt('ROKalsel1',   gen_salt('bf', 10))),
  ('Kalimantan Selatan 2',        crypt('ROKalsel2',   gen_salt('bf', 10))),
  ('Kalimantan Timur',            crypt('ROKaltim',    gen_salt('bf', 10))),
  ('Kalimantan Utara',            crypt('ROKalut',     gen_salt('bf', 10))),
  ('Kalimantan Tengah 1',         crypt('ROKalteng1',  gen_salt('bf', 10))),
  ('Kalimantan Tengah 2',         crypt('ROKalteng2',  gen_salt('bf', 10))),
  ('Kalimantan Tengah 3',         crypt('ROKalteng3',  gen_salt('bf', 10))),
  ('Sulawesi Tenggara',           crypt('ROSultra',    gen_salt('bf', 10))),
  ('Sulawesi Tengah',             crypt('ROSulteng',   gen_salt('bf', 10))),
  ('ADMIN',                       crypt('TANAMAN',     gen_salt('bf', 10)))
ON CONFLICT (region_name) DO NOTHING;

-- ============================================================
-- 10. FUNGSI: Validasi password region (dipanggil dari API login)
-- ============================================================
CREATE OR REPLACE FUNCTION check_password(p_region TEXT, p_password TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  stored_hash TEXT;
BEGIN
  SELECT password_hash INTO stored_hash
    FROM regions
   WHERE region_name = p_region
     AND is_active = TRUE;

  IF stored_hash IS NULL THEN
    RETURN FALSE;
  END IF;

  RETURN stored_hash = crypt(p_password, stored_hash);
END;
$$;

-- ============================================================
-- 11. FUNGSI: Cleanup sesi expired (jalankan via cron Supabase)
-- ============================================================
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  updated_count INTEGER;
BEGIN
  UPDATE sesi_aktif
    SET status = 'Expired'
  WHERE status = 'Aktif'
    AND expiry < NOW();
  GET DIAGNOSTICS updated_count = ROW_COUNT;

  -- Hapus audit log lebih dari 30 hari
  DELETE FROM audit_log WHERE created_at < NOW() - INTERVAL '30 days';

  -- Hapus rate limit yang sudah kadaluarsa (> 10 menit)
  DELETE FROM rate_limit WHERE updated_at < NOW() - INTERVAL '10 minutes';

  RETURN updated_count;
END;
$$;


-- ============================================================
-- 8. TABEL: delete_requests (Permintaan Hapus Data oleh Regional)
-- ============================================================
CREATE TABLE IF NOT EXISTS delete_requests (
  id           BIGSERIAL PRIMARY KEY,
  type         VARCHAR(50) NOT NULL CHECK (type IN ('REALISASI', 'ESTIMASI')),
  region       VARCHAR(100) NOT NULL,
  tanggal      DATE NOT NULL,
  jam          VARCHAR(10),
  status       VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
  requested_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at  TIMESTAMPTZ,
  resolved_by  VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_delete_req_status ON delete_requests(status);
CREATE INDEX IF NOT EXISTS idx_delete_req_region ON delete_requests(region);

-- ============================================================
-- 12. TABEL: database_palmops (Data realisasi dari PalmOps)
-- ============================================================
CREATE TABLE IF NOT EXISTS database_palmops (
  id          BIGSERIAL PRIMARY KEY,
  tanggal     DATE NOT NULL,
  region      VARCHAR(100) NOT NULL,
  tonase      NUMERIC(10,2) NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_palmops_tanggal_region UNIQUE (tanggal, region)
);

ALTER TABLE database_palmops ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'database_palmops' AND policyname = 'block_public'
    ) THEN
        CREATE POLICY "block_public" ON database_palmops FOR ALL USING (false);
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS idx_palmops_tanggal ON database_palmops(tanggal);
CREATE INDEX IF NOT EXISTS idx_palmops_region ON database_palmops(region);


