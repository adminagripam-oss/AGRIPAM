const { supabase } = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const actionCall = (p.action || '').trim();
  const token = (p.token || '').trim();
  const region = (p.region || '').trim();

  // Validasi token
  const check = await verifyToken(token, region);
  if (!check.valid) return res.json({ success: false, message: check.message });

  if (actionCall === 'requestDelete') {
    const type = (p.type || '').trim().toUpperCase(); // REALISASI or ESTIMASI
    const tanggal = (p.tanggal || '').trim();
    const jam = (p.jam || '').trim();

    if (!type || !tanggal || !region) {
      return res.json({ success: false, message: 'Data tidak lengkap (type/tanggal/region).' });
    }

    let query = supabase.from('delete_requests').select('id').eq('type', type).eq('region', region).eq('tanggal', tanggal).eq('status', 'PENDING');
    if (type === 'REALISASI' && jam) query = query.eq('jam', jam);

    const { data: existing } = await query.maybeSingle();
    if (existing) return res.json({ success: false, message: 'Permintaan hapus data untuk ini sudah diajukan dan sedang menunggu persetujuan Admin.' });

    const { error } = await supabase.from('delete_requests').insert({ type, region, tanggal, jam: type === 'REALISASI' ? jam : null, status: 'PENDING' });
    if (error) return res.json({ success: false, message: 'Gagal mengirim permintaan hapus: ' + error.message });

    return res.json({ success: true, message: 'Permintaan hapus data telah dikirim ke Admin untuk diverifikasi.' });
  }

  if (actionCall === 'getDeleteRequests') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat mengakses data ini.' });

    const { data, error } = await supabase.from('delete_requests').select('*').eq('status', 'PENDING').order('requested_at', { ascending: false });
    if (error) return res.json({ success: false, message: 'Gagal mengambil data permintaan: ' + error.message });

    return res.json({ success: true, data: data || [] });
  }

  if (actionCall === 'resolveDeleteRequest') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat melakukan aksi ini.' });

    const requestId = parseInt(p.requestId, 10);
    const resolveAction = (p.resolveAction || '').trim().toUpperCase(); // APPROVE or REJECT

    if (isNaN(requestId) || !['APPROVE', 'REJECT'].includes(resolveAction)) {
      return res.json({ success: false, message: 'Data tidak valid (requestId/action).' });
    }

    const { data: requestData, error: reqError } = await supabase.from('delete_requests').select('*').eq('id', requestId).maybeSingle();
    if (reqError || !requestData) return res.json({ success: false, message: 'Permintaan tidak ditemukan.' });
    if (requestData.status !== 'PENDING') return res.json({ success: false, message: 'Permintaan ini sudah diproses sebelumnya.' });

    if (resolveAction === 'APPROVE') {
      let delError = null;
      if (requestData.type === 'REALISASI') {
        const { error } = await supabase.from('database_input').delete().eq('tanggal', requestData.tanggal).eq('region', requestData.region).eq('jam', requestData.jam);
        delError = error;
      } else if (requestData.type === 'ESTIMASI') {
        const { error } = await supabase.from('data_estimasi').delete().eq('tanggal', requestData.tanggal).eq('region', requestData.region);
        delError = error;
      }
      if (delError) return res.json({ success: false, message: 'Gagal menghapus data target: ' + delError.message });
    }

    const { error: updateError } = await supabase.from('delete_requests').update({
      status: resolveAction === 'APPROVE' ? 'APPROVED' : 'REJECTED',
      resolved_at: new Date().toISOString(),
      resolved_by: region
    }).eq('id', requestId);

    if (updateError) return res.json({ success: false, message: 'Data terhapus, namun gagal mengupdate status permintaan: ' + updateError.message });

    return res.json({ success: true, message: resolveAction === 'APPROVE' ? 'Permintaan disetujui dan data dihapus.' : 'Permintaan ditolak.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
