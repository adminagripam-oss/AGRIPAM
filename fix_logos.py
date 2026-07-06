import re

with open('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the first img src base64
match = re.search(r'src=\"(data:image/png;base64,[^\"]+)\"', content)
if match:
    base64_src = match.group(1)
    
    # Replace in sap_admin.html
    with open('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/sap_admin.html', 'r', encoding='utf-8') as f:
        admin_content = f.read()
    admin_content = re.sub(r'src=\"data:image/png;base64,[^\"]*?original_line[^\"]*\"', f'src=\"{base64_src}\"', admin_content)
    with open('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/sap_admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_content)

    # Replace in sap_regional.html
    with open('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/sap_regional.html', 'r', encoding='utf-8') as f:
        reg_content = f.read()
    reg_content = re.sub(r'src=\"data:image/png;base64,[^\"]*?original_line[^\"]*\"', f'src=\"{base64_src}\"', reg_content)
    with open('d:/AGRINAS PALMA NUSANTARA/AGRIPAM/sap_regional.html', 'w', encoding='utf-8') as f:
        f.write(reg_content)
    print('Replaced successfully')
else:
    print('Base64 not found in login.html')
