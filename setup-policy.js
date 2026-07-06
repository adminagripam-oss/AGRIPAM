const { supabase } = require('./api/_lib/supabase');
async function setup() {
  const { data, error } = await supabase.rpc('query', { 
    query_text: "CREATE POLICY \"Allow public uploads\" ON storage.objects FOR INSERT TO public WITH CHECK (bucket_id = 'berkas_surat');" 
  });
  console.log(error || 'Policy created');
}
setup();
