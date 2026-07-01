const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p       = req.method === 'POST' ? req.body : req.query;
  const token   = (p.token   || '').trim();
  const type    = (p.type    || '').trim().toUpperCase(); // REALISASI or ESTIMASI
  const region  = (p.region  || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const jam     = (p.jam     || '').trim();

  // 1. Validasi token
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  if (!type || !tanggal || !region) {
    return res.json({ success: false, message: 'Data tidak lengkap (type/tanggal/region).' });
  }

  // 2. Cek apakah request PENDING sudah ada untuk data yang sama
  let query = supabase
    .from('delete_requests')
    .select('id')
    .eq('type', type)
    .eq('region', region)
    .eq('tanggal', tanggal)
    .eq('status', 'PENDING');
  
  if (type === 'REALISASI' && jam) {
    query = query.eq('jam', jam);
  }

  const { data: existing } = await query.maybeSingle();
  if (existing) {
    return res.json({ success: false, message: 'Permintaan hapus data untuk ini sudah diajukan dan sedang menunggu persetujuan Admin.' });
  }

  // 3. Insert permintaan
  const { error } = await supabase.from('delete_requests').insert({
    type,
    region,
    tanggal,
    jam: type === 'REALISASI' ? jam : null,
    status: 'PENDING'
  });

  if (error) {
    return res.json({ success: false, message: 'Gagal mengirim permintaan hapus: ' + error.message });
  }

  return res.json({
    success : true,
    message : 'Permintaan hapus data telah dikirim ke Admin untuk diverifikasi.'
  });
};
