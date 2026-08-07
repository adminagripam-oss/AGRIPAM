import os
import re

filepath = 'laporan_produksi.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: { label: "Kalbar 1 Ex Duta Palma", regionKey: "Kalimantan Barat 1A", "Kalimantan Barat 1B", excelKey: "Kalbar 1", luas: 77955.99, target: 1750, type: "detail" },
content = re.sub(
    r'\{\s*label:\s*"Kalbar 1 Ex Duta Palma",\s*regionKey:\s*"Kalimantan Barat 1A",\s*"Kalimantan Barat 1B",\s*excelKey:\s*"Kalbar 1",\s*luas:\s*77955\.99,\s*target:\s*1750,\s*type:\s*"detail"\s*\},',
    r'{ label: "Kalbar 1A Ex Duta Palma", regionKey: "Kalimantan Barat 1A", excelKey: "Kalbar 1A", luas: 38978, target: 875, type: "detail" }, { label: "Kalbar 1B", regionKey: "Kalimantan Barat 1B", excelKey: "Kalbar 1B", luas: 38978, target: 875, type: "detail" },',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {filepath}")
