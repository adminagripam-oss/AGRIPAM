import os
import re

filepath = 'laporan_produksi.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Append &_t= to fetch strings that use template literals
content = re.sub(
    r"fetch\((/api/[^]+)\)",
    r"fetch(\1&_t=)",
    content
)

# And for any fetch that concatenates strings or doesn't have it
# actually, let's just do the ones in fetchDashboardData
content = re.sub(
    r"(/api/realisasi\?action=getData&tanggal=\$\{filters\.tanggal\}&tanggal_akhir=\$\{filters\.tanggal_akhir \|\| filters\.tanggal\}&region=ALL)",
    r"/api/realisasi?action=getData&tanggal=&tanggal_akhir=&region=ALL&_t=",
    content
)

content = re.sub(
    r"(/api/estimasi\?action=getEstimasi&tanggal=\$\{filters\.tanggal\}&tanggal_akhir=\$\{filters\.tanggal_akhir \|\| filters\.tanggal\}&region=ALL&token=\$\{token\})",
    r"/api/estimasi?action=getEstimasi&tanggal=&tanggal_akhir=&region=ALL&token=&_t=",
    content
)

content = re.sub(
    r"(/api/realisasi\?action=getData&tanggal=\$\{yesterday\}&region=ALL)",
    r"/api/realisasi?action=getData&tanggal=&region=ALL&_t=",
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {filepath}")
