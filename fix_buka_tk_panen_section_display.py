import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update bukaTKPanenSection to ensure mainSection is display: flex and infografisSection is display: none
old_buka = r'function bukaTKPanenSection\(\) \{.*?\n    \}'

new_buka = """function bukaTKPanenSection() {
      try {
        var s = loadSession();
        if (!s) {
          alert("Sesi tidak valid, silakan login ulang.");
          prosesLogout();
          return;
        }

        // 1. Ensure mainSection is visible and body has dashboard-active
        var mainSection = document.getElementById("mainSection");
        if (mainSection) mainSection.style.display = "flex";
        document.body.classList.add("dashboard-active");

        // 2. Hide all other full-screen/modal sections (infografis, sap, estimasi)
        var infografisSec = document.getElementById("infografisSection");
        var sapSec = document.getElementById("sapSection");
        var estSec = document.getElementById("estimasiSection");
        if (infografisSec) infografisSec.style.display = "none";
        if (sapSec) sapSec.style.display = "none";
        if (estSec) estSec.style.display = "none";

        // 3. Switch main content: hide dashboard monitoring grid, show TK Panen content
        var mainGrid = document.getElementById("dashboardMainGrid");
        var tkContent = document.getElementById("tkPanenMainContent");
        if (mainGrid) mainGrid.style.display = "none";
        if (tkContent) {
          tkContent.style.display = "block";
          tkContent.classList.remove("hidden");
        }

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

# Update tutupTKPanenSection to restore mainSection cleanly
old_tutup = r'function tutupTKPanenSection\(\) \{.*?\n    \}'

new_tutup = """function tutupTKPanenSection() {
      var tkContent = document.getElementById("tkPanenMainContent");
      var mainGrid = document.getElementById("dashboardMainGrid");
      var mainSection = document.getElementById("mainSection");
      var infografisSec = document.getElementById("infografisSection");
      var sapSec = document.getElementById("sapSection");
      var estSec = document.getElementById("estimasiSection");

      if (infografisSec) infografisSec.style.display = "none";
      if (sapSec) sapSec.style.display = "none";
      if (estSec) estSec.style.display = "none";
      if (mainSection) mainSection.style.display = "flex";
      document.body.classList.add("dashboard-active");

      if (tkContent) tkContent.style.display = "none";
      if (mainGrid) mainGrid.style.display = "block";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }"""

content = re.sub(old_buka, new_buka, content, flags=re.DOTALL)
content = re.sub(old_tutup, new_tutup, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY FIXED BUKATKPANENSECTION & TUTUPTKPANENSECTION DISPLAY SWITCHING!")
