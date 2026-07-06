-- Eksekusi kode SQL ini di menu SQL Editor pada Supabase Dashboard Anda.
-- (Ini adalah skema SSO tanpa Supabase Auth, langsung mengikuti Region Agripam)

-- 1. Buat tabel Surat
CREATE TABLE IF NOT EXISTS surat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nomor_surat TEXT NOT NULL,
    jenis_surat TEXT NOT NULL CHECK (jenis_surat IN ('masuk', 'permintaan')),
    perihal TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'menunggu' CHECK (status IN ('menunggu', 'diproses', 'selesai', 'ditolak')),
    file_url TEXT NOT NULL,
    regional_pengirim TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 2. Buat tabel Log Tracking
CREATE TABLE IF NOT EXISTS log_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    surat_id UUID REFERENCES surat(id) ON DELETE CASCADE,
    status_update TEXT NOT NULL,
    catatan TEXT,
    created_by TEXT NOT NULL, -- Diisi nama Region atau 'ADMIN'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- ==============================================================================
-- Keterangan:
-- Karena kita menggunakan backend Node.js (api/sap_*) untuk query data ke database 
-- dengan service_role key, kita tidak perlu mengaktifkan Row Level Security (RLS) 
-- untuk tabel-tabel ini. Keamanan sepenuhnya ditangani oleh validasi token 
-- di backend Node.js (seperti fitur Agripam lainnya).
-- ==============================================================================
