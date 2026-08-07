/**
 * Script: delete_october.js
 * Hapus data Oktober 2026 dari database_input dan data_estimasi
 */

const { supabase } = require('../api/lib/supabase');

async function deleteOctober() {
  console.log('====================================================');
  console.log(' HAPUS DATA OKTOBER 2026');
  console.log('====================================================\n');

  // Hapus dari database_input
  const { data: delInput, error: delInputErr } = await supabase
    .from('database_input')
    .delete()
    .gte('tanggal', '2026-10-01')
    .lte('tanggal', '2026-10-31')
    .select('id, tanggal, region, jam');

  if (delInputErr) {
    console.error('❌ [database_input] GAGAL:', delInputErr.message);
  } else {
    console.log(`✅ [database_input] ${(delInput || []).length} baris dihapus:`);
    (delInput || []).forEach(r =>
      console.log(`   • ${r.tanggal} | ${r.region} | jam ${r.jam}`)
    );
  }

  console.log('');

  // Hapus dari data_estimasi
  const { data: delEst, error: delEstErr } = await supabase
    .from('data_estimasi')
    .delete()
    .gte('tanggal', '2026-10-01')
    .lte('tanggal', '2026-10-31')
    .select('id, tanggal, region');

  if (delEstErr) {
    console.error('❌ [data_estimasi] GAGAL:', delEstErr.message);
  } else {
    console.log(`✅ [data_estimasi] ${(delEst || []).length} baris dihapus:`);
    (delEst || []).forEach(r =>
      console.log(`   • ${r.tanggal} | ${r.region}`)
    );
  }

  console.log('\n====================================================');
  console.log(' SELESAI');
  console.log('====================================================');
}

deleteOctober().catch(err => {
  console.error('Error fatal:', err.message);
  process.exit(1);
});
