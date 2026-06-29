var REGION_PASSWORDS = {
  "Aceh": "ROACEH",
  "Sumatera Utara 1": "ROSUMUT1",
  "Sumatera Utara 2 Ex Torganda": "ROSUMUT2",
  "Riau 1": "RORiau1",
  "Riau 2": "RORiau2",
  "Riau 3": "RORiau3",
  "Riau 4": "RORiau4",
  "Bangka Belitung": "ROBabel",
  "Jambi": "ROJambi",
  "Sumatera Barat": "ROSumbar",
  "Sumatera Selatan": "ROSumsel",
  "Kalimantan Barat 1": "ROKalbar1",
  "Kalimantan Barat 2": "ROKalbar2",
  "Kalimantan Selatan 1": "ROKalsel1",
  "Kalimantan Selatan 2": "ROKalsel2",
  "Kalimantan Timur": "ROKaltim",
  "Kalimantan Utara": "ROKalut",
  "Kalimantan Tengah 1": "ROKalteng1",
  "Kalimantan Tengah 2": "ROKalteng2",
  "Kalimantan Tengah 3": "ROKalteng3",
  "Sulawesi Tenggara": "ROSultra",
  "Sulawesi Tengah": "ROSulteng",
  "ADMIN": "TANAMAN"
};

var SPREADSHEET_ID = "1lzMt1s-QFasCS9lCuQH5azFu4PKeXzplxxEIq7_Q-b0";
var SHEET_NAME = "Database_Input";
var SHEET_ESTIMASI_NAME = "Data_Estimasi";

// Rate limiting
var RATE_LIMIT_MAX_ATTEMPTS = 5;
var RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 menit

// Session
var SESSION_TTL_MS = 8 * 60 * 60 * 1000; // 8 jam
var TOKEN_KEY_PREFIX = "tok_";
var ACTIVE_SESS_PREFIX = "active_sess_";
var LOG_PREFIX = "log_";

// Validasi tonase
var MIN_TONASE = 0;
var MAX_TONASE = 5000;

// ---------------------------------------------------------------------------
// ENTRY POINT
// ---------------------------------------------------------------------------

function doGet(e) {
  var params = e.parameter;
  var action = params.action || "getData";
  var callback = params.callback;
  var result;

  try {
    if (action === "login") {
      result = handleLogin(params);

    } else if (action === "getData") {
      var sheet = openSheet();
      if (!sheet) {
        result = { success: false, message: "Sheet '" + SHEET_NAME + "' tidak ditemukan di Spreadsheet!" };
      } else {
        result = handleGetData(sheet, params);
      }

    } else if (action === "getRunningTextData") {
      var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
      var sheetRun = ss.getSheetByName("Database_Input");
      if (!sheetRun) {
        result = { success: false, message: "Sheet 'Database_Input' tidak ditemukan di Spreadsheet!" };
      } else {
        result = handleGetData(sheetRun, params);
      }

    } else if (action === "getEstimasiData") {
      var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
      var sheetEst = ss.getSheetByName(SHEET_ESTIMASI_NAME);
      if (!sheetEst) {
        result = { success: false, message: "Sheet '" + SHEET_ESTIMASI_NAME + "' tidak ditemukan di Spreadsheet!" };
      } else {
        result = handleGetEstimasiData(sheetEst, params);
      }

    } else if (action === "insert" || action === "delete" || action === "insertEstimasi" || action === "deleteEstimasi") {
      var tokenCheck = validateToken(params.token, params.region);
      if (!tokenCheck.valid) {
        result = { success: false, message: tokenCheck.message };
      } else {
        if (action === "insertEstimasi") {
          result = handleInsertEstimasi(params);
        } else if (action === "deleteEstimasi") {
          result = handleDeleteEstimasi(params);
        } else {
          var sheet = openSheet();
          if (!sheet) {
            result = { success: false, message: "Sheet '" + SHEET_NAME + "' tidak ditemukan di Spreadsheet!" };
          } else {
            result = (action === "insert")
              ? handleInsert(sheet, params)
              : handleDelete(sheet, params);
          }
        }
      }

    } else if (action === "logout") {
      result = handleLogout(params);

      // ✅ BARU: endpoint refresh token untuk perpanjang sesi
    } else if (action === "refreshToken") {
      result = handleRefreshToken(params);

    } else if (action === "kirimScreenshotHarian" || action === "kirimScreenshotSoreKhusus") {
      var tokenCheck = validateToken(params.token, "ADMIN");
      if (!tokenCheck.valid) {
        result = { success: false, message: tokenCheck.message };
      } else {
        if (action === "kirimScreenshotHarian") {
          try {
            kirimScreenshotHarian();
            result = { success: true, message: "Screenshot Harian berhasil diproses dan dikirim ke WhatsApp." };
          } catch (e) {
            result = { success: false, message: "Gagal memproses Screenshot Harian: " + e.toString() };
          }
        } else {
          try {
            kirimScreenshotSoreKhusus();
            result = { success: true, message: "Screenshot Sore berhasil diproses dan dikirim ke WhatsApp." };
          } catch (e) {
            result = { success: false, message: "Gagal memproses Screenshot Sore: " + e.toString() };
          }
        }
      }

    } else {
      result = { success: false, message: "Aksi tidak dikenal: " + action };
    }

  } catch (err) {
    result = { success: false, message: "Error server: " + err.message };
  }

  return buildOutput(result, callback);
}

// ---------------------------------------------------------------------------
// HANDLER: LOGIN (versi baru — tidak blokir, langsung override sesi lama)
// ---------------------------------------------------------------------------

