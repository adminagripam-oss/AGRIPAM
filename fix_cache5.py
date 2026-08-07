import re

with open('laporan_produksi.html', 'r', encoding='utf-8') as f:
    html = f.read()

def replacer(match):
    url = match.group(1)
    if '_t=' in url:
        return match.group(0)
    
    if '?' in url:
        new_url = url + r'&_t=${Date.now()}'
    else:
        new_url = url + r'?_t=${Date.now()}'
    return f"fetch(`{new_url}`"

html = re.sub(r'fetch\(`([^`]+)`', replacer, html)

with open('laporan_produksi.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated fetch calls with cache buster")
