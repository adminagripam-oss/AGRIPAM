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
  const nomor_surat = p.nomor_surat;
  const jenis_surat = p.jenis_surat;
  const perihal = p.perihal;
  const file_url = p.file_url;

  if (!region || !token) {
    return res.json({ success: false, message: 'Autentikasi gagal.' });
  }
  
  if (region === 'ADMIN') {
    return res.json({ success: false, message: 'Admin tidak dapat membuat surat.' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  const { error } = await supabase.from('surat').insert({
    nomor_surat,
    jenis_surat,
    perihal,
    file_url,
    regional_pengirim: region,
    status: 'menunggu'
  });

  if (error) {
    return res.json({ success: false, message: error.message });
  }

  return res.json({ success: true, message: 'Surat berhasil disimpan.' });
};
