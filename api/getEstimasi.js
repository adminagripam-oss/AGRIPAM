const { supabase } = require('./_lib/supabase');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p       = req.method === 'POST' ? req.body : req.query;
  const tanggal = (p.tanggal || '').trim();
  const region  = (p.region  || '').trim();

  if (!tanggal) {
    return res.json({ success: false, message: 'Tanggal wajib diisi.' });
  }

  let query = supabase
    .from('data_estimasi')
    .select('region, restan_lalu, luas_panen_ha, tk_panen_hk, estimasi_panen_kg, output_panen, estimasi_kirim_kg, estimasi_restan_kg')
    .eq('tanggal', tanggal);

  if (region && region.toUpperCase() !== 'ALL') {
    query = query.eq('region', region);
  }

  const { data, error } = await query;

  if (error) {
    return res.json({ success: false, message: 'Gagal mengambil data estimasi: ' + error.message });
  }

  // Mode ALL: kembalikan semua estimasi diindeks per region dan juga data akumulasinya
  if (!region || region.toUpperCase() === 'ALL') {
    const allEstimasi = {};
    let totalRestanLalu = 0;
    let totalLuasPanen = 0;
    let totalTkPanen = 0;
    let totalEstimasiPanen = 0;
    let totalEstimasiKirim = 0;
    let totalEstimasiRestan = 0;

    (data || []).forEach(r => {
      const restanLalu = parseFloat(r.restan_lalu) || 0;
      const luasPanen = parseFloat(r.luas_panen_ha) || 0;
      const tkPanen = parseFloat(r.tk_panen_hk) || 0;
      const estimasiPanen = parseFloat(r.estimasi_panen_kg) || 0;
      const estimasiKirim = parseFloat(r.estimasi_kirim_kg) || 0;
      const estimasiRestan = parseFloat(r.estimasi_restan_kg) || 0;

      totalRestanLalu += restanLalu;
      totalLuasPanen += luasPanen;
      totalTkPanen += tkPanen;
      totalEstimasiPanen += estimasiPanen;
      totalEstimasiKirim += estimasiKirim;
      totalEstimasiRestan += estimasiRestan;

      allEstimasi[r.region] = {
        restanLalu         : restanLalu,
        luasPanen          : luasPanen,
        tkPanen            : tkPanen,
        estPanen           : estimasiPanen,
        outPanen           : parseFloat(r.output_panen) || 0,
        estKirim           : estimasiKirim,
        estRestan          : estimasiRestan
      };
    });

    const avgOutputPanen = totalTkPanen > 0 ? Math.round(totalEstimasiPanen / totalTkPanen) : 0;

    return res.json({
      success      : true,
      exists       : Object.keys(allEstimasi).length > 0,
      allEstimasi,
      data: {
        restanLalu         : totalRestanLalu,
        luasPanen          : totalLuasPanen,
        tkPanen            : totalTkPanen,
        estPanen           : totalEstimasiPanen,
        outPanen           : avgOutputPanen,
        estKirim           : totalEstimasiKirim,
        estRestan          : totalEstimasiRestan
      }
    });
  }

  // Mode region tertentu
  if (!data || data.length === 0) {
    return res.json({ success: true, exists: false, data: null });
  }

  const r = data[0];
  return res.json({
    success : true,
    exists  : true,
    data    : {
      restanLalu         : r.restan_lalu,
      luasPanen          : r.luas_panen_ha,
      tkPanen            : r.tk_panen_hk,
      estPanen           : r.estimasi_panen_kg,
      outPanen           : r.output_panen,
      estKirim           : r.estimasi_kirim_kg,
      estRestan          : r.estimasi_restan_kg
    }
  });
};
