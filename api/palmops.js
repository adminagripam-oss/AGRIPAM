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

  // 1. Action: Get PalmOps Data for a specific date (Public/Dashboard read)
  if (action === 'get') {
    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });
    const tanggal_akhir = (p.tanggal_akhir || '').trim();

    let query = supabase.from('database_palmops').select('region, tonase, tanggal');
    if (tanggal_akhir) {
      query = query.gte('tanggal', tanggal).lte('tanggal', tanggal_akhir);
    } else {
      query = query.eq('tanggal', tanggal);
    }

    const { data, error } = await query;

    if (error) {
      return res.json({ success: false, message: 'Gagal mengambil data PalmOps: ' + error.message });
    }

    const palmopsMap = {};
    (data || []).forEach(r => {
      if (!palmopsMap[r.region]) palmopsMap[r.region] = 0;
      palmopsMap[r.region] += parseFloat(r.tonase) || 0;
    });

    // Round the values to 2 decimal places after summing
    for (const region in palmopsMap) {
      palmopsMap[region] = Math.round(palmopsMap[region] * 100) / 100;
    }

    return res.json({ success: true, data: palmopsMap });
  }

  // 2. Action: Save (Upsert) PalmOps Data (ADMIN only)
  if (action === 'save') {
    const check = await verifyToken(token, 'ADMIN');
    if (!check.valid) return res.json({ success: false, message: check.message });

    const records = p.records; // Expecting array of { region, tonase }
    if (!tanggal || !Array.isArray(records) || records.length === 0) {
      return res.json({ success: false, message: 'Data tidak lengkap atau tidak valid.' });
    }

    const rows = records.map(r => ({
      tanggal,
      region: r.region,
      tonase: parseFloat(r.tonase) || 0
    }));

    const { data, error } = await supabase
      .from('database_palmops')
      .upsert(rows, { onConflict: 'tanggal,region' });

    if (error) {
      return res.json({ success: false, message: 'Gagal menyimpan data PalmOps: ' + error.message });
    }

    return res.json({ success: true, message: 'Data PalmOps berhasil disimpan ke database!' });
  }

  // 3. Action: Delete PalmOps Data for a specific date (ADMIN only)
  if (action === 'delete') {
    const check = await verifyToken(token, 'ADMIN');
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });

    const { error } = await supabase
      .from('database_palmops')
      .delete()
      .eq('tanggal', tanggal);

    if (error) {
      return res.json({ success: false, message: 'Gagal menghapus data PalmOps: ' + error.message });
    }

    return res.json({ success: true, message: 'Data PalmOps tanggal ini berhasil dihapus dari database!' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
