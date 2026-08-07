const xlsx = require('xlsx');
const workbook = xlsx.readFile('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/RENCANA & REALISASI PANEN HARIAN.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];

console.log('B2 cell:', sheet['B2']);
console.log('A2 cell:', sheet['A2']);
console.log('C2 cell:', sheet['C2']);
