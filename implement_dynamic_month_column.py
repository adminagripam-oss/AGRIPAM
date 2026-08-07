import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. UPDATE THEAD IN LOGIN.HTML TO CONSOLIDATE ALL MONTH COLUMNS INTO 1 DYNAMIC DROPDOWN COLUMN
old_thead_pattern = r'<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">.*?</thead>'

new_thead_html = """<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">
                    <tr class="text-[11px] font-black uppercase tracking-wider text-white">
                      <th class="py-3.5 px-2 text-center w-10 font-black">No</th>
                      <th class="py-3.5 px-2 text-center font-black">CRO</th>
                      <th class="py-3.5 px-2 text-center font-black">Regional</th>
                      <th class="py-3.5 px-3 text-left font-black min-w-[180px]">Nama Kebun / PT</th>
                      <th class="py-3.5 px-2 text-center font-black">Tag</th>
                      <th class="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                      <th class="py-3.5 px-2 text-center font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>
                      <th class="py-3 px-3 text-center font-black bg-slate-950 text-white min-w-[180px]">
                        <div class="flex items-center justify-center gap-1.5">
                          <span>REALISASI TK</span>
                          <select id="tkTableSelectedMonth" onchange="onTKTableMonthChange(this.value)" class="bg-slate-900 text-white text-[11px] font-black rounded-lg px-2 py-1 border border-slate-700 focus:outline-none cursor-pointer hover:bg-slate-800 transition-colors">
                            <option value="tk_juli" selected>Juli 2026 (H-1)</option>
                            <option value="tk_agustus">Agustus 2026</option>
                            <option value="tk_juni">Juni 2026</option>
                            <option value="tk_mei">Mei 2026</option>
                          </select>
                        </div>
                      </th>
                      <th class="py-3.5 px-2 text-center font-black">AKSI</th>
                    </tr>
                  </thead>"""

content = re.sub(old_thead_pattern, new_thead_html, content, flags=re.DOTALL)

# 2. UPDATE renderTKPanenTable FUNCTION IN LOGIN.HTML
old_render_fn = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_render_fn = """var currentTableMonth = 'tk_juli';
    var currentSummaryData = null;

    function onTKTableMonthChange(selectedMonth) {
      currentTableMonth = selectedMonth || 'tk_juli';
      renderTKPanenTable(globalTKData, currentSummaryData);
    }

    function renderTKPanenTable(items, summary) {
      currentSummaryData = summary || currentSummaryData;
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-slate-500 font-medium">Tidak ada data kebun.</td></tr>';
        return;
      }

      // Sync header dropdown value
      var monthSel = document.getElementById("tkTableSelectedMonth");
      if (monthSel && monthSel.value !== currentTableMonth) {
        monthSel.value = currentTableMonth;
      }

      var html = "";
      items.forEach(function (item, idx) {
        var edit = globalTKEdits[item.id] || {};
        var monthVal = edit[currentTableMonth] !== undefined ? edit[currentTableMonth] : (item[currentTableMonth] || 0);

        html += '<tr class="border-b border-slate-200 dark:border-slate-800 hover:bg-slate-100/80 dark:hover:bg-slate-800/80 transition-colors text-slate-900 dark:text-white font-medium">';
        html += '<td class="py-3 px-2 text-center text-slate-500 font-bold">' + (idx + 1) + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-800 dark:text-slate-200">' + (item.cro || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-700 dark:text-slate-300">' + (item.region || '-') + '</td>';
        html += '<td class="py-3 px-3 text-left font-black text-slate-900 dark:text-white min-w-[180px]">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-mono text-[11px] text-slate-500 font-semibold">' + (item.name_tag || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold text-amber-700 dark:text-amber-400 font-black">' + (item.req_tk || 0).toLocaleString('id-ID') + '</td>';

        // Single Dynamic Read-only Cell based on Header Dropdown Selection
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-white bg-slate-100/70 dark:bg-slate-900/80 border-x border-slate-200 dark:border-slate-800">' + (monthVal || 0).toLocaleString('id-ID') + '</td>';

        // Action Cell: Trigger Edit Sheet Modal
        html += '<td class="py-2 px-2 text-center">';
        html += '<button onclick="openEditKebunModal(' + item.id + ')" class="p-1.5 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors" title="Edit ' + (item.nama_kebun || '') + '">';
        html += '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>';
        html += '</button>';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Large Fluid KPI Cards Grid Rendering (5 Responsive Cards)
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl) {
        var reqTk = summary && summary.totalReqTk !== undefined ? summary.totalReqTk : items.reduce(function(s, x){ return s + (parseInt(x.req_tk)||0); }, 0);
        var tkJuni = summary && summary.totalJuni !== undefined ? summary.totalJuni : items.reduce(function(s, x){ return s + (parseInt(x.tk_juni)||0); }, 0);
        var kekurangTK = reqTk - tkJuni;

        summaryEl.innerHTML = '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Kebun</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + items.length + ' <span class="text-xs font-bold text-slate-500">Kebun</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Luas</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary && summary.totalLuas ? summary.totalLuas : 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Ha</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Kebutuhan Tenaga Panen</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + reqTk.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Orang</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">TK Juni (Cut Off Juni)</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + tkJuni.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Orang</span></div>' +
          '</div>' +
          '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Kekurangan Tenaga Panen</span>' +
          '<div class="text-xl md:text-2xl font-black text-white mt-1">' + kekurangTK.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">Orang</span></div>' +
          '</div>';
      }
    }"""

content = re.sub(old_render_fn, new_render_fn, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY CONSOLIDATED MANY MONTH COLUMNS INTO ONE DYNAMIC MONTH DROPDOWN COLUMN IN LOGIN.HTML!")
