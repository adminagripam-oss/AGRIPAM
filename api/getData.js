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

  // Query data berdasarkan tanggal
  let query = supabase
    .from('database_input')
    .select('region, jam, tonase')
    .eq('tanggal', tanggal)
    .order('jam', { ascending: true });

  if (region && region.toUpperCase() !== 'ALL') {
    query = query.eq('region', region);
  }

  const { data, error } = await query;

  if (error) {
    return res.json({ success: false, message: 'Gagal mengambil data: ' + error.message });
  }

  // Mode ALL: kembalikan semua record
  if (!region || region.toUpperCase() === 'ALL') {
    const allRecords = (data || []).map(r => ({
      region : r.region,
      jam    : r.jam,
      tonase : parseFloat(r.tonase) || 0
    }));
    return res.json({ success: true, allRecords });
  }

  // Mode region tertentu: kembalikan total + jamData
  let total   = 0;
  const jamData = {};
  (data || []).forEach(r => {
    const t = parseFloat(r.tonase) || 0;
    total  += t;
    jamData[r.jam] = t;
  });

  return res.json({
    success : true,
    total   : Math.round(total * 100) / 100,
    jamData
  });
};
