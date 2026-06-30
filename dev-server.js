const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Middleware to parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Log requests
app.use((req, res, next) => {
  console.log(`[${new Date().toLocaleTimeString()}] ${req.method} ${req.url}`);
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

// Serve static files from root
app.use(express.static(__dirname));

// Fallback for html pages
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

app.listen(port, () => {
  console.log(`============================================================`);
  console.log(`  AGRI-PAM Local Dev Server started at:`);
  console.log(`  http://localhost:${port}`);
  console.log(`============================================================`);
});
