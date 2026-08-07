import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Edit Kebun Form HTML (Remove Rencana TK Panen, add Kebutuhan TK indicator & validation)
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

        <!-- Section Realisasi TK Panen (H-1 Bulan: Juli 2026) -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3 shadow-xs">
          <div class="flex items-center justify-between">
            <label class="block text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">📌 Realisasi TK Panen</label>
            <span class="text-[10px] font-bold px-2 py-0.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-md">H-1 Bulan (Juli)</span>
          </div>
          
          <div>
            <label class="block text-[11px] font-bold text-slate-500 dark:text-slate-400 mb-1">Pilih Bulan Realisasi</label>
            <select id="editSelectBulanRealisasi"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:ring-2 focus:ring-black">
              <option value="tk_juli" selected>Bulan Juli 2026 (H-1 Cut-Off)</option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">Jumlah Realisasi (Orang)</label>
            <input type="number" min="0" id="editTKRealisasiVal" oninput="validateRealizationInput(this)"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-xs"
              placeholder="Masukkan jumlah realisasi..." />
            <p id="editTKValidationMsg" class="text-[11px] font-semibold mt-1.5 text-slate-500 dark:text-slate-400 flex items-center gap-1">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span id="editTKValidationText">Maksimal pengisian: 0 Orang</span>
            </p>
          </div>
        </div>
      </form>"""

content = re.sub(old_form_pattern, new_form_html, content, flags=re.DOTALL)

# Replace JS Functions in login.html
old_js_pattern = r'var activeEditingKebunData = null;.*?function saveEditKebunForm\(e\) \{.*?\n    \}'

new_js_code = """var activeEditingKebunData = null;

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};
      var realisasiVal = editObj.tk_juli !== undefined ? editObj.tk_juli : (item.tk_juli || 0);

      document.getElementById("editKebunId").value = id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || "-";
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + " Ha";
      
      var reqTk = parseInt(item.req_tk, 10) || 0;
      document.getElementById("editReqTK").value = reqTk.toLocaleString('id-ID') + " Orang";

      var valInput = document.getElementById("editTKRealisasiVal");
      if (valInput) {
        valInput.value = realisasiVal;
        valInput.max = reqTk;
      }

      var msgText = document.getElementById("editTKValidationText");
      if (msgText) {
        msgText.innerText = "Maksimal pengisian: " + reqTk.toLocaleString('id-ID') + " Orang (sesuai Kebutuhan Tenaga Panen)";
      }

      validateRealizationInput(valInput);

      var sheet = document.getElementById("editKebunSheet");
      var backdrop = document.getElementById("editKebunBackdrop");
      if (sheet) sheet.classList.remove("hidden");
      if (backdrop) backdrop.classList.remove("hidden");
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
          msgText.innerText = "⚠️ Melebihi batas! Maksimal pengisian hanya " + reqTk.toLocaleString('id-ID') + " Orang.";
        }
        return false;
      } else {
        inputEl.classList.remove("border-red-500", "text-red-600");
        inputEl.classList.add("border-slate-900", "dark:border-slate-100");
        if (msgEl) {
          msgEl.className = "text-[11px] font-semibold mt-1.5 text-slate-500 dark:text-slate-400 flex items-center gap-1";
        }
        if (msgText) {
          msgText.innerText = "Maksimal pengisian: " + reqTk.toLocaleString('id-ID') + " Orang (sesuai Kebutuhan Tenaga Panen)";
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
      globalTKEdits[id].tk_juli = Math.max(0, val);

      closeEditKebunModal();
      simpanTKPanenEdits();
    }"""

content = re.sub(old_js_pattern, new_js_code, content, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY UPDATED LOGIN.HTML WITH REALISASI LIMIT VALIDATION!")


# 2. UPDATE API/KEBUNTK.JS BACKEND VALIDATION
api_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\api\kebunTK.js'

with open(api_path, 'r', encoding='utf-8') as f:
    api_code = f.read()

old_tk_update = r'if \(edit\.tk_juli !== undefined && edit\.tk_juli !== null\) \{\s+item\.tk_juli = Math\.max\(0, parseFloat\(edit\.tk_juli\) \|\| 0\);\s+\}'

new_tk_update = """if (edit.tk_juli !== undefined && edit.tk_juli !== null) {
            const maxReq = parseInt(item.req_tk, 10) || 0;
            const inputVal = Math.max(0, parseFloat(edit.tk_juli) || 0);
            item.tk_juli = Math.min(maxReq, inputVal);
          }"""

api_code = re.sub(old_tk_update, new_tk_update, api_code)

with open(api_path, 'w', encoding='utf-8') as f:
    f.write(api_code)

print("SUCCESSFULLY UPDATED API/KEBUNTK.JS BACKEND VALIDATION!")
