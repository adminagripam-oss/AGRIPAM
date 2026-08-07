const fs = require('fs');
const path = require('path');
const { applyCors } = require('./lib/cors');
const { verifyToken } = require('./lib/auth');
const { supabase } = require('./lib/supabase');

const jsonPath = path.join(__dirname, '..', 'data_kebun_tk.json');

// Comprehensive region normalizer mapping all 23 regional login names to dataset regions
function normalizeRegion(rStr) {
  if (!rStr) return '';
  let s = String(rStr).trim().toUpperCase();
  s = s.replace(/^REGIONAL\s+/, '');
  s = s.replace(/^RO\s+/, '');
  
  if (s.includes('SUMUT 1') || s.includes('SUMATERA UTARA 1')) return 'SUMUT 1';
  if (s.includes('SUMUT 2') || s.includes('SUMATERA UTARA 2') || s.includes('TORGANDA')) return 'SUMUT 2';
  if (s.includes('KALBAR 1') || s.includes('KALIMANTAN BARAT 1')) return 'KALBAR 1';
  if (s.includes('KALBAR 2') || s.includes('KALIMANTAN BARAT 2')) return 'KALBAR 2';
  if (s.includes('KALSEL 1') || s.includes('KALIMANTAN SELATAN 1')) return 'KALSEL 1';
  if (s.includes('KALSEL 2') || s.includes('KALIMANTAN SELATAN 2')) return 'KALSEL 2';
  if (s.includes('KALTARA') || s.includes('KALIMANTAN UTARA')) return 'KALTARA';
  if (s.includes('KALTIM') || s.includes('KALIMANTAN TIMUR')) return 'KALTIM';
  if (s.includes('KALTENG 1') || s.includes('KALIMANTAN TENGAH 1')) return 'KALTENG 1';
  if (s.includes('KALTENG 2') || s.includes('KALIMANTAN TENGAH 2')) return 'KALTENG 2';
  if (s.includes('KALTENG 3') || s.includes('KALIMANTAN TENGAH 3')) return 'KALTENG 3';
  if (s.includes('BABEL') || s.includes('BANGKA BELITUNG')) return 'BABEL';
  if (s.includes('SUMBAR') || s.includes('SUMATERA BARAT')) return 'SUMBAR';
  if (s.includes('SUMSEL') || s.includes('SUMATERA SELATAN')) return 'SUMSEL';
  if (s.includes('SULTENG') || s.includes('SULAWESI TENGAH')) return 'SULTENG';
  if (s.includes('SULTRA') || s.includes('SULAWESI TENGGARA')) return 'SULTRA';
  if (s.includes('PAPUA')) return 'PAPUA SELATAN';
  if (s.includes('ACEH')) return 'ACEH';
  if (s.includes('JAMBI')) return 'JAMBI';
  if (s.includes('RIAU 1')) return 'RIAU 1';
  if (s.includes('RIAU 2')) return 'RIAU 2';
  if (s.includes('RIAU 3')) return 'RIAU 3';
  if (s.includes('RIAU 4')) return 'RIAU 4';
  return s;
}