function handleLogin(params) {
  var region = (params.region || "").trim();
  var password = (params.password || "").trim();
  var ipAddress = (params.ip || "IP Tidak Terdeteksi").trim();

  if (!region || !password) {
    return { success: false, message: "Region dan Password wajib diisi." };
  }
  if (!REGION_PASSWORDS.hasOwnProperty(region)) {
    return { success: false, message: "Region tidak dikenal." };
  }

  var rateLimitResult = checkRateLimit(region);
  if (!rateLimitResult.allowed) {
    return {
      success: false,
      message: "Terlalu banyak percobaan login. Coba lagi dalam "
        + Math.ceil(rateLimitResult.waitMs / 60000) + " menit."
    };
  }

  if (REGION_PASSWORDS[region] !== password) {
    recordFailedAttempt(region);
    return { success: false, message: "Password salah untuk Region " + region + "!" };
  }

  // ✅ PERUBAHAN UTAMA: tidak blokir sesi aktif lama.
  // Jika ada sesi lama (expired atau masih valid) → hapus/override langsung.
  // Mengatasi kasus: tutup tab, ganti HP, lupa logout, dll.
  var props = PropertiesService.getScriptProperties();
  var activeSessKey = ACTIVE_SESS_PREFIX + region;
  var existingToken = props.getProperty(activeSessKey);

  if (existingToken) {
    var existingRaw = props.getProperty(TOKEN_KEY_PREFIX + existingToken);
    if (existingRaw) {
      try {
        var existingData = JSON.parse(existingRaw);
        var isStillValid = Date.now() < existingData.expiry;

        // Hapus token lama (expired maupun masih valid)
        props.deleteProperty(TOKEN_KEY_PREFIX + existingToken);
        props.deleteProperty(activeSessKey);

        // Catat ke audit log jika sesi lama di-override paksa
        if (isStillValid) {
          writeAuditLog(props, region, "SESSION_OVERRIDE",
            "Sesi lama di-override oleh login baru dari IP: " + ipAddress);
        }
      } catch (e) {
        props.deleteProperty(TOKEN_KEY_PREFIX + existingToken);
        props.deleteProperty(activeSessKey);
      }
    } else {
      props.deleteProperty(activeSessKey);
    }
  }

  // Reset rate limit & buat token baru
  resetRateLimit(region);
  var token = createSessionToken(region);

  var clientTimeStr = params.clientTime || "";
  var wibNow, wibExpiry;
  if (clientTimeStr) {
    wibNow = clientTimeStr;
    try {
      var parts = clientTimeStr.split(" ");
      var dateParts = parts[0].split("-");
      var timeParts = parts[1].split(":");
      var d = new Date(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      );
      var expiryTime = d.getTime() + SESSION_TTL_MS;
      wibExpiry = Utilities.formatDate(new Date(expiryTime), "Asia/Jakarta", "yyyy-MM-dd HH:mm:ss");
    } catch (e) {
      wibExpiry = Utilities.formatDate(new Date(Date.now() + SESSION_TTL_MS), "Asia/Jakarta", "yyyy-MM-dd HH:mm:ss");
    }
  } else {
    wibNow = Utilities.formatDate(new Date(), "Asia/Jakarta", "yyyy-MM-dd HH:mm:ss");
    wibExpiry = Utilities.formatDate(new Date(Date.now() + SESSION_TTL_MS), "Asia/Jakarta", "yyyy-MM-dd HH:mm:ss");
  }

  // Tulis ke Spreadsheet (Live Monitoring)
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheetSesi = ss.getSheetByName("Sesi_Aktif");
    if (sheetSesi) {
      var nextRow = sheetSesi.getLastRow() + 1;
      sheetSesi.getRange(nextRow, 1).setNumberFormat("@").setValue(region);
      sheetSesi.getRange(nextRow, 2).setNumberFormat("@").setValue(token);
      sheetSesi.getRange(nextRow, 3).setValue(wibNow);
      sheetSesi.getRange(nextRow, 4).setValue(wibExpiry);
      sheetSesi.getRange(nextRow, 5).setNumberFormat("@").setValue("Aktif");
      sheetSesi.getRange(nextRow, 6).setNumberFormat("@").setValue(ipAddress);
    }
  } catch (err) {
    console.log("Error penulisan sesi ke sheet: " + err.message);
  }

  writeAuditLog(props, region, "LOGIN_SUCCESS", "Login dari IP: " + ipAddress);

  return {
    success: true,
    message: "Login berhasil.",
    token: token,
    ttlMs: SESSION_TTL_MS
  };
}

// ---------------------------------------------------------------------------
// HANDLER: LOGOUT (versi baru — update status di sheet)
// ---------------------------------------------------------------------------

function handleLogout(params) {
  var token = (params.token || "").trim();
  var region = (params.region || "").trim();

  if (!token || !region) return { success: false, message: "Token dan Region wajib diisi." };

  var props = PropertiesService.getScriptProperties();
  props.deleteProperty(TOKEN_KEY_PREFIX + token);

  var activeSessKey = ACTIVE_SESS_PREFIX + region;
  if (props.getProperty(activeSessKey) === token) {
    props.deleteProperty(activeSessKey);
  }

  // ✅ Update status di sheet Sesi_Aktif menjadi "Logout"
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheetSesi = ss.getSheetByName("Sesi_Aktif");
    if (sheetSesi) {
      var data = sheetSesi.getDataRange().getValues();
      for (var i = data.length - 1; i >= 1; i--) {
        if (String(data[i][1]).trim() === token) {
          sheetSesi.getRange(i + 1, 5).setValue("Logout");
          break;
        }
      }
    }
  } catch (err) {
    console.log("Error update status logout: " + err.message);
  }

  writeAuditLog(props, region, "LOGOUT", "Logout normal.");
  return { success: true, message: "Logout berhasil." };
}

