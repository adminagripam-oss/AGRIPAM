const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region = (p.region || '').trim(); // Untuk verifikasi token

  if (!tanggal) {
    return res.json({ success: false, message: 'Tanggal wajib diisi.' });
  }

  // 1. GET LAPORAN
  if (action === 'getLaporan') {
    const { data, error } = await supabase
      .from('laporan_realisasi_panen')
      .select('*')
      .eq('tanggal', tanggal)
      .maybeSingle();

    if (error) {
      return res.json({ success: false, message: 'Gagal mengambil data: ' + error.message });
    }

    if (data) {
      return res.json({ success: true, exists: true, data: data.data });
    } else {
      return res.json({ success: true, exists: false });
    }
  }

  // 2. SAVE LAPORAN
  if (action === 'saveLaporan') {
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    
    if (check.region !== 'ADMIN') {
      return res.json({ success: false, message: 'Hanya Admin yang dapat menyimpan laporan keseluruhan.' });
    }

    const payloadData = p.data;
    if (!payloadData) {
      return res.json({ success: false, message: 'Data Laporan kosong.' });
    }

    const { error } = await supabase
      .from('laporan_realisasi_panen')
      .upsert({ tanggal: tanggal, data: payloadData }, { onConflict: 'tanggal' });

    if (error) {
      return res.json({ success: false, message: 'Gagal menyimpan laporan: ' + error.message });
    }

    return res.json({ success: true, message: 'Laporan berhasil disimpan.' });
  }

  // 3. DELETE LAPORAN
  if (action === 'deleteLaporan') {
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    
    if (check.region !== 'ADMIN') {
      return res.json({ success: false, message: 'Hanya Admin yang dapat menghapus laporan keseluruhan.' });
    }

    const { error } = await supabase
      .from('laporan_realisasi_panen')
      .delete()
      .eq('tanggal', tanggal);

    if (error) {
      return res.json({ success: false, message: 'Gagal menghapus laporan: ' + error.message });
    }

    return res.json({ success: true, message: 'Laporan berhasil dihapus.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