function loadKebunData() {
  try {
    if (fs.existsSync(jsonPath)) {
      const data = fs.readFileSync(jsonPath, 'utf8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('Error reading data_kebun_tk.json:', err);
  }
  return [];
}

function saveKebunData(list) {
  try {
    fs.writeFileSync(jsonPath, JSON.stringify(list, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Error saving data_kebun_tk.json:', err);
    return false;
  }
}

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const regionParam = (p.region || '').trim();
  const token = (p.token || '').trim();

  let kebunList = loadKebunData();

  // Try fetching from Supabase if configured & available
  try {
    const { data: supaData, error } = await supabase.from('data_kebun_tk').select('*');
    if (!error && supaData && supaData.length > 0) {
      kebunList = supaData;
    }
  } catch (_) {}

  // -------------------------------------------------------------------------
  // GET KEBUN DATA
  // -------------------------------------------------------------------------
  if (action === 'getKebun') {
    const filterRegion = (p.filterRegion || regionParam || '').trim();
    const isMasterAdmin = filterRegion.toUpperCase() === 'ADMIN' || !filterRegion || filterRegion.toUpperCase() === 'ALL';

    let result = kebunList;
    if (!isMasterAdmin) {
      const normRequested = normalizeRegion(filterRegion);
      result = kebunList.filter(item => {
        const normItem = normalizeRegion(item.region);
        return normItem === normRequested || (normRequested.length >= 3 && normItem.includes(normRequested)) || (normItem.length >= 3 && normRequested.includes(normItem));
      });
    }

    result.sort((a, b) => {
      const croA = (a.cro || '').toString().toUpperCase();
      const croB = (b.cro || '').toString().toUpperCase();
      if (croA < croB) return -1;
      if (croA > croB) return 1;
      const regA = (a.region || '').toString().toUpperCase();
      const regB = (b.region || '').toString().toUpperCase();
      if (regA < regB) return -1;
      if (regA > regB) return 1;
      const namaA = (a.nama_kebun || '').toString().toUpperCase();
      const namaB = (b.nama_kebun || '').toString().toUpperCase();
      if (namaA < namaB) return -1;
      if (namaA > namaB) return 1;
      return 0;
    });

    // Calculate dynamic month (H-1)
    const monthNames = ['januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember'];
    const today = new Date();
    // Default to July (index 6) if the app was meant for July/August, but let's make it truly dynamic
    let targetMonthIdx = today.getMonth() - 1;
    if (targetMonthIdx < 0) targetMonthIdx = 11;
    const targetMonthStr = monthNames[targetMonthIdx];
    const tkField = 'tk_' + targetMonthStr;
    const cutOffLabel = targetMonthStr.charAt(0).toUpperCase() + targetMonthStr.slice(1);

    // Calculate summary statistics
    const totalLuas = result.reduce((sum, item) => sum + (parseFloat(item.luasan) || 0), 0);
    const totalReqTk = result.reduce((sum, item) => sum + (parseFloat(item.req_tk) || 0), 0);
    const totalCutOff = result.reduce((sum, item) => sum + (parseFloat(item[tkField]) || 0), 0);
    const kekurangTK = totalReqTk - totalCutOff;

    return res.json({
      success: true,
      totalEntries: result.length,
      data: result,
      summary: {
        totalLuas: Math.round(totalLuas * 100) / 100,
        totalReqTk: Math.round(totalReqTk),
        totalCutOff: Math.round(totalCutOff),
        kekurangTK: Math.round(kekurangTK),
        cutOffMonth: cutOffLabel,
        cutOffField: tkField
      }
    });
  }

  // -------------------------------------------------------------------------
  // UPDATE TK PANEN (Kolom I & J)
  // -------------------------------------------------------------------------
  if (action === 'updateTK') {
    if (!regionParam) {
      return res.json({ success: false, message: 'Region wajib disertakan.' });
    }

    const edits = Array.isArray(p.edits) ? p.edits : (p.id ? [p] : []);
    if (edits.length === 0) {
      return res.json({ success: false, message: 'Tidak ada data perubahan yang dikirim.' });
    }

    const isAdmin = regionParam.toUpperCase() === 'ADMIN';
    const userNormRegion = normalizeRegion(regionParam);
    let updatedCount = 0;
    const nowIso = new Date().toISOString();

    for (const edit of edits) {
      const targetId = parseInt(edit.id, 10);
      const itemIndex = kebunList.findIndex(k => k.id === targetId);

      if (itemIndex !== -1) {
        const item = kebunList[itemIndex];
        const itemNormRegion = normalizeRegion(item.region);

        if (isAdmin || userNormRegion === itemNormRegion || userNormRegion.includes(itemNormRegion) || itemNormRegion.includes(userNormRegion)) {
          if (edit.tk_juni !== undefined && edit.tk_juni !== null) {
            item.tk_juni = Math.max(0, parseFloat(edit.tk_juni) || 0);
          }
          if (edit.target_juli !== undefined && edit.target_juli !== null) {
            item.target_juli = Math.max(0, parseFloat(edit.target_juli) || 0);
          }
          if (edit.target_agustus !== undefined && edit.target_agustus !== null) {
            item.target_agustus = Math.max(0, parseFloat(edit.target_agustus) || 0);
          }
          if (edit.tk_juli !== undefined && edit.tk_juli !== null) {
            item.tk_juli = Math.max(0, parseFloat(edit.tk_juli) || 0);
          }
          if (edit.tk_agustus !== undefined && edit.tk_agustus !== null) {
            item.tk_agustus = Math.max(0, parseFloat(edit.tk_agustus) || 0);
          }
          item.updated_by = regionParam;
          item.updated_at = nowIso;
          updatedCount++;

          // Attempt Supabase update
          try {
            await supabase.from('data_kebun_tk').update({
              tk_juni: item.tk_juni,
              target_juli: item.target_juli,
              target_agustus: item.target_agustus,
              tk_juli: item.tk_juli,
              tk_agustus: item.tk_agustus,
              updated_by: regionParam,
              updated_at: nowIso
            }).eq('id', targetId);
          } catch (_) {}
        }
      }
    }

    if (updatedCount > 0) {
      saveKebunData(kebunList);
      return res.json({
        success: true,
        message: `Berhasil memperbarui data TK Panen untuk ${updatedCount} kebun.`,
        updatedCount
      });
    } else {
      return res.json({
        success: false,
        message: 'Gagal memperbarui data. Anda hanya diizinkan mengedit kebun pada wilayah regional Anda.'
      });
    }
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
