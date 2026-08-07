import os
import re

filepath = 'laporan_produksi.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix cache for realisasi
old_realisasi = r"/api/realisasi?action=getData&tanggal=&tanggal_akhir=&region=ALL"
new_realisasi = r"/api/realisasi?action=getData&tanggal=&tanggal_akhir=&region=ALL&_t="
content = content.replace(old_realisasi, new_realisasi)

# Fix cache for estimasi
old_estimasi = r"/api/estimasi?action=getEstimasi&tanggal=&tanggal_akhir=&region=ALL&token="
new_estimasi = r"/api/estimasi?action=getEstimasi&tanggal=&tanggal_akhir=&region=ALL&token=&_t="
content = content.replace(old_estimasi, new_estimasi)

# Fix cache for yesterday
old_kemarin = r"/api/realisasi?action=getData&tanggal=&region=ALL"
new_kemarin = r"/api/realisasi?action=getData&tanggal=&region=ALL&_t="
content = content.replace(old_kemarin, new_kemarin)

# Also fix the one in LaporanProduksiHarian component
old_harian_realisasi = r"/api/realisasi?action=getData&tanggal=&tanggal_akhir=&region=ALL"
new_harian_realisasi = r"/api/realisasi?action=getData&tanggal=&tanggal_akhir=&region=ALL&_t="
content = content.replace(old_harian_realisasi, new_harian_realisasi)

old_harian_estimasi = r"/api/estimasi?action=getEstimasi&tanggal=&tanggal_akhir=&region=ALL&token="
new_harian_estimasi = r"/api/estimasi?action=getEstimasi&tanggal=&tanggal_akhir=&region=ALL&token=&_t="
content = content.replace(old_harian_estimasi, new_harian_estimasi)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {filepath}")
