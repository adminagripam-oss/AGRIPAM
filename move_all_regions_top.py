file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace line 4706 var ALL_REGIONS with top-level declaration at line 1845
all_regions_def = """    var ALL_REGIONS = [
      'Aceh', 'Sumatera Utara 1', 'Sumatera Utara 2 Ex Torganda', 'Riau 1', 'Riau 2', 'Riau 3', 'Riau 4',
      'Bangka Belitung', 'Jambi', 'Sumatera Barat', 'Sumatera Selatan',
      'Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2',
      'Kalimantan Selatan 1', 'Kalimantan Selatan 2', 'Kalimantan Timur', 'Kalimantan Utara',
      'Kalimantan Tengah 1', 'Kalimantan Tengah 2', 'Kalimantan Tengah 3',
      'Sulawesi Tenggara', 'Sulawesi Tengah', 'Papua Selatan'
    ];
"""

content = content.replace("    var ALL_REGIONS = [", "    // ALL_REGIONS defined at top\n    // var ALL_REGIONS = [")
content = content.replace("var globalTKData = [];", all_regions_def + "\n    var globalTKData = [];")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY MOVED ALL_REGIONS TO TOP OF SCRIPT IN LOGIN.HTML!")
