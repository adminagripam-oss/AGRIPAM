with open('api/realisasi.js', 'r', encoding='utf-8') as f:
    realisasi = f.read()

# Modify select fields to include tanggal
realisasi = realisasi.replace(
    "select('region, jam, tonase')",
    "select('tanggal, region, jam, tonase')"
)

# Modify allRecords mapping to include tanggal
realisasi = realisasi.replace(
    "const allRecords = allData.map(r => ({ region: r.region, jam: r.jam, tonase: parseFloat(r.tonase) || 0 }));",
    "const allRecords = allData.map(r => ({ tanggal: r.tanggal, region: r.region, jam: r.jam, tonase: parseFloat(r.tonase) || 0 }));"
)

with open('api/realisasi.js', 'w', encoding='utf-8') as f:
    f.write(realisasi)
print("Updated api/realisasi.js")


with open('api/estimasi.js', 'r', encoding='utf-8') as f:
    estimasi = f.read()

# Add allRecords to getEstimasi response when region is ALL
estimasi_old_response = """      return res.json({
        success: true, exists: Object.keys(allEstimasi).length > 0, allEstimasi,
        data: { restanLalu: totalRestanLalu, luasPanen: totalLuasPanen, tkPanen: totalTkPanen, estPanen: totalEstimasiPanen, outPanen: avgOutputPanen, estKirim: totalEstimasiKirim, estRestan: totalEstimasiRestan }
      });"""

estimasi_new_response = """      return res.json({
        success: true, exists: Object.keys(allEstimasi).length > 0, allEstimasi,
        data: { restanLalu: totalRestanLalu, luasPanen: totalLuasPanen, tkPanen: totalTkPanen, estPanen: totalEstimasiPanen, outPanen: avgOutputPanen, estKirim: totalEstimasiKirim, estRestan: totalEstimasiRestan },
        allRecords: allData
      });"""

estimasi = estimasi.replace(estimasi_old_response, estimasi_new_response)

with open('api/estimasi.js', 'w', encoding='utf-8') as f:
    f.write(estimasi)
print("Updated api/estimasi.js")
