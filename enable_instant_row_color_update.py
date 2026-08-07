import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update saveEditKebunForm to re-render table instantly on screen
old_save_fn = r'function saveEditKebunForm\(e\) \{.*?\n    \}'

new_save_fn = """function saveEditKebunForm(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!activeEditingKebunData) return;

      var id = activeEditingKebunData.id;
      if (!globalTKEdits[id]) globalTKEdits[id] = {};

      Object.keys(activeEditingValues).forEach(function(fKey) {
        globalTKEdits[id][fieldKey || fKey] = activeEditingValues[fKey];
      });

      closeEditKebunModal();

      // Instant Re-render Table on Screen (Row color changes instantly to Soft Green if exact!)
      renderTKPanenTable(globalTKData, currentSummaryData);

      // Save to Backend Database
      simpanTKPanenEdits();
    }"""

content = re.sub(old_save_fn, new_save_fn, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY ENABLED INSTANT ROW COLOR UPDATE ON EDIT IN LOGIN.HTML!")
