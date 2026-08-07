file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update loadTKPanenDataForSelectedRegion to clear global state & display loading for the EXACT region
old_load_fn = r'function loadTKPanenDataForSelectedRegion\(\) \{.*?\n    \}'

new_load_fn = """function loadTKPanenDataForSelectedRegion() {
      var s = loadSession();
      if (!s) return;

      var regParam = s.region;
      if (s.region === 'ADMIN') {
        var sel = document.getElementById("tkAdminRegionSelect");
        regParam = sel ? sel.value : 'ALL';
      }

      var tbody = document.getElementById("tkPanenTableBody");
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-slate-500 font-semibold animate-pulse">Memuat data kebun untuk Region ' + regParam + '...</td></tr>';
      }

      globalTKData = [];
      globalTKEdits = {};

      fetch('/api/kebunTK?action=getKebun&region=' + encodeURIComponent(regParam) + '&_t=' + Date.now())
        .then(function(res) { return res.json(); })
        .then(function(json) {
          if (json.success) {
            globalTKData = json.data || [];
            globalTKEdits = {};
            renderTKPanenTable(globalTKData, json.summary);
          } else {
            if (tbody) tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-red-500 font-semibold">Gagal memuat data: ' + json.message + '</td></tr>';
          }
        })
        .catch(function(err) {
          console.error(err);
          if (tbody) tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-red-500 font-semibold">Terjadi kesalahan koneksi.</td></tr>';
        });
    }"""

import re
content = re.sub(old_load_fn, new_load_fn, content, flags=re.DOTALL)

# Add session clearing in prosesLogout
if 'globalTKData = [];' not in content.split('function prosesLogout()')[1]:
    content = content.replace('function prosesLogout() {', 'function prosesLogout() {\n      globalTKData = [];\n      globalTKEdits = {};\n      var tbody = document.getElementById("tkPanenTableBody");\n      if (tbody) tbody.innerHTML = "";\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY UPDATED LOGIN.HTML SESSION SWITCHING FOR TK PANEN DATA!")
