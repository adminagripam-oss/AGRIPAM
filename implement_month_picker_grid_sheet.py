import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. REPLACE FORM IN EDIT KEBUN SHEET WITH MONTH PICKER GRID (Matching Image 2)
old_form_pattern = r'<form id="editKebunForm".*?</form>'

new_form_html = """<form id="editKebunForm" onsubmit="saveEditKebunForm(event)" class="py-6 space-y-4">
        <input type="hidden" id="editKebunId" />

        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nama Kebun</label>
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

        <!-- Section Realisasi TK Panen dengan Month Picker Grid -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3.5 shadow-xs">
          <div class="flex items-center justify-between">
            <label class="block text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">📌 REALISASI TK PANEN</label>
            <span id="editSelectedMonthBadge" class="text-[10px] font-bold px-2.5 py-0.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-md">Juli 2026</span>
          </div>
          
          <!-- Modern Month Picker Grid (12 Months) -->
          <div>
            <label class="block text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-2">Pilih Bulan Realisasi</label>
            <div id="monthPickerGrid" class="grid grid-cols-4 gap-2 bg-white dark:bg-slate-950 p-2.5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <button type="button" data-field="tk_januari" data-label="Januari 2026" onclick="selectMonthPicker('tk_januari', 'Januari 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Jan</button>
              <button type="button" data-field="tk_februari" data-label="Februari 2026" onclick="selectMonthPicker('tk_februari', 'Februari 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Feb</button>
              <button type="button" data-field="tk_maret" data-label="Maret 2026" onclick="selectMonthPicker('tk_maret', 'Maret 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Mar</button>
              <button type="button" data-field="tk_april" data-label="April 2026" onclick="selectMonthPicker('tk_april', 'April 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Apr</button>
              <button type="button" data-field="tk_mei" data-label="Mei 2026" onclick="selectMonthPicker('tk_mei', 'Mei 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">May</button>
              <button type="button" data-field="tk_juni" data-label="Juni 2026" onclick="selectMonthPicker('tk_juni', 'Juni 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Jun</button>
              <button type="button" data-field="tk_juli" data-label="Juli 2026" onclick="selectMonthPicker('tk_juli', 'Juli 2026', this)" class="month-btn py-2 px-1 text-xs font-black bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 rounded-xl shadow-md text-center">Jul</button>
              <button type="button" data-field="tk_agustus" data-label="Agustus 2026" onclick="selectMonthPicker('tk_agustus', 'Agustus 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Aug</button>
              <button type="button" data-field="tk_september" data-label="September 2026" onclick="selectMonthPicker('tk_september', 'September 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Sep</button>
              <button type="button" data-field="tk_oktober" data-label="Oktober 2026" onclick="selectMonthPicker('tk_oktober', 'Oktober 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Oct</button>
              <button type="button" data-field="tk_november" data-label="November 2026" onclick="selectMonthPicker('tk_november', 'November 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Nov</button>
              <button type="button" data-field="tk_desember" data-label="Desember 2026" onclick="selectMonthPicker('tk_desember', 'Desember 2026', this)" class="month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center">Dec</button>
            </div>
          </div>

          <!-- Input Box Dinamis untuk Bulan Terpilih -->
          <div>
            <label id="editInputBulanTitle" class="block text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">Jumlah Realisasi (Juli 2026)</label>
            <input type="number" min="0" id="editTKRealisasiVal" oninput="onMonthInputValueChange(this.value)"
              class="w-full px-3.5 py-2.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-xs"
              placeholder="Masukkan jumlah realisasi..." />
            <p id="editTKValidationMsg" class="text-[11px] font-semibold mt-1.5 text-slate-500 dark:text-slate-400 flex items-center gap-1">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span id="editTKValidationText">Maksimal pengisian: 0 Orang</span>
            </p>
          </div>
        </div>
      </form>"""

content = re.sub(old_form_pattern, new_form_html, content, flags=re.DOTALL)

# 2. UPDATE JS FUNCTIONS IN LOGIN.HTML FOR MONTH PICKER LOGIC
old_js_pattern = r'var activeEditingKebunData = null;.*?function saveEditKebunForm\(e\) \{.*?\n    \}'

