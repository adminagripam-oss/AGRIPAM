import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update loadTKPanenDataForSelectedRegion to reset KPI summary badges immediately
old_load_fn = r'function loadTKPanenDataForSelectedRegion\(\) \{.*?\n    \}'

new_load_fn = """function loadTKPanenDataForSelectedRegion() {
      var s = loadSession();
      if (!s) return;

      var regParam = s.region;
      if (s.region === 'ADMIN') {
        var sel = document.getElementById("tkAdminRegionSelect");
        regParam = sel ? sel.value : 'ALL';
      }

      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl) {
        summaryEl.innerHTML = '<div class="col-span-full py-4 text-center text-slate-400 font-semibold animate-pulse">Memuat ringkasan KPI untuk Region ' + regParam + '...</div>';
      }

      var tbody = document.getElementById("tkPanenTableBody");
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="14" class="py-12 text-center text-slate-500 font-semibold animate-pulse">Memuat data kebun untuk Region ' + regParam + '...</td></tr>';
      }

      globalTKData = [];
      globalTKEdits = {};

      fetch('/api/kebunTK?action=getKebun&region=' + encodeURIComponent(regParam) + '&_t=' + Date.now())
        .then(function (res) { return res.json(); })
        .then(function (json) {
          if (json.success) {
            globalTKData = json.data || [];
            globalTKEdits = {};
            renderTKPanenTable(globalTKData, json.summary);
          } else {
            if (tbody) tbody.innerHTML = '<tr><td colspan="14" class="py-12 text-center text-red-500 font-semibold">Gagal memuat data: ' + json.message + '</td></tr>';
            if (summaryEl) summaryEl.innerHTML = '';
          }
        })
        .catch(function (err) {
          console.error(err);
          if (tbody) tbody.innerHTML = '<tr><td colspan="14" class="py-12 text-center text-red-500 font-semibold">Terjadi kesalahan koneksi.</td></tr>';
          if (summaryEl) summaryEl.innerHTML = '';
        });
    }"""

content = re.sub(old_load_fn, new_load_fn, content, flags=re.DOTALL)

# 2. Update prosesLogout to also reset summaryEl
if 'var summaryEl = document.getElementById("tkSummaryBadges");' not in content.split('function prosesLogout()')[1]:
    content = content.replace('if (tbody) tbody.innerHTML = "";', 'if (tbody) tbody.innerHTML = "";\n      var summaryEl = document.getElementById("tkSummaryBadges");\n      if (summaryEl) summaryEl.innerHTML = "";\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY FIXED STUCK / LENGKET KPI DATA IN LOGIN.HTML!")