// ---------------------------------------------------------------------------
// HANDLER: REFRESH TOKEN (perpanjang sesi tanpa login ulang)
// ---------------------------------------------------------------------------

function handleRefreshToken(params) {
  var token = (params.token || "").trim();
  var region = (params.region || "").trim();

  var check = validateToken(token, region);
  if (!check.valid) {
    return { success: false, message: check.message };
  }

  var props = PropertiesService.getScriptProperties();
  var raw = props.getProperty(TOKEN_KEY_PREFIX + token);
  if (!raw) {
    return { success: false, message: "Token tidak ditemukan." };
  }

  try {
    var data = JSON.parse(raw);
    data.expiry = Date.now() + SESSION_TTL_MS;
    props.setProperty(TOKEN_KEY_PREFIX + token, JSON.stringify(data));
    return { success: true, message: "Sesi diperpanjang.", ttlMs: SESSION_TTL_MS };
  } catch (e) {
    return { success: false, message: "Gagal memperpanjang sesi: " + e.message };
  }
}

// ---------------------------------------------------------------------------
// HANDLER: ESTIMASI PANEN
// ---------------------------------------------------------------------------

function handleInsertEstimasi(params) {
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();
  var estimasiRestanLalu = params.estimasiRestanLalu;
  var luasPanen = params.luasPanen;
  var tkPanen = params.tkPanen;
  var estimasiPanen = params.estimasiPanen;
  var outputPanen = params.outputPanen;
  var estimasiKirim = params.estimasiKirim;
  var estimasiRestan = params.estimasiRestan;

  if (!tanggal || !region || estimasiRestanLalu === undefined || estimasiRestanLalu === ""
    || !luasPanen || !tkPanen || !estimasiPanen || !estimasiKirim || !estimasiRestan) {
    return { success: false, message: "Data estimasi tidak lengkap (pastikan semua kolom terisi)." };
  }

  var restanLaluNum = parseFloat(estimasiRestanLalu);
  var luasPanenNum = parseFloat(luasPanen);
  var tkPanenNum = parseFloat(tkPanen);
  var estPanenNum = parseFloat(estimasiPanen);
  var outPanenNum = parseFloat(outputPanen) || 0;
  var estKirimNum = parseFloat(estimasiKirim);
  var estRestanNum = parseFloat(estimasiRestan);

  if (isNaN(restanLaluNum) || isNaN(luasPanenNum) || isNaN(tkPanenNum) ||
    isNaN(estPanenNum) || isNaN(estKirimNum) || isNaN(estRestanNum)) {
    return { success: false, message: "Terdapat nilai yang bukan angka. Periksa kembali isian Anda." };
  }

  var lock = LockService.getScriptLock();
  var gotLock = lock.tryLock(30000);
  if (!gotLock) {
    return { success: false, message: "Server sedang memproses data lain. Silakan coba beberapa saat lagi." };
  }

  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var ssTimezone = ss.getSpreadsheetTimeZone();
    var sheetEst = ss.getSheetByName(SHEET_ESTIMASI_NAME);

    if (!sheetEst) {
      return { success: false, message: "Sheet '" + SHEET_ESTIMASI_NAME + "' belum dibuat di Spreadsheet!" };
    }

    var data = sheetEst.getDataRange().getDisplayValues();
    for (var i = 1; i < data.length; i++) {
      var rowTanggal = formatTanggal(data[i][1], ssTimezone);
      var rowRegion = String(data[i][2]).trim();
      if (rowTanggal === tanggal && rowRegion === region) {
        return {
          success: false,
          message: "Data estimasi tanggal " + isoToDisplay(tanggal) + " sudah ada. Gunakan 'Hapus Estimasi' untuk merevisi."
        };
      }
    }

    var nextRow = sheetEst.getLastRow() + 1;
    var clientTimeStr = params.clientTime || Utilities.formatDate(new Date(), "Asia/Jakarta", "yyyy-MM-dd HH:mm:ss");
    sheetEst.getRange(nextRow, 1).setValue(clientTimeStr);
    sheetEst.getRange(nextRow, 2).setNumberFormat("@").setValue(isoToDisplay(tanggal));
    sheetEst.getRange(nextRow, 3).setNumberFormat("@").setValue(region);
    sheetEst.getRange(nextRow, 4).setValue(restanLaluNum);
    sheetEst.getRange(nextRow, 5).setValue(luasPanenNum);
    sheetEst.getRange(nextRow, 6).setValue(tkPanenNum);
    sheetEst.getRange(nextRow, 7).setValue(estPanenNum);
    sheetEst.getRange(nextRow, 8).setValue(outPanenNum);
    sheetEst.getRange(nextRow, 9).setValue(estKirimNum);
    sheetEst.getRange(nextRow, 10).setValue(estRestanNum);

    return { success: true, message: "Data estimasi berhasil disimpan!" };
  } finally {
    lock.releaseLock();
  }
}

// ---------------------------------------------------------------------------
// HANDLER: DELETE ESTIMASI PANEN
// ---------------------------------------------------------------------------

