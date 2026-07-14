const dns = require('dns');
dns.setDefaultResultOrder('ipv4first');

const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON and URL-encoded bodies
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ limit: '10mb', extended: true }));

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
  try {
    const handlerPath = path.join(__dirname, 'api', `${route}.js`);
    // Clear require cache for development to pick up api changes instantly
    try {
      delete require.cache[require.resolve(handlerPath)];
    } catch (_) {}
    
    const handler = require(handlerPath);
    await handler(req, res);
  } catch (err) {
    console.error(`Error handling API route /api/${route}:`, err);
    res.status(500).json({ success: false, message: `Server error: ${err.message}` });
  }
});

// Serve static files from root (images, CSS, JS assets — cached normally)
app.use(express.static(__dirname));

// Fallback for html pages (anti-cache headers sudah diterapkan oleh middleware di atas)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

app.get('/laporan-produksi', (req, res) => {
  res.sendFile(path.join(__dirname, 'laporan_produksi.html'));
});


app.listen(port, () => {
  console.log(`============================================================`);
  console.log(`  AGRI-PAM Local Dev Server started at:`);
  console.log(`  http://localhost:${port}`);
  console.log(`============================================================`);
});

