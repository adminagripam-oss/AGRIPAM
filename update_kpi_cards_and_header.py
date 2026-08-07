import re

# 1. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

# Replace summary badges container class to grid layout
old_summary_div = r'<!-- Summary Badges Bar -->\s*<div id="tkSummaryBadges" class="flex flex-wrap items-center gap-3 text-xs font-semibold"></div>'
new_summary_div = '<!-- Large Fluid KPI Cards Grid -->\n            <div id="tkSummaryBadges" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 w-full transition-all duration-300"></div>'

login_code = re.sub(old_summary_div, new_summary_div, login_code)

# Replace REQ TK with KEBUTUHAN TENAGA PANEN in table header
login_code = login_code.replace('<th class="py-3.5 px-2 text-right font-black">Req TK</th>', '<th class="py-3.5 px-2 text-right font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>')

# Replace summaryEl.innerHTML rendering in renderTKPanenTable
old_summary_js = r'// Monochrome Summary Badges\s*var summaryEl = document\.getElementById\("tkSummaryBadges"\);.*?\}\s*\}'

new_summary_js = """// Large Fluid KPI Cards Grid Rendering
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl && summary) {
        summaryEl.innerHTML = '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
                                '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Kebun</span>' +
                                '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + items.length + ' <span class="text-xs font-bold text-slate-500">Kebun</span></div>' +
                              '</div>' +
                              '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
                                '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Luas</span>' +
                                '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary.totalLuas || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Ha</span></div>' +
                              '</div>' +
                              '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
                                '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Target Juli</span>' +
                                '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary.totalJuliTgt || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">TK</span></div>' +
                              '</div>' +
                              '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
                                '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Real Jul (Col I)</span>' +
                                '<div class="text-xl md:text-2xl font-black text-white mt-1">' + (summary.totalJuliAct || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">TK</span></div>' +
                              '</div>' +
                              '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
                                '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Real Ags (Col J)</span>' +
                                '<div class="text-xl md:text-2xl font-black text-white mt-1">' + (summary.totalAgustAct || 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">TK</span></div>' +
                              '</div>';
      }
    }"""

login_code = re.sub(old_summary_js, new_summary_js, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html with Large Fluid KPI Cards Grid and KEBUTUHAN TENAGA PANEN header!")


# 2. UPDATE LAPORAN_PRODUKSI.HTML
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

# Replace REQ TK with KEBUTUHAN TENAGA PANEN in laporan_produksi.html
lap_code = lap_code.replace('<th class="py-3.5 px-2 text-right font-black">Req TK</th>', '<th class="py-3.5 px-2 text-right font-black whitespace-nowrap">KEBUTUHAN TENAGA PANEN</th>')
lap_code = lap_code.replace('Req TK', 'KEBUTUHAN TENAGA PANEN')

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html with KEBUTUHAN TENAGA PANEN header!")
