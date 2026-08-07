const { supabase } = require('../api/lib/supabase');

async function getRegions() {
  try {
    const { data, error } = await supabase.from('regions').select('region_name, is_active');
    if (error) {
      console.error("Error fetching regions:", error);
    } else {
      console.log("Active Regions:", data);
    }
  } catch (err) {
    console.error("Exception:", err);
  }
}

getRegions();