function handleDeleteEstimasi(params) {
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();

  if (!tanggal || !region) {
    return { success: false, message: "Tanggal dan Region wajib diisi untuk menghapus data estimasi." };
  }

  var lock = LockService.getScriptLock();
  var gotLock = lock.tryLock(30000);
  if (!gotLock) {
    return { success: false, message: "Server sedang memproses data lain. Silakan coba beberapa saat lagi." };
  }

  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var ssTimezone = ss.getSpreadsheetTimeZone();
    var sheetEst = ss.getSheetByName(SHEET_ESTIMASI_NAME);

    if (!sheetEst) {
      return { success: false, message: "Sheet '" + SHEET_ESTIMASI_NAME + "' belum dibuat di Spreadsheet!" };
    }

    var data = sheetEst.getDataRange().getDisplayValues();
    var deletedCount = 0;

    for (var i = data.length - 1; i >= 1; i--) {
      var rowTanggal = formatTanggal(data[i][1], ssTimezone);
      var rowRegion = String(data[i][2]).trim();
      if (rowTanggal === tanggal && rowRegion === region) {
        sheetEst.deleteRow(i + 1);
        deletedCount++;
      }
    }

    if (deletedCount === 0) {
      return { success: false, message: "Data estimasi untuk tanggal " + isoToDisplay(tanggal) + " dan Region " + region + " tidak ditemukan." };
    }
    return { success: true, message: "Berhasil menghapus " + deletedCount + " baris data estimasi." };
  } finally {
    lock.releaseLock();
  }
}

// ---------------------------------------------------------------------------
// HANDLER: GET DATA
// ---------------------------------------------------------------------------

function handleGetData(sheet, params) {
  if (!sheet) {
    return { success: false, message: "Objek sheet tidak valid (null)." };
  }
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();

  if (!tanggal) {
    return { success: false, message: "Tanggal wajib diisi." };
  }

  var ssTimezone = sheet.getParent().getSpreadsheetTimeZone();
  var data = sheet.getDataRange().getValues();

  if (region === "" || region.toUpperCase() === "ALL") {
    var records = [];
    for (var i = 1; i < data.length; i++) {
      var rowTanggal = formatTanggal(data[i][0], ssTimezone);
      if (rowTanggal === tanggal) {
        records.push({
          region: String(data[i][1]).trim(),
          jam: String(data[i][2]).trim(),
          tonase: parseFloat(data[i][3]) || 0
        });
      }
    }
    return { success: true, allRecords: records };
  } else {
    var total = 0;
    var jamData = {};

    for (var i = 1; i < data.length; i++) {
      var rowTanggal = formatTanggal(data[i][0], ssTimezone);
      var rowRegion = String(data[i][1]).trim();
      var rowJam = String(data[i][2]).trim();
      var rowTonase = parseFloat(data[i][3]) || 0;

      if (rowTanggal === tanggal && rowRegion === region) {
        total += rowTonase;
        jamData[rowJam] = rowTonase;
      }
    }

    return { success: true, total: round2(total), jamData: jamData };
  }
}

// ---------------------------------------------------------------------------
// HANDLER: INSERT REALISASI
// ---------------------------------------------------------------------------

function handleInsert(sheet, params) {
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();
  var jam = (params.jam || "").trim();
  var tonase = params.tonase;

  if (!tanggal || !region || !jam || tonase === undefined || tonase === "") {
    return { success: false, message: "Data tidak lengkap (tanggal/region/jam/tonase)." };
  }

  var tonaseNum = parseFloat(tonase);
  if (isNaN(tonaseNum)) {
    return { success: false, message: "Nilai tonase tidak valid." };
  }
  if (tonaseNum < MIN_TONASE || tonaseNum > MAX_TONASE) {
    return { success: false, message: "Tonase harus antara " + MIN_TONASE + " dan " + MAX_TONASE + " ton." };
  }

  var lock = LockService.getScriptLock();
  var gotLock = lock.tryLock(30000);
  if (!gotLock) {
    return { success: false, message: "Server sedang memproses data lain. Silakan coba beberapa saat lagi." };
  }

  try {
    var existing = handleGetData(sheet, params);

    if (existing.jamData.hasOwnProperty(jam)) {
      return {
        success: false,
        message: "Data jam " + jam + " sudah ada. Gunakan 'Hapus Jam Ini' untuk merevisi.",
        total: existing.total,
        jamData: existing.jamData
      };
    }

    var nextRow = sheet.getLastRow() + 1;
    sheet.getRange(nextRow, 1).setNumberFormat("@").setValue(isoToDisplay(tanggal));
    sheet.getRange(nextRow, 2).setNumberFormat("@").setValue(region);
    sheet.getRange(nextRow, 3).setNumberFormat("@").setValue(jam);
    sheet.getRange(nextRow, 4).setValue(tonaseNum);

    var newTotal = round2(existing.total + tonaseNum);
    existing.jamData[jam] = tonaseNum;

    return { success: true, message: "Data berhasil disimpan.", total: newTotal, jamData: existing.jamData };
  } finally {
    lock.releaseLock();
  }
}

// ---------------------------------------------------------------------------
// HANDLER: DELETE REALISASI
// ---------------------------------------------------------------------------

