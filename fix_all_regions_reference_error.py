file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define ALL_REGIONS array & improve bukaTKPanenSection robustness
all_regions_js = """
    var ALL_REGIONS = [
      'Aceh', 'Sumatera Utara 1', 'Sumatera Utara 2 Ex Torganda', 'Riau 1', 'Riau 2', 'Riau 3', 'Riau 4',
      'Bangka Belitung', 'Jambi', 'Sumatera Barat', 'Sumatera Selatan',
      'Kalimantan Barat 1A', 'Kalimantan Barat 1B', 'Kalimantan Barat 2',
      'Kalimantan Selatan 1', 'Kalimantan Selatan 2', 'Kalimantan Timur', 'Kalimantan Utara',
      'Kalimantan Tengah 1', 'Kalimantan Tengah 2', 'Kalimantan Tengah 3',
      'Sulawesi Tenggara', 'Sulawesi Tengah', 'Papua Selatan'
    ];
"""

if 'var ALL_REGIONS = [' not in content:
    content = content.replace("  <script>", "  <script>\n" + all_regions_js, 1)

# Improve bukaTKPanenSection & populateTKAdminRegionSelect safety
old_buka = r'function bukaTKPanenSection\(\) \{.*?\n    \}'

new_buka = """function bukaTKPanenSection() {
      try {
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
      } catch (err) {
        console.error("Error in bukaTKPanenSection:", err);
      }
    }"""

import re
content = re.sub(old_buka, new_buka, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY FIXED ALL_REGIONS REFERENCE ERROR AND ENHANCED BUKATKPANENSECTION ROBUSTNESS!")
