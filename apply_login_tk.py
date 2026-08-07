file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject TK Panen button into leftSidebar nav
sidebar_nav_target = '''<!-- Button 3: SAP -->
        <button id="btnOpenSAP" onclick="bukaSAP(); setActiveSidebar(2);"
          class="flex items-center p-3 text-gray-400 hover:bg-gray-50 rounded-lg transition-colors relative w-full"
          data-purpose="nav-item" title="ARSIP">
          <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewbox="0 0 24 24">
            <path
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span
            class="nav-text text-sm font-semibold ml-3 overflow-hidden whitespace-nowrap transition-all duration-300">ARSIP</span>
          <span id="sapNotifBadge" class="hidden absolute top-3 left-7">
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
          </span>
        </button>'''

tk_nav_button = '''<!-- Button 4: TK Panen -->
        <button id="btnOpenTKPanen" onclick="bukaTKPanenSection(); setActiveSidebar(3);"
          class="flex items-center p-3 text-gray-400 hover:bg-gray-50 rounded-lg transition-colors relative w-full"
          data-purpose="nav-item" title="TK Panen">
          <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          <span
            class="nav-text text-sm font-semibold ml-3 overflow-hidden whitespace-nowrap transition-all duration-300">TK Panen</span>
        </button>'''

if sidebar_nav_target in content and 'btnOpenTKPanen' not in content:
    content = content.replace(sidebar_nav_target, sidebar_nav_target + '\n        ' + tk_nav_button)
    print("Added btnOpenTKPanen to leftSidebar in login.html")

# 2. Add tkPanenSection HTML structure before closing </body>
tk_section_html = """
  <!-- ===================== TK PANEN SECTION MODAL ===================== -->
  <div id="tkPanenSection" style="display:none;" class="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-md flex flex-col p-4 lg:p-8 overflow-y-auto">
    <div class="max-w-7xl w-full mx-auto bg-white dark:bg-slate-800 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-700 flex flex-col overflow-hidden my-auto">
      
      <!-- Top Header -->
      <div class="px-6 py-5 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
        <div class="flex items-center gap-3">
          <div class="p-3 bg-emerald-500/10 text-emerald-600 rounded-2xl">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">Fitur Pengisian TK Panen</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">Input & Monitoring Realisasi Tenaga Kerja Panen Kebun (Kolom I Juli & Kolom J Agustus)</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button id="btnSaveTKPanen" onclick="simpanTKPanenEdits()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 active:scale-95 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-600/20 transition-all flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
            <span>Simpan Data TK Panen</span>
          </button>

          <button onclick="tutupTKPanenSection()" class="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>

      <!-- Content Area -->
      <div class="p-6 flex flex-col gap-5 max-h-[80vh] overflow-y-auto">
        
        <!-- Regional & Search Bar -->
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div id="tkAdminRegionContainer" style="display:none;" class="flex items-center gap-2">
            <span class="text-xs font-semibold text-slate-500">Filter Regional:</span>
            <select id="tkAdminRegionSelect" onchange="loadTKPanenDataForSelectedRegion()" class="px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200">
              <option value="ALL">Semua Regional (23 Region)</option>
            </select>
          </div>

          <div class="flex-1 max-w-md relative">
            <input type="text" id="tkSearchInput" onkeyup="filterTKPanenTable()" placeholder="Cari kebun, tag kebun, atau regional..." class="w-full pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            <svg class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>

          <div id="tkSummaryBadges" class="flex flex-wrap items-center gap-2 text-xs font-semibold"></div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-700">
          <table class="w-full text-left border-collapse" id="tkPanenTable">
            <thead>
              <tr class="bg-slate-100 dark:bg-slate-900/90 text-[11px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider border-b border-slate-200 dark:border-slate-700">
                <th class="py-3 px-3 text-center w-12">No</th>
                <th class="py-3 px-3">CRO</th>
                <th class="py-3 px-3">Regional</th>
                <th class="py-3 px-4 min-w-[200px]">Nama Kebun / PT</th>
                <th className="py-3 px-3">Tag Kebun</th>
                <th class="py-3 px-3 text-right">Luas (Ha)</th>
                <th class="py-3 px-3 text-right">Req TK</th>
                <th class="py-3 px-3 text-right">TK Mei</th>
                <th class="py-3 px-3 text-right">TK Juni</th>
                <th class="py-3 px-3 text-right text-amber-700 bg-amber-500/10">Target Jul</th>
                <th class="py-3 px-3 text-right text-amber-700 bg-amber-500/10">Target Ags</th>
                <th class="py-3 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-x border-red-300">
                  🟥 TK PANEN JULI (COL I)
                </th>
                <th class="py-3 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-r border-red-300">
                  🟥 TK PANEN AGUSTUS (COL J)
                </th>
              </tr>
            </thead>
            <tbody id="tkPanenTableBody" class="divide-y divide-slate-100 dark:divide-slate-700/50 text-xs">
              <tr>
                <td colspan="13" class="py-12 text-center text-slate-400">Memuat data kebun...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
"""

