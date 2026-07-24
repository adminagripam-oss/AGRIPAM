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

  if (actionCall === 'requestUnlock' || actionCall === 'requestRevision') {
    const tanggal = (p.tanggal || '').trim();
    const isRevision = actionCall === 'requestRevision' || p.type === 'REVISI_REALISASI';

    if (!tanggal || !region) {
      return res.json({ success: false, message: 'Data tidak lengkap (tanggal/region).' });
    }

    if (isRevision) {
      // Check existing pending request in delete_requests
      const { data: existingDel } = await supabase.from('delete_requests')
        .select('id').eq('type', 'UNLOCK_REALISASI').eq('region', region).eq('tanggal', tanggal).eq('status', 'PENDING').maybeSingle();

      if (existingDel) {
        return res.json({ success: false, message: 'Permintaan revisi realisasi produksi tanggal ini sudah diajukan dan sedang menunggu persetujuan Admin.' });
      }

      // Insert into delete_requests for clear type identification
      const { error: errDel } = await supabase.from('delete_requests').insert({ type: 'UNLOCK_REALISASI', region, tanggal, status: 'PENDING' });
      if (errDel) {
        return res.json({ success: false, message: 'Gagal mengirim permintaan revisi: ' + errDel.message });
      }

      // Also insert into unlock_requests for fallback
      const insertData = { region, tanggal, status: 'PENDING' };
      await supabase.from('unlock_requests').insert(insertData);

      return res.json({ success: true, message: 'Permintaan revisi realisasi produksi tanggal ' + tanggal + ' telah dikirim ke Admin untuk diverifikasi.' });
    } else {
      // Request unlock for Estimasi Panen
      const { data: existing } = await supabase.from('unlock_requests')
        .select('id').eq('region', region).eq('tanggal', tanggal).eq('status', 'PENDING').maybeSingle();

      if (existing) {
        return res.json({ success: false, message: 'Permintaan buka akses pengisian estimasi untuk tanggal ini sudah diajukan dan sedang menunggu persetujuan Admin.' });
      }

      const insertData = { region, tanggal, status: 'PENDING' };
      const { error } = await supabase.from('unlock_requests').insert(insertData);
      if (error) {
        return res.json({ success: false, message: 'Gagal mengirim permintaan buka akses: ' + error.message });
      }

      return res.json({ success: true, message: 'Permintaan buka akses pengisian estimasi tanggal ' + tanggal + ' telah dikirim ke Admin untuk diverifikasi.' });
    }
  }

  if (actionCall === 'checkRevisionStatus') {
    const tanggal = (p.tanggal || '').trim();
    if (!tanggal || !region) {
      return res.json({ success: false, message: 'Data tidak lengkap (tanggal/region).' });
    }

    // First check delete_requests for UNLOCK_REALISASI
    const { data: delData } = await supabase.from('delete_requests')
      .select('status')
      .eq('region', region)
      .eq('tanggal', tanggal)
      .eq('type', 'UNLOCK_REALISASI')
      .order('requested_at', { ascending: false })
      .limit(1);

    if (delData && delData.length > 0) {
      return res.json({ success: true, status: delData[0].status });
    }

    // Fallback check unlock_requests
    const { data: unlData } = await supabase.from('unlock_requests')
      .select('status')
      .eq('region', region)
      .eq('tanggal', tanggal)
      .order('requested_at', { ascending: false })
      .limit(1);

    if (unlData && unlData.length > 0) {
      return res.json({ success: true, status: unlData[0].status });
    }

    return res.json({ success: true, status: 'NONE' });
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

  if (actionCall === 'getUnlockRequests' || actionCall === 'getRevisionRequests') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Unauthorized. Hanya ADMIN yang dapat mengakses data ini.' });

    let query = supabase.from('unlock_requests').select('*').eq('status', 'PENDING').order('requested_at', { ascending: false });
    if (actionCall === 'getRevisionRequests') {
      query = query.eq('type', 'REVISI_REALISASI');
    }

    const { data, error } = await query;
    if (error) {
      if (error.message.includes('type')) {
        const fallback = await supabase.from('unlock_requests').select('*').eq('status', 'PENDING').order('requested_at', { ascending: false });
        return res.json({ success: true, data: fallback.data || [] });
      }
      return res.json({ success: false, message: 'Gagal mengambil data permintaan: ' + error.message });
    }

    return res.json({ success: true, data: data || [] });
  }

  if (actionCall === 'resolveUnlockRequest' || actionCall === 'resolveRevisionRequest') {
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

    return res.json({ success: true, message: resolveAction === 'APPROVE' ? 'Permintaan Revisi disetujui.' : 'Permintaan Revisi ditolak.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
