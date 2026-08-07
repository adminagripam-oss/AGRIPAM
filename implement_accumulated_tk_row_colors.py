import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# 1A. Update renderTKPanenTable row generation logic with Soft Green / Soft Red background based on (Mei+Juni+Juli+Agustus == req_tk)
old_render_fn = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_render_fn = """function renderTKPanenTable(items, summary) {
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="12" class="py-12 text-center text-slate-500 font-medium">Tidak ada data kebun.</td></tr>';
        return;
      }

      var html = "";
      items.forEach(function (item, idx) {
        var edit = globalTKEdits[item.id] || {};
        var valMei = item.tk_mei || 0;
        var valJuni = item.tk_juni || 0;
        var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
        var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

        var reqTk = parseInt(item.req_tk, 10) || 0;
        var accumTK = valMei + valJuni + valJuli + valAgs;

        // Validation Rule: (Mei + Juni + Juli + Agustus == Kebutuhan TK Panen)
        var isTercukupi = (reqTk > 0 && accumTK === reqTk) || (reqTk === 0 && accumTK === 0);

        var rowClass = isTercukupi
          ? "bg-emerald-50/90 dark:bg-emerald-950/40 hover:bg-emerald-100/90 dark:hover:bg-emerald-900/60 border-b border-emerald-200 dark:border-emerald-900/50 text-slate-900 dark:text-white transition-colors"
          : "bg-red-50/90 dark:bg-red-950/40 hover:bg-red-100/90 dark:hover:bg-red-900/60 border-b border-red-200 dark:border-red-900/50 text-slate-900 dark:text-white transition-colors";

        html += '<tr class="' + rowClass + '">';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-500 dark:text-slate-400">' + (idx + 1) + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-800 dark:text-slate-200">' + (item.cro || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-700 dark:text-slate-300">' + (item.region || '-') + '</td>';
        html += '<td class="py-3 px-3 text-left font-black text-slate-900 dark:text-white min-w-[180px]">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-mono text-[11px] text-slate-500 font-semibold">' + (item.name_tag || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-amber-700 dark:text-amber-400">' + reqTk.toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center text-slate-600 dark:text-slate-400 font-medium">' + valMei.toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center text-slate-600 dark:text-slate-400 font-medium">' + valJuni.toLocaleString('id-ID') + '</td>';

        // Read-only Preview Cell: TK Juli
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-white bg-white/60 dark:bg-slate-900/50 border-x border-slate-200/60 dark:border-slate-800">' + valJuli.toLocaleString('id-ID') + '</td>';

        // Read-only Preview Cell: TK Agustus
        html += '<td class="py-3 px-2 text-center font-black text-slate-900 dark:text-white bg-white/60 dark:bg-slate-900/50 border-r border-slate-200/60 dark:border-slate-800">' + valAgs.toLocaleString('id-ID') + '</td>';

        // Action Cell: Edit Button with Indicator Badge
        html += '<td class="py-2 px-2 text-center">';
        html += '<button onclick="openEditKebunModal(' + item.id + ')" class="p-1.5 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors" title="Edit ' + (item.nama_kebun || '') + '">';
        html += '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>';
        html += '</button>';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // Large Fluid KPI Cards Grid Rendering
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

login_code = re.sub(old_render_fn, new_render_fn, login_code, flags=re.DOTALL)

# 1B. Update validateRealizationInput to display accumulation status in Sheet Edit Modal
old_val_fn = r'function validateRealizationInput\(inputEl\) \{.*?\n    \}'

new_val_fn = """function validateRealizationInput(inputEl) {
      if (!activeEditingKebunData) return true;
      var reqTk = parseInt(activeEditingKebunData.req_tk, 10) || 0;
      var item = activeEditingKebunData;

      var valMei = item.tk_mei || 0;
      var valJuni = item.tk_juni || 0;
      var currentEditingVal = parseFloat(document.getElementById("editTKRealisasiVal").value) || 0;

      // Calculate total accumulation based on currently selected month field
      var valJuli = activeSelectedMonthField === 'tk_juli' ? currentEditingVal : (activeEditingValues.tk_juli || item.tk_juli || 0);
      var valAgs = activeSelectedMonthField === 'tk_agustus' ? currentEditingVal : (activeEditingValues.tk_agustus || item.tk_agustus || 0);

      var accumTK = valMei + valJuni + valJuli + valAgs;

      var msgEl = document.getElementById("editTKValidationMsg");
      var msgText = document.getElementById("editTKValidationText");

      if (accumTK === reqTk && reqTk > 0) {
        if (inputEl) {
          inputEl.classList.remove("border-red-500", "text-red-600");
          inputEl.classList.add("border-emerald-600", "dark:border-emerald-400");
        }
        if (msgEl) {
          msgEl.className = "text-[11px] font-bold mt-1.5 text-emerald-700 dark:text-emerald-400 flex items-center gap-1 bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200 dark:border-emerald-900";
        }
        if (msgText) {
          msgText.innerHTML = "✅ <b>Tercukupi!</b> Akumulasi (Mei+Juni+Juli+Ags) = <b>" + accumTK + " / " + reqTk + " Orang</b>.";
        }
        return true;
      } else {
        if (inputEl) {
          inputEl.classList.add("border-red-500", "text-red-600");
          inputEl.classList.remove("border-slate-900", "dark:border-slate-100", "border-emerald-600");
        }
        if (msgEl) {
          msgEl.className = "text-[11px] font-bold mt-1.5 text-red-700 dark:text-red-400 flex items-center gap-1 bg-red-50 dark:bg-red-950/40 p-2.5 rounded-xl border border-red-200 dark:border-red-900";
        }
        var statusStr = accumTK < reqTk ? "Kurang " + (reqTk - accumTK) + " Orang" : "Kelebihan " + (accumTK - reqTk) + " Orang";
        if (msgText) {
          msgText.innerHTML = "⚠️ <b>Belum Sesuai (" + statusStr + ")!</b><br/>Akumulasi (Mei+Juni+Juli+Ags) = <b>" + accumTK + " / " + reqTk + " Orang</b>.";
        }
        return false;
      }
    }"""

login_code = re.sub(old_val_fn, new_val_fn, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("SUCCESSFULLY IMPLEMENTED ACCUMULATED TK VALIDATION (MEI+JUNI+JULI+AGS == REQ_TK) & ROW COLORING!")
