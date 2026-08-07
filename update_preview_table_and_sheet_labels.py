import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# 1A. Remove inline input boxes in table rows and convert TK Panen Juli & Agustus into clean read-only preview cells
old_render = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_render = """function renderTKPanenTable(items, summary) {
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="14" class="py-12 text-center text-slate-500 font-medium">Tidak ada data kebun.</td></tr>';
        return;
      }

      var html = "";
      items.forEach(function (item, idx) {
        var edit = globalTKEdits[item.id] || {};
        var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
        var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

        html += '<tr class="border-b border-slate-200 dark:border-slate-800 hover:bg-slate-100/80 dark:hover:bg-slate-800/80 transition-colors text-slate-900 dark:text-white font-medium">';
        html += '<td class="py-3 px-2 text-center text-slate-500 font-bold">' + (idx + 1) + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-800 dark:text-slate-200">' + (item.cro || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-700 dark:text-slate-300">' + (item.region || '-') + '</td>';
        html += '<td class="py-3 px-3 text-left font-black text-slate-900 dark:text-white min-w-[180px]">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-mono text-[11px] text-slate-500 font-semibold">' + (item.name_tag || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold">' + (item.req_tk || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center text-slate-600 dark:text-slate-400 font-medium">' + (item.tk_mei || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center text-slate-600 dark:text-slate-400 font-medium">' + (item.tk_juni || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-slate-100 bg-slate-50 dark:bg-slate-900/50">' + (item.target_juli || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-slate-100 bg-slate-50 dark:bg-slate-900/50">' + (item.target_agustus || 0).toLocaleString('id-ID') + '</td>';

        // Read-only Preview Cell: TK Panen Juli
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-white bg-slate-50/70 dark:bg-slate-900/50 border-x border-slate-200 dark:border-slate-800">' + (valJuli || 0).toLocaleString('id-ID') + '</td>';

        // Read-only Preview Cell: TK Panen Agustus
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-white bg-slate-50/70 dark:bg-slate-900/50 border-r border-slate-200 dark:border-slate-800">' + (valAgs || 0).toLocaleString('id-ID') + '</td>';

        // Action Cell: Trigger Edit Sheet Modal
        html += '<td class="py-2 px-2 text-center">';
        html += '<button onclick="openEditKebunModal(' + item.id + ')" class="p-1.5 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors" title="Edit ' + (item.nama_kebun || '') + '">';
        html += '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>';
        html += '</button>';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Large Fluid KPI Cards Grid Rendering (Unit "Orang")
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl && summary) {
        summaryEl.innerHTML = '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Kebun</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + items.length + ' <span class="text-xs font-bold text-slate-500">Kebun</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Luas</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary.totalLuas || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Ha</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Target Juli</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary.totalJuliTgt || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Orang</span></div>' +
          '</div>' +
          '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Realisasi Juli</span>' +
          '<div class="text-xl md:text-2xl font-black text-white mt-1">' + (summary.totalJuliAct || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">Orang</span></div>' +
          '</div>' +
          '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Realisasi Agustus</span>' +
          '<div class="text-xl md:text-2xl font-black text-white mt-1">' + (summary.totalAgustAct || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">Orang</span></div>' +
          '</div>';
      }
    }"""

login_code = re.sub(old_render, new_render, login_code, flags=re.DOTALL)

# 1B. Fix Sheet Modal labels: remove (Col I) and (Col J)
login_code = login_code.replace("TK Panen Juli (Col I)", "TK Panen Juli")
login_code = login_code.replace("TK Panen Agustus (Col J)", "TK Panen Agustus")

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html: table cells are read-only preview, sheet modal labels fixed!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

# Fix labels in laporan_produksi.html as well
lap_code = lap_code.replace("TK Panen Juli (Col I)", "TK Panen Juli")
lap_code = lap_code.replace("TK Panen Agustus (Col J)", "TK Panen Agustus")

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html: sheet labels fixed!")
