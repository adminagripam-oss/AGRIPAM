const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

const MIN_TONASE = 0;
const MAX_TONASE = 5000;

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
    
    let allData = [];
    let page = 0;
    const pageSize = 1000;
    
    while (true) {
      let query = supabase.from('database_input').select('tanggal, region, jam, tonase').order('jam', { ascending: true });
      if (tanggal_akhir) {
        query = query.gte('tanggal', tanggal).lte('tanggal', tanggal_akhir);
      } else {
        query = query.eq('tanggal', tanggal);
      }
      if (region && region.toUpperCase() !== 'ALL') query = query.eq('region', region);
      
      query = query.range(page * pageSize, (page + 1) * pageSize - 1);
      
      const { data, error } = await query;
      if (error) return res.json({ success: false, message: 'Gagal mengambil data: ' + error.message });
      if (!data || data.length === 0) break;
      
      allData = allData.concat(data);
      if (data.length < pageSize) break;
      page++;
    }

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
