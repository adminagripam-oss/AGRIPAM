import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove old #tkPanenSection modal overlay at bottom
content = re.sub(r'<!-- =+\s*TK PANEN SECTION MODAL =+ -->\s*<div id="tkPanenSection".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Wrap main content inside <main> with #dashboardMainGrid and add #tkPanenMainContent
main_start_tag = '<main class="flex-1 overflow-y-auto p-6 space-y-6">'

# We find where main content ends before </main>
main_end_tag = '</main>\n    </div>\n  </div>'

tk_embedded_html = """
          <!-- ===================== TK PANEN EMBEDDED ROUTER CONTENT ===================== -->
          <div id="tkPanenMainContent" style="display:none;" class="space-y-6">
            
            <!-- Top Card Header & Action Bar -->
            <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div class="flex items-center gap-3">
                  <div class="p-2.5 bg-emerald-500/10 text-emerald-600 rounded-xl">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                  </div>
                  <div>
                    <h2 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">Fitur Pengisian TK Panen</h2>
                    <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Monitoring & Realisasi Tenaga Kerja Panen Kebun (Kolom I Juli & Kolom J Agustus)</p>
                  </div>
                </div>
              </div>

              <div class="flex items-center gap-3">
                <button id="btnSaveTKPanen" onclick="simpanTKPanenEdits()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 active:scale-95 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-600/20 transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
                  <span>Simpan Data TK Panen</span>
                </button>
              </div>
            </div>

            <!-- Summary Badges Bar -->
            <div id="tkSummaryBadges" class="flex flex-wrap items-center gap-3 text-xs font-semibold"></div>

            <!-- Search & Regional Filter Row -->
            <div class="bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4 shadow-sm">
              <div id="tkAdminRegionContainer" style="display:none;" class="flex items-center gap-2">
                <span class="text-xs font-semibold text-slate-500">Filter Regional:</span>
                <select id="tkAdminRegionSelect" onchange="loadTKPanenDataForSelectedRegion()" class="px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200">
                  <option value="ALL">Semua Regional (23 Region)</option>
                </select>
              </div>

              <div class="flex-1 max-w-md relative">
                <input type="text" id="tkSearchInput" onkeyup="filterTKPanenTable()" placeholder="Cari kebun, tag kebun, atau regional..." class="w-full pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500" />
                <svg class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              </div>
            </div>

            <!-- Kebun Table -->
            <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-100 dark:border-slate-800 overflow-hidden shadow-sm">
              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse" id="tkPanenTable">
                  <thead>
                    <tr class="bg-slate-50 dark:bg-slate-800/80 text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider border-b border-slate-100 dark:border-slate-800">
                      <th class="py-3.5 px-3 text-center w-12">No</th>
                      <th class="py-3.5 px-3">CRO</th>
                      <th class="py-3.5 px-3">Regional</th>
                      <th class="py-3.5 px-4 min-w-[200px]">Nama Kebun / PT</th>
                      <th class="py-3.5 px-3">Tag Kebun</th>
                      <th class="py-3.5 px-3 text-right">Luas (Ha)</th>
                      <th class="py-3.5 px-3 text-right">Req TK</th>
                      <th class="py-3.5 px-3 text-right">TK Mei</th>
                      <th class="py-3.5 px-3 text-right">TK Juni</th>
                      <th class="py-3.5 px-3 text-right text-amber-700 bg-amber-500/10">Target Jul</th>
                      <th class="py-3.5 px-3 text-right text-amber-700 bg-amber-500/10">Target Ags</th>
                      <th class="py-3.5 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-x border-red-300 dark:border-red-800">
                        🟥 TK PANEN JULI (COL I)
                      </th>
                      <th class="py-3.5 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-r border-red-300 dark:border-red-800">
                        🟥 TK PANEN AGUSTUS (COL J)
                      </th>
                    </tr>
                  </thead>
                  <tbody id="tkPanenTableBody" class="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
                    <tr>
                      <td colspan="13" class="py-12 text-center text-slate-400">Memuat data kebun...</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
"""

if main_start_tag in content and 'id="dashboardMainGrid"' not in content:
    content = content.replace(main_start_tag, main_start_tag + '\n          <div id="dashboardMainGrid" class="space-y-6">')
    print("Wrapped dashboard content in #dashboardMainGrid.")

if main_end_tag in content and 'id="tkPanenMainContent"' not in content:
    content = content.replace(main_end_tag, '</div>\n' + tk_embedded_html + '\n        ' + main_end_tag)
    print("Inserted #tkPanenMainContent inside <main>.")

# 3. Update JavaScript router logic
old_buka_tk = r'function bukaTKPanenSection\(\) \{.*?\n    \}'

new_buka_tk = """function bukaTKPanenSection() {
      var s = loadSession();
      if (!s) {
        alert("Sesi tidak valid, silakan login ulang.");
        prosesLogout();
        return;
      }

      if (window.history.pushState) {
        window.history.pushState(null, '', 'login.html#TKPanen');
      } else {
        window.location.hash = 'TKPanen';
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
        window.history.pushState(null, '', 'login.html');
      } else {
        window.location.hash = '';
      }
      var tkContent = document.getElementById("tkPanenMainContent");
      var mainGrid = document.getElementById("dashboardMainGrid");
      if (tkContent) tkContent.style.display = "none";
      if (mainGrid) mainGrid.style.display = "block";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }"""

content = re.sub(r'function bukaTKPanenSection\(\) \{.*?\n    \}', new_buka_tk, content, flags=re.DOTALL)

# Add route check on page load / hashchange
hash_check_code = """
    // Hash router listener for #TKPanen
    window.addEventListener('hashchange', function() {
      if (window.location.hash === '#TKPanen' || window.location.href.includes('TKPanen')) {
        bukaTKPanenSection();
      } else {
        tutupTKPanenSection();
      }
    });
"""

if 'window.addEventListener(\'hashchange\'' not in content:
    content = content.replace("</script>", hash_check_code + "\n</script>", 1)
    print("Added hashchange router listener to login.html")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY CONVERTED TK PANEN TO EMBEDDED ROUTER!")
