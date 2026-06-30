const { supabase }                    = require('./_lib/supabase');
const { verifyToken, SESSION_TTL_MS } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p      = req.method === 'POST' ? req.body : req.query;
  const token  = (p.token  || '').trim();
  const region = (p.region || '').trim();

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  // Perpanjang expiry di tabel sesi_aktif
  const newExpiry = new Date(Date.now() + SESSION_TTL_MS);
  await supabase.from('sesi_aktif')
    .update({ expiry: newExpiry.toISOString() })
    .eq('token', token)
    .eq('status', 'Aktif');

  return res.json({
    success : true,
    message : 'Sesi diperpanjang.',
    ttlMs   : SESSION_TTL_MS
  });
};