if tk_section_html not in content:
    content = content.replace("</body>", tk_section_html + "\n</body>")
    print("Added #tkPanenSection HTML modal to login.html")

# 3. Inject JavaScript functions for TK Panen Modal in login.html
js_functions = """
    // =========================================================================
    // FITUR TK PANEN (ROUTER & DATA INPUT)
    // =========================================================================
    var globalTKData = [];
    var globalTKEdits = {};

    function bukaTKPanenSection() {
      var s = loadSession();
      if (!s) {
        alert("Sesi telah habis, silakan login ulang.");
        prosesLogout();
        return;
      }

      var sec = document.getElementById("tkPanenSection");
      if (sec) sec.style.display = "flex";

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
      var sec = document.getElementById("tkPanenSection");
      if (sec) sec.style.display = "none";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }

    function populateTKAdminRegionSelect() {
      var sel = document.getElementById("tkAdminRegionSelect");
      if (!sel || sel.options.length > 1) return;
      sel.innerHTML = '<option value="ALL">Semua Regional (23 Region)</option>';
      ALL_REGIONS.forEach(function(r) {
        var opt = document.createElement("option");
        opt.value = r;
        opt.textContent = r;
        sel.appendChild(opt);
      });
    }

    function loadTKPanenDataForSelectedRegion() {
      var s = loadSession();
      if (!s) return;

      var regParam = s.region;
      if (s.region === 'ADMIN') {
        var sel = document.getElementById("tkAdminRegionSelect");
        regParam = sel ? sel.value : 'ALL';
      }

      var tbody = document.getElementById("tkPanenTableBody");
      if (tbody) tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-slate-400">Memuat data kebun...</td></tr>';

      fetch('/api/kebunTK?action=getKebun&region=' + encodeURIComponent(regParam) + '&_t=' + Date.now())
        .then(function(res) { return res.json(); })
        .then(function(json) {
          if (json.success) {
            globalTKData = json.data || [];
            globalTKEdits = {};
            renderTKPanenTable(globalTKData, json.summary);
          } else {
            if (tbody) tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-red-500">Gagal memuat data: ' + json.message + '</td></tr>';
          }
        })
        .catch(function(err) {
          console.error(err);
          if (tbody) tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-red-500">Terjadi kesalahan koneksi.</td></tr>';
        });
    }

    function renderTKPanenTable(items, summary) {
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-slate-400">Tidak ada data kebun.</td></tr>';
        return;
      }

      var html = "";
      items.forEach(function(item, idx) {
        var edit = globalTKEdits[item.id] || {};
        var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
        var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

        html += '<tr class="hover:bg-slate-50 dark:hover:bg-slate-700/40 transition-colors">';
        html += '<td class="py-2.5 px-3 text-center text-slate-400 font-medium">' + (idx + 1) + '</td>';
        html += '<td class="py-2.5 px-3 font-semibold text-slate-700 dark:text-slate-300">' + (item.cro || '-') + '</td>';
        html += '<td class="py-2.5 px-3 font-medium text-slate-600 dark:text-slate-400">' + (item.region || '-') + '</td>';
        html += '<td class="py-2.5 px-4 font-bold text-slate-800 dark:text-slate-100">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="py-2.5 px-3 font-mono text-[11px] text-slate-500">' + (item.name_tag || '-') + '</td>';
        html += '<td class="py-2.5 px-3 text-right font-medium">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-2.5 px-3 text-right font-medium">' + (item.req_tk || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-2.5 px-3 text-right text-slate-600 dark:text-slate-400">' + (item.tk_mei || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-2.5 px-3 text-right text-slate-600 dark:text-slate-400">' + (item.tk_juni || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-2.5 px-3 text-right font-semibold text-amber-700 bg-amber-500/5">' + (item.target_juli || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-2.5 px-3 text-right font-semibold text-amber-700 bg-amber-500/5">' + (item.target_agustus || 0).toLocaleString('id-ID') + '</td>';
        
        // Editable Kolom I (Juli)
        html += '<td class="py-2.5 px-4 text-center bg-red-500/10 border-x border-red-200">';
        html += '<input type="number" min="0" value="' + valJuli + '" onchange="onTKInputChange(' + item.id + ', \'tk_juli\', this.value)" class="w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm" />';
        html += '</td>';

        // Editable Kolom J (Agustus)
        html += '<td class="py-2.5 px-4 text-center bg-red-500/10 border-r border-red-200">';
        html += '<input type="number" min="0" value="' + valAgs + '" onchange="onTKInputChange(' + item.id + ', \'tk_agustus\', this.value)" class="w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm" />';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Summary badges
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl && summary) {
        summaryEl.innerHTML = '<span class="px-3 py-1 bg-slate-100 rounded-lg text-slate-700">Total Kebun: <b>' + items.length + '</b></span>' +
                              '<span class="px-3 py-1 bg-slate-100 rounded-lg text-slate-700">Luas: <b>' + (summary.totalLuas || 0).toLocaleString('id-ID') + ' Ha</b></span>' +
                              '<span class="px-3 py-1 bg-amber-100 text-amber-800 rounded-lg">Target Jul: <b>' + (summary.totalJuliTgt || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3 py-1 bg-red-100 text-red-800 rounded-lg">Real Jul (I): <b>' + (summary.totalJuliAct || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3 py-1 bg-red-100 text-red-800 rounded-lg">Real Ags (J): <b>' + (summary.totalAgustAct || 0).toLocaleString('id-ID') + '</b></span>';
      }
    }

    function onTKInputChange(id, field, value) {
      if (!globalTKEdits[id]) globalTKEdits[id] = {};
      globalTKEdits[id][field] = Math.max(0, parseFloat(value) || 0);
    }

    function simpanTKPanenEdits() {
      var editKeys = Object.keys(globalTKEdits);
      if (editKeys.length === 0) {
        alert("Tidak ada perubahan data yang dibuat.");
        return;
      }

      var s = loadSession();
      if (!s) return;

      var btn = document.getElementById("btnSaveTKPanen");
      if (btn) btn.disabled = true;

      var editsArray = editKeys.map(function(k) {
        var obj = globalTKEdits[k];
        obj.id = parseInt(k, 10);
        return obj;
      });

      fetch('/api/kebunTK', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'updateTK',
          region: s.region,
          token: s.token,
          edits: editsArray
        })
      })
      .then(function(res) { return res.json(); })
      .then(function(json) {
        if (btn) btn.disabled = false;
        if (json.success) {
          alert(json.message || "Data TK Panen berhasil disimpan!");
          globalTKEdits = {};
          loadTKPanenDataForSelectedRegion();
        } else {
          alert("Gagal menyimpan: " + json.message);
        }
      })
      .catch(function(err) {
        if (btn) btn.disabled = false;
        alert("Terjadi kesalahan koneksi saat menyimpan.");
      });
    }

    function filterTKPanenTable() {
      var input = document.getElementById("tkSearchInput");
      var filter = input ? input.value.toLowerCase() : "";
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      var trs = tbody.getElementsByTagName("tr");
      for (var i = 0; i < trs.length; i++) {
        var text = trs[i].textContent || trs[i].innerText;
        if (text.toLowerCase().indexOf(filter) > -1) {
          trs[i].style.display = "";
        } else {
          trs[i].style.display = "none";
        }
      }
    }
"""

if 'function bukaTKPanenSection()' not in content:
    content = content.replace("</script>", js_functions + "\n</script>", 1)
    print("Added JS functions for TK Panen to login.html")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY UPDATED login.html!")
