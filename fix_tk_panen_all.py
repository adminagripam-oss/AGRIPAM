import re

# ==============================================================================
# FIX LAPORAN_PRODUKSI.HTML
# ==============================================================================
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_content = f.read()

# Fix App view router in laporan_produksi.html
target_app_view = "{activeNav === 'validasi' ? ("
replacement_app_view = "{activeNav === 'tk-panen' ? (\n                  <TKPanenView />\n                ) : activeNav === 'validasi' ? ("

if target_app_view in lap_content and "activeNav === 'tk-panen' ?" not in lap_content:
    lap_content = lap_content.replace(target_app_view, replacement_app_view)
    print("Fixed App view router in laporan_produksi.html")

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_content)


# ==============================================================================
# FIX LOGIN.HTML
# ==============================================================================
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_content = f.read()

# Make sure monitoring button calls tutupTKPanenSection()
mon_btn_old = 'onclick="tutupSAP(); tutupEstimasiModal(); setActiveSidebar(0);"'
mon_btn_new = 'onclick="tutupTKPanenSection(); tutupSAP(); tutupEstimasiModal(); setActiveSidebar(0);"'
if mon_btn_old in login_content:
    login_content = login_content.replace(mon_btn_old, mon_btn_new)
    print("Updated Monitoring button onclick in login.html")

# Remove any orphaned scripts or duplicates at bottom of login.html
login_content = re.sub(r'// =+\s*// FITUR TK PANEN.*?function filterTKPanenTable\(\) \{.*?\n\s*\}', '', login_content, flags=re.DOTALL)

# Clean JS code to be inserted BEFORE the main closing </script>
js_tk_code = """
    // =========================================================================
    // FITUR TK PANEN (ROUTER & DATA INPUT)
    // =========================================================================
    var globalTKData = [];
    var globalTKEdits = {};

    function bukaTKPanenSection() {
      var s = loadSession();
      if (!s) {
        alert("Sesi tidak valid, silakan login ulang.");
        prosesLogout();
        return;
      }

      var mainSec = document.getElementById("mainSection");
      var sapSec = document.getElementById("sapSection");
      var estSec = document.getElementById("estimasiSection");
      var tkSec = document.getElementById("tkPanenSection");

      if (mainSec) mainSec.style.display = "none";
      if (sapSec) sapSec.style.display = "none";
      if (estSec) estSec.style.display = "none";
      if (tkSec) {
        tkSec.style.display = "flex";
        tkSec.classList.remove("hidden");
      }

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
      var tkSec = document.getElementById("tkPanenSection");
      var mainSec = document.getElementById("mainSection");
      if (tkSec) tkSec.style.display = "none";
      if (mainSec) mainSec.style.display = "flex";
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

# Insert JS code inside main script before </script>
script_close_idx = login_content.find("</script>")
if script_close_idx != -1 and "function bukaTKPanenSection()" not in login_content[:script_close_idx]:
    login_content = login_content[:script_close_idx] + js_tk_code + "\n  " + login_content[script_close_idx:]
    print("Inserted JS code inside main <script> tag in login.html")

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_content)

print("SUCCESSFULLY FIXED BOTH FILES!")
