const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p       = req.method === 'POST' ? req.body : req.query;
  const token   = (p.token   || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region  = (p.region  || '').trim();

  // ── Validasi token ─────────────────────────────────────────
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  if (!tanggal || !region) {
    return res.json({ success: false, message: 'Tanggal dan Region wajib diisi.' });
  }

  // ── Hapus estimasi ─────────────────────────────────────────
  const { data: deleted, error } = await supabase
    .from('data_estimasi')
    .delete()
    .eq('tanggal', tanggal)
    .eq('region', region)
    .select('id');

  if (error) {
    return res.json({ success: false, message: 'Gagal menghapus estimasi: ' + error.message });
  }

  const deletedCount = (deleted || []).length;

  if (deletedCount === 0) {
    const parts = tanggal.split('-');
    const displayDate = parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : tanggal;
    return res.json({
      success : false,
      message : `Data estimasi untuk tanggal ${displayDate} dan Region ${region} tidak ditemukan.`
    });
  }

  return res.json({
    success : true,
    message : `Berhasil menghapus ${deletedCount} data estimasi.`
  });
};
