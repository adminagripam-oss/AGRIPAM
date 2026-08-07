const xlsx = require('xlsx');
const workbook = xlsx.readFile('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/RENCANA & REALISASI PANEN HARIAN.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];

const data = [];
for (let r = 5; r <= 37; r++) {
  const wilayah = sheet['B' + r] ? sheet['B' + r].v : '';
  const luas = sheet['C' + r] ? sheet['C' + r].v : 0;
  const target = sheet['D' + r] ? sheet['D' + r].v : 0;
  data.push({ row: r, wilayah, luas, target });
}
console.log(JSON.stringify(data, null, 2));
