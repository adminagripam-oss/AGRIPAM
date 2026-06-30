const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

const MIN_TONASE = 0;
const MAX_TONASE = 5000;

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
  const tonase  = p.tonase;

  // ── Validasi token ─────────────────────────────────────────
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  // ── Validasi input ─────────────────────────────────────────
  if (!tanggal || !region || !jam || tonase === undefined || tonase === '') {
    return res.json({ success: false, message: 'Data tidak lengkap (tanggal/region/jam/tonase).' });
  }

  const tonaseNum = parseFloat(tonase);
  if (isNaN(tonaseNum)) {
    return res.json({ success: false, message: 'Nilai tonase tidak valid.' });
  }
  if (tonaseNum < MIN_TONASE || tonaseNum > MAX_TONASE) {
    return res.json({ success: false, message: `Tonase harus antara ${MIN_TONASE} dan ${MAX_TONASE}.` });
  }

  // ── Cek duplikasi jam ──────────────────────────────────────
  const { data: existing } = await supabase
    .from('database_input')
    .select('id, tonase')
    .eq('tanggal', tanggal)
    .eq('region', region)
    .eq('jam', jam)
    .maybeSingle();

  if (existing) {
    // Hitung total & jamData saat ini untuk dikembalikan ke client
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
      message  : `Data jam ${jam} sudah ada. Gunakan 'Hapus Jam Ini' untuk merevisi.`,
      total    : Math.round(total * 100) / 100,
      jamData
    });
  }

  // ── Insert data baru ───────────────────────────────────────
  const { error } = await supabase.from('database_input').insert({
    tanggal,
    region,
    jam,
    tonase: tonaseNum
  });

  if (error) {
    return res.json({ success: false, message: 'Gagal menyimpan data: ' + error.message });
  }

  // Refresh total & jamData setelah insert
  const { data: allRows } = await supabase
    .from('database_input')
    .select('jam, tonase')
    .eq('tanggal', tanggal)
    .eq('region', region);

  let newTotal  = 0;
  const jamData = {};
  (allRows || []).forEach(r => {
    const t = parseFloat(r.tonase) || 0;
    newTotal += t;
    jamData[r.jam] = t;
  });

  return res.json({
    success : true,
    message : 'Data berhasil disimpan.',
    total   : Math.round(newTotal * 100) / 100,
    jamData
  });
};