new_js_code = """var activeEditingKebunData = null;
    var activeSelectedMonthField = 'tk_juli';
    var activeSelectedMonthLabel = 'Juli 2026';
    var activeEditingValues = {};

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};

      activeEditingValues = {
        tk_januari: editObj.tk_januari !== undefined ? editObj.tk_januari : (item.tk_januari || 0),
        tk_februari: editObj.tk_februari !== undefined ? editObj.tk_februari : (item.tk_februari || 0),
        tk_maret: editObj.tk_maret !== undefined ? editObj.tk_maret : (item.tk_maret || 0),
        tk_april: editObj.tk_april !== undefined ? editObj.tk_april : (item.tk_april || 0),
        tk_mei: editObj.tk_mei !== undefined ? editObj.tk_mei : (item.tk_mei || 0),
        tk_juni: editObj.tk_juni !== undefined ? editObj.tk_juni : (item.tk_juni || 0),
        tk_juli: editObj.tk_juli !== undefined ? editObj.tk_juli : (item.tk_juli || 0),
        tk_agustus: editObj.tk_agustus !== undefined ? editObj.tk_agustus : (item.tk_agustus || 0),
        tk_september: editObj.tk_september !== undefined ? editObj.tk_september : (item.tk_september || 0),
        tk_oktober: editObj.tk_oktober !== undefined ? editObj.tk_oktober : (item.tk_oktober || 0),
        tk_november: editObj.tk_november !== undefined ? editObj.tk_november : (item.tk_november || 0),
        tk_desember: editObj.tk_desember !== undefined ? editObj.tk_desember : (item.tk_desember || 0)
      };

      document.getElementById("editKebunId").value = id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || "-";
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + " Ha";

      var reqTk = parseInt(item.req_tk, 10) || 0;
      document.getElementById("editReqTK").value = reqTk.toLocaleString('id-ID') + " Orang";

      // Default select Juli 2026
      var defaultBtn = document.querySelector("#monthPickerGrid button[data-field='tk_juli']");
      selectMonthPicker('tk_juli', 'Juli 2026', defaultBtn);

      var sheet = document.getElementById("editKebunSheet");
      var backdrop = document.getElementById("editKebunBackdrop");
      if (sheet) sheet.classList.remove("hidden");
      if (backdrop) backdrop.classList.remove("hidden");
    }

    function selectMonthPicker(fieldKey, monthLabel, btnEl) {
      activeSelectedMonthField = fieldKey;
      activeSelectedMonthLabel = monthLabel;

      var allBtns = document.querySelectorAll("#monthPickerGrid .month-btn");
      allBtns.forEach(function(btn) {
        btn.className = "month-btn py-2 px-1 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all text-center";
      });

      if (btnEl) {
        btnEl.className = "month-btn py-2 px-1 text-xs font-black bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 rounded-xl shadow-md text-center";
      } else {
        var matchBtn = document.querySelector("#monthPickerGrid button[data-field='" + fieldKey + "']");
        if (matchBtn) matchBtn.className = "month-btn py-2 px-1 text-xs font-black bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 rounded-xl shadow-md text-center";
      }

      var badge = document.getElementById("editSelectedMonthBadge");
      if (badge) badge.innerText = monthLabel;

      var title = document.getElementById("editInputBulanTitle");
      if (title) title.innerText = "Jumlah Realisasi (" + monthLabel + ")";

      var valInput = document.getElementById("editTKRealisasiVal");
      if (valInput) {
        var currentVal = activeEditingValues[fieldKey] !== undefined ? activeEditingValues[fieldKey] : 0;
        valInput.value = currentVal;
        validateRealizationInput(valInput);
      }
    }

    function onMonthInputValueChange(val) {
      var numVal = Math.max(0, parseFloat(val) || 0);
      activeEditingValues[activeSelectedMonthField] = numVal;
      var valInput = document.getElementById("editTKRealisasiVal");
      validateRealizationInput(valInput);
    }

    function closeEditKebunModal() {
      var sheet = document.getElementById("editKebunSheet");
      var backdrop = document.getElementById("editKebunBackdrop");
      if (sheet) sheet.classList.add("hidden");
      if (backdrop) backdrop.classList.add("hidden");
    }

    function validateRealizationInput(inputEl) {
      if (!inputEl || !activeEditingKebunData) return true;
      var reqTk = parseInt(activeEditingKebunData.req_tk, 10) || 0;
      var val = parseFloat(inputEl.value) || 0;
      var msgEl = document.getElementById("editTKValidationMsg");
      var msgText = document.getElementById("editTKValidationText");

      if (val > reqTk) {
        inputEl.classList.add("border-red-500", "text-red-600");
        inputEl.classList.remove("border-slate-900", "dark:border-slate-100");
        if (msgEl) {
          msgEl.className = "text-[11px] font-bold mt-1.5 text-red-600 dark:text-red-400 flex items-center gap-1";
        }
        if (msgText) {
          msgText.innerText = "⚠️ Melebihi batas! Maksimal pengisian " + activeSelectedMonthLabel + " hanya " + reqTk.toLocaleString('id-ID') + " Orang.";
        }
        return false;
      } else {
        inputEl.classList.remove("border-red-500", "text-red-600");
        inputEl.classList.add("border-slate-900", "dark:border-slate-100");
        if (msgEl) {
          msgEl.className = "text-[11px] font-semibold mt-1.5 text-slate-500 dark:text-slate-400 flex items-center gap-1";
        }
        if (msgText) {
          msgText.innerText = "Maksimal pengisian " + activeSelectedMonthLabel + ": " + reqTk.toLocaleString('id-ID') + " Orang (sesuai Kebutuhan Tenaga Panen)";
        }
        return true;
      }
    }

    function saveEditKebunForm(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!activeEditingKebunData) return;

      var id = activeEditingKebunData.id;
      var reqTk = parseInt(activeEditingKebunData.req_tk, 10) || 0;
      var valInput = document.getElementById("editTKRealisasiVal");
      var val = parseFloat(valInput ? valInput.value : 0) || 0;

      if (val > reqTk) {
        alert("⚠️ Pengisian Gagal: Realisasi TK Panen (" + val + " Orang) tidak boleh melebihi Kebutuhan Tenaga Panen (" + reqTk + " Orang)!");
        valInput.focus();
        return;
      }

      if (!globalTKEdits[id]) globalTKEdits[id] = {};

      Object.keys(activeEditingValues).forEach(function(fKey) {
        globalTKEdits[id][fKey] = activeEditingValues[fKey];
      });

      closeEditKebunModal();
      simpanTKPanenEdits();
    }"""

content = re.sub(old_js_pattern, new_js_code, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY IMPLEMENTED MONTH PICKER GRID (12 MONTHS JAN-DEC) IN LOGIN.HTML!")
