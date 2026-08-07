file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Edit Kebun Sheet Modal HTML
edit_modal_html = """
    <!-- Edit Kebun Sheet Modal (Shadcn Pattern) -->
    <div id="editKebunBackdrop" onclick="closeEditKebunModal()" class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 hidden transition-opacity"></div>
    <div id="editKebunSheet" class="fixed top-0 right-0 bottom-0 w-full max-w-md bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 z-50 hidden shadow-2xl p-6 flex flex-col justify-between overflow-y-auto">
      <div>
        <div class="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
          <div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white">Edit Data Kebun</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1" id="editKebunSubtitle">Lakukan perubahan data kebun di sini. Klik simpan jika sudah selesai.</p>
          </div>
          <button onclick="closeEditKebunModal()" class="p-2 rounded-xl text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <form id="editKebunForm" onsubmit="saveEditKebunForm(event)" class="py-6 space-y-4">
          <input type="hidden" id="editKebunId" />
          
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nama Kebun</label>
            <input type="text" id="editNamaKebun" class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-extrabold text-slate-900 dark:text-white focus:ring-2 focus:ring-black dark:focus:ring-white" readonly />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Luasan Lahan (Ha)</label>
            <input type="text" id="editLuasanLahan" class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300" readonly />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-900 dark:text-white mb-1">TK Panen Juli (Col I)</label>
              <input type="number" min="0" id="editTKPanenJuli" class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black" />
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-900 dark:text-white mb-1">TK Panen Agustus (Col J)</label>
              <input type="number" min="0" id="editTKPanenAgustus" class="w-full px-3.5 py-2 bg-white dark:bg-slate-950 border-2 border-slate-900 dark:border-slate-100 rounded-xl text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-black" />
            </div>
          </div>
        </form>
      </div>

      <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end gap-3">
        <button type="button" onclick="closeEditKebunModal()" class="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">
          Batal
        </button>
        <button type="button" onclick="saveEditKebunForm()" class="px-5 py-2 bg-slate-900 hover:bg-black text-white dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white rounded-xl text-xs font-black shadow-md transition-all">
          Simpan Perubahan
        </button>
      </div>
    </div>"""

if 'id="editKebunSheet"' not in content:
    content = content.replace('</body>', edit_modal_html + '\n</body>')

# 2. Add JS functions for openEditKebunModal and saveEditKebunForm
js_edit_modal = """
    function openEditKebunModal(id) {
      var item = (globalTKData || []).find(function(k) { return k.id === id; });
      if (!item) return;

      var edit = globalTKEdits[id] || {};
      var valJuli = edit.tk_juli !== undefined ? edit.tk_juli : (item.tk_juli || 0);
      var valAgs = edit.tk_agustus !== undefined ? edit.tk_agustus : (item.tk_agustus || 0);

      document.getElementById("editKebunId").value = item.id;
      document.getElementById("editNamaKebun").value = item.nama_kebun || '-';
      document.getElementById("editLuasanLahan").value = (item.luasan || 0).toLocaleString('id-ID') + ' Ha';
      document.getElementById("editTKPanenJuli").value = valJuli;
      document.getElementById("editTKPanenAgustus").value = valAgs;

      document.getElementById("editKebunBackdrop").classList.remove("hidden");
      document.getElementById("editKebunSheet").classList.remove("hidden");
    }

    function closeEditKebunModal() {
      document.getElementById("editKebunBackdrop").classList.add("hidden");
      document.getElementById("editKebunSheet").classList.add("hidden");
    }

    function saveEditKebunForm(e) {
      if (e) e.preventDefault();
      var id = parseInt(document.getElementById("editKebunId").value);
      var juli = parseInt(document.getElementById("editTKPanenJuli").value) || 0;
      var ags = parseInt(document.getElementById("editTKPanenAgustus").value) || 0;

      onTKInputChange(id, 'tk_juli', juli);
      onTKInputChange(id, 'tk_agustus', ags);

      closeEditKebunModal();
    }"""

if 'function openEditKebunModal' not in content:
    content = content.replace('function renderTKPanenTable', js_edit_modal + '\n\n    function renderTKPanenTable')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY ADDED EDIT KEBUN SHEET MODAL IN LOGIN.HTML!")
