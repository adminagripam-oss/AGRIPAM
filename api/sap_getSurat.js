const { supabase } = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const region = (p.region || '').trim();
  const token = (p.token || '').trim();

  if (!region || !token) {
    return res.json({ success: false, message: 'Autentikasi gagal.' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  let query = supabase.from('surat').select('*').order('created_at', { ascending: false });

  // Jika bukan ADMIN, hanya boleh melihat surat milik region tersebut
  if (region !== 'ADMIN') {
    query = query.eq('regional_pengirim', region);
  }

  const { data, error } = await query;

  if (error) {
    return res.json({ success: false, message: error.message });
  }

  return res.json({ success: true, data: data });
};
