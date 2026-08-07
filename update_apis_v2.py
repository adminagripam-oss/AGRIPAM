with open('api/realisasi.js', 'r', encoding='utf-8') as f:
    real = f.read()

real = real.replace(
    "if (!region || region.toUpperCase() === 'ALL') {",
    "if (!region || region.toUpperCase() === 'ALL' || tanggal_akhir) {"
)

with open('api/realisasi.js', 'w', encoding='utf-8') as f:
    f.write(real)
print("Updated api/realisasi.js to support range queries for specific regions")


with open('api/estimasi.js', 'r', encoding='utf-8') as f:
    est = f.read()

est = est.replace(
    "if (!region || region.toUpperCase() === 'ALL') {",
    "if (!region || region.toUpperCase() === 'ALL' || tanggal_akhir) {"
)

with open('api/estimasi.js', 'w', encoding='utf-8') as f:
    f.write(est)
print("Updated api/estimasi.js to support range queries for specific regions")
