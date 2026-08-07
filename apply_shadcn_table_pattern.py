import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Update renderTKPanenTable in login.html for Shadcn Card & Table styling
old_render = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_render = """function renderTKPanenTable(items, summary) {
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

        html += '<tr class="border-b border-slate-100 dark:border-slate-800/60 hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">';
        html += '<td class="p-3.5 text-center text-slate-400 font-semibold">' + (idx + 1) + '</td>';
        html += '<td class="p-3.5 font-bold text-slate-700 dark:text-slate-300">' + (item.cro || '-') + '</td>';
        html += '<td class="p-3.5 font-medium text-slate-600 dark:text-slate-400">' + (item.region || '-') + '</td>';
        html += '<td class="p-3.5 px-4 font-extrabold text-slate-800 dark:text-slate-100">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="p-3.5 font-mono text-[11px] text-slate-500">' + (item.name_tag || '-') + '</td>';
        html += '<td class="p-3.5 text-right font-medium">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-medium">' + (item.req_tk || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right text-slate-600 dark:text-slate-400">' + (item.tk_mei || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right text-slate-600 dark:text-slate-400">' + (item.tk_juni || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5">' + (item.target_juli || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5">' + (item.target_agustus || 0).toLocaleString('id-ID') + '</td>';
        
        // Editable Kolom I (Juli) - Shadcn Red Accent Cell
        html += '<td class="p-3 text-center bg-red-500/10 border-x border-red-200 dark:border-red-900/50">';
        html += '<input type="number" min="0" value="' + valJuli + '" onchange="onTKInputChange(' + item.id + ', \'tk_juli\', this.value)" class="w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all" />';
        html += '</td>';

        // Editable Kolom J (Agustus) - Shadcn Red Accent Cell
        html += '<td class="p-3 text-center bg-red-500/10 border-r border-red-200 dark:border-red-900/50">';
        html += '<input type="number" min="0" value="' + valAgs + '" onchange="onTKInputChange(' + item.id + ', \'tk_agustus\', this.value)" class="w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all" />';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Summary badges
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl && summary) {
        summaryEl.innerHTML = '<span class="px-3.5 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 shadow-sm">Total Kebun: <b>' + items.length + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 shadow-sm">Luas: <b>' + (summary.totalLuas || 0).toLocaleString('id-ID') + ' Ha</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-300 rounded-xl shadow-sm">Target Jul: <b>' + (summary.totalJuliTgt || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 rounded-xl shadow-sm">Real Jul (I): <b>' + (summary.totalJuliAct || 0).toLocaleString('id-ID') + '</b></span>' +
                              '<span class="px-3.5 py-1.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 rounded-xl shadow-sm">Real Ags (J): <b>' + (summary.totalAgustAct || 0).toLocaleString('id-ID') + '</b></span>';
      }
    }"""

login_code = re.sub(old_render, new_render, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html table with Shadcn Card & Table pattern!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

# Replace React table rendering in TKPanenView to match Shadcn Table pattern
old_react_tr = r'<tr key=\{item\.id\} className="hover:bg-slate-50 dark:hover:bg-slate-700/40 transition-colors">.*?</tr>'

new_react_tr = """<tr key={item.id} className="border-b border-slate-100 dark:border-slate-800/60 hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">
                            <td className="p-3.5 text-center text-slate-400 font-semibold">{idx + 1}</td>
                            <td className="p-3.5 font-bold text-slate-700 dark:text-slate-300">{item.cro || '-'}</td>
                            <td className="p-3.5 font-medium text-slate-600 dark:text-slate-400">{item.region || '-'}</td>
                            <td className="p-3.5 px-4 font-extrabold text-slate-800 dark:text-slate-100">{item.nama_kebun || '-'}</td>
                            <td className="p-3.5 font-mono text-[11px] text-slate-500">{item.name_tag || '-'}</td>
                            <td className="p-3.5 text-right font-medium">{formatRibuan(item.luasan || 0)}</td>
                            <td className="p-3.5 text-right font-medium">{formatRibuan(item.req_tk || 0)}</td>
                            <td className="p-3.5 text-right text-slate-600 dark:text-slate-400">{formatRibuan(item.tk_mei || 0)}</td>
                            <td className="p-3.5 text-right text-slate-600 dark:text-slate-400">{formatRibuan(item.tk_juni || 0)}</td>
                            <td className="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5">{formatRibuan(item.target_juli || 0)}</td>
                            <td className="p-3.5 text-right font-bold text-amber-700 bg-amber-500/5">{formatRibuan(item.target_agustus || 0)}</td>
                            
                            <td className="p-3 text-center bg-red-500/10 border-x border-red-200 dark:border-red-900/50">
                              <input
                                type="number"
                                min="0"
                                value={valJuli}
                                onChange={(e) => handleInputChange(item.id, 'tk_juli', e.target.value)}
                                className="w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all"
                              />
                            </td>

                            <td className="p-3 text-center bg-red-500/10 border-r border-red-200 dark:border-red-900/50">
                              <input
                                type="number"
                                min="0"
                                value={valAgs}
                                onChange={(e) => handleInputChange(item.id, 'tk_agustus', e.target.value)}
                                className="w-24 px-2.5 py-1.5 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-xl text-center font-extrabold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm transition-all"
                              />
                            </td>
                          </tr>"""

lap_code = re.sub(old_react_tr, new_react_tr, lap_code, flags=re.DOTALL)

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html table with Shadcn Card & Table pattern!")
