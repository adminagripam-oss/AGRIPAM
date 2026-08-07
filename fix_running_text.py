with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate and replace inside updateRunningText
old_block = """      // If user has selected a date in the form, use that instead
      var tanggalEl = document.getElementById("tanggal");
      if (tanggalEl && tanggalEl.value) {
        tanggal = tanggalEl.value;
      }

      var isToday = (tanggal === todayDateStr);"""

new_block = """      // If user has selected a date in the form, use that instead
      var tanggalEl = document.getElementById("tanggal");
      if (tanggalEl && tanggalEl.value) {
        tanggal = tanggalEl.value;
      }
      var tanggal_akhir = tanggal; // Fix ReferenceError

      var isToday = (tanggal === todayDateStr);"""

content = content.replace(old_block, new_block)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed updateRunningText ReferenceError successfully.")
