import re

login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# 1. UPDATE STATIC THEAD IN LOGIN.HTML TO MATCH EXCEL COLS A-L (13 COLUMNS + NO)
old_thead_pattern = r'<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">.*?</thead>'

new_thead_html = """<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">
                  <tr class="text-[10px] font-black uppercase tracking-wider text-white">
                    <th class="py-3.5 px-2 text-center w-8 font-black">No</th>
                    <th class="py-3.5 px-2 text-center font-black">CRO</th>
                    <th class="py-3.5 px-2 text-center font-black">Wilayah</th>
                    <th class="py-3.5 px-3 text-left font-black min-w-[170px]">Nama Kebun / PT HO</th>
                    <th class="py-3.5 px-2 text-center font-black">Tag</th>
                    <th class="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                    <th class="py-3.5 px-2 text-center font-black whitespace-nowrap bg-amber-950/60 text-amber-200">Kebutuhan TK</th>
                    <th class="py-3.5 px-2 text-center font-black text-slate-300">Realisasi Mei</th>
                    <th class="py-3.5 px-2 text-center font-black bg-blue-900/80 text-blue-100 border-x border-blue-700">Realisasi Juni (Col H)</th>
                    <th class="py-3.5 px-2 text-center font-black bg-emerald-900/80 text-emerald-100 border-r border-emerald-700">Rencana Juli (Col I)</th>
                    <th class="py-3.5 px-2 text-center font-black bg-emerald-900/80 text-emerald-100 border-r border-emerald-700">Rencana Ags (Col J)</th>
                    <th class="py-3.5 px-2 text-center font-black text-slate-300">Realisasi Juli</th>
                    <th class="py-3.5 px-2 text-center font-black text-slate-300">Realisasi Ags</th>
                    <th class="py-3.5 px-2 text-center font-black">AKSI</th>
                  </tr>
                </thead>"""

login_code = re.sub(old_thead_pattern, new_thead_html, login_code, flags=re.DOTALL)
login_code = login_code.replace('colspan="12"', 'colspan="14"')

# 2. UPDATE renderTKPanenTable IN LOGIN.HTML WITH (Col H + Col I + Col J >= req_tk) ROW COLORING
old_render_fn = r'function renderTKPanenTable\(items, summary\) \{.*?\n    \}'

