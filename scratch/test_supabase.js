const { supabase } = require('../api/lib/supabase');

async function test() {
  console.log("Connecting to Supabase...");
  const start = Date.now();
  try {
    const { data, error } = await supabase.from('database_input').select('count', { count: 'exact', head: true });
    if (error) {
      console.error("Error query:", error);
    } else {
      console.log(`Success! Total rows: ${data}, time taken: ${Date.now() - start}ms`);
    }
  } catch (err) {
    console.error("Exception:", err);
  }
}

test();
