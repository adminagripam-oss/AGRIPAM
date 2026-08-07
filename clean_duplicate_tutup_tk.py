import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace multiple duplicate tutupTKPanenSection with single clean definition
pattern = r'(function tutupTKPanenSection\(\) \{.*?\n    \}\s*)+'
clean_tutup = """function tutupTKPanenSection() {
      var tkContent = document.getElementById("tkPanenMainContent");
      var mainGrid = document.getElementById("dashboardMainGrid");
      if (tkContent) tkContent.style.display = "none";
      if (mainGrid) mainGrid.style.display = "block";
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
    }"""

content = re.sub(pattern, clean_tutup + "\n\n    ", content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("CLEANED UP DUPLICATE tutupTKPanenSection IN LOGIN.HTML!")
