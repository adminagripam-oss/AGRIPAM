-- 1. Buat bucket bernama 'surat_files' dan set menjadi Publik
INSERT INTO storage.buckets (id, name, public) 
VALUES ('surat_files', 'surat_files', true)
ON CONFLICT (id) DO NOTHING;

-- 2. Izinkan semua orang melihat file yang diupload (Read)
CREATE POLICY "Public Access" 
ON storage.objects FOR SELECT 
USING (bucket_id = 'surat_files');

-- 3. Izinkan upload file ke bucket (Insert)
CREATE POLICY "Allow Uploads" 
ON storage.objects FOR INSERT 
WITH CHECK (bucket_id = 'surat_files');
