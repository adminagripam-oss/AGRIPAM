import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Replace table container in login.html with fluid responsive Shadcn Card wrapper
old_table_wrap = r'<!-- Kebun Table -->\s*<div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-100 dark:border-slate-800 overflow-hidden shadow-sm">.*?</table>\s*</div>\s*</div>'

new_table_wrap = """<!-- Kebun Table Card Container (Fluid Responsive & Sticky Header) -->
            <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/80 dark:border-slate-800 overflow-hidden shadow-sm w-full transition-all duration-300">
              <div class="overflow-x-auto custom-scrollbar w-full">
                <table class="w-full text-left text-xs border-collapse min-w-[1100px]" id="tkPanenTable">
                  <thead class="sticky top-0 z-10 bg-slate-50/95 dark:bg-slate-800/95 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700">
                    <tr class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                      <th class="h-11 px-3.5 text-center w-12 whitespace-nowrap">No</th>
                      <th class="h-11 px-3.5 whitespace-nowrap">CRO</th>
                      <th class="h-11 px-3.5 whitespace-nowrap">Regional</th>
                      <th class="h-11 px-4 min-w-[220px] max-w-[320px] whitespace-nowrap">Nama Kebun / PT</th>
                      <th class="h-11 px-3.5 whitespace-nowrap">Tag Kebun</th>
                      <th class="h-11 px-3.5 text-right whitespace-nowrap">Luas (Ha)</th>
                      <th class="h-11 px-3.5 text-right whitespace-nowrap">Req TK</th>
                      <th class="h-11 px-3.5 text-right whitespace-nowrap">TK Mei</th>
                      <th class="h-11 px-3.5 text-right whitespace-nowrap">TK Juni</th>
                      <th class="h-11 px-3.5 text-right text-amber-700 bg-amber-500/10 whitespace-nowrap">Target Jul</th>
                      <th class="h-11 px-3.5 text-right text-amber-700 bg-amber-500/10 whitespace-nowrap">Target Ags</th>
                      <th class="h-11 px-4 text-center bg-red-500/15 text-red-700 dark:text-red-300 font-extrabold border-x border-red-300 dark:border-red-900/50 whitespace-nowrap">
                        🟥 TK PANEN JULI (COL I)
                      </th>
                      <th class="h-11 px-4 text-center bg-red-500/15 text-red-700 dark:text-red-300 font-extrabold border-r border-red-300 dark:border-red-900/50 whitespace-nowrap">
                        🟥 TK PANEN AGUSTUS (COL J)
                      </th>
                    </tr>
                  </thead>
                  <tbody id="tkPanenTableBody" class="divide-y divide-slate-100 dark:divide-slate-800">
                    <tr>
                      <td colspan="13" class="py-12 text-center text-slate-400">Memuat data kebun...</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>"""

login_code = re.sub(old_table_wrap, new_table_wrap, login_code, flags=re.DOTALL)

