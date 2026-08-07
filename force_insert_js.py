file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

js_code = """
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

anchor = "function filterTKPanenTable() {"
if anchor in content:
    content = content.replace(anchor, js_code + "\n    " + anchor)
    print("REPLACED ANCHOR SUCCESSFULLY!")
else:
    print("ANCHOR NOT FOUND!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
