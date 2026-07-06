const https = require('https');

const url = new URL(process.env.SUPABASE_URL);
const host = url.hostname; // e.g. xxxx.supabase.co
const key = process.env.SUPABASE_SERVICE_KEY;

const sql = "ALTER TABLE surat ADD COLUMN IF NOT EXISTS tujuan TEXT;";

const postData = JSON.stringify({ query: sql });

const options = {
  hostname: host,
  path: '/rest/v1/rpc',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${key}`,
    'apikey': key,
  }
};

// Try Supabase pg-meta approach
const metaHost = host.replace('.supabase.co', '.supabase.co');

// Use the pg endpoint directly
fetch(`https://${host}/pg/query`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${key}`,
    'apikey': key,
  },
  body: JSON.stringify({ query: sql })
})
.then(r => r.text())
.then(txt => {
  console.log('pg/query response:', txt.substring(0, 500));
})
.catch(err => console.error(err));
