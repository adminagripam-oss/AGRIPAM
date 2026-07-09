const ALLOWED_ORIGINS = [
  'https://agri-pam.id',
  'https://www.agri-pam.id',
  'http://localhost:3000'
];

/**
 * Set CORS headers hanya untuk origin yang di-whitelist.
 * Mencegah situs lain memanggil API ini menggunakan token korban (CSRF-like abuse).
 */
function applyCors(req, res) {
  const origin = req.headers.origin;
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

module.exports = { applyCors };
