/**
 * Script: check_future_months.js
 * Cek semua data yang bukan bulan Juli 2026 di database_input dan data_estimasi
 */

const { supabase } = require('../api/lib/supabase');

async function checkFutureData() {
  console.log('====================================================');
  console.log(' CEK DATA DI LUAR BULAN JULI 2026');
  console.log('====================================================\n');

  // Cek database_input — semua data di luar Juli 2026
  const { data: inputData, error: inputError } = await supabase
    .from('database_input')
    .select('id, tanggal, region, jam, tonase')
    .not('tanggal', 'gte', '2026-07-01')
    .not('tanggal', 'lte', '2026-07-31');

  // Cara lebih reliable: ambil semua lalu filter manual
  const { data: allInput, error: allInputErr } = await supabase
    .from('database_input')
    .select('id, tanggal, region, jam, tonase')
    .or('tanggal.lt.2026-07-01,tanggal.gt.2026-07-31');

  if (allInputErr) {
    console.error('[database_input] Error:', allInputErr.message);
  } else {
    const grouped = {};
    (allInput || []).forEach(r => {
      const m = r.tanggal.substring(0, 7);
      if (!grouped[m]) grouped[m] = [];
      grouped[m].push(r);
    });

    if (Object.keys(grouped).length === 0) {
      console.log('✅ [database_input] Tidak ada data di luar Juli 2026\n');
    } else {
      console.log(`⚠️  [database_input] Ditemukan data di luar Juli 2026:`);
      Object.entries(grouped).sort().forEach(([month, rows]) => {
        console.log(`\n  📅 Bulan ${month} → ${rows.length} baris`);
        rows.slice(0, 5).forEach(r =>
          console.log(`     • ${r.tanggal} | ${r.region} | jam ${r.jam} | ${r.tonase} ton`)
        );
        if (rows.length > 5) console.log(`     ... dan ${rows.length - 5} baris lainnya`);
      });
      console.log('');
    }
  }

  // Cek data_estimasi
  const { data: allEst, error: allEstErr } = await supabase
    .from('data_estimasi')
    .select('id, tanggal, region, estimasi_panen_kg')
    .or('tanggal.lt.2026-07-01,tanggal.gt.2026-07-31');

  if (allEstErr) {
    console.error('[data_estimasi] Error:', allEstErr.message);
  } else {
    const grouped = {};
    (allEst || []).forEach(r => {
      const m = r.tanggal.substring(0, 7);
      if (!grouped[m]) grouped[m] = [];
      grouped[m].push(r);
    });

    if (Object.keys(grouped).length === 0) {
      console.log('✅ [data_estimasi] Tidak ada data di luar Juli 2026\n');
    } else {
      console.log(`⚠️  [data_estimasi] Ditemukan data di luar Juli 2026:`);
      Object.entries(grouped).sort().forEach(([month, rows]) => {
        console.log(`\n  📅 Bulan ${month} → ${rows.length} baris`);
        rows.slice(0, 5).forEach(r =>
          console.log(`     • ${r.tanggal} | ${r.region} | est. ${r.estimasi_panen_kg} kg`)
        );
        if (rows.length > 5) console.log(`     ... dan ${rows.length - 5} baris lainnya`);
      });
      console.log('');
    }
  }

  console.log('====================================================');
  console.log(' CEK SELESAI');
  console.log('====================================================');
}

checkFutureData().catch(err => {
  console.error('Error fatal:', err.message);
  process.exit(1);
});