new_render_fn = """function renderTKPanenTable(items, summary) {
      var tbody = document.getElementById("tkPanenTableBody");
      if (!tbody) return;

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="14" class="py-12 text-center text-slate-500 font-medium">Tidak ada data kebun.</td></tr>';
        return;
      }

      var html = "";
      items.forEach(function (item, idx) {
        var edit = globalTKEdits[item.id] || {};

        var valMei = item.tk_mei || 0;
        var valJuni = edit.tk_juni !== undefined ? edit.tk_juni : (item.tk_juni || 0);
        var targetJuli = edit.target_juli !== undefined ? edit.target_juli : (item.target_juli || 0);
        var targetAgs = edit.target_agustus !== undefined ? edit.target_agustus : (item.target_agustus || 0);
        var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
        var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

        var reqTk = parseInt(item.req_tk, 10) || 0;

        // Formula Rule: (Realisasi Juni [H] + Rencana Juli [I] + Rencana Ags [J] >= Kebutuhan TK Panen)
        var sumThreeCols = valJuni + targetJuli + targetAgs;
        var isTercukupi = (sumThreeCols >= reqTk);

        // Soft Green if sumThreeCols >= reqTk, Soft Red if sumThreeCols < reqTk
        var rowClass = isTercukupi
          ? "bg-emerald-50/90 dark:bg-emerald-950/40 hover:bg-emerald-100/90 dark:hover:bg-emerald-900/60 border-b border-emerald-200 dark:border-emerald-900/50 text-slate-900 dark:text-white transition-colors"
          : "bg-red-50/90 dark:bg-red-950/40 hover:bg-red-100/90 dark:hover:bg-red-900/60 border-b border-red-200 dark:border-red-900/50 text-slate-900 dark:text-white transition-colors";

        html += '<tr class="' + rowClass + '">';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-500 dark:text-slate-400">' + (idx + 1) + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-slate-800 dark:text-slate-200">' + (item.cro || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold text-slate-700 dark:text-slate-300">' + (item.region || '-') + '</td>';
        html += '<td class="py-3 px-3 text-left font-black text-slate-900 dark:text-white min-w-[170px]">' + (item.nama_kebun || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-mono text-[11px] text-slate-500 font-semibold">' + (item.name_tag || '-') + '</td>';
        html += '<td class="py-3 px-2 text-center font-bold">' + (item.luasan || 0).toLocaleString('id-ID') + '</td>';
        html += '<td class="py-3 px-2 text-center font-black text-amber-800 dark:text-amber-300 bg-amber-50/50 dark:bg-amber-950/30">' + reqTk.toLocaleString('id-ID') + '</td>';

        // Read-only Realisasi Mei
        html += '<td class="py-3 px-2 text-center text-slate-600 dark:text-slate-400 font-medium">' + valMei.toLocaleString('id-ID') + '</td>';

        // Editable Col H: Realisasi TK Panen Juni
        html += '<td class="py-3 px-2 text-center font-black text-blue-900 dark:text-blue-200 bg-blue-50/60 dark:bg-blue-950/40 border-x border-blue-200 dark:border-blue-900">' + valJuni.toLocaleString('id-ID') + '</td>';

        // Editable Col I: Rencana Pemenuhan TK Panen Juli
        html += '<td class="py-3 px-2 text-center font-black text-emerald-900 dark:text-emerald-200 bg-emerald-100/50 dark:bg-emerald-950/50 border-r border-emerald-200 dark:border-emerald-900">' + targetJuli.toLocaleString('id-ID') + '</td>';

        // Editable Col J: Rencana Pemenuhan TK Panen Agustus
        html += '<td class="py-3 px-2 text-center font-black text-emerald-900 dark:text-emerald-200 bg-emerald-100/50 dark:bg-emerald-950/50 border-r border-emerald-200 dark:border-emerald-900">' + targetAgs.toLocaleString('id-ID') + '</td>';

        // Read-only Realisasi Juli
        html += '<td class="py-3 px-2 text-center font-medium text-slate-700 dark:text-slate-300">' + valJuli.toLocaleString('id-ID') + '</td>';

        // Read-only Realisasi Agustus
        html += '<td class="py-3 px-2 text-center font-medium text-slate-700 dark:text-slate-300">' + valAgs.toLocaleString('id-ID') + '</td>';

        // Action Cell: Edit Button
        html += '<td class="py-2 px-2 text-center">';
        html += '<button onclick="openEditKebunModal(' + item.id + ')" class="p-1.5 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors" title="Edit ' + (item.nama_kebun || '') + '">';
        html += '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>';
        html += '</button>';
        html += '</td>';

        html += '</tr>';
      });

      tbody.innerHTML = html;

      // KPI Badges
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

# 3. UPDATE FORM IN EDIT KEBUN SHEET TO EDIT COL H (tk_juni), COL I (target_juli), COL J (target_agustus)
old_form_pattern = r'<form id="editKebunForm".*?</form>'

new_form_html = """<form id="editKebunForm" onsubmit="saveEditKebunForm(event)" class="py-6 space-y-4">
        <input type="hidden" id="editKebunId" />

        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nama Kebun / PT HO</label>
          <input type="text" id="editNamaKebun"
            class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-extrabold text-slate-900 dark:text-white"
            readonly />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Luasan Lahan (Ha)</label>
            <input type="text" id="editLuasanLahan"
              class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300"
              readonly />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Kebutuhan TK Panen</label>
            <input type="text" id="editReqTK"
              class="w-full px-3.5 py-2 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700 rounded-xl text-xs font-black text-amber-900 dark:text-amber-200"
              readonly />
          </div>
        </div>

        <!-- Form Edit 3 Kolom Utama (Col H, Col I, Col J) -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3.5 shadow-xs">
          <div class="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-700">
            <label class="block text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">📌 PENGISIAN KOLOM H, I, J</label>
            <span class="text-[10px] font-bold px-2.5 py-0.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-md">Col H, I, J</span>
          </div>

          <!-- Col H: Realisasi TK Panen Juni -->
          <div>
            <label class="block text-[11px] font-extrabold text-blue-900 dark:text-blue-300 mb-1">Col H: Realisasi TK Panen Juni (Orang)</label>
            <input type="number" min="0" id="editTKJuniVal" oninput="calculateThreeColSum()"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border border-blue-300 dark:border-blue-700 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 shadow-xs"
              placeholder="Masukkan realisasi Juni..." />
          </div>

          <!-- Col I: Rencana Pemenuhan TK Panen Juli -->
          <div>
            <label class="block text-[11px] font-extrabold text-emerald-900 dark:text-emerald-300 mb-1">Col I: Rencana Pemenuhan TK Panen Juli (Orang)</label>
            <input type="number" min="0" id="editTargetJuliVal" oninput="calculateThreeColSum()"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border border-emerald-300 dark:border-emerald-700 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 shadow-xs"
              placeholder="Masukkan rencana Juli..." />
          </div>

          <!-- Col J: Rencana Pemenuhan TK Panen Agustus -->
          <div>
            <label class="block text-[11px] font-extrabold text-emerald-900 dark:text-emerald-300 mb-1">Col J: Rencana Pemenuhan TK Panen Agustus (Orang)</label>
            <input type="number" min="0" id="editTargetAgsVal" oninput="calculateThreeColSum()"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border border-emerald-300 dark:border-emerald-700 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 shadow-xs"
              placeholder="Masukkan rencana Agustus..." />
          </div>

          <!-- Status Card Indicator -->
          <div id="threeColValidationMsg" class="text-[11px] font-bold mt-2 p-3 rounded-xl border flex flex-col gap-1 transition-all">
            <span id="threeColValidationText">Perhitungan akumulasi 3 kolom...</span>
          </div>
        </div>
      </form>"""

login_code = re.sub(old_form_pattern, new_form_html, login_code, flags=re.DOTALL)

# 4. UPDATE JS MODAL FUNCTIONS IN LOGIN.HTML
old_modal_js = r'var activeEditingKebunData = null;.*?function filterTKPanenTable\(\) \{'

new_modal_js = """var activeEditingKebunData = null;

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};

      document.getElementById("editKebunId").value = id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || "-";
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + " Ha";

      var reqTk = parseInt(item.req_tk, 10) || 0;
      document.getElementById("editReqTK").value = reqTk.toLocaleString('id-ID') + " Orang";

      var valJuni = editObj.tk_juni !== undefined ? editObj.tk_juni : (item.tk_juni || 0);
      var targetJuli = editObj.target_juli !== undefined ? editObj.target_juli : (item.target_juli || 0);
      var targetAgs = editObj.target_agustus !== undefined ? editObj.target_agustus : (item.target_agustus || 0);

      document.getElementById("editTKJuniVal").value = valJuni;
      document.getElementById("editTargetJuliVal").value = targetJuli;
      document.getElementById("editTargetAgsVal").value = targetAgs;

      calculateThreeColSum();

      var sheet = document.getElementById("editKebunSheet");
      var backdrop = document.getElementById("editKebunBackdrop");
      if (sheet) sheet.classList.remove("hidden");
      if (backdrop) backdrop.classList.remove("hidden");
    }

    function calculateThreeColSum() {
      if (!activeEditingKebunData) return;

      var reqTk = parseInt(activeEditingKebunData.req_tk, 10) || 0;

      var vJuni = parseFloat(document.getElementById("editTKJuniVal").value) || 0;
      var vTarJuli = parseFloat(document.getElementById("editTargetJuliVal").value) || 0;
      var vTarAgs = parseFloat(document.getElementById("editTargetAgsVal").value) || 0;

      var sumThree = vJuni + vTarJuli + vTarAgs;

      var msgEl = document.getElementById("threeColValidationMsg");
      var msgText = document.getElementById("threeColValidationText");

      if (sumThree >= reqTk) {
        if (msgEl) {
          msgEl.className = "text-[11px] font-bold mt-2 text-emerald-800 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 p-3 rounded-xl border border-emerald-300 dark:border-emerald-900 shadow-xs";
        }
        if (msgText) {
          msgText.innerHTML = "✅ <b>TERCUKUPI (Warna Baris Hijau)!</b><br/>Jumlah Col H + I + J = <b>" + sumThree + " / " + reqTk + " Orang</b> (Sudah ≥ Kebutuhan).";
        }
      } else {
        if (msgEl) {
          msgEl.className = "text-[11px] font-bold mt-2 text-red-800 dark:text-red-300 bg-red-50 dark:bg-red-950/40 p-3 rounded-xl border border-red-300 dark:border-red-900 shadow-xs";
        }
        var diff = reqTk - sumThree;
        if (msgText) {
          msgText.innerHTML = "⚠️ <b>BELUM TERCUKUPI (Warna Baris Merah)!</b><br/>Jumlah Col H + I + J = <b>" + sumThree + " / " + reqTk + " Orang</b> (Kurang " + diff + " Orang).";
        }
      }
    }

    function closeEditKebunModal() {
      var sheet = document.getElementById("editKebunSheet");
      var backdrop = document.getElementById("editKebunBackdrop");
      if (sheet) sheet.classList.add("hidden");
      if (backdrop) backdrop.classList.add("hidden");
    }

    function saveEditKebunForm(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!activeEditingKebunData) return;

      var id = activeEditingKebunData.id;
      var vJuni = Math.max(0, parseFloat(document.getElementById("editTKJuniVal").value) || 0);
      var vTarJuli = Math.max(0, parseFloat(document.getElementById("editTargetJuliVal").value) || 0);
      var vTarAgs = Math.max(0, parseFloat(document.getElementById("editTargetAgsVal").value) || 0);

      if (!globalTKEdits[id]) globalTKEdits[id] = {};
      globalTKEdits[id].tk_juni = vJuni;
      globalTKEdits[id].target_juli = vTarJuli;
      globalTKEdits[id].target_agustus = vTarAgs;

      closeEditKebunModal();

      // Instant Re-render Table on Screen
      renderTKPanenTable(globalTKData, currentSummaryData);

      // Save to Backend Database
      simpanTKPanenEdits();
    }

    function filterTKPanenTable() {"""

login_code = re.sub(old_modal_js, new_modal_js, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("SUCCESSFULLY IMPLEMENTED EXCEL COLS H, I, J TABLE STRUCTURE AND FORMULA (COL H + I + J >= REQ_TK) IN LOGIN.HTML!")
