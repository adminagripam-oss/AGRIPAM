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
  const surat_id = p.surat_id;
  const status = p.status;
  const catatan = p.catatan;

  if (!region || !token) {
    return res.json({ success: false, message: 'Autentikasi gagal.' });
  }

  if (region !== 'ADMIN') {
    return res.json({ success: false, message: 'Hanya Admin yang dapat mengupdate status surat.' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  // Update surat status
  const { error: updateError } = await supabase
    .from('surat')
    .update({ status: status })
    .eq('id', surat_id);
    
  if (updateError) {
    return res.json({ success: false, message: updateError.message });
  }

  // Insert to log_tracking
  const { error: logError } = await supabase
    .from('log_tracking')
    .insert({
        surat_id: surat_id,
        status_update: status,
        catatan: catatan,
        created_by: 'ADMIN'
    });

  if (logError) {
    return res.json({ success: false, message: logError.message });
  }

  return res.json({ success: true, message: 'Status surat berhasil diupdate.' });
};
