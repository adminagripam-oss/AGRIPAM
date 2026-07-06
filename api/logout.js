module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  // Logout is handled client-side via sessionStorage.removeItem
  // This stub prevents 500 errors if /api/logout is called
  return res.json({ success: true, message: 'Logged out.' });
};
