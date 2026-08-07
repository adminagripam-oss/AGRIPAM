import re

# 1. Clean up login.html
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Fix iframe relative paths to root absolute paths
login_code = login_code.replace("sapIframe.src = 'sap_admin.html'", "sapIframe.src = '/sap_admin.html'")
login_code = login_code.replace("sapIframe.src = 'sap_regional.html'", "sapIframe.src = '/sap_regional.html'")
login_code = login_code.replace("sapIframe.src = 'sap_admin.html' + params;", "sapIframe.src = '/sap_admin.html' + params;")
login_code = login_code.replace("sapIframe.src = 'sap_regional.html' + params;", "sapIframe.src = '/sap_regional.html' + params;")
login_code = login_code.replace("iframe.src = 'FORMAT_ESTIMASI_PANEN.html", "iframe.src = '/FORMAT_ESTIMASI_PANEN.html")

# Remove window.checkCurrentRoute and popstate/load listeners
login_code = re.sub(r'\s*// Global Route detector for /login\.html/TKPanen or /TKPanen\s*window\.checkCurrentRoute = function\(\) \{.*?\n    \};\s*window\.addEventListener\(\'popstate\'.*?\n\s*window\.addEventListener\(\'load\'.*?\n', '\n', login_code, flags=re.DOTALL)
login_code = login_code.replace('checkCurrentRoute();\n', '')
login_code = login_code.replace('checkCurrentRoute();', '')

# Revert bukaTKPanenSection and tutupTKPanenSection to pure element toggles without pushState
clean_buka_tk = """function bukaTKPanenSection() {
      var s = loadSession();
      if (!s) {
        alert("Sesi tidak valid, silakan login ulang.");
        prosesLogout();
        return;
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
      var tkContent = document.getElementById("tkPanenMainContent");
      var mainGrid = document.getElementById("dashboardMainGrid");
      if (tkContent) tkContent.style.display = "none";
      if (mainGrid) mainGrid.style.display = "block";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }"""

login_code = re.sub(r'function bukaTKPanenSection\(\) \{.*?\n    \}', clean_buka_tk, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Successfully reverted router & fixed iframe paths in login.html!")
