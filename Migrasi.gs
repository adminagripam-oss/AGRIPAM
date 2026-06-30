/**
 * ============================================================================
 * SCRIPT MIGRASI DATA: GOOGLE SHEETS → SUPABASE
 * ============================================================================
 * Petunjuk Penggunaan:
 * 1. Buka Google Sheets Anda.
 * 2. Klik Extensions → Apps Script.
 * 3. Buat file baru bernama `Migrasi.gs` dan paste kode di bawah ini.
 * 4. Ganti nilai `SUPABASE_URL` dan `SUPABASE_SERVICE_KEY` dengan milik Anda.
 * 5. Pilih fungsi `migrasiSemua` di dropdown atas lalu klik Run (▶).
 * ============================================================================
 */

var SUPABASE_URL = "https://wcocmwkccntmmtlofowe.supabase.co";
// Gunakan service_role key dari dashboard Supabase API Settings
var SUPABASE_SERVICE_KEY = "sb_secret_vjLgbKDiOGGCw8GGfLb53Q_a2Rr8jp0"; 

function migrasiSemua() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  Logger.log("=== MULAI MIGRASI DATA ===");
  
  // 1. Migrasi Database_Input
  try {
    migrasiDatabaseInput(ss);
  } catch(e) {
    Logger.log("❌ Error migrasi Database_Input: " + e.message);
  }
  
  // 2. Migrasi Data_Estimasi
  try {
    migrasiDataEstimasi(ss);
  } catch(e) {
    Logger.log("❌ Error migrasi Data_Estimasi: " + e.message);
  }
  
  // 3. Migrasi Sesi_Aktif
  try {
    migrasiSesiAktif(ss);
  } catch(e) {
    Logger.log("❌ Error migrasi Sesi_Aktif: " + e.message);
  }
  
  Logger.log("=== MIGRASI SELESAI ===");
}

function migrasiDatabaseInput(ss) {
  var sheet = ss.getSheetByName("Database_Input");
  if (!sheet) {
    Logger.log("⚠️ Sheet 'Database_Input' tidak ditemukan.");
    return;
  }
  
  var values = sheet.getDataRange().getValues();
  Logger.log("Membaca " + (values.length - 1) + " baris dari Database_Input...");
  
  var records = [];
  var timezone = ss.getSpreadsheetTimeZone();
  
  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    if (!row[0] || !row[1] || !row[2]) continue;
    
    // Format tanggal ke YYYY-MM-DD
    var tgl = "";
    try {
      tgl = Utilities.formatDate(new Date(row[0]), timezone, "yyyy-MM-dd");
    } catch(e) {
      tgl = String(row[0]).trim();
    }
    
    records.push({
      tanggal: tgl,
      region: String(row[1]).trim(),
      jam: String(row[2]).trim(),
      tonase: parseFloat(row[3]) || 0
    });
  }
  
  if (records.length > 0) {
    kirimKeSupabase("database_input", records);
  } else {
    Logger.log("Tidak ada data di Database_Input yang valid untuk dimigrasi.");
  }
}

function migrasiDataEstimasi(ss) {
  var sheet = ss.getSheetByName("Data_Estimasi");
  if (!sheet) {
    Logger.log("⚠️ Sheet 'Data_Estimasi' tidak ditemukan.");
    return;
  }
  
  var values = sheet.getDataRange().getValues();
  Logger.log("Membaca " + (values.length - 1) + " baris dari Data_Estimasi...");
  
  var records = [];
  var timezone = ss.getSpreadsheetTimeZone();
  
  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    if (!row[1] || !row[2]) continue;
    
    var waktuInputIso = "";
    try {
      waktuInputIso = new Date(row[0]).toISOString();
    } catch(e) {
      waktuInputIso = new Date().toISOString();
    }
    
    var tgl = "";
    try {
      tgl = Utilities.formatDate(new Date(row[1]), timezone, "yyyy-MM-dd");
    } catch(e) {
      tgl = String(row[1]).trim();
    }
    
    records.push({
      waktu_input: waktuInputIso,
      tanggal: tgl,
      region: String(row[2]).trim(),
      restan_lalu: parseFloat(row[3]) || 0,
      luas_panen_ha: parseFloat(row[4]) || 0,
      tk_panen_hk: parseFloat(row[5]) || 0,
      estimasi_panen_kg: parseFloat(row[6]) || 0,
      output_panen: parseFloat(row[7]) || 0,
      estimasi_kirim_kg: parseFloat(row[8]) || 0,
      estimasi_restan_kg: parseFloat(row[9]) || 0
    });
  }
  
  if (records.length > 0) {
    kirimKeSupabase("data_estimasi", records, true); // Gunakan upsert
  } else {
    Logger.log("Tidak ada data di Data_Estimasi yang valid untuk dimigrasi.");
  }
}

function migrasiSesiAktif(ss) {
  var sheet = ss.getSheetByName("Sesi_Aktif");
  if (!sheet) {
    Logger.log("⚠️ Sheet 'Sesi_Aktif' tidak ditemukan.");
    return;
  }
  
  var values = sheet.getDataRange().getValues();
  Logger.log("Membaca " + (values.length - 1) + " baris dari Sesi_Aktif...");
  
  var records = [];
  
  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    if (!row[0] || !row[1]) continue;
    
    var loginTimeIso = "";
    try {
      loginTimeIso = new Date(row[2]).toISOString();
    } catch(e) {
      loginTimeIso = new Date().toISOString();
    }
    
    var expiryIso = "";
    try {
      expiryIso = new Date(row[3]).toISOString();
    } catch(e) {
      expiryIso = new Date(Date.now() + 8*60*60*1000).toISOString();
    }
    
    records.push({
      region: String(row[0]).trim(),
      token: String(row[1]).trim(),
      login_time: loginTimeIso,
      expiry: expiryIso,
      status: String(row[4] || "Aktif").trim(),
      ip_address: String(row[5] || "").trim()
    });
  }
  
  if (records.length > 0) {
    kirimKeSupabase("sesi_aktif", records);
  } else {
    Logger.log("Tidak ada data di Sesi_Aktif yang valid untuk dimigrasi.");
  }
}

function kirimKeSupabase(tableName, records, isUpsert) {
  var url = SUPABASE_URL + "/rest/v1/" + tableName;
  var batchSize = 100;
  
  for (var i = 0; i < records.length; i += batchSize) {
    var chunk = records.slice(i, i + batchSize);
    var payload = JSON.stringify(chunk);
    
    var headers = {
      "apikey": SUPABASE_SERVICE_KEY,
      "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
      "Content-Type": "application/json",
      "Prefer": isUpsert ? "resolution=merge-duplicates" : "return=minimal"
    };
    
    var options = {
      "method": "post",
      "headers": headers,
      "payload": payload,
      "muteHttpExceptions": true
    };
    
    var response = UrlFetchApp.fetch(url, options);
    var code = response.getResponseCode();
    
    if (code >= 200 && code < 300) {
      Logger.log("✅ Berhasil mengunggah batch " + (i/batchSize + 1) + " (" + chunk.length + " baris) ke tabel " + tableName);
    } else {
      Logger.log("❌ Gagal mengunggah batch ke tabel " + tableName + " (Code " + code + "): " + response.getContentText());
    }
  }
}
