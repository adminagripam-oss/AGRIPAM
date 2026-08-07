const fs = require('fs');
const path = require('path');
const logoPath = path.join(__dirname, '..', 'AGRINAS DANANTARA.png');
if (fs.existsSync(logoPath)) {
  const base64 = fs.readFileSync(logoPath).toString('base64');
  console.log('data:image/png;base64,' + base64.substring(0, 100) + '...');
  fs.writeFileSync(path.join(__dirname, 'logo_base64.txt'), 'data:image/png;base64,' + base64);
} else {
  console.log('Logo file not found');
}
