import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix single quotes on lines 1981 and 1986
broken_juli = "onchange=\"onTKInputChange(' + item.id + ', 'tk_juli', this.value)\""
fixed_juli = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_juli\\', this.value)\""

broken_ags = "onchange=\"onTKInputChange(' + item.id + ', 'tk_agustus', this.value)\""
fixed_ags = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_agustus\\', this.value)\""

content = content.replace(broken_juli, fixed_juli)
content = content.replace(broken_ags, fixed_ags)

# 2. Remove orphaned array lines near line 4706-4739
pattern_orphaned = r'// ALL_REGIONS defined at top\s*// var ALL_REGIONS = \[\s*"Aceh",\s*"Sumatera Utara 1",\s*"Sumatera Utara 2 Ex Torganda",\s*"Riau 1",\s*"Riau 2",\s*"Riau 3",\s*"Riau 4",\s*"Bangka Belitung",\s*"Jambi",\s*"Sumatera Barat",\s*"Sumatera Selatan",\s*"Kalimantan Barat 1A",\s*"Kalimantan Barat 1B",\s*"Kalimantan Barat 2",\s*"Kalimantan Selatan 1",\s*"Kalimantan Selatan 2",\s*"Kalimantan Timur",\s*"Kalimantan Utara",\s*"Kalimantan Tengah 1",\s*"Kalimantan Tengah 2",\s*"Kalimantan Tengah 3",\s*"Sulawesi Tenggara",\s*"Sulawesi Tengah"\s*\];'

content = re.sub(pattern_orphaned, '// ALL_REGIONS defined at top script section', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY FIXED ALL SYNTAX ERRORS IN LOGIN.HTML!")
