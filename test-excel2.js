const XLSX = require('xlsx');
const workbook = XLSX.readFile('Export_LHP_2026-07-13 (1).xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '', blankrows: true });

for(let i=10; i<=20; i++) {
    console.log('Row ' + (i+1) + ': ' + rows[i].slice(0, 10).join(' | '));
}
