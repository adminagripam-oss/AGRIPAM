const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const actionCall = (p.action || '').trim();
  const token = (p.token || '').trim();
  const region = (p.region || '').trim();

  // Validasi token
  const check = await verifyToken(token, region);
  if (!check.valid) return res.json({ success: false, message: check.message });

  if (actionCall === 'requestUnlock') {
    const tanggal = (p.tanggal || '').trim();

    if (!tanggal || !region) {
      return res.json({ success: false, message: 'Data tidak lengkap (tanggal/region).' });
    }

    let query = supabase.from('unlock_requests').select('id').eq('region', region).eq('tanggal', tanggal).eq('status', 'PENDING');

    const { data: existing } = await query.maybeSingle();
    if (existing) return res.json({ success: false, message: 'Permintaan buka akses estimasi untuk ini sudah diajukan dan sedang menunggu persetujuan Admin.' });

    const { error } = await supabase.from('unlock_requests').insert({ region, tanggal, status: 'PENDING' });
    if (error) return res.json({ success: false, message: 'Gagal mengirim permintaan buka akses: ' + error.message });

    return res.json({ success: true, message: 'Permintaan buka akses estimasi telah dikirim ke Admin untuk diverifikasi.' });
  }

  if (actionCall === 'checkUnlock') {
    const tanggal = (p.tanggal || '').trim();
    const jam = (p.jam || '').trim();
    if (!tanggal || !region) {
      return res.json({ success: false, message: 'Data tidak lengkap.' });
    }
    
    if (jam) {
      // Check Realisasi unlock in delete_requests table
      const { data, error } = await supabase.from('delete_requests')
        .select('status')
        .eq('type', 'UNLOCK_REALISASI')
        .eq('region', region)
        .eq('tanggal', tanggal)
        .eq('jam', jam)
        .order('requested_at', { ascending: false })
        .limit(1);

      if (error) return res.json({ success: false, message: 'Gagal mengecek status unlock: ' + error.message });

      if (data && data.length > 0) {
        return res.json({ success: true, status: data[0].status });
      } else {
        return res.json({ success: true, status: 'NONE' });
      }
    } else {
      // Check Estimasi unlock in unlock_requests table
      const { data, error } = await supabase.from('unlock_requests')
        .select('status')
        .eq('region', region)
        .eq('tanggal', tanggal)
        .order('requested_at', { ascending: false })
        .limit(1);

      if (error) return res.json({ success: false, message: 'Gagal mengecek status unlock: ' + error.message });

      if (data && data.length > 0) {
        return res.json({ success: true, status: data[0].status });
      } else {
        return res.json({ success: true, status: 'NONE' });
      }
    }
  }

  if (actionCall === 'getUnlockRequests') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat mengakses data ini.' });

    const { data, error } = await supabase.from('unlock_requests').select('*').eq('status', 'PENDING').order('requested_at', { ascending: false });
    if (error) return res.json({ success: false, message: 'Gagal mengambil data permintaan: ' + error.message });

    return res.json({ success: true, data: data || [] });
  }

  if (actionCall === 'resolveUnlockRequest') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat melakukan aksi ini.' });

    const requestId = parseInt(p.requestId, 10);
    const resolveAction = (p.resolveAction || '').trim().toUpperCase(); // APPROVE or REJECT

    if (isNaN(requestId) || !['APPROVE', 'REJECT'].includes(resolveAction)) {
      return res.json({ success: false, message: 'Data tidak valid (requestId/action).' });
    }

    const { data: requestData, error: reqError } = await supabase.from('unlock_requests').select('*').eq('id', requestId).maybeSingle();
    if (reqError || !requestData) return res.json({ success: false, message: 'Permintaan tidak ditemukan.' });
    if (requestData.status !== 'PENDING') return res.json({ success: false, message: 'Permintaan ini sudah diproses sebelumnya.' });

    const { error: updateError } = await supabase.from('unlock_requests').update({
      status: resolveAction === 'APPROVE' ? 'APPROVED' : 'REJECTED',
      resolved_at: new Date().toISOString(),
      resolved_by: region
    }).eq('id', requestId);

    if (updateError) return res.json({ success: false, message: 'Gagal mengupdate status permintaan: ' + updateError.message });

    return res.json({ success: true, message: resolveAction === 'APPROVE' ? 'Permintaan Buka Akses disetujui.' : 'Permintaan Buka Akses ditolak.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
