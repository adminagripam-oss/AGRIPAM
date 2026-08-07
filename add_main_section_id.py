file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add id="mainSection" to <main> tag at line 2600
old_main_tag = '<main class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col justify-between">'
new_main_tag = '<main id="mainSection" class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col justify-between">'

if old_main_tag in content:
    content = content.replace(old_main_tag, new_main_tag)
    print("Successfully added id='mainSection' to <main> tag!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FINISHED UPDATING LOGIN.HTML WITH MAINSECTION ID!")
