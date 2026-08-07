import re

def check_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    script_starts = len(re.findall(r'<script', code, re.IGNORECASE))
    script_ends = len(re.findall(r'</script>', code, re.IGNORECASE))
    print(f"{path}: {script_starts} <script> tags, {script_ends} </script> tags")

check_html(r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html')
check_html(r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html')

