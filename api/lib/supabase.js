const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Auto load .env if not loaded yet
if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_KEY) {
  try {
    const envPath = path.join(__dirname, '..', '..', '.env');
    if (fs.existsSync(envPath)) {
      const envConfig = fs.readFileSync(envPath, 'utf8');
      envConfig.split(/\r?\n/).forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const parts = trimmed.split('=');
          if (parts.length >= 2) {
            const key = parts[0].trim();
            const value = parts.slice(1).join('=').trim().replace(/^['"]|['"]$/g, '');
            if (!process.env[key]) {
              process.env[key] = value;
            }
          }
        }
      });
    }
  } catch (_) {}
}

const supabaseUrl  = process.env.SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseKey  = process.env.SUPABASE_SERVICE_KEY || 'placeholder-key';

const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: { persistSession: false, autoRefreshToken: false }
});

module.exports = { supabase };
