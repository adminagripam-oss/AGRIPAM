const xlsx = require('xlsx');
const workbook = xlsx.readFile('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/RENCANA & REALISASI PANEN HARIAN.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];

// Print cells in row 5 with their formulas
const cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'];
cols.forEach(col => {
  const cell = sheet[col + '5'];
  console.log(`${col}5:`, cell);
});
