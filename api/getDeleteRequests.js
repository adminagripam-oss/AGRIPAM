const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p       = req.method === 'POST' ? req.body : req.query;
  const token   = (p.token   || '').trim();
  const region  = (p.region  || '').trim();

  // 1. Validasi token & pastikan hanya ADMIN
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }
  
  if (region !== 'ADMIN') {
    return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat mengakses data ini.' });
  }

  // 2. Ambil data delete_requests yang statusnya PENDING
  const { data, error } = await supabase
    .from('delete_requests')
    .select('*')
    .eq('status', 'PENDING')
    .order('requested_at', { ascending: false });

  if (error) {
    return res.json({ success: false, message: 'Gagal mengambil data permintaan: ' + error.message });
  }

  return res.json({
    success: true,
    data: data || []
  });
};
