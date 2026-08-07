with open('laporan_produksi.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Label CRO VI di filter dropdown
old1 = "'CRO VI  - Kalbar 1, Kalbar 2': ['Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2'],"
new1 = "'CRO VI  - Kalbar 1A, Kalbar 1B, Kalbar 2': ['Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2'],"

# Fix 2: Subtotal CRO VI children di tabel SAP
old2 = '{ label: "CRO VI", type: "subtotal", children: ["Kalbar 1 Ex Duta Palma", "Kalimantan Barat 2"] },'
new2 = '{ label: "CRO VI", type: "subtotal", children: ["Kalimantan Barat 1A", "Kalimantan Barat 1B", "Kalimantan Barat 2"] },'

if old1 in html:
    html = html.replace(old1, new1, 1)
    print("Fix 1 applied: CRO VI label updated")
else:
    print("Fix 1 NOT FOUND - checking existing label...")
    import re
    m = re.search(r"'CRO VI[^']*':\s*\[", html)
    if m: print("Found:", m.group(0))

if old2 in html:
    html = html.replace(old2, new2, 1)
    print("Fix 2 applied: CRO VI subtotal children updated")
else:
    print("Fix 2 NOT FOUND - checking existing...")
    import re
    m = re.search(r'label: "CRO VI"[^}]+}', html)
    if m: print("Found:", m.group(0))

with open('laporan_produksi.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done.")
