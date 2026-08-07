import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the form inside editKebunSheet
old_form_pattern = r'<form id="editKebunForm".*?</form>'

new_form_html = """<form id="editKebunForm" onsubmit="saveEditKebunForm(event)" class="py-6 space-y-4">
        <input type="hidden" id="editKebunId" />

        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nama Kebun</label>
          <input type="text" id="editNamaKebun"
            class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-extrabold text-slate-900 dark:text-white"
            readonly />
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Luasan Lahan (Ha)</label>
          <input type="text" id="editLuasanLahan"
            class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300"
            readonly />
        </div>

        <!-- Strict Month Rules Selector (H-1 Realisasi & H+1 Rencana) -->
        <div>
          <label class="block text-xs font-bold text-slate-900 dark:text-white mb-1">Pilih Jenis & Bulan Pengisian</label>
          <select id="editSelectBulan" onchange="onEditMonthChange()"
            class="w-full px-3.5 py-2.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black dark:focus:ring-white shadow-sm">
            <option value="tk_juli">📌 Realisasi TK Panen — Juli 2026 (H-1 Bulan)</option>
            <option value="target_september">🎯 Rencana TK Panen — September 2026 (H+1 Bulan)</option>
          </select>
          <p class="text-[11px] font-semibold text-amber-700 dark:text-amber-400 mt-1.5 flex items-center gap-1.5 bg-amber-50 dark:bg-amber-950/40 p-2.5 rounded-lg border border-amber-200 dark:border-amber-900">
            <svg class="w-4 h-4 flex-shrink-0 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Bulan Berjalan: <b>Agustus 2026</b>.<br/>• Realisasi hanya untuk <b>H-1 (Juli)</b>.<br/>• Rencana hanya untuk <b>H+1 (September)</b>.</span>
          </p>
        </div>

        <!-- Single Dynamic Input Box for Selected Mode & Month -->
        <div>
          <label id="editInputBulanLabel" class="block text-xs font-bold text-slate-900 dark:text-white mb-1">
            Jumlah Realisasi TK Panen (Juli 2026)
          </label>
          <input type="number" min="0" id="editJumlahTKVal" oninput="onEditTKValChange(this.value)"
            class="w-full px-3.5 py-2.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-sm"
            placeholder="Masukkan jumlah TK..." />
        </div>
      </form>"""

content = re.sub(old_form_pattern, new_form_html, content, flags=re.DOTALL)

# 2. Update JS functions for openEditKebunModal, onEditMonthChange, saveEditKebunForm
old_js_pattern = r'var activeEditingKebunData = null;.*?function saveEditKebunForm\(e\) \{.*?\n    \}'

new_js_code = """var activeEditingKebunData = null;
    var activeEditingValues = {};

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};
      
      activeEditingValues = {
        tk_juli: editObj.tk_juli !== undefined ? editObj.tk_juli : (item.tk_juli || 0),
        target_september: editObj.target_september !== undefined ? editObj.target_september : (item.target_september || item.tk_september || 0)
      };

      document.getElementById("editKebunId").value = id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || "-";
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + " Ha";

      var selBulan = document.getElementById("editSelectBulan");
      if (selBulan) selBulan.value = "tk_juli";

      onEditMonthChange();

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

    function onEditMonthChange() {
      var selBulan = document.getElementById("editSelectBulan");
      var label = document.getElementById("editInputBulanLabel");
      var input = document.getElementById("editJumlahTKVal");
      if (!selBulan || !label || !input) return;

      var field = selBulan.value;
      if (field === 'tk_juli') {
        label.innerText = "Jumlah Realisasi TK Panen (Juli 2026 - H-1 Bulan)";
      } else {
        label.innerText = "Jumlah Rencana TK Panen (September 2026 - H+1 Bulan)";
      }
      input.value = activeEditingValues[field] !== undefined ? activeEditingValues[field] : 0;
    }

    function onEditTKValChange(val) {
      var selBulan = document.getElementById("editSelectBulan");
      if (!selBulan) return;
      var field = selBulan.value;
      activeEditingValues[field] = Math.max(0, parseFloat(val) || 0);
    }

    function saveEditKebunForm(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!activeEditingKebunData) return;

      var id = activeEditingKebunData.id;
      if (!globalTKEdits[id]) globalTKEdits[id] = {};

      Object.keys(activeEditingValues).forEach(function(field) {
        globalTKEdits[id][field] = activeEditingValues[field];
      });

      closeEditKebunModal();
      simpanTKPanenEdits();
    }"""

content = re.sub(old_js_pattern, new_js_code, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY IMPLEMENTED STRICT MONTH RULES (H-1 JULI REALISASI & H+1 SEPTEMBER RENCANA)!")
