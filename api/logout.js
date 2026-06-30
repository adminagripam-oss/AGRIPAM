const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p      = req.method === 'POST' ? req.body : req.query;
  const token  = (p.token  || '').trim();
  const region = (p.region || '').trim();

  if (!token || !region) {
    return res.json({ success: false, message: 'Token dan Region wajib diisi.' });
  }

  // Update status sesi → Logout (tanpa strict verify agar logout tetap berhasil)
  await supabase.from('sesi_aktif')
    .update({ status: 'Logout' })
    .eq('token', token)
    .eq('status', 'Aktif');

  await supabase.from('audit_log').insert({
    region, action: 'LOGOUT', detail: 'Logout normal.'
  });

  return res.json({ success: true, message: 'Logout berhasil.' });
};
