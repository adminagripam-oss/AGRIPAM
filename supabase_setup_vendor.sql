-- Migration Script: Setup Vendor Monitoring System

CREATE TABLE IF NOT EXISTS public.vendor_monitoring (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cro VARCHAR(255) NOT NULL,
    regional VARCHAR(255) NOT NULL,
    nama_vendor VARCHAR(255) NOT NULL,
    kebun VARCHAR(255) NOT NULL,
    luas_ha DECIMAL(10, 2) NOT NULL,
    luas_tm_ha DECIMAL(10, 2) DEFAULT 0,
    target_produksi_ton DECIMAL(10, 2) DEFAULT 0,
    pic VARCHAR(255),
    link_dokumen TEXT,
    kontak_vendor VARCHAR(255),
    ket_admin_kurang TEXT,
    keterangan TEXT,
    action_status VARCHAR(50) DEFAULT 'Pending',
    tanggal_terima DATE,
    status VARCHAR(50) DEFAULT 'Menunggu Jawaban Region',
    tanggal_update_status DATE,
    tanggal_penugasan DATE,
    durasi_proses_hari INT DEFAULT 0,
    link_surat_spk TEXT,
    no_surat VARCHAR(255),
    tahap VARCHAR(50) DEFAULT 'Tahap 1',
    nama_pt_palm_ops VARCHAR(255),
    jasa_pekerjaan TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for sensitive files
CREATE TABLE IF NOT EXISTS public.vendor_rahasia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id UUID REFERENCES public.vendor_monitoring(id) ON DELETE CASCADE,
    jenis_dokumen VARCHAR(255) NOT NULL,
    link_rahasia TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Optional: Initial seed data for demonstration
INSERT INTO public.vendor_monitoring (
    cro, regional, nama_vendor, kebun, luas_ha, pic, status, tanggal_terima
)
SELECT 
    'CRO 1', 'Riau 1', 'PT Maju Bersama', 'Kebun Plasma 1', 1250.50, 'Budi Santoso', 'Lengkap', CURRENT_DATE
WHERE NOT EXISTS (
    SELECT 1 FROM public.vendor_monitoring WHERE nama_vendor = 'PT Maju Bersama'
);

INSERT INTO public.vendor_monitoring (
    cro, regional, nama_vendor, kebun, luas_ha, pic, status, tanggal_terima
)
SELECT 
    'CRO 2', 'Kalimantan Barat 1A', 'CV Alam Raya', 'Afdeling 2', 800.00, 'Andi', 'Kurang Administrasi', CURRENT_DATE - INTERVAL '2 days'
WHERE NOT EXISTS (
    SELECT 1 FROM public.vendor_monitoring WHERE nama_vendor = 'CV Alam Raya'
);
