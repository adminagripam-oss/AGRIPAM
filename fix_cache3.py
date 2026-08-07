import os

filepath = 'laporan_produksi.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix cache for palmops
old_palmops = r"`/api/palmops?action=get&tanggal=${filters.tanggal}${isRange ? `&tanggal_akhir=${filters.tanggal_akhir}` : ''}`"
new_palmops = r"`/api/palmops?action=get&tanggal=${filters.tanggal}${isRange ? `&tanggal_akhir=${filters.tanggal_akhir}` : ''}&_t=${Date.now()}`"
content = content.replace(old_palmops, new_palmops)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {filepath}")
