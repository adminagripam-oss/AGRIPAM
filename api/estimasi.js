const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

/**
 * Kembalikan tanggal hari ini dan besok dalam zona WIB (UTC+7).
 * Format: 'YYYY-MM-DD'
 *
 * Estimasi bersifat H+1 — user boleh input estimasi untuk:
 *   • Hari ini (hari berjalan)
 *   • Besok / H+1 (termasuk lintas bulan, misal 31 Juli → 1 Agustus)
 * Estimasi TIDAK boleh lebih dari H+1 (jauh ke depan).
 */
function getWIBDateInfo() {
  const nowUTC = Date.now() + 7 * 60 * 60 * 1000; // offset WIB
  const today  = new Date(nowUTC);

  const yyyy  = today.getUTCFullYear();
  const mm    = String(today.getUTCMonth() + 1).padStart(2, '0');
  const dd    = String(today.getUTCDate()).padStart(2, '0');
  const todayStr = `${yyyy}-${mm}-${dd}`;

  // Hitung besok (H+1)
  const tomorrowDate = new Date(nowUTC + 24 * 60 * 60 * 1000);
  const yyyy2 = tomorrowDate.getUTCFullYear();
  const mm2   = String(tomorrowDate.getUTCMonth() + 1).padStart(2, '0');
  const dd2   = String(tomorrowDate.getUTCDate()).padStart(2, '0');
  const tomorrowStr = `${yyyy2}-${mm2}-${dd2}`;

  return { today: todayStr, tomorrow: tomorrowStr };
}

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const token = (p.token || '').trim();
  const tanggal = (p.tanggal || '').trim();
  const region = (p.region || '').trim();

  if (action === 'getEstimasi') {
    if (!tanggal) return res.json({ success: false, message: 'Tanggal wajib diisi.' });

    const tanggal_akhir = (p.tanggal_akhir || '').trim();

    // Fetch in parallel pages of 1,000 to bypass PostgREST max_rows limit (1000/2000)
    const pageSize = 1000;
    const numPages = 5;
    const pagePromises = [];

    for (let i = 0; i < numPages; i++) {
      let q = supabase.from('data_estimasi').select('*').gte('tanggal', tanggal);
      if (tanggal_akhir) {
        q = q.lte('tanggal', tanggal_akhir);
      } else {
        q = q.lte('tanggal', tanggal);
      }
      if (region && region.toUpperCase() !== 'ALL') q = q.eq('region', region);
      q = q.range(i * pageSize, (i + 1) * pageSize - 1);

      pagePromises.push(q);
    }

    const pageResults = await Promise.all(pagePromises);
    let allData = [];
    for (const r of pageResults) {
      if (r.error) return res.json({ success: false, message: 'Gagal mengambil data estimasi: ' + r.error.message });
      if (r.data && r.data.length > 0) {
        allData = allData.concat(r.data);
      }
    }

    const allEstimasi = {};
    let totalRestanLalu = 0, totalLuasPanen = 0, totalTkPanen = 0, totalEstimasiPanen = 0, totalEstimasiKirim = 0, totalEstimasiRestan = 0;

    (allData || []).forEach(r => {
      const restanLalu = parseFloat(r.restan_lalu) || 0;
      const luasPanen = parseFloat(r.luas_panen_ha) || 0;
      const tkPanen = parseFloat(r.tk_panen_hk) || 0;
      const estimasiPanen = parseFloat(r.estimasi_panen_kg) || 0;
      const estimasiKirim = parseFloat(r.estimasi_kirim_kg) || 0;
      const estimasiRestan = parseFloat(r.estimasi_restan_kg) || 0;

      totalRestanLalu += restanLalu; totalLuasPanen += luasPanen; totalTkPanen += tkPanen;
      totalEstimasiPanen += estimasiPanen; totalEstimasiKirim += estimasiKirim; totalEstimasiRestan += estimasiRestan;

      if (!allEstimasi[r.region]) {
        allEstimasi[r.region] = { restanLalu: 0, luasPanen: 0, tkPanen: 0, estPanen: 0, outPanen: 0, estKirim: 0, estRestan: 0 };
      }
      allEstimasi[r.region].restanLalu += restanLalu;
      allEstimasi[r.region].luasPanen += luasPanen;
      allEstimasi[r.region].tkPanen += tkPanen;
      allEstimasi[r.region].estPanen += estimasiPanen;
      allEstimasi[r.region].estKirim += estimasiKirim;
      allEstimasi[r.region].estRestan += estimasiRestan;
    });

    Object.keys(allEstimasi).forEach(reg => {
      const d = allEstimasi[reg];
      d.outPanen = d.tkPanen > 0 ? Math.round(d.estPanen / d.tkPanen) : 0;
    });

    const avgOutputPanen = totalTkPanen > 0 ? Math.round(totalEstimasiPanen / totalTkPanen) : 0;

    return res.json({
      success: true,
      exists: allData.length > 0,
      allEstimasi,
      data: { restanLalu: totalRestanLalu, luasPanen: totalLuasPanen, tkPanen: totalTkPanen, estPanen: totalEstimasiPanen, outPanen: avgOutputPanen, estKirim: totalEstimasiKirim, estRestan: totalEstimasiRestan },
      allRecords: allData
    });
  }

  if (action === 'insertEstimasi') {
    const check = await verifyToken(token, null);
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (check.region !== 'ADMIN' && check.region !== region) {
      return res.json({ success: false, message: 'Anda tidak memiliki akses ke region ini.' });
    }

    const restanLalu = parseFloat(p.estimasiRestanLalu);
    const luasPanen = parseFloat(p.luasPanen);
    const tkPanen = parseFloat(p.tkPanen);
    const estPanen = parseFloat(p.estimasiPanen);
    const outPanen = parseFloat(p.outputPanen) || 0;
    const estKirim = parseFloat(p.estimasiKirim);
    const estRestan = parseFloat(p.estimasiRestan);

    if (!tanggal || !region || isNaN(restanLalu) || isNaN(luasPanen) || isNaN(tkPanen) || isNaN(estPanen) || isNaN(estKirim) || isNaN(estRestan)) {
      return res.json({ success: false, message: 'Data estimasi tidak lengkap atau tidak valid.' });
    }

    // ✅ Validasi H+1 — estimasi hanya boleh untuk hari ini atau besok (WIB)
    // Contoh skenario yang diizinkan:
    //   • Hari ini  31 Juli  → estimasi 31 Juli  ✅
    //   • Hari ini  31 Juli  → estimasi 1 Agustus ✅ (H+1, lintas bulan)
    //   • Hari ini  31 Juli  → estimasi 2 Agustus ❌ (terlalu jauh ke depan)
    //   • Hari ini  31 Juli  → estimasi 30 Juni   ❌ (masa lalu)
    const { today: todayWIB, tomorrow: tomorrowWIB } = getWIBDateInfo();
    if (tanggal !== todayWIB && tanggal !== tomorrowWIB && check.region !== 'ADMIN') {
      const { data: appReq } = await supabase.from('unlock_requests')
        .select('status')
        .eq('region', region)
        .eq('tanggal', tanggal)
        .eq('status', 'APPROVED')
        .limit(1);

      if (!appReq || appReq.length === 0) {
        const isInPast = tanggal < todayWIB;
        const [ty, tm, td] = todayWIB.split('-');
        const [ry, rm, rd] = tomorrowWIB.split('-');
        const monthNames = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
        const todayLabel    = `${td} ${monthNames[parseInt(tm,10)-1]} ${ty}`;
        const tomorrowLabel = `${rd} ${monthNames[parseInt(rm,10)-1]} ${ry}`;
        return res.json({
          success: false,
          message: isInPast
            ? `❌ Input estimasi ditolak! Tanggal (${tanggal}) sudah lewat. Estimasi hanya bisa diisi untuk hari ini (${todayLabel}) atau besok / H+1 (${tomorrowLabel}). Silakan ajukan permohonan buka akses ke Admin.`
            : `❌ Input estimasi ditolak! Tanggal (${tanggal}) terlalu jauh ke depan. Estimasi hanya bisa diisi untuk hari ini (${todayLabel}) atau besok / H+1 (${tomorrowLabel}).`
        });
      }
    }

    const { data: existing } = await supabase.from('data_estimasi').select('id').eq('tanggal', tanggal).eq('region', region).maybeSingle();

    if (existing) {
      const { error: updateError } = await supabase.from('data_estimasi').update({
        restan_lalu: restanLalu, luas_panen_ha: luasPanen, tk_panen_hk: tkPanen,
        estimasi_panen_kg: estPanen, output_panen: outPanen, estimasi_kirim_kg: estKirim, estimasi_restan_kg: estRestan
      }).eq('id', existing.id);

      if (updateError) return res.json({ success: false, message: 'Gagal memperbarui estimasi: ' + updateError.message });
      return res.json({ success: true, message: 'Data estimasi berhasil diperbarui!' });
    }

    const { error } = await supabase.from('data_estimasi').insert({
      tanggal, region, restan_lalu: restanLalu, luas_panen_ha: luasPanen, tk_panen_hk: tkPanen,
      estimasi_panen_kg: estPanen, output_panen: outPanen, estimasi_kirim_kg: estKirim, estimasi_restan_kg: estRestan
    });

    if (error) {
      if (error.code === '23505') return res.json({ success: false, message: 'Data estimasi untuk tanggal dan region ini sudah ada.' });
      return res.json({ success: false, message: 'Gagal menyimpan estimasi: ' + error.message });
    }

    return res.json({ success: true, message: 'Data estimasi berhasil disimpan!' });
  }

  if (action === 'deleteEstimasi') {
    const check = await verifyToken(token, null);
    if (!check.valid) return res.json({ success: false, message: check.message });

    if (check.region !== 'ADMIN' && check.region !== region) {
      return res.json({ success: false, message: 'Anda tidak memiliki akses ke region ini.' });
    }

    if (!tanggal || !region) return res.json({ success: false, message: 'Tanggal dan Region wajib diisi.' });

    const { today: todayWIB, tomorrow: tomorrowWIB } = getWIBDateInfo();
    if (tanggal !== todayWIB && tanggal !== tomorrowWIB && check.region !== 'ADMIN') {
      const { data: appReq } = await supabase.from('unlock_requests')
        .select('status')
        .eq('region', region)
        .eq('tanggal', tanggal)
        .eq('status', 'APPROVED')
        .limit(1);

      if (!appReq || appReq.length === 0) {
        return res.json({
          success: false,
          message: `❌ Penghapusan estimasi untuk tanggal ${tanggal} terkunci. Silakan ajukan permohonan buka akses ke Admin.`
        });
      }
    }

    const { data: deleted, error } = await supabase.from('data_estimasi').delete().eq('tanggal', tanggal).eq('region', region).select('id');
    if (error) return res.json({ success: false, message: 'Gagal menghapus estimasi: ' + error.message });

    const deletedCount = (deleted || []).length;
    if (deletedCount === 0) {
      const parts = tanggal.split('-');
      const displayDate = parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : tanggal;
      return res.json({ success: false, message: `Data estimasi untuk tanggal ${displayDate} dan Region ${region} tidak ditemukan.` });
    }

    return res.json({ success: true, message: `Berhasil menghapus ${deletedCount} data estimasi.` });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
