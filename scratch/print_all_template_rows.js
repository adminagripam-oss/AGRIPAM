const XLSX = require('xlsx');
const workbook = XLSX.readFile('RENCANA & REALISASI PANEN HARIAN.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });
data.forEach((row, idx) => {
  console.log(`Row ${idx + 1}:`, row);
});
