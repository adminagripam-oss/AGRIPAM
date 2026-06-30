# 📊 AGRIPAM - Agrinas Panen Monitoring App

AGRIPAM (Agrinas Panen Monitoring) adalah aplikasi pemantauan realisasi panen kelapa sawit secara real-time. Sistem ini dibangun dengan arsitektur **Fullstack Terdistribusi Modern**:
- **Database**: Supabase (PostgreSQL) - Aman, cepat, dengan enkripsi password (bcrypt) & Row Level Security (RLS).
- **Backend API**: Vercel Serverless Functions (Node.js/JWT Auth) - Menggantikan Google Apps Script lama agar data credential tersembunyi dengan aman di sisi server.
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS, Chart.js (Dihos di Vercel).
- **Notification & Media Reporting**: Fonnte API (Pengiriman pesan & grafik otomatis ke WhatsApp via Google Apps Script `Kode2.gs` di background).
- **File Archiving**: Google Drive API.

---

## 🏗️ Struktur Repositori

```text
├── api/
│   ├── _lib/
│   │   ├── auth.js          # Helper JWT token (Sign/Verify, 8-hour TTL)
│   │   └── supabase.js      # Singleton client Supabase PostgreSQL
│   ├── login.js             # Endpoint login (rate limit + bcrypt check)
│   ├── logout.js            # Endpoint logout
│   ├── refresh.js           # Perpanjang sesi JWT aktif
│   ├── getData.js           # Mengambil realisasi tonase per jam
│   ├── insert.js            # Input data realisasi baru
│   ├── delete.js            # Hapus data realisasi
│   ├── getEstimasi.js       # Mengambil data estimasi panen harian
│   ├── insertEstimasi.js    # Menyimpan estimasi panen harian
│   └── deleteEstimasi.js    # Hapus estimasi panen harian
├── supabase/
│   └── schema.sql           # Skema database PostgreSQL (tabel, index, RLS & seed)
├── index.html               # Frontend utama (Dashboard & Admin Panel)
├── admin.html               # Panel Admin terpisah
├── Migrasi.gs               # Script Google Apps Script untuk migrasi data Sheets → Supabase
├── Code.js                  # Backup backend lama Google Apps Script (tidak aktif)
├── Kode2.gs                 # Automasi screenshot Fonnte + Google Drive (tetap aktif di GAS)
├── vercel.json              # Konfigurasi routing serverless Vercel
├── package.json             # Manifes dependensi backend
├── .env.example             # Template konfigurasi environment variables
└── README.md                # Dokumentasi proyek (Dokumen ini)
```

---

## 🗄️ Langkah Setup Database Supabase

1. Buka **[Supabase Dashboard](https://supabase.com)** dan pilih project Anda.
2. Buka menu **SQL Editor** -> **New Query**.
3. Buka file [supabase/schema.sql](file:///d:/AGRINAS%20PALMA%20NUSANTARA/AGRIPAM/supabase/schema.sql), salin (copy) semua isinya, paste di editor, lalu klik **Run (▶)**.
4. SQL tersebut akan membuat tabel-tabel berikut:
   - `regions` — Data master region & hash password (bcrypt)
   - `database_input` — Data realisasi tonase per jam
   - `data_estimasi` — Estimasi target panen harian
   - `sesi_aktif` — Sesi token JWT login aktif
   - `rate_limit` — Pencegah brute force login
   - `audit_log` — Log audit aktivitas sistem

---

## ⚙️ Migrasi Data Historis dari Google Sheets ke Supabase

Jika Anda memiliki data lama di Spreadsheet dan ingin memindahkannya ke Supabase:
1. Buka spreadsheet lama Anda, klik **Extensions** -> **Apps Script**.
2. Buat berkas script baru bernama `Migrasi.gs` dan paste isi berkas [Migrasi.gs](file:///d:/AGRINAS%20PALMA%20NUSANTARA/AGRIPAM/Migrasi.gs).
3. Masukkan `SUPABASE_SERVICE_KEY` Anda di dalam variabel script tersebut.
4. Pilih fungsi `migrasiSemua` pada dropdown atas, lalu klik **Run (▶)**.
5. Proses migrasi akan memindahkan seluruh data `Database_Input`, `Data_Estimasi`, dan `Sesi_Aktif` ke Supabase secara otomatis.

---

## 💻 Panduan Menjalankan / Debugging Lokal

### Prasyarat
- **Node.js LTS** terinstall di komputer Anda (Download dari [nodejs.org](https://nodejs.org/)).

### Langkah 1: Setup Environment Variables
Buat file bernama `.env` di folder root proyek ini dan isi sesuai credential Anda:
```env
SUPABASE_URL=https://wcocmwkccntmmtlofowe.supabase.co
SUPABASE_SERVICE_KEY=isi_dengan_service_role_key_supabase_anda
JWT_SECRET=isi_dengan_random_string_64_karakter
```

### Langkah 2: Install CLI & Jalankan Server Lokal
Buka terminal proyek Anda (di VS Code tekan `Ctrl + \``) dan jalankan:
```bash
# Install Vercel CLI secara global (jika belum ada)
npm install -g vercel

# Jalankan development server lokal
vercel dev
```
Aplikasi lokal Anda akan berjalan di `http://localhost:3000`.

### Langkah 3: Jalankan Debugger
1. Tekan **F5** di VS Code (atau klik menu Run and Debug -> *Launch Chrome against localhost*).
2. Browser Chrome akan terbuka mengarah ke server lokal Anda dan siap untuk di-debug.

---

## 🌐 Deploy ke Vercel (Produksi)

1. Commit dan push seluruh kode proyek ini ke repositori **GitHub** Anda (pastikan file `.env` sudah masuk dalam `.gitignore`).
2. Masuk ke **[Vercel Dashboard](https://vercel.com)**, impor proyek GitHub baru ini.
3. Di bagian **Settings** -> **Environment Variables**, tambahkan 3 variabel yang sama dengan isi `.env` lokal Anda:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `JWT_SECRET`
4. Klik **Deploy**. Situs web Anda sekarang aktif secara publik dengan domain aman!

---

## 📸 Sistem Otomatisasi Laporan & Screenshot Grafik

Modul screenshot otomatis grafik laporan harian tetap dijalankan via Google Apps Script (`Kode2.gs` di Google Drive Anda) karena memerlukan API bawaan Google:
1. **Pemicu Otomatis (Scheduler)**: Di dalam `index.html` terdapat loop interval yang berjalan di latar belakang setiap 30 detik. Loop ini akan secara otomatis mendeteksi jam pengiriman laporan kumulatif pada jam-jam berikut:
   - **06.00 s/d 17.30 WIB** setiap jam secara berkala.
2. Penjadwal akan memicu Apps Script untuk men-screenshot dashboard visual ADMIN, mengupload gambar JPEG ke Google Drive, dan mengirimkan pesan notifikasi gambar via Fonnte API ke grup WhatsApp.

> [!TIP]
> Agar pelaporan otomatis berjalan tepat waktu setiap hari, pastikan salah satu laman dashboard ADMIN (`index.html` atau `admin.html`) tetap terbuka aktif di browser perangkat monitoring kantor (seperti PC monitoring kantor atau TV dashboard).
