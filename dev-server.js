const dns = require('dns');
dns.setDefaultResultOrder('ipv4first');

const fs = require('fs');
const path = require('path');

// Load environment variables from .env if process.env values are not already set
try {
  const envPath = path.join(__dirname, '.env');
  if (fs.existsSync(envPath)) {
    const envConfig = fs.readFileSync(envPath, 'utf8');
    envConfig.split(/\r?\n/).forEach(line => {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#')) {
        const parts = trimmed.split('=');
        if (parts.length >= 2) {
          const key = parts[0].trim();
          const value = parts.slice(1).join('=').trim();
          // Remove wrapping single or double quotes
          const cleanValue = value.replace(/^['"]|['"]$/g, '');
          if (!process.env[key]) {
            process.env[key] = cleanValue;
          }
        }
      }
    });
  }
} catch (err) {
  console.error("Failed to load .env manually:", err.message);
}

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON and URL-encoded bodies
app.use(express.json({ limit: '100mb' }));
app.use(express.urlencoded({ limit: '100mb', extended: true }));

// Log requests
app.use((req, res, next) => {
  console.log(`[${new Date().toLocaleTimeString()}] ${req.method} ${req.url}`);
  next();
});

// =========================================================================
// ANTI-CACHE MIDDLEWARE — mencegah browser cache halaman yang diproteksi
// =========================================================================
// Middleware ini diterapkan pada semua request file .html agar browser
// tidak menyimpan cache halaman setelah logout. Tanpa ini, tombol Back
// browser masih bisa menampilkan halaman dashboard dari cache.
// =========================================================================
function noCacheHeaders(req, res, next) {
  res.set({
    'Cache-Control': 'no-cache, private, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '-1'
  });
  next();
}

// Terapkan anti-cache ke semua request file .html
app.use((req, res, next) => {
  // Match .html files or clean URLs (no extension, no dot in last segment)
  const urlPath = req.path;
  if (urlPath.endsWith('.html') || 
      urlPath === '/' || 
      (!urlPath.includes('.') && urlPath !== '/api')) {
    return noCacheHeaders(req, res, next);
  }
  next();
});

// Serve API routes
app.all('/api/:route', async (req, res) => {
  const route = req.params.route;
  const handlerPath = path.join(__dirname, 'api', `${route}.js`);
  if (!fs.existsSync(handlerPath)) {
    return res.status(404).json({ success: false, message: `API route /api/${route} not found` });
  }
  try {
    try {
      delete require.cache[require.resolve(handlerPath)];
    } catch (_) {}
    
    const handler = require(handlerPath);
    await handler(req, res);
  } catch (err) {
    console.error(`Error handling API route /api/${route}:`, err);
    if (!res.headersSent) {
      res.status(500).json({ success: false, message: `Server error: ${err.message}` });
    }
  }
});

// Page routes & clean URLs
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

app.get('/laporan-produksi', (req, res) => {
  res.sendFile(path.join(__dirname, 'laporan_produksi.html'));
});

// Clean URL routes for TKPanen router
app.get('/login.html/TKPanen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/TKPanen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/tk-panen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});


// Serve static files from root with .html auto-extension
app.use(express.static(__dirname, { extensions: ['html'] }));


process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

app.listen(port, () => {
  console.log(`============================================================`);
  console.log(`  AGRI-PAM Local Dev Server started at:`);
  console.log(`  http://localhost:3000`);
  console.log(`============================================================`);
});

