const { supabase } = require('./lib/supabase');
const { verifyToken } = require('./lib/auth');
const { applyCors } = require('./lib/cors');
const HTMLtoDOCX = require('html-to-docx');

module.exports = async (req, res) => {
  applyCors(req, res);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const p = req.method === 'POST' ? req.body : req.query;
  const action = (p.action || '').trim();
  const region = (p.region || '').trim();
  const token = (p.token || '').trim();

  if (!region || !token) {
    return res.json({ success: false, message: 'Autentikasi gagal.' });
  }

  const check = await verifyToken(token, region);
  if (!check.valid) {
    return res.json({ success: false, message: check.message });
  }

  if (action === 'getSurat') {
    let query = supabase.from('surat').select('*').order('created_at', { ascending: false });
    if (region !== 'ADMIN') query = query.eq('regional_pengirim', region);

    const { data, error } = await query;
    if (error) return res.json({ success: false, message: error.message });

    return res.json({ success: true, data: data });
  }

  if (action === 'insertSurat') {
    const nomor_surat = p.nomor_surat;
    const jenis_surat = p.jenis_surat;
    const asal_surat = p.asal_surat || null;
    const perihal = p.perihal;
    const tanggal_surat = p.tanggal_surat || null;
    const tujuan = p.tujuan || null;
    const link_redirect = p.link_redirect || null;

    let file_url = p.file_url;
    if (p.fileData && p.fileName) {
      try {
        const buffer = Buffer.from(p.fileData, 'base64');

        // Validasi ukuran berkas di backend (Maksimal 50 MB)
        if (buffer.length > 50 * 1024 * 1024) {
          return res.json({ success: false, message: 'Gagal: Ukuran file melebihi batas maksimal 50 MB.' });
        }

        const { data: uploadData, error: uploadError } = await supabase.storage
          .from('berkas_surat')
          .upload(p.fileName, buffer, {
            contentType: p.mimeType || 'application/pdf',
            upsert: true
          });

        if (uploadError) return res.json({ success: false, message: 'Gagal upload file: ' + uploadError.message });

        const { data: { publicUrl } } = supabase.storage.from('berkas_surat').getPublicUrl(p.fileName);
        file_url = publicUrl;
      } catch (e) {
        return res.json({ success: false, message: 'Error memproses file: ' + e.message });
      }
    }

    const payload = {
      nomor_surat, jenis_surat, perihal, file_url, regional_pengirim: asal_surat || region, status: 'menunggu', tanggal_surat: tanggal_surat, tujuan: tujuan
    };

    if (asal_surat) {
      payload.asal_surat = asal_surat;
    }
    
    if (link_redirect) {
      payload.link_redirect = link_redirect;
    }

    const { error } = await supabase.from('surat').insert(payload);

    if (error) return res.json({ success: false, message: error.message });

    return res.json({ success: true, message: 'Surat berhasil disimpan.' });
  }

  if (action === 'updateSurat') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Hanya Admin yang dapat mengupdate status surat.' });

    const surat_id = p.surat_id;
    const status = p.status;
    const catatan = p.catatan || '';
    const tujuan = p.tujuan || null;
    const tanggal_surat = p.tanggal_surat || null;

    const updateData = { status: status };
    if (tujuan) updateData.tujuan = tujuan;
    if (catatan) updateData.catatan = catatan; // Tambahkan catatan ke tabel surat
    if (tanggal_surat !== null) updateData.tanggal_surat = tanggal_surat;

    let updateError;
    // Coba update semua field yang ada
    const { error: err1 } = await supabase.from('surat').update(updateData).eq('id', surat_id);
    if (err1 && (err1.code === 'PGRST204' || err1.code === '42703' || err1.message.includes('column'))) {
      // Jika kolom (seperti tujuan/catatan) tidak ada, fallback update hanya status
      const { error: err2 } = await supabase.from('surat').update({ status: status }).eq('id', surat_id);
      updateError = err2;
    } else {
      updateError = err1;
    }

    if (updateError) return res.json({ success: false, message: updateError.message });

    const { error: logError } = await supabase.from('log_tracking').insert({
      surat_id: surat_id, status_update: status, catatan: catatan
    });

    if (logError) return res.json({ success: false, message: logError.message });

    const fileData = p.fileData;
    const fileName = p.fileName;
    const mimeType = p.mimeType;

    let balasanMsg = '';

    if (fileData && fileName && mimeType) {
      try {
        const uniqueFileName = `${Date.now()}_${fileName.replace(/\\s+/g, '_')}`;
        const buffer = Buffer.from(fileData, 'base64');
        
        const { error: uploadError } = await supabase
          .storage
          .from('surat_files')
          .upload(`uploads/${uniqueFileName}`, buffer, {
            contentType: mimeType,
            upsert: false
          });
          
        if (uploadError) throw new Error('Gagal mengupload file balasan: ' + uploadError.message);

        const { data: publicUrlData } = supabase.storage.from('surat_files').getPublicUrl(`uploads/${uniqueFileName}`);
        const fileUrl = publicUrlData.publicUrl;

        const { data: origData } = await supabase.from('surat').select('*').eq('id', surat_id).single();
        
        if (origData) {
            const newSurat = {
                jenis_surat: 'Surat Balasan',
                nomor_surat: 'BALASAN-' + (origData.nomor_surat || surat_id),
                perihal: 'Balasan: ' + (origData.perihal || '-'),
                asal_surat: origData.tujuan || region,
                tujuan: origData.asal_surat || origData.regional_pengirim || '-',
                tanggal_surat: new Date().toISOString().split('T')[0],
                file_url: fileUrl,
                regional_pengirim: region,
                status: 'menunggu'
            };
            const { error: insertError } = await supabase.from('surat').insert([newSurat]);
            if (insertError) throw new Error('Gagal membuat Surat Balasan: ' + insertError.message);
            
            balasanMsg = ' dan Surat Balasan berhasil dibuat';
        }
      } catch (err) {
        balasanMsg = ` (namun terjadi kesalahan pada Surat Balasan: ${err.message})`;
      }
    }

    if (err1 && (err1.code === 'PGRST204' || err1.code === '42703' || err1.message.includes('column'))) {
      return res.json({
        success: true,
        message: 'Status diupdate' + balasanMsg + ', TAPI Tujuan/Catatan gagal disimpan! Anda wajib menambahkan kolom "tujuan" dan "catatan" di tabel surat.'
      });
    }

    return res.json({ success: true, message: 'Data surat berhasil diupdate sepenuhnya' + balasanMsg + '.' });
  }

  if (action === 'saveSuratDocx') {
    const surat_id = p.surat_id;
    const htmlContent = p.htmlContent;

    if (!surat_id || typeof htmlContent !== 'string') {
      return res.json({ success: false, message: 'Data tidak lengkap untuk menyimpan dokumen.' });
    }

    try {
      const docxBuffer = await HTMLtoDOCX(htmlContent, null, {
        table: { row: { cantSplit: true } },
      });

      const fileName = `${surat_id}_edited_${Date.now()}.docx`;
      const { error: uploadError } = await supabase.storage
        .from('berkas_surat')
        .upload(fileName, docxBuffer, {
          contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          upsert: true
        });

      if (uploadError) return res.json({ success: false, message: 'Gagal upload dokumen: ' + uploadError.message });

      const { data: { publicUrl } } = supabase.storage.from('berkas_surat').getPublicUrl(fileName);

      const { error: updateError } = await supabase.from('surat').update({ file_url: publicUrl }).eq('id', surat_id);
      if (updateError) return res.json({ success: false, message: updateError.message });

      return res.json({ success: true, message: 'Dokumen berhasil disimpan.', file_url: publicUrl });
    } catch (e) {
      return res.json({ success: false, message: 'Gagal memproses dokumen: ' + e.message });
    }
  }

  if (action === 'deleteSurat') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Hanya Admin yang dapat menghapus surat.' });

    const surat_id = p.surat_id;
    if (!surat_id) return res.json({ success: false, message: 'ID surat tidak valid.' });

    const { error } = await supabase.from('surat').delete().eq('id', surat_id);
    if (error) return res.json({ success: false, message: 'Gagal menghapus surat: ' + error.message });

    return res.json({ success: true, message: 'Surat berhasil dihapus.' });
  }
  if (action === 'deleteSuratMultiple') {
    if (region !== 'ADMIN') return res.json({ success: false, message: 'Hanya Admin yang dapat menghapus surat.' });

    const surat_ids = p.surat_ids;
    if (!surat_ids || !Array.isArray(surat_ids) || surat_ids.length === 0) {
        return res.json({ success: false, message: 'ID surat tidak valid.' });
    }

    const { error } = await supabase.from('surat').delete().in('id', surat_ids);
    if (error) return res.json({ success: false, message: 'Gagal menghapus surat: ' + error.message });

    return res.json({ success: true, message: 'Surat berhasil dihapus.' });
  }

  return res.json({ success: false, message: 'Action tidak dikenal.' });
};

