/**
 * Script: delete_aug_sep.js
 * Tujuan: Cek & hapus semua data Agustus dan September dari:
 *   - database_input  (data realisasi)
 *   - data_estimasi   (data estimasi)
 *
 * Jalankan dari root proyek:
 *   node --env-file=.env scratch/delete_aug_sep.js
 */

const { supabase } = require('../api/lib/supabase');

const MONTHS_TO_DELETE = [
  { prefix: '2026-08', label: 'Agustus 2026',   lastDay: '31' },
  { prefix: '2026-09', label: 'September 2026',  lastDay: '30' },
];

async function checkAndDelete() {
  console.log('====================================================');
  console.log(' CEK DATA AGUSTUS & SEPTEMBER DI DATABASE');
  console.log('====================================================\n');

  // ============================================================
  // FASE 1: CEK & TAMPILKAN DATA YANG ADA
  // ============================================================
  for (const { prefix, label, lastDay } of MONTHS_TO_DELETE) {
    console.log(`📅 ${label}`);
    console.log('─'.repeat(50));

    // Cek database_input
    const { data: inputData, error: inputError } = await supabase
      .from('database_input')
      .select('id, tanggal, region, jam, tonase')
      .gte('tanggal', `${prefix}-01`)
      .lte('tanggal', `${prefix}-${lastDay}`);

    if (inputError) {
      console.error(`  ❌ [database_input] Error: ${inputError.message}`);
    } else {
      console.log(`  📊 [database_input]  → ${inputData.length} baris ditemukan`);
      if (inputData.length > 0) {
        inputData.slice(0, 5).forEach(r =>
          console.log(`       • ${r.tanggal} | ${r.region} | jam ${r.jam} | ${r.tonase} ton`)
        );
        if (inputData.length > 5)
          console.log(`       ... dan ${inputData.length - 5} baris lainnya`);
      }
    }

    // Cek data_estimasi
    const { data: estData, error: estError } = await supabase
      .from('data_estimasi')
      .select('id, tanggal, region, estimasi_panen_kg')
      .gte('tanggal', `${prefix}-01`)
      .lte('tanggal', `${prefix}-${lastDay}`);

    if (estError) {
      console.error(`  ❌ [data_estimasi] Error: ${estError.message}`);
    } else {
      console.log(`  📋 [data_estimasi]   → ${estData.length} baris ditemukan`);
      if (estData.length > 0) {
        estData.slice(0, 5).forEach(r =>
          console.log(`       • ${r.tanggal} | ${r.region} | est. panen ${r.estimasi_panen_kg} kg`)
        );
        if (estData.length > 5)
          console.log(`       ... dan ${estData.length - 5} baris lainnya`);
      }
    }
    console.log('');
  }

  // ============================================================
  // FASE 2: HAPUS DATA
  // ============================================================
  console.log('====================================================');
  console.log(' MEMULAI PENGHAPUSAN...');
  console.log('====================================================\n');

  let grandTotal = 0;

  for (const { prefix, label, lastDay } of MONTHS_TO_DELETE) {
    console.log(`🗑️  Menghapus ${label}...`);

    // Hapus dari database_input
    const { data: delInput, error: delInputErr } = await supabase
      .from('database_input')
      .delete()
      .gte('tanggal', `${prefix}-01`)
      .lte('tanggal', `${prefix}-${lastDay}`)
      .select('id');

    if (delInputErr) {
      console.error(`  ❌ [database_input] GAGAL: ${delInputErr.message}`);
    } else {
      const n = (delInput || []).length;
      console.log(`  ✅ [database_input]  ${n} baris dihapus`);
      grandTotal += n;
    }

    // Hapus dari data_estimasi
    const { data: delEst, error: delEstErr } = await supabase
      .from('data_estimasi')
      .delete()
      .gte('tanggal', `${prefix}-01`)
      .lte('tanggal', `${prefix}-${lastDay}`)
      .select('id');

    if (delEstErr) {
      console.error(`  ❌ [data_estimasi] GAGAL: ${delEstErr.message}`);
    } else {
      const n = (delEst || []).length;
      console.log(`  ✅ [data_estimasi]   ${n} baris dihapus`);
      grandTotal += n;
    }

    console.log('');
  }

  console.log('====================================================');
  console.log(` ✅ SELESAI — Total ${grandTotal} baris berhasil dihapus`);
  console.log('====================================================');
}

checkAndDelete().catch(err => {
  console.error('\n❌ Error fatal:', err.message);
  process.exit(1);
});
