const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const bulan = (p.bulan || '').trim(); // Format: YYYY-MM
  const region = (p.region || '').trim(); // Untuk verifikasi token (ADMIN)

  if (!bulan) {
    return res.json({ success: false, message: 'Parameter bulan (YYYY-MM) wajib diisi.' });
  }

  // 1. GET TARGET CHALLENGE
  if (action === 'getTarget') {
    const { data, error } = await supabase
      .from('target_challenge_bulanan')
      .select('*')
      .eq('bulan', bulan)
      .maybeSingle();

    if (error) {
      return res.json({ success: false, message: 'Gagal mengambil data target: ' + error.message });
    }

    if (data) {
      return res.json({ success: true, exists: true, data: data.data });
    } else {
      return res.json({ success: true, exists: false, data: {} });
    }
  }

  // 2. SAVE (UPLOAD) TARGET CHALLENGE
  if (action === 'saveTarget') {
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    
    if (check.region !== 'ADMIN') {
      return res.json({ success: false, message: 'Hanya Admin yang dapat mengunggah target challenge.' });
    }

    const payloadData = p.data;
    if (!payloadData) {
      return res.json({ success: false, message: 'Data Target kosong.' });
    }

    const { error } = await supabase
      .from('target_challenge_bulanan')
      .upsert({ bulan: bulan, data: payloadData }, { onConflict: 'bulan' });

    if (error) {
      return res.json({ success: false, message: 'Gagal menyimpan target bulanan: ' + error.message });
    }

    return res.json({ success: true, message: 'Target bulanan berhasil disimpan.' });
  }

  // 3. DELETE TARGET CHALLENGE
  if (action === 'deleteTarget') {
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    
    if (check.region !== 'ADMIN') {
      return res.json({ success: false, message: 'Hanya Admin yang dapat menghapus target challenge.' });
    }

    const { error } = await supabase
      .from('target_challenge_bulanan')
      .delete()
      .eq('bulan', bulan);

    if (error) {
      return res.json({ success: false, message: 'Gagal menghapus target bulanan: ' + error.message });
    }

    return res.json({ success: true, message: 'Target bulanan berhasil dihapus.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
