const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');

const DEFAULT_ID = '00000000-0000-0000-0000-000000000000';

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const token = req.headers['authorization']?.split(' ')[1] || req.body.token || req.query.token;
  const region = req.headers['x-region'] || req.body.region || req.query.region;

  // Basic auth check
  if (!token || !region) {
    return res.status(401).json({ success: false, message: 'Unauthorized' });
  }

  // Only QC admin or ADMIN should access this
  if (region !== 'QC admin' && region !== 'ADMIN') {
    return res.status(403).json({ success: false, message: 'Forbidden' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.status(401).json({ success: false, message: 'Session invalid or expired' });
  }

  try {
    if (req.method === 'GET') {
      const { data, error } = await supabase
        .from('qc_spreadsheet')
        .select('*')
        .eq('id', DEFAULT_ID)
        .single();

      if (error) throw error;
      return res.json({ success: true, data });
    }

    if (req.method === 'POST') {
      const { sheetData, columns, settings } = req.body;

      const { data, error } = await supabase
        .from('qc_spreadsheet')
        .update({
          data: sheetData,
          columns: columns,
          settings: settings,
          updated_at: new Date().toISOString()
        })
        .eq('id', DEFAULT_ID)
        .select()
        .single();

      if (error) throw error;
      return res.json({ success: true, message: 'Data saved successfully', data });
    }

    return res.status(405).json({ success: false, message: 'Method not allowed' });
  } catch (error) {
    console.error('API /qcSheet Error:', error);
    return res.status(500).json({ success: false, message: 'Internal Server Error' });
  }
};
