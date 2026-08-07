const xlsx = require('xlsx');

function inspectExcel(filename) {
  console.log('=== Inspecting file:', filename, '===');
  const workbook = xlsx.readFile(filename);
  const sheetNames = workbook.SheetNames;
  console.log('Sheets:', sheetNames);
  
  const firstSheetName = sheetNames[0];
  const worksheet = workbook.Sheets[firstSheetName];
  
  // Read first 15 rows
  const rows = xlsx.utils.sheet_to_json(worksheet, { header: 1 });
  console.log('First 15 rows:');
  rows.slice(0, 15).forEach((row, i) => {
    console.log(`Row ${i + 1}:`, row);
  });
}

inspectExcel('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/RENCANA & REALISASI PANEN HARIAN.xlsx');
console.log('\n');
inspectExcel('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/Export_LHP_2026-07-18.xlsx');
