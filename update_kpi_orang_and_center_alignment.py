import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# 1A. Update Table Header in login.html to center align headers
old_thead = r'<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">.*?</thead>'

new_thead = """<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">
                    <tr class="text-[11px] font-black uppercase tracking-wider text-white">
                      <th class="py-3.5 px-2 text-center w-10 font-black">No</th>
                      <th class="py-3.5 px-2 text-center font-black">CRO</th>
                      <th class="py-3.5 px-2 text-center font-black">Regional</th>
                      <th class="py-3.5 px-3 text-left font-black min-w-[180px]">Nama Kebun / PT</th>
                      <th class="py-3.5 px-2 text-center font-black">Tag</th>
                      <th class="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                      <th class="py-3.5 px-2 text-center font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>
                      <th class="py-3.5 px-2 text-center font-black">TK Mei</th>
                      <th class="py-3.5 px-2 text-center font-black">TK Juni</th>
                      <th class="py-3.5 px-2 text-center font-black bg-slate-800 text-slate-100">Target Jul</th>
                      <th class="py-3.5 px-2 text-center font-black bg-slate-800 text-slate-100">Target Ags</th>
                      <th class="py-3.5 px-2 text-center font-black bg-black text-white border-x border-slate-700">
                        TK PANEN JULI
                      </th>
                      <th class="py-3.5 px-2 text-center font-black bg-black text-white border-r border-slate-700">
                        TK PANEN AGUSTUS
                      </th>
                      <th class="py-3.5 px-2 text-center font-black">AKSI</th>
                    </tr>
                  </thead>"""

login_code = re.sub(old_thead, new_thead, login_code, flags=re.DOTALL)

# 1B. Update renderTKPanenTable function in login.html to center align cell values & update KPI unit to "Orang"
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

        // Minimalist Black Input Box (Juli)
        html += '<td class="py-2 px-2 text-center bg-slate-100/50 dark:bg-slate-900 border-x border-slate-200 dark:border-slate-800">';
        html += '<input type="number" min="0" value="' + valJuli + '" onchange="onTKInputChange(' + item.id + ', \'tk_juli\', this.value)" class="w-20 px-2 py-1.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-lg text-center font-black text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white shadow-sm text-xs" />';
        html += '</td>';

        // Minimalist Black Input Box (Agustus)
        html += '<td class="py-2 px-2 text-center bg-slate-100/50 dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800">';
        html += '<input type="number" min="0" value="' + valAgs + '" onchange="onTKInputChange(' + item.id + ', \'tk_agustus\', this.value)" class="w-20 px-2 py-1.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-lg text-center font-black text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white shadow-sm text-xs" />';
        html += '</td>';

        // Action Cell: Edit Button
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

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html with KPI unit 'Orang' and centered table cell alignments!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

# Replace React Table Header in TKPanenView in laporan_produksi.html
old_react_thead_lap = r'<thead className="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700 text-\[11px\] font-black uppercase tracking-wider">.*?</thead>'

new_react_thead_lap = """<thead className="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700 text-[11px] font-black uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-2 text-center w-10 font-black">No</th>
                      <th className="py-3.5 px-2 text-center font-black">CRO</th>
                      <th className="py-3.5 px-2 text-center font-black">Regional</th>
                      <th className="py-3.5 px-3 text-left font-black min-w-[180px]">Nama Kebun / PT</th>
                      <th className="py-3.5 px-2 text-center font-black">Tag</th>
                      <th className="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                      <th className="py-3.5 px-2 text-center font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>
                      <th className="py-3.5 px-2 text-center font-black">TK Mei</th>
                      <th className="py-3.5 px-2 text-center font-black">TK Juni</th>
                      <th className="py-3.5 px-2 text-center font-black bg-slate-800 text-slate-100">Target Jul</th>
                      <th className="py-3.5 px-2 text-center font-black bg-slate-800 text-slate-100">Target Ags</th>
                      <th className="py-3.5 px-2 text-center font-black bg-black text-white border-x border-slate-700">
                        TK PANEN JULI
                      </th>
                      <th className="py-3.5 px-2 text-center font-black bg-black text-white border-r border-slate-700">
                        TK PANEN AGUSTUS
                      </th>
                      <th className="py-3.5 px-2 text-center font-black">AKSI</th>
                    </tr>
                  </thead>"""

lap_code = re.sub(old_react_thead_lap, new_react_thead_lap, lap_code, flags=re.DOTALL)

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html React view with centered table alignments!")
