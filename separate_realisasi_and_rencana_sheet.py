import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. REPLACE EDIT KEBUN FORM WITH TWO SEPARATE SECTIONS (REALISASI & RENCANA)
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

        <!-- Section 1: Realisasi TK Panen (H-1 Bulan: Juli 2026) -->
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
            <input type="number" min="0" id="editTKRealisasiVal"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-xs"
              placeholder="Masukkan jumlah realisasi..." />
          </div>
        </div>

        <!-- Section 2: Rencana TK Panen (H+1 Bulan: September 2026) -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3 shadow-xs">
          <div class="flex items-center justify-between">
            <label class="block text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">🎯 Rencana TK Panen</label>
            <span class="text-[10px] font-bold px-2 py-0.5 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 rounded-md">H+1 Bulan (September)</span>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-500 dark:text-slate-400 mb-1">Pilih Bulan Rencana</label>
            <select id="editSelectBulanRencana"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:ring-2 focus:ring-black">
              <option value="target_september" selected>Bulan September 2026 (H+1 Rencana)</option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">Jumlah Rencana (Orang)</label>
            <input type="number" min="0" id="editTKRencanaVal"
              class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-xs"
              placeholder="Masukkan jumlah rencana..." />
          </div>
        </div>
      </form>"""

content = re.sub(old_form_pattern, new_form_html, content, flags=re.DOTALL)

# 2. UPDATE JS FUNCTIONS FOR SEPARATE SECTIONS
old_js_pattern = r'var activeEditingKebunData = null;.*?function saveEditKebunForm\(e\) \{.*?\n    \}'

new_js_code = """var activeEditingKebunData = null;

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};

      var realisasiVal = editObj.tk_juli !== undefined ? editObj.tk_juli : (item.tk_juli || 0);
      var rencanaVal = editObj.target_september !== undefined ? editObj.target_september : (item.target_september || item.tk_september || 0);

      document.getElementById("editKebunId").value = id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || "-";
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + " Ha";

      document.getElementById("editTKRealisasiVal").value = realisasiVal;
      document.getElementById("editTKRencanaVal").value = rencanaVal;

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

    function saveEditKebunForm(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!activeEditingKebunData) return;

      var id = activeEditingKebunData.id;
      if (!globalTKEdits[id]) globalTKEdits[id] = {};

      var realInput = document.getElementById("editTKRealisasiVal");
      var rencInput = document.getElementById("editTKRencanaVal");

      globalTKEdits[id].tk_juli = Math.max(0, parseFloat(realInput.value) || 0);
      globalTKEdits[id].target_september = Math.max(0, parseFloat(rencInput.value) || 0);

      closeEditKebunModal();
      simpanTKPanenEdits();
    }"""

content = re.sub(old_js_pattern, new_js_code, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY SEPARATED REALISASI AND RENCANA IN SHEET EDIT DATA KEBUN!")
