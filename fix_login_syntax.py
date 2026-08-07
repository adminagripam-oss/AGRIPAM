file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix line 1841: closing tailwind script tag & removing stray JS code
old_head_block = """  <!-- TailwindCSS -->
  <script src="https://cdn.tailwindcss.com">
     else {
          trs[i].style.display = "none";
        }
      }
    }


    // =========================================================================
    // FITUR TK PANEN (ROUTER & DATA INPUT)
    // =========================================================================="""

new_head_block = """  <!-- TailwindCSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    // =========================================================================
    // FITUR TK PANEN (ROUTER & DATA INPUT)
    // =========================================================================="""

if old_head_block in content:
    content = content.replace(old_head_block, new_head_block)
    print("Fixed Tailwind script tag and stray JS code in head.")

# 2. Fix unescaped single quotes on lines 1967 and 1972
old_input_juli = "html += '<td class=\"py-2.5 px-4 text-center bg-red-500/10 border-x border-red-200\"><input type=\"number\" min=\"0\" value=\"' + valJuli + '\" onchange=\"onTKInputChange(' + item.id + ', \'tk_juli\', this.value)\" class=\"w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm\" /></td>';"

# Search and replace single quote issues in renderTKPanenTable string concatenations
broken_juli = "html += '<td class=\"py-2.5 px-4 text-center bg-red-500/10 border-x border-red-200\"><input type=\"number\" min=\"0\" value=\"' + valJuli + '\" onchange=\"onTKInputChange(' + item.id + ', 'tk_juli', this.value)\" class=\"w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm\" /></td>';"
fixed_juli = "html += '<td class=\"py-2.5 px-4 text-center bg-red-500/10 border-x border-red-200\"><input type=\"number\" min=\"0\" value=\"' + valJuli + '\" onchange=\"onTKInputChange(' + item.id + ', &quot;tk_juli&quot;, this.value)\" class=\"w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm\" /></td>';"

broken_ags = "html += '<td class=\"py-2.5 px-4 text-center bg-red-500/10 border-r border-red-200\"><input type=\"number\" min=\"0\" value=\"' + valAgs + '\" onchange=\"onTKInputChange(' + item.id + ', 'tk_agustus', this.value)\" class=\"w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm\" /></td>';"
fixed_ags = "html += '<td class=\"py-2.5 px-4 text-center bg-red-500/10 border-r border-red-200\"><input type=\"number\" min=\"0\" value=\"' + valAgs + '\" onchange=\"onTKInputChange(' + item.id + ', &quot;tk_agustus&quot;, this.value)\" class=\"w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm\" /></td>';"

if broken_juli in content:
    content = content.replace(broken_juli, fixed_juli)
    print("Fixed unescaped single quotes on Juli input line.")

if broken_ags in content:
    content = content.replace(broken_ags, fixed_ags)
    print("Fixed unescaped single quotes on Agustus input line.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating login.html!")