function handleDelete(sheet, params) {
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();
  var jam = (params.jam || "").trim();

  if (!tanggal || !region || !jam) {
    return { success: false, message: "Tanggal, Region, dan Jam wajib diisi." };
  }

  var lock = LockService.getScriptLock();
  var gotLock = lock.tryLock(30000);
  if (!gotLock) {
    return { success: false, message: "Server sedang memproses data lain. Silakan coba beberapa saat lagi." };
  }

  try {
    var ssTimezone = sheet.getParent().getSpreadsheetTimeZone();
    var data = sheet.getDataRange().getValues();
    var deletedCount = 0;
    var debugRows = [];

    for (var i = data.length - 1; i >= 1; i--) {
      var rowTanggal = formatTanggal(data[i][0], ssTimezone);
      var rowRegion = String(data[i][1]).trim();
      var rowJam = String(data[i][2]).trim();
      var isMatch = (rowTanggal === tanggal && rowRegion === region && rowJam === jam);

      if (debugRows.length < 10) {
        debugRows.push({ sheetRow: i + 1, rowTanggal: rowTanggal, rowRegion: rowRegion, rowJam: rowJam, match: isMatch });
      }
      if (isMatch) { sheet.deleteRow(i + 1); deletedCount++; }
    }

    if (deletedCount === 0) {
      var current = handleGetData(sheet, params);
      return {
        success: false,
        message: "Data jam " + jam + " tidak ditemukan di database.",
        total: current.total,
        jamData: current.jamData,
        debug: { inputTanggal: tanggal, inputRegion: region, inputJam: jam, deletedCount: 0, sampleRows: debugRows }
      };
    }

    var refreshed = handleGetData(sheet, params);
    return {
      success: true,
      message: "Data jam " + jam + " berhasil dihapus (" + deletedCount + " baris).",
      total: refreshed.total,
      jamData: refreshed.jamData,
      debug: { inputTanggal: tanggal, inputRegion: region, inputJam: jam, deletedCount: deletedCount, sampleRows: debugRows }
    };
  } finally {
    lock.releaseLock();
  }
}

// ---------------------------------------------------------------------------
// HANDLER: GET ESTIMASI DATA
// ---------------------------------------------------------------------------

function handleGetEstimasiData(sheet, params) {
  if (!sheet) {
    return { success: false, message: "Objek sheet tidak valid (null)." };
  }
  var tanggal = (params.tanggal || "").trim();
  var region = (params.region || "").trim();

  if (!tanggal) {
    return { success: false, message: "Tanggal wajib diisi." };
  }

  var ssTimezone = sheet.getParent().getSpreadsheetTimeZone();
  var data = sheet.getDataRange().getDisplayValues();

  if (region === "" || region.toUpperCase() === "ALL") {
    var allEstimasi = {};
    for (var i = 1; i < data.length; i++) {
      var rowTanggal = formatTanggal(data[i][1], ssTimezone);
      if (rowTanggal === tanggal) {
        var rowRegion = String(data[i][2]).trim();
        allEstimasi[rowRegion] = {
          estimasiRestanLalu: data[i][3],
          luasPanen: data[i][4],
          tkPanen: data[i][5],
          estimasiPanen: data[i][6],
          outputPanen: data[i][7],
          estimasiKirim: data[i][8],
          estimasiRestan: data[i][9]
        };
      }
    }
    return { success: true, exists: Object.keys(allEstimasi).length > 0, allEstimasi: allEstimasi };
  } else {
    var exists = false;
    var existingData = null;

    for (var i = 1; i < data.length; i++) {
      var rowTanggal = formatTanggal(data[i][1], ssTimezone);
      var rowRegion = String(data[i][2]).trim();

      if (rowTanggal === tanggal && rowRegion === region) {
        exists = true;
        existingData = {
          estimasiRestanLalu: data[i][3],
          luasPanen: data[i][4],
          tkPanen: data[i][5],
          estimasiPanen: data[i][6],
          outputPanen: data[i][7],
          estimasiKirim: data[i][8],
          estimasiRestan: data[i][9]
        };
        break;
      }
    }

    return { success: true, exists: exists, data: existingData };
  }
}

// ---------------------------------------------------------------------------
// RATE LIMITING
// ---------------------------------------------------------------------------

function checkRateLimit(region) {
  var props = PropertiesService.getScriptProperties();
  var key = "rl_" + region;
  var raw = props.getProperty(key);
  var now = Date.now();

  if (!raw) return { allowed: true };

  var record = JSON.parse(raw);
  if (now - record.windowStart > RATE_LIMIT_WINDOW_MS) {
    props.deleteProperty(key);
    return { allowed: true };
  }
  if (record.attempts >= RATE_LIMIT_MAX_ATTEMPTS) {
    return { allowed: false, waitMs: RATE_LIMIT_WINDOW_MS - (now - record.windowStart) };
  }
  return { allowed: true };
}

function recordFailedAttempt(region) {
  var props = PropertiesService.getScriptProperties();
  var key = "rl_" + region;
  var raw = props.getProperty(key);
  var now = Date.now();
  var record;

  if (!raw || (now - JSON.parse(raw).windowStart > RATE_LIMIT_WINDOW_MS)) {
    record = { attempts: 1, windowStart: now };
  } else {
    record = JSON.parse(raw);
    record.attempts += 1;
  }
  props.setProperty(key, JSON.stringify(record));
}

function resetRateLimit(region) {
  PropertiesService.getScriptProperties().deleteProperty("rl_" + region);
}

// ---------------------------------------------------------------------------
// SESSION TOKEN
// ---------------------------------------------------------------------------