# Update renderTKPanenTable rows in login.html to add whitespace-nowrap & fluid classes
old_js_render = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_js_render = """function renderTKPanenTable(items, summary) {
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="13" class="py-12 text-center text-slate-400 font-medium">Tidak ada data kebun.</td></tr>';
        return;
      }

      var html = "";
      items.forEach(function(item, idx) {
        var edit = globalTKEdits[item.id] || {};
        var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
        var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

        html += '<tr class="border-b border-slate-100 dark:border-slate-800/60 hover:bg-slate-50/70 dark:hover:bg-slate-800/50 transition-colors">';
        html += '<td class="p-3.5 text-center text-slate-400 font-semibold whitespace-nowrap">' + (idx + 1) + '</td>';
        html += '<td class="p-3.5 font-bold text-slate-700 dark:text-slate-300 whitespace-nowrap">' + (item.cro || '-') + '</td>';
        html += '<td class="p-3.5 font-medium text-slate-600 dark:text-slate-400 whitespace-nowrap">' + (item.region || '-') + '</td>';
        html += '<td class="p-3.5 px-4 font-extrabold text-slate-800 dark:text-slate-100 min-w-[220px] max-w-[320px] truncate" title="' + (item.nama_kebun || '') + '">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="p-3.5 font-mono text-[11px] text-slate-500 whitespace-nowrap">' + (item.name_tag || '-') + '</td>';
        html += '<td class="p-3.5 text-right font-medium whitespace-nowrap">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-medium whitespace-nowrap">' + (item.req_tk || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right text-slate-600 dark:text-slate-400 whitespace-nowrap">' + (item.tk_mei || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right text-slate-600 dark:text-slate-400 whitespace-nowrap">' + (item.tk_juni || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5 whitespace-nowrap">' + (item.target_juli || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5 whitespace-nowrap">' + (item.target_agustus || 0).toLocaleString('id-ID') + '</td>';
        
        // Editable Kolom I (Juli)
        html += '<td class="p-3 text-center bg-red-500/10 border-x border-red-200 dark:border-red-900/50 whitespace-nowrap">';
        html += '<input type="number" min="0" value="' + valJuli + '" onchange="onTKInputChange(' + item.id + ', \'tk_juli\', this.value)" class="w-20 md:w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all text-xs md:text-sm" />';
        html += '</td>';

        // Editable Kolom J (Agustus)
        html += '<td class="p-3 text-center bg-red-500/10 border-r border-red-200 dark:border-red-900/50 whitespace-nowrap">';
        html += '<input type="number" min="0" value="' + valAgs + '" onchange="onTKInputChange(' + item.id + ', \'tk_agustus\', this.value)" class="w-20 md:w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all text-xs md:text-sm" />';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Summary badges
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl && summary) {
        summaryEl.innerHTML = '<span class="px-3.5 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 shadow-sm whitespace-nowrap">Total Kebun: <b>' + items.length + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 shadow-sm whitespace-nowrap">Luas: <b>' + (summary.totalLuas || 0).toLocaleString('id-ID') + ' Ha</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-300 rounded-xl shadow-sm whitespace-nowrap">Target Jul: <b>' + (summary.totalJuliTgt || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 rounded-xl shadow-sm whitespace-nowrap">Real Jul (I): <b>' + (summary.totalJuliAct || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 rounded-xl shadow-sm whitespace-nowrap">Real Ags (J): <b>' + (summary.totalAgustAct || 0).toLocaleString('id-ID') + '</b></span>';
      }
    }"""

login_code = re.sub(old_js_render, new_js_render, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html with fluid responsive table & sticky header!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

# Update React table header in TKPanenView to add sticky header & whitespace-nowrap
old_react_thead = r'<thead className="bg-slate-50 dark:bg-slate-900/80 text-\[11px\] font-bold text-slate-500 uppercase tracking-wider border-b border-slate-200 dark:border-slate-700">.*?</thead>'

new_react_thead = """<thead className="sticky top-0 z-10 bg-slate-50/95 dark:bg-slate-800/95 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700 text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    <tr>
                      <th className="h-11 px-3.5 text-center w-12 whitespace-nowrap">No</th>
                      <th className="h-11 px-3.5 whitespace-nowrap">CRO</th>
                      <th className="h-11 px-3.5 whitespace-nowrap">Regional</th>
                      <th className="h-11 px-4 min-w-[220px] max-w-[320px] whitespace-nowrap">Nama Kebun / PT</th>
                      <th className="h-11 px-3.5 whitespace-nowrap">Tag Kebun</th>
                      <th className="h-11 px-3.5 text-right whitespace-nowrap">Luas (Ha)</th>
                      <th className="h-11 px-3.5 text-right whitespace-nowrap">Req TK</th>
                      <th className="h-11 px-3.5 text-right whitespace-nowrap">TK Mei</th>
                      <th className="h-11 px-3.5 text-right whitespace-nowrap">TK Juni</th>
                      <th className="h-11 px-3.5 text-right bg-amber-500/10 text-amber-700 dark:text-amber-400 whitespace-nowrap">Target Jul</th>
                      <th className="h-11 px-3.5 text-right bg-amber-500/10 text-amber-700 dark:text-amber-400 whitespace-nowrap">Target Ags</th>
                      <th className="h-11 px-4 text-center bg-red-500/15 text-red-700 dark:text-red-300 font-extrabold border-x border-red-300 dark:border-red-800 whitespace-nowrap">
                        🟥 TK PANEN JULI (COL I)
                      </th>
                      <th className="h-11 px-4 text-center bg-red-500/15 text-red-700 dark:text-red-300 font-extrabold border-r border-red-300 dark:border-red-800 whitespace-nowrap">
                        🟥 TK PANEN AGUSTUS (COL J)
                      </th>
                    </tr>
                  </thead>"""

lap_code = re.sub(old_react_thead, new_react_thead, lap_code, flags=re.DOTALL)

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html React table header with fluid responsive & sticky header!")
