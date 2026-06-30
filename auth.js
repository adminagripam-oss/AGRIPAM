const jwt      = require('jsonwebtoken');
const { supabase } = require('./supabase');

const JWT_SECRET     = process.env.JWT_SECRET;
const SESSION_TTL_MS = 8 * 60 * 60 * 1000; // 8 jam

if (!JWT_SECRET) {
  throw new Error('Missing JWT_SECRET environment variable');
}

/**
 * Buat token JWT baru untuk region tertentu (berlaku 8 jam)
 */
function signToken(region) {
  return jwt.sign(
    { region },
    JWT_SECRET,
    { expiresIn: '8h' }
  );
}

/**
 * Verifikasi token:
 *  1. Cek signature JWT
 *  2. Cek expiry JWT
 *  3. Cek status di tabel sesi_aktif (bisa sudah di-logout)
 *
 * @returns { valid: boolean, region?: string, message?: string }
 */
async function verifyToken(token, expectedRegion) {
  if (!token) {
    return { valid: false, message: 'Sesi tidak ditemukan. Silakan login ulang.' };
  }

  let decoded;
  try {
    decoded = jwt.verify(token, JWT_SECRET);
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return { valid: false, message: 'Sesi sudah kedaluwarsa. Silakan login ulang.' };
    }
    return { valid: false, message: 'Token tidak valid. Silakan login ulang.' };
  }

  if (expectedRegion && decoded.region !== expectedRegion) {
    return { valid: false, message: 'Token tidak sesuai dengan region. Silakan login ulang.' };
  }

  // Cek apakah sesi masih Aktif di database (belum logout/expired)
  const { data, error } = await supabase
    .from('sesi_aktif')
    .select('id, status')
    .eq('token', token)
    .eq('status', 'Aktif')
    .maybeSingle();

  if (error || !data) {
    return { valid: false, message: 'Sesi tidak valid atau sudah diakhiri. Silakan login ulang.' };
  }

  return { valid: true, region: decoded.region };
}

module.exports = { signToken, verifyToken, SESSION_TTL_MS };
