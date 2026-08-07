file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_line_2004 = "onchange=\"onTKInputChange(' + item.id + ', 'tk_juli', this.value)\""
good_line_2004 = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_juli\\', this.value)\""

bad_line_2009 = "onchange=\"onTKInputChange(' + item.id + ', 'tk_agustus', this.value)\""
good_line_2009 = "onchange=\"onTKInputChange(' + item.id + ', \\'tk_agustus\\', this.value)\""

content = content.replace(bad_line_2004, good_line_2004)
content = content.replace(bad_line_2009, good_line_2009)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY FIXED SYNTAX ERRORS ON LINES 2004 & 2009 IN LOGIN.HTML!")
