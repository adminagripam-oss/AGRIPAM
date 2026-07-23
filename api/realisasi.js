const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

const MIN_TONASE = 0;
const MAX_TONASE = 5000;

const WITA_REGIONS = [
  'Kalimantan Selatan 1', 'Kalimantan Selatan 2', 
  'Kalimantan Timur', 'Kalimantan Utara', 
  'Sulawesi Tenggara', 'Sulawesi Tengah'
];

function formatTimeWindow(jamStr) {
  const [h, m] = jamStr.split('.').map(Number);
  const totalMins = h * 60 + m;
  const minStart = totalMins - 90;
  const minEnd = totalMins + 90;
  
  const toStr = (mins) => {
    let hh = Math.floor(mins / 60);
    let mm = mins % 60;
    if (hh < 0) hh += 24;
    if (hh >= 24) hh -= 24;
    return String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
  };
  return `${toStr(minStart)} - ${toStr(minEnd)}`;
}

/**
 * Kembalikan prefix bulan berjalan dalam zona WIB (UTC+7).
 * Contoh: '2026-07'
 */
function getCurrentMonthWIB() {
  const now = new Date(Date.now() + 7 * 60 * 60 * 1000); // offset ke WIB
  const yyyy = now.getUTCFullYear();
  const mm   = String(now.getUTCMonth() + 1).padStart(2, '0');
  return `${yyyy}-${mm}`;
}

function computeJamDataAndTotal(rows) {
  const jamData = {};
  (rows || []).forEach(r => {
    if (!jamData[r.jam]) jamData[r.jam] = 0;
    jamData[r.jam] += parseFloat(r.tonase) || 0;
  });
  // Round each hour sum to 2 decimal places
  Object.keys(jamData).forEach(k => {
    jamData[k] = Math.round(jamData[k] * 100) / 100;
  });
  const total = Object.values(jamData).reduce((sum, t) => sum + t, 0);
  return { jamData, total: Math.round(total * 100) / 100 };
}

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region = (p.region || '').trim();

  if (action === 'getData' || action === 'getRunningTextData') {
    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });
    const tanggal_akhir = (p.tanggal_akhir || '').trim();
    
    // Single query with high limit to avoid Vercel 10s timeout from while(true) loop
    let query = supabase
      .from('database_input')
      .select('tanggal, region, jam, tonase')
      .order('jam', { ascending: true })
      .limit(5000);

    if (tanggal_akhir) {
      query = query.gte('tanggal', tanggal).lte('tanggal', tanggal_akhir);
    } else {
      query = query.eq('tanggal', tanggal);
    }
    if (region && region.toUpperCase() !== 'ALL') query = query.eq('region', region);

    const { data: allData, error } = await query;
    if (error) return res.json({ success: false, message: 'Gagal mengambil data: ' + error.message });

    const { jamData, total } = computeJamDataAndTotal(allData);
    const allRecords = allData.map(r => ({ tanggal: r.tanggal, region: r.region, jam: r.jam, tonase: parseFloat(r.tonase) || 0 }));
    
    return res.json({ success: true, total, jamData, allRecords });
  }

  if (action === 'insert') {
    const jam = (p.jam || '').trim();
    const tonase = p.tonase;

    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (!tanggal || !region || !jam || tonase === undefined || tonase === '') {
      return res.json({ success: false, message: 'Data tidak lengkap.' });
    }

    // ✅ Validasi bulan berjalan (WIB)
    const currentMonth = getCurrentMonthWIB(); // e.g. '2026-07'
    const inputMonth   = tanggal.substring(0, 7); // e.g. '2026-07'
    if (inputMonth !== currentMonth) {
      const [cy, cm] = currentMonth.split('-');
      const monthNames = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
      const bulanIni = `${monthNames[parseInt(cm, 10) - 1]} ${cy}`;
      return res.json({
        success: false,
        message: `❌ Input ditolak! Tanggal yang Anda masukkan (${tanggal}) berada di luar bulan berjalan. Hanya data bulan ${bulanIni} yang diizinkan.`
      });
    }

    // ✅ Validasi Batas Waktu Input Per-Jam berdasarkan Zona Waktu
    const isWita = WITA_REGIONS.includes(region);
    const offsetHours = isWita ? 8 : 7;
    const offsetMs = offsetHours * 60 * 60 * 1000;
    
    // Parse tanggal and jam
    const [yyyy, mm, dd] = tanggal.split('-').map(Number);
    const [hh, min] = jam.split('.').map(Number);
    
    // Target time in true UTC timestamp
    const targetUtcTimestamp = Date.UTC(yyyy, mm - 1, dd, hh, min, 0);
    const targetRealUnixTimestamp = targetUtcTimestamp - offsetMs;
    
    if (targetRealUnixTimestamp > Date.now()) {
      const localNow = new Date(Date.now() + offsetMs);
      const localNowStr = localNow.getUTCHours().toString().padStart(2, '0') + ':' + localNow.getUTCMinutes().toString().padStart(2, '0');
      const tzName = isWita ? 'WITA' : 'WIB';
      
      return res.json({
        success: false,
        message: `❌ Gagal: Jam ${jam} belum bisa diisi karena waktunya belum tiba. Waktu server Anda saat ini adalah ${localNowStr} ${tzName}.`
      });
    }

    const tonaseNum = parseFloat(tonase);
    if (isNaN(tonaseNum)) return res.json({ success: false, message: 'Nilai tonase tidak valid.' });
    if (tonaseNum < MIN_TONASE || tonaseNum > MAX_TONASE) return res.json({ success: false, message: `Tonase harus antara ${MIN_TONASE} dan ${MAX_TONASE}.` });

    const { data: existing } = await supabase.from('database_input').select('id, tonase').eq('tanggal', tanggal).eq('region', region).eq('jam', jam).maybeSingle();

    if (existing) {
      const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
      const { jamData, total } = computeJamDataAndTotal(allRows);
      return res.json({ success: false, message: `Data jam ${jam} sudah ada. Gunakan 'Hapus Jam Ini' untuk merevisi.`, total, jamData });
    }

    const { error } = await supabase.from('database_input').insert({ tanggal, region, jam, tonase: tonaseNum });
    if (error) return res.json({ success: false, message: 'Gagal menyimpan data: ' + error.message });

    const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
    const { jamData, total } = computeJamDataAndTotal(allRows);

    return res.json({ success: true, message: 'Data berhasil disimpan.', total, jamData });
  }

  if (action === 'delete') {
    const jam = (p.jam || '').trim();
    
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    if (!tanggal || !region || !jam) return res.json({ success: false, message: 'Tanggal, Region, dan Jam wajib diisi.' });

    const { data: deleted, error } = await supabase.from('database_input').delete().eq('tanggal', tanggal).eq('region', region).eq('jam', jam).select('id');
    if (error) return res.json({ success: false, message: 'Gagal menghapus data: ' + error.message });

    const deletedCount = (deleted || []).length;
    if (deletedCount === 0) {
      const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
      const { jamData, total } = computeJamDataAndTotal(allRows);
      return res.json({ success: false, message: `Data jam ${jam} tidak ditemukan.`, total, jamData });
    }

    const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
    const { jamData, total } = computeJamDataAndTotal(allRows);

    return res.json({ success: true, message: `Data jam ${jam} berhasil dihapus.`, total, jamData });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
