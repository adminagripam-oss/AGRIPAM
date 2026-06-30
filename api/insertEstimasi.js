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

  // ── Validasi input ─────────────────────────────────────────
  const restanLalu  = parseFloat(p.estimasiRestanLalu);
  const luasPanen   = parseFloat(p.luasPanen);
  const tkPanen     = parseFloat(p.tkPanen);
  const estPanen    = parseFloat(p.estimasiPanen);
  const outPanen    = parseFloat(p.outputPanen) || 0;
  const estKirim    = parseFloat(p.estimasiKirim);
  const estRestan   = parseFloat(p.estimasiRestan);

  if (!tanggal || !region ||
      isNaN(restanLalu) || isNaN(luasPanen) || isNaN(tkPanen) ||
      isNaN(estPanen) || isNaN(estKirim) || isNaN(estRestan)) {
    return res.json({ success: false, message: 'Data estimasi tidak lengkap atau tidak valid.' });
  }

  // ── Cek duplikasi (unique per tanggal+region) ──────────────
  const { data: existing } = await supabase
    .from('data_estimasi')
    .select('id')
    .eq('tanggal', tanggal)
    .eq('region', region)
    .maybeSingle();

  if (existing) {
    // Format tampilan tanggal DD/MM/YYYY
    const parts = tanggal.split('-');
    const displayDate = parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : tanggal;
    return res.json({
      success : false,
      message : `Data estimasi tanggal ${displayDate} sudah ada. Gunakan 'Hapus Estimasi' untuk merevisi.`
    });
  }

  // ── Insert data estimasi baru ──────────────────────────────
  const { error } = await supabase.from('data_estimasi').insert({
    tanggal,
    region,
    restan_lalu        : restanLalu,
    luas_panen_ha      : luasPanen,
    tk_panen_hk        : tkPanen,
    estimasi_panen_kg  : estPanen,
    output_panen       : outPanen,
    estimasi_kirim_kg  : estKirim,
    estimasi_restan_kg : estRestan
  });

  if (error) {
    // Handle unique constraint violation
    if (error.code === '23505') {
      return res.json({ success: false, message: 'Data estimasi untuk tanggal dan region ini sudah ada.' });
    }
    return res.json({ success: false, message: 'Gagal menyimpan estimasi: ' + error.message });
  }

  return res.json({ success: true, message: 'Data estimasi berhasil disimpan!' });
};
