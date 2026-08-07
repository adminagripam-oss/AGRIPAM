with open('laporan_produksi.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the exact bytes around CRO VI label
idx = html.find("CRO VI")
print("Char at idx-1:", repr(html[idx-1]))
print("Context:", repr(html[idx-5:idx+50]))

# Try to find and replace using what we actually have
import re
m = re.search(r"'CRO VI[^']+Kalbar 1, Kalbar 2'", html)
if m:
    old = m.group(0)
    new = old.replace("Kalbar 1, Kalbar 2", "Kalbar 1A, Kalbar 1B, Kalbar 2")
    html = html.replace(old, new, 1)
    print("Fixed CRO VI label:", old, "->", new)
else:
    print("Pattern not found!")

with open('laporan_produksi.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done.")
