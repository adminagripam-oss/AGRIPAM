const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');
const fs = require('fs');
const path = require('path');
const HTMLtoDOCX = require('html-to-docx');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const token = req.headers['authorization']?.split(' ')[1] || req.body.token || req.query.token;
  const region = req.headers['x-region'] || req.body.region || req.query.region;

  if (!token || !region) {
    return res.status(401).json({ success: false, message: 'Unauthorized' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.status(401).json({ success: false, message: 'Session invalid or expired' });
  }

  const isAdmin = region.toUpperCase() === 'ADMIN';

  try {
    // GET: Fetch Data
    if (req.method === 'GET') {
      let query = supabase.from('vendor_monitoring').select('*').order('created_at', { ascending: false });
      
      // Role-based access control: CROs only see their own regional data
      if (!isAdmin) {
        query = query.eq('regional', region);
      }

      const { data, error } = await query;
      if (error) throw error;
      return res.json({ success: true, data });
    }

    // POST: Create or Update Document Generation (Mail Merge)
    if (req.method === 'POST') {
      const { action } = req.body;

      // 1. Mail Merge / Generate SPK
      if (action === 'generate-spk') {
        const { vendorId } = req.body;
        
        // Fetch the row
        const { data: vendor, error: fetchErr } = await supabase
          .from('vendor_monitoring')
          .select('*')
          .eq('id', vendorId)
          .single();
          
        if (fetchErr) throw fetchErr;

        // Create HTML Template for the document
        const htmlString = `
          <!DOCTYPE html>
          <html>
            <head><meta charset="UTF-8"></head>
            <body>
              <h2 style="text-align: center;">SURAT PENUGASAN PENGELOLAAN KEBUN MANDIRI</h2>
              <p>Nomor: ${vendor.no_surat || 'SPK/001/AGRIPAM/2026'}</p>
              <br/>
              <p>Kepada Yth.,<br/>
              <strong>${vendor.nama_vendor}</strong><br/>
              PIC: ${vendor.pic || '-'}<br/>
              Kontak: ${vendor.kontak_vendor || '-'}</p>
              <br/>
              <p>Dengan hormat,</p>
              <p>Berdasarkan hasil evaluasi, dengan ini kami menugaskan perusahaan Saudara untuk mengelola kebun mandiri dengan rincian sebagai berikut:</p>
              <ul>
                <li><strong>Regional:</strong> ${vendor.regional}</li>
                <li><strong>Nama Kebun:</strong> ${vendor.kebun}</li>
                <li><strong>Luas (Ha):</strong> ${vendor.luas_ha} Ha</li>
                <li><strong>Luas TM (Ha):</strong> ${vendor.luas_tm_ha || 0} Ha</li>
                <li><strong>Target Produksi:</strong> ${vendor.target_produksi_ton || 0} Ton</li>
              </ul>
              <p>Rincian Jasa Pekerjaan: <br/>${vendor.jasa_pekerjaan || 'Sesuai standar operasional yang disepakati.'}</p>
              <br/>
              <p>Surat Penugasan ini berlaku sejak tanggal diterbitkan.</p>
              <br/><br/>
              <p>Hormat kami,</p>
              <p><strong>Manajemen AGRI-PAM</strong></p>
            </body>
          </html>
        `;

        // Generate DOCX
        const fileBuffer = await HTMLtoDOCX(htmlString, null, {
          table: { row: { cantSplit: true } },
          footer: true,
          pageNumber: true,
        });

        // Save locally (for demo purposes)
        const fileName = \`SPK_\${vendor.nama_vendor.replace(/\\s+/g, '_')}_\${Date.now()}.docx\`;
        const docsDir = path.join(__dirname, '..', 'public', 'docs');
        
        // Ensure directory exists
        if (!fs.existsSync(docsDir)){
            fs.mkdirSync(docsDir, { recursive: true });
        }

        const filePath = path.join(docsDir, fileName);
        fs.writeFileSync(filePath, fileBuffer);

        const fileUrl = \`/docs/\${fileName}\`; // Local URL

        // Update database with the link
        const { data: updateData, error: updateErr } = await supabase
          .from('vendor_monitoring')
          .update({ 
            link_surat_spk: fileUrl, 
            status: 'Penerbitan SPK',
            tanggal_update_status: new Date().toISOString().split('T')[0],
            tanggal_penugasan: new Date().toISOString().split('T')[0],
            updated_at: new Date().toISOString()
          })
          .eq('id', vendorId)
          .select()
          .single();

        if (updateErr) throw updateErr;

        return res.json({ 
          success: true, 
          message: 'Surat Penugasan berhasil dibuat', 
          fileUrl: fileUrl,
          data: updateData
        });
      }

      // 2. Create new record
      if (action === 'create') {
        const { record } = req.body;
        // CRO can only create for their own region unless Admin
        if (!isAdmin && record.regional !== region) {
           return res.status(403).json({ success: false, message: 'Cannot create record for another region' });
        }
        
        const { data, error } = await supabase
          .from('vendor_monitoring')
          .insert(record)
          .select()
          .single();

        if (error) throw error;
        return res.json({ success: true, data });
      }

      // 3. Update record
      if (action === 'update') {
        const { id, updates } = req.body;
        updates.updated_at = new Date().toISOString();
        
        const { data, error } = await supabase
          .from('vendor_monitoring')
          .update(updates)
          .eq('id', id)
          .select()
          .single();

        if (error) throw error;
        return res.json({ success: true, data });
      }
    }

    return res.status(405).json({ success: false, message: 'Method not allowed' });
  } catch (error) {
    console.error('API /vendor Error:', error);
    return res.status(500).json({ success: false, message: error.message || 'Internal Server Error' });
  }
};
