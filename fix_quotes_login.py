file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_line_2040 = "onchange=\"onTKInputChange(' + item.id + ', 'tk_juli', this.value)\""
good_line_2040 = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_juli\\', this.value)\""

bad_line_2045 = "onchange=\"onTKInputChange(' + item.id + ', 'tk_agustus', this.value)\""
good_line_2045 = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_agustus\\', this.value)\""

content = content.replace(bad_line_2040, good_line_2040)
content = content.replace(bad_line_2045, good_line_2045)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY ESCAPED QUOTES IN LOGIN.HTML!")
