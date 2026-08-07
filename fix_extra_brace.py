file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_closing = "      }\n    }\n\n    function onTKInputChange"
good_closing = "      }\n    }\n\n    function onTKInputChange"

if "      }\n    }\n    }\n\n    function onTKInputChange" in content:
    content = content.replace("      }\n    }\n    }\n\n    function onTKInputChange", "      }\n    }\n\n    function onTKInputChange")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed closing brace in login.html!")
