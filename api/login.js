const { supabase }                    = require('./_lib/supabase');
const { signToken, SESSION_TTL_MS }   = require('./_lib/auth');

const RATE_LIMIT_MAX    = 5;
const RATE_LIMIT_WIN_MS = 10 * 60 * 1000; // 10 menit

module.exports = async (req, res) => {
  // ── CORS ───────────────────────────────────────────────────
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const region    = (p.region    || '').trim();
  const password  = (p.password  || '').trim();
  const ipAddress = (p.ip        || req.headers['x-forwarded-for'] || 'Tidak Terdeteksi').split(',')[0].trim();

  if (!region || !password) {
    return res.json({ success: false, message: 'Region dan Password wajib diisi.' });
  }

  // ── 1. Cek Rate Limit ──────────────────────────────────────
  const { data: rl } = await supabase
    .from('rate_limit')
    .select('*')
    .eq('region', region)
    .maybeSingle();

  if (rl) {
    const age = Date.now() - new Date(rl.window_start).getTime();
    if (age < RATE_LIMIT_WIN_MS && rl.attempts >= RATE_LIMIT_MAX) {
      const wait = Math.ceil((RATE_LIMIT_WIN_MS - age) / 60000);
      return res.json({
        success: false,
        message: `Terlalu banyak percobaan login. Coba lagi dalam ${wait} menit.`
      });
    }
  }

  // ── 2. Validasi Region & Password (bcrypt via pgcrypto) ───
  const { data: regionRow, error: regionErr } = await supabase
    .from('regions')
    .select('password_hash, is_active')
    .eq('region_name', region)
    .maybeSingle();

  if (regionErr || !regionRow) {
    return res.json({ success: false, message: 'Region tidak dikenal.' });
  }

  if (!regionRow.is_active) {
    return res.json({ success: false, message: 'Region tidak aktif.' });
  }

  // Validasi password menggunakan fungsi crypt() pgcrypto langsung di DB
  const { data: pwCheck } = await supabase
    .rpc('check_password', { p_region: region, p_password: password });

  if (!pwCheck) {
    // Catat percobaan gagal
    if (rl) {
      const age = Date.now() - new Date(rl.window_start).getTime();
      if (age > RATE_LIMIT_WIN_MS) {
        await supabase.from('rate_limit').upsert(
          { region, attempts: 1, window_start: new Date().toISOString(), updated_at: new Date().toISOString() },
          { onConflict: 'region' }
        );
      } else {
        await supabase.from('rate_limit')
          .update({ attempts: rl.attempts + 1, updated_at: new Date().toISOString() })
          .eq('region', region);
      }
    } else {
      await supabase.from('rate_limit').insert(
        { region, attempts: 1, window_start: new Date().toISOString() }
      );
    }
    return res.json({ success: false, message: `Password salah untuk Region ${region}!` });
  }

  // ── 3. Reset rate limit & override sesi lama ──────────────
  await supabase.from('rate_limit').delete().eq('region', region);

  await supabase.from('sesi_aktif')
    .update({ status: 'Logout' })
    .eq('region', region)
    .eq('status', 'Aktif');

  // ── 4. Buat token baru & simpan sesi ──────────────────────
  const token  = signToken(region);
  const now    = new Date();
  const expiry = new Date(now.getTime() + SESSION_TTL_MS);

  await supabase.from('sesi_aktif').insert({
    region,
    token,
    login_time : now.toISOString(),
    expiry     : expiry.toISOString(),
    status     : 'Aktif',
    ip_address : ipAddress
  });

  await supabase.from('audit_log').insert({
    region, action: 'LOGIN_SUCCESS', detail: `Login dari IP: ${ipAddress}`
  });

  return res.json({
    success : true,
    message : 'Login berhasil.',
    token,
    ttlMs   : SESSION_TTL_MS
  });
};
