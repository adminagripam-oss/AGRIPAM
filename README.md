# 📊 AGRIPAM - Agrinas Panen Monitoring App

AGRIPAM (Agrinas Panen Monitoring) adalah aplikasi pemantauan realisasi panen kelapa sawit secara real-time. Sistem ini dibangun dengan arsitektur **Fullstack Terdistribusi**:
- **Database**: Google Sheets (Spreadsheet).
- **Backend**: Google Apps Script (REST API).
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS, Chart.js (Dihos di Vercel).
- **Notification & Media Reporting**: Fonnte API (Pengiriman pesan & grafik otomatis ke WhatsApp).
- **File Archiving**: Google Drive API.

---

## 🏗️ Struktur Repositori

```text
├── index.html          # Laman frontend utama (Dashboard & Admin Panel)
├── Code.js             # Kode utama backend Google Apps Script
├── appsscript.json     # Konfigurasi perizinan Google Apps Script
├── Kode2.gs            # Referensi script lama (dapat diabaikan/disimpan)
├── vercel.json         # Konfigurasi deployment Vercel (clean URLs)
├── package.json        # Dependensi pengujian lokal
└── README.md           # Dokumentasi proyek (Dokumen ini)
```

---

## 🗄️ Panduan Skema & Pembuatan Google Sheets

Sebelum mendeploy backend, Anda perlu membuat Google Spreadsheet baru dan membuat tiga sheet dengan struktur kolom berikut:

### 1. Sheet `Database_Input` (Realisasi Panen)
Digunakan untuk mencatat laporan realisasi panen tiap jam per region.
- **Kolom A**: `Tanggal` (Format: `DD/MM/YYYY`)
- **Kolom B**: `Region` (Teks nama wilayah)
- **Kolom C**: `Jam` (Format: `HH.MM`, misal `06.00`)
- **Kolom D**: `Tonase` (Angka desimal tonase panen)

### 2. Sheet `Data_Estimasi` (Rencana/Estimasi)
Digunakan untuk mencatat estimasi target panen harian.
- **Kolom A**: `Timestamp` (Tanggal/waktu pembuatan baris)
- **Kolom B**: `Tanggal` (Format: `DD/MM/YYYY`)
- **Kolom C**: `Region` (Teks nama wilayah)
- **Kolom D**: `Estimasi Restan Lalu` (Angka target sisa kemarin)
- **Kolom E**: `Luas Panen` (Angka luas wilayah panen dalam hektar)
- **Kolom F**: `TK Panen` (Jumlah tenaga kerja panen)
- **Kolom G**: `Estimasi Panen` (Target panen dalam Kg)
- **Kolom H**: `Output Panen` (Tonase)
- **Kolom I**: `Estimasi Kirim` (Tonase kirim)
- **Kolom J**: `Estimasi Restan` (Tonase sisa target)

### 3. Sheet `Sesi_Aktif` (Manajemen Login)
Mencatat token sesi aktif admin dan pengguna wilayah.
- **Kolom A**: `Region` (Nama region atau `ADMIN`)
- **Kolom B**: `Token` (Token string acak untuk otentikasi)
- **Kolom C**: `Waktu Login` (Format: `YYYY-MM-DD HH:mm:ss`)
- **Kolom D**: `Waktu Kadaluarsa` (Format: `YYYY-MM-DD HH:mm:ss`)
- **Kolom E**: `Status` (`Aktif` / `Logout` / `Expired`)
- **Kolom F**: `IP Address` (Alamat IP pengguna saat login)

---

## ⚙️ Deploy Backend (Google Apps Script)

> [!IMPORTANT]
> Backend berfungsi sebagai penghubung (API) antara database Spreadsheet, Google Drive (penyimpanan gambar grafik), dan Fonnte (WhatsApp).

### Langkah 1: Buat Script
1. Di Google Spreadsheet Anda, klik **Ekstensi** -> **Apps Script**.
2. Ubah nama proyek menjadi `AGRIPAM_Backend`.
3. Hapus kode default dan paste-kan seluruh isi berkas **Code.js**.
4. Sesuaikan konstanta di baris atas **Code.js**:
   - `SPREADSHEET_ID`: ID Google Spreadsheet Anda.
   - `tokenWa`: Token API Fonnte Anda.
   - `nomorTujuan`: Nomor grup/tujuan pengiriman WhatsApp (format: `120363410041245092@g.us` atau nomor biasa).

### Langkah 2: Konfigurasi Manifest (`appsscript.json`)
1. Di editor Apps Script, masuk ke **Setelan Proyek** (ikon ⚙️ di kiri).
2. Centang opsi **"Tampilkan file manifes 'appsscript.json' di editor"**.
3. Kembali ke editor berkas, buka **appsscript.json** dan ganti isinya dengan isi berkas **appsscript.json**. Langkah ini wajib agar Apps Script mengizinkan pemanggilan API Google Drive.

### Langkah 3: Otorisasi Awal
1. Di editor Apps Script, pilih fungsi **`testDriveAccess`** pada dropdown fungsi di atas.
2. Klik tombol **▶ Run**.
3. Izinkan akses Google Drive, Google Sheets, dan External Request saat pop-up verifikasi akun muncul.

### Langkah 4: Publikasikan Web App
1. Klik **Deploy** -> **New deployment**.
2. Pilih tipe **Web app**.
3. Konfigurasi:
   - **Execute as**: `Me` (email Anda).
   - **Who has access**: `Anyone`.
4. Klik **Deploy**, salin **URL Web App** yang didapatkan.

---

## 🌐 Deploy Frontend (Vercel)

### Langkah 1: Atur URL Backend
1. Buka berkas **index.html**.
2. Cari variabel global `SCRIPT_URL` di sekitar baris 1082:
   ```javascript
   var SCRIPT_URL = "URL_WEB_APP_ANDA_DISINI";
   ```
3. Tempelkan URL Web App yang Anda salin dari langkah deployment backend sebelumnya.

### Langkah 2: Jalankan Lokal (Opsional)
Untuk menguji secara lokal di komputer:
```bash
npm install
npm run dev
```

### Langkah 3: Deploy ke Vercel (Produksi)
1. Commit dan push proyek ini ke repositori **GitHub** Anda.
2. Buka dashboard [Vercel](https://vercel.com) dan buat proyek baru dengan mengimpor repositori tersebut.
3. Klik **Deploy**. Vercel akan otomatis menyajikan situs web Anda secara publik dengan protokol HTTPS yang aman.

---

## 📸 Sistem Otomatisasi Laporan & Screenshot Grafik

Aplikasi ini dilengkapi dengan modul **Auto-Screenshot Terjadwal**:

1. **Pemicu Manual**: Ketika login sebagai `ADMIN` (Password: `TANAMAN`), memilih opsi **"Tampilkan Total Semua Region"** akan merender grafik kumulatif real-time, menangkapnya menjadi file gambar JPEG, menyimpannya ke Google Drive, dan mengirimkannya ke WhatsApp.
2. **Pemicu Otomatis (Scheduler)**: Di dalam `index.html` terdapat loop interval yang berjalan di latar belakang setiap 30 detik. Loop ini akan secara otomatis memperbarui dashboard ke tanggal hari ini dan men-screenshot/mengirim grafik ringkasan pada jam-jam berikut:
   - **06.00, 07.00, 08.00, 09.00, 10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00, dan 17.30 WIB**

> [!TIP]
> Agar pelaporan otomatis berjalan tepat waktu setiap hari, pastikan laman dashboard ADMIN (`index.html`) tetap terbuka di browser salah satu perangkat (seperti PC monitoring kantor atau TV dashboard).
