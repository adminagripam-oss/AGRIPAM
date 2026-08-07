import re

# 1. Update dev-server.js to support /login.html/TKPanen and /TKPanen routes
dev_server_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\dev-server.js'

with open(dev_server_path, 'r', encoding='utf-8') as f:
    dev_code = f.read()

route_injection = """// Clean URL routes for TKPanen router
app.get('/login.html/TKPanen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/TKPanen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/tk-panen', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});
"""

if "app.get('/login.html/TKPanen'" not in dev_code:
    dev_code = dev_code.replace("app.get('/laporan-produksi', (req, res) => {\n  res.sendFile(path.join(__dirname, 'laporan_produksi.html'));\n});", "app.get('/laporan-produksi', (req, res) => {\n  res.sendFile(path.join(__dirname, 'laporan_produksi.html'));\n});\n\n" + route_injection)
    with open(dev_server_path, 'w', encoding='utf-8') as f:
        f.write(dev_code)
    print("Updated dev-server.js with clean routes /login.html/TKPanen and /TKPanen")


# 2. Update login.html JavaScript router for clean pathname /login.html/TKPanen
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Update bukaTKPanenSection and tutupTKPanenSection
old_router_js = r'function bukaTKPanenSection\(\) \{.*?\n    \}'

new_router_js = """function bukaTKPanenSection() {
      var s = loadSession();
      if (!s) {
        alert("Sesi tidak valid, silakan login ulang.");
        prosesLogout();
        return;
      }

      if (window.history.pushState) {
        window.history.pushState(null, '', '/login.html/TKPanen');
      }

      var mainGrid = document.getElementById("dashboardMainGrid");
      var tkContent = document.getElementById("tkPanenMainContent");
      var sapSec = document.getElementById("sapSection");
      var estSec = document.getElementById("estimasiSection");

      if (mainGrid) mainGrid.style.display = "none";
      if (sapSec) sapSec.style.display = "none";
      if (estSec) estSec.style.display = "none";
      if (tkContent) tkContent.style.display = "block";

      if (typeof setActiveSidebar === 'function') setActiveSidebar(3);

      var adminContainer = document.getElementById("tkAdminRegionContainer");
      if (s.region === 'ADMIN') {
        if (adminContainer) adminContainer.style.display = "flex";
        populateTKAdminRegionSelect();
      } else {
        if (adminContainer) adminContainer.style.display = "none";
      }

      loadTKPanenDataForSelectedRegion();
    }

    function tutupTKPanenSection() {
      if (window.history.pushState) {
        window.history.pushState(null, '', '/login.html');
      }
      var tkContent = document.getElementById("tkPanenMainContent");
      var mainGrid = document.getElementById("dashboardMainGrid");
      if (tkContent) tkContent.style.display = "none";
      if (mainGrid) mainGrid.style.display = "block";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }"""

login_code = re.sub(r'function bukaTKPanenSection\(\) \{.*?\n    \}', new_router_js, login_code, flags=re.DOTALL)

# Add listener for popstate & initial URL check on page load
popstate_js = """
    // Route detector for /login.html/TKPanen or /TKPanen on load and popstate
    function checkCurrentRoute() {
      var path = window.location.pathname || '';
      var hash = window.location.hash || '';
      if (path.includes('TKPanen') || path.includes('tk-panen') || hash === '#TKPanen') {
        bukaTKPanenSection();
      }
    }

    window.addEventListener('popstate', checkCurrentRoute);
    window.addEventListener('load', checkCurrentRoute);
"""

if "function checkCurrentRoute()" not in login_code:
    login_code = login_code.replace("</script>", popstate_js + "\n</script>", 1)

# Also check route when login is successful in prosesLogin / loadDashboard
if "checkCurrentRoute();" not in login_code:
    login_code = login_code.replace("applyUserRoleUI();", "applyUserRoleUI();\n        checkCurrentRoute();")

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html with clean pathname router /login.html/TKPanen")
