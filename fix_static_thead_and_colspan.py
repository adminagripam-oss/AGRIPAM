import re

# 1. FIX STATIC THEAD IN LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Replace ALL occurrences of static thead in login.html
old_thead_pattern = r'<thead\s+class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">.*?</thead>'

new_thead_html = """<thead class="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700">
                  <tr class="text-[11px] font-black uppercase tracking-wider text-white">
                    <th class="py-3.5 px-2 text-center w-10 font-black">No</th>
                    <th class="py-3.5 px-2 text-center font-black">CRO</th>
                    <th class="py-3.5 px-2 text-center font-black">Regional</th>
                    <th class="py-3.5 px-3 text-left font-black min-w-[180px]">Nama Kebun / PT</th>
                    <th class="py-3.5 px-2 text-center font-black">Tag</th>
                    <th class="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                    <th class="py-3.5 px-2 text-center font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>
                    <th class="py-3.5 px-2 text-center font-black">TK MEI</th>
                    <th class="py-3.5 px-2 text-center font-black">TK JUNI</th>
                    <th class="py-3.5 px-2 text-center font-black bg-black text-white border-x border-slate-700">TK JULI</th>
                    <th class="py-3.5 px-2 text-center font-black bg-black text-white border-r border-slate-700">TK AGUSTUS</th>
                    <th class="py-3.5 px-2 text-center font-black">AKSI</th>
                  </tr>
                </thead>"""

login_code = re.sub(old_thead_pattern, new_thead_html, login_code, flags=re.DOTALL)

# Update colspan 14 -> 12 in login.html
login_code = login_code.replace('colspan="14"', 'colspan="12"')

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("SUCCESSFULLY REMOVED TARGET JUL & TARGET AGS FROM STATIC THEAD IN LOGIN.HTML!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

old_react_thead = r'<thead className="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700 text-\[11px\] font-black uppercase tracking-wider">.*?</thead>'

new_react_thead = """<thead className="bg-slate-900 text-white dark:bg-slate-800 border-b-2 border-slate-900 dark:border-slate-700 text-[11px] font-black uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-2 text-center w-10 font-black">No</th>
                      <th className="py-3.5 px-2 text-center font-black">CRO</th>
                      <th className="py-3.5 px-2 text-center font-black">Regional</th>
                      <th className="py-3.5 px-3 text-left font-black min-w-[180px]">Nama Kebun / PT</th>
                      <th className="py-3.5 px-2 text-center font-black">Tag</th>
                      <th className="py-3.5 px-2 text-center font-black">Luas (Ha)</th>
                      <th className="py-3.5 px-2 text-center font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>
                      <th className="py-3.5 px-2 text-center font-black">TK MEI</th>
                      <th className="py-3.5 px-2 text-center font-black">TK JUNI</th>
                      <th className="py-3.5 px-2 text-center font-black bg-black text-white border-x border-slate-700">TK JULI</th>
                      <th className="py-3.5 px-2 text-center font-black bg-black text-white border-r border-slate-700">TK AGUSTUS</th>
                      <th className="py-3.5 px-2 text-center font-black">AKSI</th>
                    </tr>
                  </thead>"""

lap_code = re.sub(old_react_thead, new_react_thead, lap_code, flags=re.DOTALL)
lap_code = lap_code.replace('colSpan={14}', 'colSpan={12}')

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("SUCCESSFULLY REMOVED TARGET JUL & TARGET AGS FROM LAPORAN_PRODUKSI.HTML!")
