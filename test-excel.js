const XLSX = require('xlsx');
const workbook = XLSX.readFile('Export_LHP_2026-07-13 (1).xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '', blankrows: true });

console.log('Row 14 (Aceh):');
console.log(rows[14]);
console.log('Row 38 (Sumut 1):');
console.log(rows[38]);
