const { supabase } = require('../api/lib/supabase');

async function test() {
  console.log("Fetching Aceh data...");
  try {
    const { data: realData, error: realErr } = await supabase
      .from('database_input')
      .select('tanggal, region, jam, tonase')
      .eq('region', 'Aceh')
      .gte('tanggal', '2026-07-01')
      .lte('tanggal', '2026-07-16');

    if (realErr) {
      console.error("Realisasi Error:", realErr);
    } else {
      console.log(`Realisasi rows: ${realData.length}`);
      if (realData.length > 0) {
        console.log("Sample:", realData.slice(0, 3));
      }
    }

    const { data: estData, error: estErr } = await supabase
      .from('data_estimasi')
      .select('tanggal, region, estimasi_panen_kg')
      .eq('region', 'Aceh')
      .gte('tanggal', '2026-07-01')
      .lte('tanggal', '2026-07-16');

    if (estErr) {
      console.error("Estimasi Error:", estErr);
    } else {
      console.log(`Estimasi rows: ${estData.length}`);
      if (estData.length > 0) {
        console.log("Sample:", estData.slice(0, 3));
      }
    }
  } catch (err) {
    console.error("Exception:", err);
  }
}

test();
