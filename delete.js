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
  const jam     = (p.jam     || '').trim();

  // ── Validasi token ─────────────────────────────────────────
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  if (!tanggal || !region || !jam) {
    return res.json({ success: false, message: 'Tanggal, Region, dan Jam wajib diisi.' });
  }

  // ── Hapus baris yang cocok ─────────────────────────────────
  const { data: deleted, error } = await supabase
    .from('database_input')
    .delete()
    .eq('tanggal', tanggal)
    .eq('region', region)
    .eq('jam', jam)
    .select('id');

  if (error) {
    return res.json({ success: false, message: 'Gagal menghapus data: ' + error.message });
  }

  const deletedCount = (deleted || []).length;

  if (deletedCount === 0) {
    const { data: allRows } = await supabase
      .from('database_input')
      .select('jam, tonase')
      .eq('tanggal', tanggal)
      .eq('region', region);

    let total = 0;
    const jamData = {};
    (allRows || []).forEach(r => {
      const t = parseFloat(r.tonase) || 0;
      total += t;
      jamData[r.jam] = t;
    });

    return res.json({
      success  : false,
      message  : `Data jam ${jam} tidak ditemukan di database.`,
      total    : Math.round(total * 100) / 100,
      jamData
    });
  }

  // Refresh data setelah hapus
  const { data: allRows } = await supabase
    .from('database_input')
    .select('jam, tonase')
    .eq('tanggal', tanggal)
    .eq('region', region);

  let total   = 0;
  const jamData = {};
  (allRows || []).forEach(r => {
    const t = parseFloat(r.tonase) || 0;
    total += t;
    jamData[r.jam] = t;
  });

  return res.json({
    success : true,
    message : `Data jam ${jam} berhasil dihapus (${deletedCount} baris).`,
    total   : Math.round(total * 100) / 100,
    jamData
  });
};
