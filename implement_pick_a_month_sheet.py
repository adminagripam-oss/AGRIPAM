import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. REPLACE EDIT KEBUN FORM HTML IN LOGIN.HTML WITH PICK A MONTH DROPDOWN & SINGLE DYNAMIC INPUT
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

        <!-- Pick a Month Dropdown Selector -->
        <div>
          <label class="block text-xs font-bold text-slate-900 dark:text-white mb-1">Pilih Bulan Realisasi TK Panen</label>
          <select id="editSelectBulan" onchange="onEditMonthChange()"
            class="w-full px-3.5 py-2.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black dark:focus:ring-white shadow-sm">
            <option value="tk_juli">Bulan Juli 2026</option>
            <option value="tk_agustus">Bulan Agustus 2026</option>
            <option value="tk_september">Bulan September 2026</option>
            <option value="tk_oktober">Bulan Oktober 2026</option>
            <option value="tk_november">Bulan November 2026</option>
            <option value="tk_desember">Bulan Desember 2026</option>
          </select>
        </div>

        <!-- Single Dynamic Input Box for Selected Month -->
        <div>
          <label id="editInputBulanLabel" class="block text-xs font-bold text-slate-900 dark:text-white mb-1">Jumlah Realisasi TK Panen (Juli 2026)</label>
          <input type="number" min="0" id="editJumlahTKVal" oninput="onEditTKValChange(this.value)"
            class="w-full px-3.5 py-2.5 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black shadow-sm"
            placeholder="Masukkan jumlah TK..." />
        </div>
      </form>"""

content = re.sub(old_form_pattern, new_form_html, content, flags=re.DOTALL)

# 2. ADD JS FUNCTIONS FOR PICK A MONTH LOGIC
js_functions = """
    var activeEditingKebunData = null;
    var activeEditingValues = {};

    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k){ return k.id === id; });
      if (!item) return;

      activeEditingKebunData = item;
      var editObj = globalTKEdits[id] || {};
      
      activeEditingValues = {
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
      var monthName = selBulan.options[selBulan.selectedIndex].text;
      label.innerText = "Jumlah Realisasi TK Panen (" + monthName + ")";
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
    }
"""

if "function openEditKebunModal" not in content:
    content = content.replace("function filterTKPanenTable() {", js_functions + "\n    function filterTKPanenTable() {")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY IMPLEMENTED PICK A MONTH DROPDOWN & DYNAMIC INPUT IN SHEET EDIT DATA KEBUN!")
