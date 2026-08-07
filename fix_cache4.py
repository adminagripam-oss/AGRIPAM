import re

with open('laporan_produksi.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any fetch(/api/...) with fetch(/api/...&_t=\)
# but avoid double appending
def replacer(match):
    url = match.group(1)
    if '_t=' in url:
        return match.group(0)
    
    if '?' in url:
        new_url = url + r'&_t='
    else:
        new_url = url + r'?_t='
    return f"fetch({new_url}"

# Match fetch(...
html = re.sub(r'fetch\(([^]+)', replacer, html)

with open('laporan_produksi.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated fetch calls with cache buster")
