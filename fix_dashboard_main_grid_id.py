file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_start = """      <!-- MainContentContainer (Scrollable) -->
      <main class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col justify-between">
        <div>"""

replacement_start = """      <!-- MainContentContainer (Scrollable) -->
      <main class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col justify-between">
        <div id="dashboardMainGrid">"""

if target_start in content:
    content = content.replace(target_start, replacement_start)
    print("Successfully replaced plain <div> with <div id=\"dashboardMainGrid\">")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished fixing #dashboardMainGrid ID!")
