const { applyCors } = require('./lib/cors');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();
  // Logout is handled client-side via sessionStorage.removeItem
  // This stub prevents 500 errors if /api/logout is called
  return res.json({ success: true, message: 'Logged out.' });
};
