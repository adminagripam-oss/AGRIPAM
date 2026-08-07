const xlsx = require('xlsx');
const workbook = xlsx.readFile('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/RENCANA & REALISASI PANEN HARIAN.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const data = xlsx.utils.sheet_to_json(sheet, { header: 1 });
data.forEach((row, i) => {
  console.log(`Row ${i + 1}:`, JSON.stringify(row));
});
