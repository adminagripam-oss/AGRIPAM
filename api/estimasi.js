const { supabase } = require('./lib/supabase');
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

    let query = supabase.from('data_estimasi').select('*').eq('tanggal', tanggal);
    if (region && region.toUpperCase() !== 'ALL') query = query.eq('region', region);

    const { data, error } = await query;
    if (error) return res.json({ success: false, message: 'Gagal mengambil data estimasi: ' + error.message });

    if (!region || region.toUpperCase() === 'ALL') {
      const allEstimasi = {};
      let totalRestanLalu = 0, totalLuasPanen = 0, totalTkPanen = 0, totalEstimasiPanen = 0, totalEstimasiKirim = 0, totalEstimasiRestan = 0;

      (data || []).forEach(r => {
        const restanLalu = parseFloat(r.restan_lalu) || 0;
        const luasPanen = parseFloat(r.luas_panen_ha) || 0;
        const tkPanen = parseFloat(r.tk_panen_hk) || 0;
        const estimasiPanen = parseFloat(r.estimasi_panen_kg) || 0;
        const estimasiKirim = parseFloat(r.estimasi_kirim_kg) || 0;
        const estimasiRestan = parseFloat(r.estimasi_restan_kg) || 0;

        totalRestanLalu += restanLalu; totalLuasPanen += luasPanen; totalTkPanen += tkPanen;
        totalEstimasiPanen += estimasiPanen; totalEstimasiKirim += estimasiKirim; totalEstimasiRestan += estimasiRestan;

        allEstimasi[r.region] = {
          restanLalu, luasPanen, tkPanen, estPanen: estimasiPanen,
          outPanen: parseFloat(r.output_panen) || 0, estKirim: estimasiKirim, estRestan: estimasiRestan
        };
      });

      const avgOutputPanen = totalTkPanen > 0 ? Math.round(totalEstimasiPanen / totalTkPanen) : 0;
      return res.json({
        success: true, exists: Object.keys(allEstimasi).length > 0, allEstimasi,
        data: { restanLalu: totalRestanLalu, luasPanen: totalLuasPanen, tkPanen: totalTkPanen, estPanen: totalEstimasiPanen, outPanen: avgOutputPanen, estKirim: totalEstimasiKirim, estRestan: totalEstimasiRestan }
      });
    }

    if (!data || data.length === 0) return res.json({ success: true, exists: false, data: null });

    const r = data[0];
    return res.json({
      success: true, exists: true,
      data: { restanLalu: r.restan_lalu, luasPanen: r.luas_panen_ha, tkPanen: r.tk_panen_hk, estPanen: r.estimasi_panen_kg, outPanen: r.output_panen, estKirim: r.estimasi_kirim_kg, estRestan: r.estimasi_restan_kg }
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
