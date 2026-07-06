function kirimScreenshotHarian() {
  // 1. Cek Jam Kerja
  var now = new Date();
  var jam = now.getHours();
  var menit = now.getMinutes();
  var totalMenit = jam * 60 + menit;
  var mulai = 6 * 60; 
  var selesai = 21 * 60 + 30;
  
  if (totalMenit < mulai || totalMenit > selesai) {
    Logger.log("Di luar jam kerja, dilewati.");
    return;
  }
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var convertApiSecret = "7YTl1Ws08gpS6KgEyNofVH8AJGLFCX5Y"; 
  var folderId = "1HaZkgflPW6IkLXaBUMl8nJCGWIMCyOxM";
  
  // 2. Setup Array Sheet yang akan diproses
  var daftarSheet = [
    { nama: "Screenshot 01", range: "A1:R38", judulWA: "Detail Laporan Panen" },
    { nama: "Screenshot 02", range: "A1:N62", judulWA: "Grafik Laporan Panen" } 
  ];
  
  var daftarFile = []; 
  
  // 3 & 4. Looping untuk memproses konversi setiap sheet
  for (var i = 0; i < daftarSheet.length; i++) {
    var sheetData = daftarSheet[i];
    var sheet = ss.getSheetByName(sheetData.nama);
    
    if (!sheet) {
      Logger.log("Sheet '" + sheetData.nama + "' tidak ditemukan. Dilewati.");
      continue;
    }
    
    Logger.log("Memproses " + sheetData.nama + "...");
    
    var url = "https://docs.google.com/spreadsheets/d/" + ss.getId() +
      "/export?format=pdf&gid=" + sheet.getSheetId() +
      "&range=" + sheetData.range +
      "&portrait=false&fitw=true&fith=false&gridlines=false" +
      "&top_margin=0.00&bottom_margin=0.00&left_margin=0.00&right_margin=0.00" +
      "&pageorder=1&size=letter";
    
    var pdfBlob = UrlFetchApp.fetch(url, { headers: { Authorization: "Bearer " + ScriptApp.getOAuthToken() } }).getBlob();
    
    // Konversi PDF ke JPG via ConvertAPI
    var apiResponse = UrlFetchApp.fetch("https://v2.convertapi.com/convert/pdf/to/jpg?Secret=" + convertApiSecret, {
      "method": "post",
      "payload": { 
        "File": pdfBlob,
        "AutoCrop": "true" 
      },
      "muteHttpExceptions": true
    });
    
    var json = JSON.parse(apiResponse.getContentText());
    if (json.Files && json.Files.length > 0) {
      var fileData = json.Files[0].FileData; 
      var jpgBlob = Utilities.newBlob(Utilities.base64Decode(fileData), "image/jpeg");
      
      // 5. Simpan ke Google Drive
      var namaFile = "Laporan_" + sheetData.nama.replace(/\s+/g, '') + "_" + Utilities.formatDate(now, "GMT+7", "dd-MM-yyyy_HH-mm") + ".jpg";
      jpgBlob.setName(namaFile);
      
      var folder = DriveApp.getFolderById(folderId);
      var fileTersimpan = folder.createFile(jpgBlob);
      fileTersimpan.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
      
      daftarFile.push({
        nama: sheetData.judulWA, 
        blob: fileTersimpan.getBlob()
      });
      Logger.log("Berhasil memproses " + sheetData.nama);
    } else {
      Logger.log("Gagal mengonversi " + sheetData.nama + " melalui API.");
    }
  }
  
  if (daftarFile.length === 0) {
    Logger.log("Tidak ada screenshot yang berhasil diunggah. Pengiriman WA dibatalkan.");
    return;
  }

  // ====================================================================
  // [TAMBAHAN] MEMBACA DATA REGION YANG BELUM MENGISI LAPORAN
  // ====================================================================
  var sheetRegion = ss.getSheetByName("Screenshot 02"); 
  var teksRegionTambahan = "";
  
  if (sheetRegion) {
    var rangeData = sheetRegion.getRange("B39:D60").getValues(); 
    var regionBelumIsi = [];
    
    for (var k = 0; k < rangeData.length; k++) {
      var namaRegion = rangeData[k][0];    
      var statusLaporan = rangeData[k][2]; 
      
      if (namaRegion !== "" && (statusLaporan === "" || statusLaporan === 0 || statusLaporan === "0")) { 
        regionBelumIsi.push(namaRegion);
      }
    }

    if (regionBelumIsi.length > 0) {
      teksRegionTambahan = "*⚠️ Region Belum Isi Laporan:*\n" + "📌 " + regionBelumIsi.join("\n📌 ");
    } else {
      teksRegionTambahan = "*✅ Status:* Semua region sudah mengisi laporan.";
    }
  }

  // ====================================================================
  // [TAMBAHAN] HITUNG JADWAL LAPORAN BERIKUTNYA
  // ====================================================================
  var waktuBerikutnya = new Date(now.getTime() + (60 * 60 * 1000));
  
  // PERBAIKAN: Ubah "HH:00" menjadi "HH:mm" agar menitnya ikut terbawa secara dinamis
  var jamBerikutnya = Utilities.formatDate(waktuBerikutnya, "GMT+7", "HH:mm");
  
  var totalMenitBerikutnya = waktuBerikutnya.getHours() * 60 + waktuBerikutnya.getMinutes();
  var selesaiMenit = 20 * 60 + 30;
  
  var teksJadwalBerikutnya = "";
  if (totalMenitBerikutnya <= selesaiMenit) {
    // Menghapus spasi berlebih di sekitar variabel jamBerikutnya agar rapi seperti screenshot Anda
    teksJadwalBerikutnya = "🕒 _Laporan berikutnya dikirim otomatis pukul *" + jamBerikutnya + " WIB*._";
  } else {
    teksJadwalBerikutnya = "🕒 _Ini adalah laporan terakhir untuk hari ini. Laporan berikutnya akan dikirim besok pagi pukul *06:37 WIB*._";
  }

  // ====================================================================
  // 6. KIRIM KE WHATSAPP
  // ====================================================================
  var tokenWa = "NgcPkuu5vmUmHYRpRLGw"; 
  var nomorTujuan = "120363410041245092@g.us"; 
  
  var waktuCetak = Utilities.formatDate(now, "GMT+7", "dd/MM/yyyy - HH:mm") + " WIB";

  Logger.log("Mengirim pesan gambar ke WhatsApp...");

  for (var j = 0; j < daftarFile.length; j++) {
    var pesanWa = "";
    
    if (j === 0) {
      // PESAN 1: Format Sesuai Gambar Contoh Anda
      pesanWa = "📊 *[LAPORAN PANEN PER JAM]*\n" +
                "📅 Data per: *" + waktuCetak + "*\n\n" +
                "▪️ *Part 1:* " + daftarFile[j].nama;
    } else {
      // PESAN 2: Menggunakan format penanda yang seragam dengan Part 1
      pesanWa = "📊 *[LAPORAN PANEN PER JAM]*\n" +
                "📅 Data per: *" + waktuCetak + "*\n\n" +
                "▪️ *Part 2:* " + daftarFile[j].nama + "\n\n" +
                "-------------------------------------------\n\n" +
                teksRegionTambahan + "\n\n" +
                "-------------------------------------------\n\n" +
                teksJadwalBerikutnya;
    }

    var waPayload = {
      "target": nomorTujuan,
      "message": pesanWa.trim(),
      "file": daftarFile[j].blob 
    };
    
    var waOptions = {
      "method": "post",
      "headers": { "Authorization": tokenWa },
      "payload": waPayload,
      "muteHttpExceptions": true
    };
    
    var waResponse = UrlFetchApp.fetch("https://api.fonnte.com/send", waOptions);
    Logger.log("Respon WA (Gambar " + (j+1) + "): " + waResponse.getContentText());
  }
}

// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


// FUNGSI BARU KHUSUS UNTUK DIKIRIM JAM 6 SORE +++++++
function kirimScreenshotSoreKhusus() {
  var now = new Date();
  var jam = now.getHours();
  var menit = now.getMinutes();
  
  // 1. CEK BATAS JAM KERJA (18.00 s/d 22.00)
  var totalMenitSekarang = jam * 60 + menit;
  var mulaiSore = 18 * 60;       // Jam 18.00
  var selesaiSore = 22 * 60 + 0; // Batas akhir operasi sore
  
  if (totalMenitSekarang < mulaiSore || totalMenitSekarang > selesaiSore) {
    Logger.log("Di luar jam operasi sore, dilewati.");
    return; 
  }
  
  // 2. CEK INTERVAL WAKTU (Target Kirim)
  var targetWaktuKirim = [
    18 * 60 + 50,  // 18.50
    19 * 60 + 50,  // 19.50
    20 * 60 + 50,  // 20.50
    21 * 60 + 50,  // 21.50
  ];
  
  var apakahWaktunyaKirim = targetWaktuKirim.some(function(target) {
    return Math.abs(totalMenitSekarang - target) < 3; // Toleransi ±3 menit dari trigger Google
  });
  
  if (!apakahWaktunyaKirim) {
    Logger.log("Berada di jam operasi sore, namun belum masuk jadwal kirim. Dilewati.");
    return; 
  }
  
  // ====================================================================
  // PROSES EKSPOR VIA HTML & KIRIM LAPORAN (FIT TO TABLE)
  // ====================================================================
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var convertApiSecret = "tW4lrclQ8abE2iSlhTjQGzHmSIYdJSWP"; 
  var folderId = "10ndPbXGipkyXuybZa6x6AMG2pGLU3t9X";
  
  var sheetData = { nama: "Screenshot 03", range: "A1:P38", judulWA: "Laporan Estimasi dan Rencanan Panen" };
  var sheet = ss.getSheetByName(sheetData.nama);
  if (!sheet) {
    Logger.log("Sheet '" + sheetData.nama + "' tidak ditemukan. Pengiriman dibatalkan.");
    return;
  }
  
  Logger.log("Interval cocok! Memproses khusus " + sheetData.nama + " via HTML...");
  
  var url = "https://docs.google.com/spreadsheets/d/" + ss.getId() +
            "/export?format=pdf" +
            "&gid=" + sheet.getSheetId() +
            "&range=" + encodeURIComponent(sheetData.range) +
            "&portrait=false" +          
            "&fitw=true" +              
            "&fith=true" +              
            "&gridlines=false" +        
            "&top_margin=0.00&bottom_margin=0.00&left_margin=0.00&right_margin=0.00" + 
            "&size=A4";
            
  Logger.log("URL Ekspor PDF Sore: " + url);
  
  var pdfBlob = UrlFetchApp.fetch(url, { 
    headers: { Authorization: "Bearer " + ScriptApp.getOAuthToken() },
    muteHttpExceptions: true 
  }).getBlob();
  
  // Konversi menggunakan endpoint pdf/to/jpg
  var apiResponse = UrlFetchApp.fetch("https://v2.convertapi.com/convert/pdf/to/jpg?Secret=" + convertApiSecret, {
    "method": "post",
    "payload": { 
      "File": pdfBlob,
      "AutoCrop": "true" 
    },
    "muteHttpExceptions": true
  });
  
  var json = JSON.parse(apiResponse.getContentText());
  if (json.Files && json.Files.length > 0) {
    var fileData = json.Files[0].FileData; 
    var jpgBlob = Utilities.newBlob(Utilities.base64Decode(fileData), "image/jpeg");
    
    var namaFile = "Laporan_Sore_" + sheetData.nama.replace(/\s+/g, '') + "_" + Utilities.formatDate(now, "GMT+7", "dd-MM-yyyy_HH-mm") + ".jpg";
    jpgBlob.setName(namaFile);
    
    var folder = DriveApp.getFolderById(folderId);
    var fileTersimpan = folder.createFile(jpgBlob);
    fileTersimpan.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
    
    // ====================================================================
    // KONFIGURASI PENGIRIMAN LOGIKA BLOB & MESSAGE (IKUT SCRIPT HARIAN)
    // ====================================================================
    var tokenWa = "NgcPkuu5vmUmHYRpRLGw"; 
    var nomorTujuan = "120363410041245092@g.us"; 
    var waktuCetak = Utilities.formatDate(now, "GMT+7", "dd/MM/yyyy - HH:mm") + " WIB";
    
    // Format caption teks persis seperti potongan gambar utama Anda
    var pesanWa = "📊 *[LAPORAN ESTIMASI DAN RENCANA PANEN]*\n" +
                  "📅 Data per: *" + waktuCetak + "*";
    
    // Menggunakan parameter 'message' untuk teks dan 'file' untuk blob objek langsung
    var waPayload = {
      "target": nomorTujuan,
      "message": pesanWa.trim(),
      "file": fileTersimpan.getBlob() 
    };
    
    var waOptions = {
      "method": "post",
      "headers": { "Authorization": tokenWa },
      "payload": waPayload,
      "muteHttpExceptions": true
    };
    
    Logger.log("Mengirim pesan gambar sore ke WhatsApp...");
    var waResponse = UrlFetchApp.fetch("https://api.fonnte.com/send", waOptions);
    Logger.log("Respon WA: " + waResponse.getContentText());
  } else {
    Logger.log("Gagal mengonversi melalui API. Respon: " + apiResponse.getContentText());
  }
}