function createSessionToken(region) {
  var props = PropertiesService.getScriptProperties();
  var activeSessKey = ACTIVE_SESS_PREFIX + region;
  var oldToken = props.getProperty(activeSessKey);

  if (oldToken) props.deleteProperty(TOKEN_KEY_PREFIX + oldToken);

  var newToken = "";
  for (var i = 0; i < 32; i++) {
    newToken += Math.floor(Math.random() * 16).toString(16);
  }

  var expiry = Date.now() + SESSION_TTL_MS;
  props.setProperty(TOKEN_KEY_PREFIX + newToken, JSON.stringify({ region: region, expiry: expiry }));
  props.setProperty(activeSessKey, newToken);
  return newToken;
}

function validateToken(token, regionFromClient) {
  if (!token) return { valid: false, message: "Sesi tidak ditemukan. Silakan login ulang." };

  var props = PropertiesService.getScriptProperties();
  var raw = props.getProperty(TOKEN_KEY_PREFIX + token);

  if (!raw) return { valid: false, message: "Sesi tidak valid atau sudah kedaluwarsa. Silakan login ulang." };

  var data = JSON.parse(raw);

  if (Date.now() > data.expiry) {
    props.deleteProperty(TOKEN_KEY_PREFIX + token);
    var activeSessKey = ACTIVE_SESS_PREFIX + data.region;
    if (props.getProperty(activeSessKey) === token) props.deleteProperty(activeSessKey);
    return { valid: false, message: "Sesi sudah kedaluwarsa. Silakan login ulang." };
  }

  if (regionFromClient && data.region !== regionFromClient) {
    return { valid: false, message: "Token tidak sesuai dengan region. Silakan login ulang." };
  }

  var activeSessKey = ACTIVE_SESS_PREFIX + data.region;
  var currentToken = props.getProperty(activeSessKey);

  if (currentToken !== token) {
    return { valid: false, message: "Sesi Anda diakhiri karena ada login baru di perangkat lain. Silakan login ulang." };
  }

  return { valid: true, region: data.region };
}

// ---------------------------------------------------------------------------
// AUDIT LOG
// ---------------------------------------------------------------------------

function writeAuditLog(props, region, action, detail) {
  try {
    var logKey = LOG_PREFIX + region + "_" + Date.now();
    var logEntry = JSON.stringify({ region: region, action: action, detail: detail, time: new Date().toISOString() });
    props.setProperty(logKey, logEntry);
  } catch (e) {
    console.log("Audit log error: " + e.message);
  }
}

// ---------------------------------------------------------------------------
// CLEANUP — pasang Time Trigger tiap 1 jam di Apps Script
// ---------------------------------------------------------------------------

function cleanupAllExpiredTokens() {
  var props = PropertiesService.getScriptProperties();
  var now = Date.now();
  var all = props.getProperties();
  var count = 0;
  var expiredTokens = [];

  Object.keys(all).forEach(function (key) {
    if (key.indexOf(TOKEN_KEY_PREFIX) !== 0) return;
    try {
      var data = JSON.parse(all[key]);
      if (now > data.expiry) {
        expiredTokens.push({ key: key, token: key.slice(TOKEN_KEY_PREFIX.length), region: data.region });
        props.deleteProperty(key);
        count++;
      }
    } catch (err) {
      props.deleteProperty(key);
      count++;
    }
  });

  expiredTokens.forEach(function (item) {
    // Bersihkan pointer active_sess
    var activeSessKey = ACTIVE_SESS_PREFIX + item.region;
    if (props.getProperty(activeSessKey) === item.token) {
      props.deleteProperty(activeSessKey);
    }

    // ✅ Update status di sheet Sesi_Aktif → "Expired"
    try {
      var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
      var sheetSesi = ss.getSheetByName("Sesi_Aktif");
      if (sheetSesi) {
        var sheetData = sheetSesi.getDataRange().getValues();
        for (var i = sheetData.length - 1; i >= 1; i--) {
          if (String(sheetData[i][1]).trim() === item.token) {
            sheetSesi.getRange(i + 1, 5).setValue("Expired");
            break;
          }
        }
      }
    } catch (e) {
      console.log("Gagal update status expired: " + e.message);
    }
  });

  // ✅ Cleanup audit log lama (> 7 hari)
  Object.keys(all).forEach(function (key) {
    if (key.indexOf(LOG_PREFIX) !== 0) return;
    var parts = key.split("_");
    var timestamp = parseInt(parts[parts.length - 1], 10);
    if (!isNaN(timestamp) && timestamp < now - (7 * 24 * 60 * 60 * 1000)) {
      props.deleteProperty(key);
    }
  });

  console.log("Cleanup selesai: " + count + " token expired dihapus.");
  return count;
}

// ---------------------------------------------------------------------------
// FORCE LOGOUT MANUAL (darurat, ubah nama region sesuai kebutuhan)
// ---------------------------------------------------------------------------

function forceLogoutRegion() {
  var props = PropertiesService.getScriptProperties();
  var region = "ADMIN"; // ← ganti nama region jika perlu
  var activeSessKey = "active_sess_" + region;
  var token = props.getProperty(activeSessKey);

  if (token) {
    props.deleteProperty("tok_" + token);
    props.deleteProperty(activeSessKey);
    console.log("Force logout berhasil untuk region: " + region);
  } else {
    console.log("Tidak ada sesi aktif untuk region: " + region);
  }
}

// ---------------------------------------------------------------------------
// UTILITAS
// ---------------------------------------------------------------------------

function openSheet() {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);
}

function validatePassword(region, password) {
  return REGION_PASSWORDS.hasOwnProperty(region) && REGION_PASSWORDS[region] === password;
}

