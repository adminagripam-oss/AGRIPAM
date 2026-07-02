-- Eksekusi kode SQL ini di menu SQL Editor pada Supabase Dashboard Anda.

-- 1. Buat tipe ENUM untuk role
CREATE TYPE user_role AS ENUM ('admin', 'regional');

-- 2. Buat tabel Profiles yang terhubung ke Supabase Auth (auth.users)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    nama_lengkap TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'regional',
    nama_regional TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 3. Buat tabel Surat
CREATE TABLE surat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nomor_surat TEXT NOT NULL,
    jenis_surat TEXT NOT NULL CHECK (jenis_surat IN ('masuk', 'permintaan')),
    perihal TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'menunggu' CHECK (status IN ('menunggu', 'diproses', 'selesai', 'ditolak')),
    file_url TEXT NOT NULL,
    dibuat_oleh UUID REFERENCES profiles(id) ON DELETE SET NULL,
    regional_pengirim TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 4. Buat tabel Log Tracking
CREATE TABLE log_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    surat_id UUID REFERENCES surat(id) ON DELETE CASCADE,
    status_update TEXT NOT NULL,
    catatan TEXT,
    created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 5. Aktifkan Row Level Security (RLS)
ALTER TABLE surat ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE log_tracking ENABLE ROW LEVEL SECURITY;

-- 6. Policy RLS untuk Tabel 'surat'
-- Admin: Bisa melihat dan mengedit SEMUA surat
CREATE POLICY "Admin bisa melihat semua surat" ON surat FOR SELECT
USING (EXISTS (SELECT 1 FROM profiles WHERE profiles.id = auth.uid() AND role = 'admin'));

CREATE POLICY "Admin bisa mengedit semua surat" ON surat FOR UPDATE
USING (EXISTS (SELECT 1 FROM profiles WHERE profiles.id = auth.uid() AND role = 'admin'));

-- Regional: Hanya bisa melihat dan insert surat yang dibuatnya sendiri
CREATE POLICY "Regional melihat surat sendiri" ON surat FOR SELECT
USING (dibuat_oleh = auth.uid());

CREATE POLICY "Regional bisa menambah surat" ON surat FOR INSERT
WITH CHECK (dibuat_oleh = auth.uid());

-- 7. Policy RLS untuk Tabel 'log_tracking'
-- Regional bisa melihat log untuk suratnya sendiri
CREATE POLICY "Regional bisa melihat log suratnya" ON log_tracking FOR SELECT
USING (EXISTS (SELECT 1 FROM surat WHERE surat.id = log_tracking.surat_id AND surat.dibuat_oleh = auth.uid()));

-- Admin bisa melihat dan insert log tracking
CREATE POLICY "Admin bisa melihat semua log" ON log_tracking FOR SELECT
USING (EXISTS (SELECT 1 FROM profiles WHERE profiles.id = auth.uid() AND role = 'admin'));

CREATE POLICY "Admin bisa menambah log" ON log_tracking FOR INSERT
WITH CHECK (EXISTS (SELECT 1 FROM profiles WHERE profiles.id = auth.uid() AND role = 'admin'));

-- 8. Policy RLS untuk Tabel 'profiles'
-- Semua user terautentikasi bisa membaca profiles
CREATE POLICY "User bisa melihat profiles" ON profiles FOR SELECT USING (auth.role() = 'authenticated');


-- ==============================================================================
-- TRIGGER & FUNGSI (Opsional tapi disarankan)
-- Fungsi ini otomatis menambahkan baris ke tabel profiles saat user Sign Up
-- ==============================================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, nama_lengkap, role, nama_regional)
  VALUES (
    new.id,
    new.email,
    COALESCE(new.raw_user_meta_data->>'nama_lengkap', 'User Baru'),
    COALESCE((new.raw_user_meta_data->>'role')::user_role, 'regional'),
    COALESCE(new.raw_user_meta_data->>'nama_regional', 'Belum Diatur')
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- ==============================================================================
-- DUMMY DATA SEEDING
-- (Jalankan ini SETELAH Anda membuat user dari Supabase Auth Dashboard secara manual)
-- Karena tabel profiles terkait dengan auth.users, Anda harus membuat user di menu Authentication terlebih dahulu,
-- lalu update row profile mereka dengan query UPDATE.
-- Contoh:
-- UPDATE profiles SET role = 'admin', nama_lengkap = 'Admin HO', nama_regional = 'HO Jakarta' WHERE email = 'admin@example.com';
-- UPDATE profiles SET role = 'regional', nama_lengkap = 'User Sumut', nama_regional = 'Sumatera Utara' WHERE email = 'sumut@example.com';
-- ==============================================================================
