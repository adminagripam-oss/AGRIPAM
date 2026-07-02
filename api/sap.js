const { supabase } = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const region = (p.region || '').trim();
  const token = (p.token || '').trim();

  if (!region || !token) {
    return res.json({ success: false, message: 'Autentikasi gagal.' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  if (action === 'getSurat') {
    let query = supabase.from('surat').select('*').order('created_at', { ascending: false });
    if (region !== 'ADMIN') query = query.eq('regional_pengirim', region);

    const { data, error } = await query;
    if (error) return res.json({ success: false, message: error.message });

    return res.json({ success: true, data: data });
  }

  if (action === 'insertSurat') {
    if (region === 'ADMIN') return res.json({ success: false, message: 'Admin tidak dapat membuat surat.' });

    const nomor_surat = p.nomor_surat;
    const jenis_surat = p.jenis_surat;
    const perihal = p.perihal;
    const file_url = p.file_url;

    const { error } = await supabase.from('surat').insert({
      nomor_surat, jenis_surat, perihal, file_url, regional_pengirim: region, status: 'menunggu'
    });

    if (error) return res.json({ success: false, message: error.message });

    return res.json({ success: true, message: 'Surat berhasil disimpan.' });
  }

  if (action === 'updateSurat') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Hanya Admin yang dapat mengupdate status surat.' });

    const surat_id = p.surat_id;
    const status = p.status;
    const catatan = p.catatan;

    const { error: updateError } = await supabase.from('surat').update({ status: status }).eq('id', surat_id);
    if (updateError) return res.json({ success: false, message: updateError.message });

    const { error: logError } = await supabase.from('log_tracking').insert({
      surat_id: surat_id, status_update: status, catatan: catatan, created_by: 'ADMIN'
    });

    if (logError) return res.json({ success: false, message: logError.message });

    return res.json({ success: true, message: 'Status surat berhasil diupdate.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
