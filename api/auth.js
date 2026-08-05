const { supabase } = require('./lib/supabase');
const { signToken, verifyToken, SESSION_TTL_MS } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WIN_MS = 10 * 60 * 1000; // 10 menit

const LOCAL_REGIONS_MAP = {
  'Aceh': 'ROACEH',
  'Sumatera Utara 1': 'ROSUMUT1',
  'Sumatera Utara 2 Ex Torganda': 'ROSUMUT2',
  'Riau 1': 'RORiau1',
  'Riau 2': 'RORiau2',
  'Riau 3': 'RORiau3',
  'Riau 4': 'RORiau4',
  'Bangka Belitung': 'ROBabel',
  'Jambi': 'ROJ4mb1',
  'Sumatera Barat': 'ROSumbar',
  'Sumatera Selatan': 'ROSumsel',
  'Kalimantan Barat 1A': 'ROKalbar1a',
  'Kalimantan Barat 1B': 'ROKalbar1B',
  'Kalimantan Barat 2': 'ROKalbar2',
  'Kalimantan Selatan 1': 'ROKalsel1',
  'Kalimantan Selatan 2': 'ROKalsel2',
  'Kalimantan Timur': 'ROKaltim',
  'Kalimantan Utara': 'ROKalut',
  'Kalimantan Tengah 1': 'ROKalteng1',
  'Kalimantan Tengah 2': 'ROKalteng2',
  'Kalimantan Tengah 3': 'ROKalteng3',
  'Sulawesi Tenggara': 'ROSultra',
  'Sulawesi Tengah': 'ROSulteng',
  'ADMIN': 'TANAMAN'
};

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const region = (p.region || '').trim();
  const token = (p.token || '').trim();

  if (action === 'login') {
    const password = (p.password || '').trim();
    const ipAddress = (p.ip || (req.headers && req.headers['x-forwarded-for']) || 'Tidak Terdeteksi').split(',')[0].trim();

    if (!region || !password) {
      return res.json({ success: false, message: 'Region dan Password wajib diisi.' });
    }

    // 1. Try Supabase Auth first
    let loginSuccess = false;
    let authErrorMsg = null;

    try {
      const { data: regionRow, error: regionErr } = await supabase
        .from('regions')
        .select('password_hash, is_active')
        .eq('region_name', region)
        .maybeSingle();

      if (!regionErr && regionRow) {
        if (!regionRow.is_active) {
          return res.json({ success: false, message: 'Region tidak aktif.' });
        }
        const { data: pwCheck } = await supabase.rpc('check_password', { p_region: region, p_password: password });
        if (pwCheck) {
          loginSuccess = true;
        } else {
          authErrorMsg = `Password salah untuk Region ${region}!`;
        }
      }
    } catch (e) {
      console.warn("Supabase query warning:", e.message);
    }

    // 2. Fallback to LOCAL_REGIONS_MAP if Supabase error or offline
    if (!loginSuccess && !authErrorMsg) {
      if (!LOCAL_REGIONS_MAP[region]) {
        return res.json({ success: false, message: 'Region tidak dikenal.' });
      }
      if (LOCAL_REGIONS_MAP[region] === password) {
        loginSuccess = true;
      } else {
        authErrorMsg = `Password salah untuk Region ${region}!`;
      }
    }

    if (!loginSuccess) {
      return res.json({ success: false, message: authErrorMsg || 'Password salah!' });
    }

    // 3. Generate token & return success
    const newToken = signToken(region);
    const now = new Date();
    const expiry = new Date(now.getTime() + SESSION_TTL_MS);

    try {
      await supabase.from('sesi_aktif').insert({
        region,
        token: newToken,
        login_time: now.toISOString(),
        expiry: expiry.toISOString(),
        status: 'Aktif',
        ip_address: ipAddress
      });
    } catch (_) {}

    return res.json({ success: true, message: 'Login berhasil.', token: newToken, ttlMs: SESSION_TTL_MS });
  }

  if (action === 'logout') {
    if (!token || !region) return res.json({ success: false, message: 'Token dan Region wajib diisi.' });
    try {
      await supabase.from('sesi_aktif').update({ status: 'Logout' }).eq('token', token).eq('status', 'Aktif');
    } catch (_) {}
    return res.json({ success: true, message: 'Logout berhasil.' });
  }

  if (action === 'refresh') {
    const check = await verifyToken(token, region);
    if (!check.valid) return res.json({ success: false, message: check.message });
    return res.json({ success: true, message: 'Sesi diperpanjang.', ttlMs: SESSION_TTL_MS });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};
