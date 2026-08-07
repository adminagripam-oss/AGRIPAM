file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('globalTKEdits[id][fieldKey || fKey] = activeEditingValues[fKey];', 'globalTKEdits[id][fKey] = activeEditingValues[fKey];')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIXED BUG IN SAVEEDITKEBUNFORM IN LOGIN.HTML!")
