const { supabase }    = require('./_lib/supabase');
const { verifyToken } = require('./_lib/auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p       = req.method === 'POST' ? req.body : req.query;
  const token   = (p.token   || '').trim();
  const region  = (p.region  || '').trim();
  const requestId = parseInt(p.requestId, 10);
  const action  = (p.resolveAction  || '').trim().toUpperCase(); // APPROVE or REJECT

  // 1. Validasi token & pastikan hanya ADMIN
  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }
  
  if (region !== 'ADMIN') {
    return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat melakukan aksi ini.' });
  }

  if (isNaN(requestId) || !['APPROVE', 'REJECT'].includes(action)) {
    return res.json({ success: false, message: 'Data tidak valid (requestId/action).' });
  }

  // 2. Ambil data delete_request
  const { data: requestData, error: reqError } = await supabase
    .from('delete_requests')
    .select('*')
    .eq('id', requestId)
    .maybeSingle();

  if (reqError || !requestData) {
    return res.json({ success: false, message: 'Permintaan tidak ditemukan.' });
  }

  if (requestData.status !== 'PENDING') {
    return res.json({ success: false, message: 'Permintaan ini sudah diproses sebelumnya.' });
  }

  // 3. Jika APPROVE, lakukan penghapusan data
  if (action === 'APPROVE') {
    let delError = null;

    if (requestData.type === 'REALISASI') {
      const { error } = await supabase
        .from('database_input')
        .delete()
        .eq('tanggal', requestData.tanggal)
        .eq('region', requestData.region)
        .eq('jam', requestData.jam);
      delError = error;
    } else if (requestData.type === 'ESTIMASI') {
      const { error } = await supabase
        .from('data_estimasi')
        .delete()
        .eq('tanggal', requestData.tanggal)
        .eq('region', requestData.region);
      delError = error;
    }

    if (delError) {
      return res.json({ success: false, message: 'Gagal menghapus data target: ' + delError.message });
    }
  }

  // 4. Update status permintaan
  const { error: updateError } = await supabase
    .from('delete_requests')
    .update({
      status: action === 'APPROVE' ? 'APPROVED' : 'REJECTED',
      resolved_at: new Date().toISOString(),
      resolved_by: region
    })
    .eq('id', requestId);

  if (updateError) {
    return res.json({ success: false, message: 'Data terhapus, namun gagal mengupdate status permintaan: ' + updateError.message });
  }

  return res.json({
    success: true,
    message: action === 'APPROVE' ? 'Permintaan disetujui dan data dihapus.' : 'Permintaan ditolak.'
  });
};
