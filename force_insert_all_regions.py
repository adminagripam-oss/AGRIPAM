file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

all_regions_code = """    var ALL_REGIONS = [
      'Aceh', 'Sumatera Utara 1', 'Sumatera Utara 2 Ex Torganda', 'Riau 1', 'Riau 2', 'Riau 3', 'Riau 4',
      'Bangka Belitung', 'Jambi', 'Sumatera Barat', 'Sumatera Selatan',
      'Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2',
      'Kalimantan Selatan 1', 'Kalimantan Selatan 2', 'Kalimantan Timur', 'Kalimantan Utara',
      'Kalimantan Tengah 1', 'Kalimantan Tengah 2', 'Kalimantan Tengah 3',
      'Sulawesi Tenggara', 'Sulawesi Tengah', 'Papua Selatan'
    ];
"""

if 'var ALL_REGIONS = [' not in content:
    content = content.replace('function bukaTKPanenSection() {', all_regions_code + '\n    function bukaTKPanenSection() {')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Force inserted ALL_REGIONS code!")
else:
    print("ALL_REGIONS already in file.")

