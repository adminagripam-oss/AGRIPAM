realisasi_code = """const { supabase } = require('./lib/supabase');
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
"""

estimasi_code = """const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region = (p.region || '').trim();

  if (action === 'getEstimasi') {
    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });

    const tanggal_akhir = (p.tanggal_akhir || '').trim();

    let allData = [];
    let page = 0;
    const pageSize = 1000;

    while (true) {
      let query = supabase.from('data_estimasi').select('*').gte('tanggal', tanggal);
      if (tanggal_akhir) {
        query = query.lte('tanggal', tanggal_akhir);
      } else {
        query = query.lte('tanggal', tanggal);
      }
      if (region && region.toUpperCase() !== 'ALL') query = query.eq('region', region);
      
      query = query.range(page * pageSize, (page + 1) * pageSize - 1);

      const { data, error } = await query;
      if (error) return res.json({ success: false, message: 'Gagal mengambil data estimasi: ' + error.message });
      if (!data || data.length === 0) break;

      allData = allData.concat(data);
      if (data.length < pageSize) break;
      page++;
    }

    const allEstimasi = {};
    let totalRestanLalu = 0, totalLuasPanen = 0, totalTkPanen = 0, totalEstimasiPanen = 0, totalEstimasiKirim = 0, totalEstimasiRestan = 0;

    (allData || []).forEach(r => {
      const restanLalu = parseFloat(r.restan_lalu) || 0;
      const luasPanen = parseFloat(r.luas_panen_ha) || 0;
      const tkPanen = parseFloat(r.tk_panen_hk) || 0;
      const estimasiPanen = parseFloat(r.estimasi_panen_kg) || 0;
      const estimasiKirim = parseFloat(r.estimasi_kirim_kg) || 0;
      const estimasiRestan = parseFloat(r.estimasi_restan_kg) || 0;

      totalRestanLalu += restanLalu; totalLuasPanen += luasPanen; totalTkPanen += tkPanen;
      totalEstimasiPanen += estimasiPanen; totalEstimasiKirim += estimasiKirim; totalEstimasiRestan += estimasiRestan;

      if (!allEstimasi[r.region]) {
        allEstimasi[r.region] = { restanLalu: 0, luasPanen: 0, tkPanen: 0, estPanen: 0, outPanen: 0, estKirim: 0, estRestan: 0 };
      }
      allEstimasi[r.region].restanLalu += restanLalu;
      allEstimasi[r.region].luasPanen += luasPanen;
      allEstimasi[r.region].tkPanen += tkPanen;
      allEstimasi[r.region].estPanen += estimasiPanen;
      allEstimasi[r.region].estKirim += estimasiKirim;
      allEstimasi[r.region].estRestan += estimasiRestan;
    });

    Object.keys(allEstimasi).forEach(reg => {
      const d = allEstimasi[reg];
      d.outPanen = d.tkPanen > 0 ? Math.round(d.estPanen / d.tkPanen) : 0;
    });

    const avgOutputPanen = totalTkPanen > 0 ? Math.round(totalEstimasiPanen / totalTkPanen) : 0;

    return res.json({
      success: true,
      exists: allData.length > 0,
      allEstimasi,
      data: { restanLalu: totalRestanLalu, luasPanen: totalLuasPanen, tkPanen: totalTkPanen, estPanen: totalEstimasiPanen, outPanen: avgOutputPanen, estKirim: totalEstimasiKirim, estRestan: totalEstimasiRestan },
      allRecords: allData
    });
  }

  if (action === 'insertEstimasi') {
    const check = await verifyToken(token, null);
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (check.region !== 'ADMIN' && check.region !== region) {
      return res.json({ success: false, message: 'Anda tidak memiliki akses ke region ini.' });
    }

    const restanLalu = parseFloat(p.estimasiRestanLalu);
    const luasPanen = parseFloat(p.luasPanen);
    const tkPanen = parseFloat(p.tkPanen);
    const estPanen = parseFloat(p.estimasiPanen);
    const outPanen = parseFloat(p.outputPanen) || 0;
    const estKirim = parseFloat(p.estimasiKirim);
    const estRestan = parseFloat(p.estimasiRestan);

    if (!tanggal || !region || isNaN(restanLalu) || isNaN(luasPanen) || isNaN(tkPanen) || isNaN(estPanen) || isNaN(estKirim) || isNaN(estRestan)) {
      return res.json({ success: false, message: 'Data estimasi tidak lengkap atau tidak valid.' });
    }

    const { data: existing } = await supabase.from('data_estimasi').select('id').eq('tanggal', tanggal).eq('region', region).maybeSingle();

    if (existing) {
      const parts = tanggal.split('-');
      const displayDate = parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : tanggal;
      return res.json({ success: false, message: `Data estimasi tanggal ${displayDate} sudah ada. Gunakan 'Hapus Estimasi' untuk merevisi.` });
    }

    const { error } = await supabase.from('data_estimasi').insert({
      tanggal, region, restan_lalu: restanLalu, luas_panen_ha: luasPanen, tk_panen_hk: tkPanen,
      estimasi_panen_kg: estPanen, output_panen: outPanen, estimasi_kirim_kg: estKirim, estimasi_restan_kg: estRestan
    });

    if (error) {
      if (error.code === '23505') return res.json({ success: false, message: 'Data estimasi untuk tanggal dan region ini sudah ada.' });
      return res.json({ success: false, message: 'Gagal menyimpan estimasi: ' + error.message });
    }

    return res.json({ success: true, message: 'Data estimasi berhasil disimpan!' });
  }

  if (action === 'deleteEstimasi') {
    const check = await verifyToken(token, null);
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (check.region !== 'ADMIN' && check.region !== region) {
      return res.json({ success: false, message: 'Anda tidak memiliki akses ke region ini.' });
    }

    if (!tanggal || !region) return res.json({ success: false, message: 'Tanggal dan Region wajib diisi.' });

    const { data: deleted, error } = await supabase.from('data_estimasi').delete().eq('tanggal', tanggal).eq('region', region).select('id');
    if (error) return res.json({ success: false, message: 'Gagal menghapus estimasi: ' + error.message });

    const deletedCount = (deleted || []).length;
    if (deletedCount === 0) {
      const parts = tanggal.split('-');
      const displayDate = parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : tanggal;
      return res.json({ success: false, message: `Data estimasi untuk tanggal ${displayDate} dan Region ${region} tidak ditemukan.` });
    }

    return res.json({ success: true, message: `Berhasil menghapus ${deletedCount} data estimasi.` });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
"""

with open('api/realisasi.js', 'w', encoding='utf-8') as f:
    f.write(realisasi_code)
print("Rewrote api/realisasi.js with unified return format.")

with open('api/estimasi.js', 'w', encoding='utf-8') as f:
    f.write(estimasi_code)
print("Rewrote api/estimasi.js with unified return format.")