function formatTanggal(rawDate, ssTimezone) {
  if (rawDate instanceof Date) {
    var tz = ssTimezone || "Asia/Jakarta";
    return Utilities.formatDate(rawDate, tz, "yyyy-MM-dd");
  }
  var str = String(rawDate).trim();
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(str)) return displayToIso(str);
  return str;
}

function isoToDisplay(isoDate) {
  var parts = String(isoDate).trim().split("-");
  return parts.length === 3 ? parts[2] + "/" + parts[1] + "/" + parts[0] : String(isoDate).trim();
}

function displayToIso(displayDate) {
  var parts = String(displayDate).trim().split("/");
  return parts.length === 3 ? parts[2] + "-" + parts[1] + "-" + parts[0] : String(displayDate).trim();
}

function round2(num) {
  return Math.round(num * 100) / 100;
}

function buildOutput(result, callback) {
  var json = JSON.stringify(result);
  if (callback) {
    return ContentService.createTextOutput(callback + "(" + json + ")").setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
}

// ---------------------------------------------------------------------------
// MIGRASI DATA LAMA (jalankan SEKALI SAJA secara manual)
// ---------------------------------------------------------------------------

function migrateTanggalToDDMMYYYY() {
  var sheet = openSheet();
  var data = sheet.getDataRange().getValues();
  var count = 0;

  for (var i = 1; i < data.length; i++) {
    var raw = data[i][0];
    var str;

    if (raw instanceof Date) {
      var y = raw.getFullYear();
      var m = ("0" + (raw.getMonth() + 1)).slice(-2);
      var d = ("0" + raw.getDate()).slice(-2);
      str = y + "-" + m + "-" + d;
    } else {
      str = String(raw).trim();
    }

    if (/^\d{4}-\d{2}-\d{2}$/.test(str)) {
      sheet.getRange(i + 1, 1).setNumberFormat("@").setValue(isoToDisplay(str));
      count++;
    }
  }
  return count;
}

// ---------------------------------------------------------------------------
// POST ENTRY POINT & SCREENSHOT HANDLERS
// ---------------------------------------------------------------------------

function doPost(e) {
  var params = {};
  try {
    if (e && e.postData && e.postData.contents) {
      try {
        params = JSON.parse(e.postData.contents);
      } catch (ex) {
        params = {};
        var parts = e.postData.contents.split("&");
        for (var i = 0; i < parts.length; i++) {
          var pair = parts[i].split("=");
          var key = decodeURIComponent(pair[0]);
          var value = decodeURIComponent(pair[1] || "");
          params[key] = value;
        }
      }
    } else if (e && e.parameter) {
      params = e.parameter;
    }
    
    var action = params.action;
    var result;
    
    if (action === "uploadScreenshot" || action === "sendScreenshotSummary" || action === "sendScreenshotActiveDashboard") {
      var tokenCheck = validateToken(params.token, "ADMIN");
      if (!tokenCheck.valid) {
        result = { success: false, message: tokenCheck.message };
      } else {
        if (action === "uploadScreenshot") {
          result = handleUploadScreenshot(params);
        } else if (action === "sendScreenshotSummary") {
          result = handleSendScreenshotSummary(params);
        } else {
          result = handleSendActiveDashboardScreenshot(params);
        }
      }
    } else {
      result = { success: false, message: "Aksi POST tidak dikenal: " + String(action) };
    }
  } catch (err) {
    result = { success: false, message: "Error server: " + err.message };
  }
  
  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
}

function handleUploadScreenshot(params) {
  if (!params) {
    return { success: false, message: "Parameter tidak boleh kosong." };
  }
  var base64Data = params.base64Data;
  var region = params.region || "UNKNOWN";
  var tanggal = params.tanggal || "TODAY";
  
  if (!base64Data) {
    return { success: false, message: "Data gambar kosong." };
  }
  
  try {
    var base64Image = base64Data.split(",")[1];
    var decodedBlob = Utilities.newBlob(Utilities.base64Decode(base64Image), "image/jpeg");
    
    var now = new Date();
    var namaFile = "Grafik_" + region.replace(/\s+/g, '') + "_" + tanggal.replace(/[\/\s]/g, '-') + "_" + Utilities.formatDate(now, "GMT+7", "HH-mm") + ".jpg";
    decodedBlob.setName(namaFile);
    
    var folderId = "1HaZkgflPW6IkLXaBUMl8nJCGWIMCyOxM";
    var folder = DriveApp.getFolderById(folderId);
    var fileTersimpan = folder.createFile(decodedBlob);
    fileTersimpan.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
    
    return { 
      success: true, 
      message: "Screenshot region " + region + " berhasil disimpan.",
      url: fileTersimpan.getUrl()
    };
  } catch (err) {
    return { success: false, message: "Gagal menyimpan screenshot: " + err.toString() };
  }
}

function handleSendScreenshotSummary(params) {
  if (!params) {
    return { success: false, message: "Parameter tidak boleh kosong." };
  }
  var base64Data = params.base64Data;
  var tanggal = params.tanggal || "TODAY";
  var linksJson = params.links || "{}";
  
  if (!base64Data) {
    return { success: false, message: "Data gambar ringkasan kosong." };
  }
  
  try {
    var links = JSON.parse(linksJson);
    
    var base64Image = base64Data.split(",")[1];
    var decodedBlob = Utilities.newBlob(Utilities.base64Decode(base64Image), "image/jpeg");
    
    var now = new Date();
    var namaFile = "Grafik_SemuaRegion_" + tanggal.replace(/[\/\s]/g, '-') + "_" + Utilities.formatDate(now, "GMT+7", "HH-mm") + ".jpg";
    decodedBlob.setName(namaFile);
    
    var folderId = "1HaZkgflPW6IkLXaBUMl8nJCGWIMCyOxM";
    var folder = DriveApp.getFolderById(folderId);
    var fileTersimpan = folder.createFile(decodedBlob);
    fileTersimpan.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
    
    var waktuCetak = Utilities.formatDate(now, "GMT+7", "dd/MM/yyyy - HH:mm") + " WIB";
    
    var pesanWa = "📊 *[LAPORAN GRAFIK REALISASI TIAP JAM]*\n" +
                  "📅 Tanggal: *" + tanggal + "*\n" +
                  "🕒 Waktu Cetak: *" + waktuCetak + "*\n\n" +
                  "-------------------------------------------\n" +
                  "*Grafik Realisasi Tiap Jam (Semua Region)*\n" +
                  "Berikut adalah link grafik realisasi masing-masing region:\n\n";
                  
    var REGIONS_ORDER = [
        "Aceh", "Sumatera Utara 1", "Sumatera Utara 2 Ex Torganda", 
        "Riau 1", "Riau 2", "Riau 3", "Riau 4", 
        "Bangka Belitung", "Jambi", "Sumatera Barat", "Sumatera Selatan", 
        "Kalimantan Barat 1", "Kalimantan Barat 2", 
        "Kalimantan Selatan 1", "Kalimantan Selatan 2", 
        "Kalimantan Timur", "Kalimantan Utara", 
        "Kalimantan Tengah 1", "Kalimantan Tengah 2", "Kalimantan Tengah 3", 
        "Sulawesi Tenggara", "Sulawesi Tengah"
    ];
    
    for (var i = 0; i < REGIONS_ORDER.length; i++) {
      var r = REGIONS_ORDER[i];
      if (links[r]) {
        pesanWa += "📌 *" + r + "*: " + links[r] + "\n";
      }
    }
    
    pesanWa += "\n🔗 *Link Detail Semua Region*: " + fileTersimpan.getUrl();
    
    var tokenWa = "NgcPkuu5vmUmHYRpRLGw";
    var nomorTujuan = "120363410041245092@g.us";
    
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
    
    var waResponse = UrlFetchApp.fetch("https://api.fonnte.com/send", waOptions);
    
    return {
      success: true,
      message: "Laporan ringkasan berhasil dikirim ke WhatsApp.",
      driveUrl: fileTersimpan.getUrl(),
      waResponse: waResponse.getContentText()
    };
  } catch (err) {
    return { success: false, message: "Gagal memproses ringkasan pelaporan: " + err.toString() };
  }
}

function handleSendActiveDashboardScreenshot(params) {
  if (!params) {
    return { success: false, message: "Parameter tidak boleh kosong." };
  }
  var base64Data = params.base64Data;
  var tanggal = params.tanggal || "TODAY";
  
  if (!base64Data) {
    return { success: false, message: "Data gambar kosong." };
  }
  
  try {
    var base64Image = base64Data.split(",")[1];
    var decodedBlob = Utilities.newBlob(Utilities.base64Decode(base64Image), "image/jpeg");
    
    var now = new Date();
    var namaFile = "Grafik_SemuaRegion_Active_" + tanggal.replace(/[\/\s]/g, '-') + "_" + Utilities.formatDate(now, "GMT+7", "HH-mm") + ".jpg";
    decodedBlob.setName(namaFile);
    
    var folderId = "1HaZkgflPW6IkLXaBUMl8nJCGWIMCyOxM";
    var folder = DriveApp.getFolderById(folderId);
    var fileTersimpan = folder.createFile(decodedBlob);
    fileTersimpan.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
    
    var waktuCetak = Utilities.formatDate(now, "GMT+7", "dd/MM/yyyy - HH:mm") + " WIB";
    
    var pesanWa = "📊 *[LAPORAN GRAFIK REALISASI TIAP JAM]*\n" +
                  "📅 Tanggal: *" + tanggal + "*\n" +
                  "🕒 Waktu Cetak: *" + waktuCetak + "*\n" +
                  "📌 Status: *Semua Region (Kumulatif)*\n\n" +
                  "🔗 *Link Detail Semua Region*: " + fileTersimpan.getUrl();
    
    var tokenWa = "NgcPkuu5vmUmHYRpRLGw";
    var nomorTujuan = "120363410041245092@g.us";
    
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
    
    var waResponse = UrlFetchApp.fetch("https://api.fonnte.com/send", waOptions);
    
    return {
      success: true,
      message: "Screenshot aktif berhasil dikirim ke WhatsApp.",
      driveUrl: fileTersimpan.getUrl(),
      waResponse: waResponse.getContentText()
    };
  } catch (err) {
    return { success: false, message: "Gagal mengirim screenshot aktif: " + err.toString() };
  }
}

// =========================================================================
// FUNGSI UJI COBA - Jalankan ini dari editor untuk memaksa otorisasi Drive
// =========================================================================
function testDriveAccess() {
  var folder = DriveApp.getFolderById("1HaZkgflPW6IkLXaBUMl8nJCGWIMCyOxM");
  Logger.log("Berhasil mengakses folder: " + folder.getName());
  Logger.log("URL folder: " + folder.getUrl());
  
  // Test UrlFetchApp juga
  Logger.log("UrlFetchApp tersedia.");
  
  // Test SpreadsheetApp
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  Logger.log("Spreadsheet: " + ss.getName());
  
  Logger.log("=== SEMUA IZIN BERHASIL DIVERIFIKASI ===");
}
