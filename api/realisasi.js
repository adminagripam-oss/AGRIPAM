const { supabase } = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

const MIN_TONASE = 0;
const MAX_TONASE = 5000;

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region = (p.region || '').trim();

  if (action === 'getData' || action === 'getRunningTextData') {
    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });
    
    let query = supabase.from('database_input').select('region, jam, tonase').eq('tanggal', tanggal).order('jam', { ascending: true });
    if (region && region.toUpperCase() !== 'ALL') query = query.eq('region', region);
    
    const { data, error } = await query;
    if (error) return res.json({ success: false, message: 'Gagal mengambil data: ' + error.message });

    if (!region || region.toUpperCase() === 'ALL') {
      const allRecords = (data || []).map(r => ({ region: r.region, jam: r.jam, tonase: parseFloat(r.tonase) || 0 }));
      return res.json({ success: true, allRecords });
    }

    let total = 0;
    const jamData = {};
    (data || []).forEach(r => {
      const t = parseFloat(r.tonase) || 0;
      total += t;
      jamData[r.jam] = t;
    });

    return res.json({ success: true, total: Math.round(total * 100) / 100, jamData });
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
      let total = 0; const jamData = {};
      (allRows || []).forEach(r => { const t = parseFloat(r.tonase) || 0; total += t; jamData[r.jam] = t; });
      return res.json({ success: false, message: `Data jam ${jam} sudah ada. Gunakan 'Hapus Jam Ini' untuk merevisi.`, total: Math.round(total * 100) / 100, jamData });
    }

    const { error } = await supabase.from('database_input').insert({ tanggal, region, jam, tonase: tonaseNum });
    if (error) return res.json({ success: false, message: 'Gagal menyimpan data: ' + error.message });

    const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
    let newTotal = 0; const jamData = {};
    (allRows || []).forEach(r => { const t = parseFloat(r.tonase) || 0; newTotal += t; jamData[r.jam] = t; });

    return res.json({ success: true, message: 'Data berhasil disimpan.', total: Math.round(newTotal * 100) / 100, jamData });
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
      let total = 0; const jamData = {};
      (allRows || []).forEach(r => { const t = parseFloat(r.tonase) || 0; total += t; jamData[r.jam] = t; });
      return res.json({ success: false, message: `Data jam ${jam} tidak ditemukan.`, total: Math.round(total * 100) / 100, jamData });
    }

    const { data: allRows } = await supabase.from('database_input').select('jam, tonase').eq('tanggal', tanggal).eq('region', region);
    let total = 0; const jamData = {};
    (allRows || []).forEach(r => { const t = parseFloat(r.tonase) || 0; total += t; jamData[r.jam] = t; });

    return res.json({ success: true, message: `Data jam ${jam} berhasil dihapus.`, total: Math.round(total * 100) / 100, jamData });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
