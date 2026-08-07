import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Tailwind tag & stray JS lines 1840-1848
pattern = r'<!-- TailwindCSS -->\s*<script src="https://cdn\.tailwindcss\.com">\s*else \{\s*trs\[i\]\.style\.display = "none";\s*\}\s*\}\s*\}'
replacement = '<!-- TailwindCSS -->\n  <script src="https://cdn.tailwindcss.com"></script>\n  <script>'

new_content, count = re.subn(pattern, replacement, content)
print(f"Replaced {count} Tailwind script tag issues.")

# Fix single quote syntax errors on inputs
pattern_juli = r"onchange=\"onTKInputChange\(' \+ item\.id \+ ', 'tk_juli', this\.value\)\""
replacement_juli = "onchange=\"onTKInputChange(' + item.id + ', ' + \"'\" + 'tk_juli' + \"'\" + ', this.value)\""

pattern_ags = r"onchange=\"onTKInputChange\(' \+ item\.id \+ ', 'tk_agustus', this\.value\)\""
replacement_ags = "onchange=\"onTKInputChange(' + item.id + ', ' + \"'\" + 'tk_agustus' + \"'\" + ', this.value)\""

new_content, count1 = re.subn(pattern_juli, 'onchange="onTKInputChange(\' + item.id + \', \\\'tk_juli\\\', this.value)"', new_content)
new_content, count2 = re.subn(pattern_ags, 'onchange="onTKInputChange(\' + item.id + \', \\\'tk_agustus\\\', this.value)"', new_content)

print(f"Replaced {count1} Juli quotes and {count2} Ags quotes.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESSFULLY CLEANED login.html!")
