import re

# 1. UPDATE API/KEBUNTK.JS
api_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\api\kebunTK.js'

with open(api_path, 'r', encoding='utf-8') as f:
    api_code = f.read()

old_summary_calc = r'// Calculate summary statistics.*?return res\.json\(\{\s+success: true,.*?summary: \{.*?\}\s+\}\);'

new_summary_calc = """// Calculate summary statistics
    const totalLuas = result.reduce((sum, item) => sum + (parseFloat(item.luasan) || 0), 0);
    const totalReqTk = result.reduce((sum, item) => sum + (parseFloat(item.req_tk) || 0), 0);
    const totalJuni = result.reduce((sum, item) => sum + (parseFloat(item.tk_juni) || 0), 0);
    const kekurangTK = totalReqTk - totalJuni;

    return res.json({
      success: true,
      totalEntries: result.length,
      data: result,
      summary: {
        totalLuas: Math.round(totalLuas * 100) / 100,
        totalReqTk: Math.round(totalReqTk),
        totalJuni: Math.round(totalJuni),
        kekurangTK: Math.round(kekurangTK)
      }
    });"""

api_code = re.sub(old_summary_calc, new_summary_calc, api_code, flags=re.DOTALL)

with open(api_path, 'w', encoding='utf-8') as f:
    f.write(api_code)

print("Updated api/kebunTK.js summary calculation!")


# 2. UPDATE LOGIN.HTML
login_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(login_path, 'r', encoding='utf-8') as f:
    login_code = f.read()

old_kpi_render = r'// Large Fluid KPI Cards Grid Rendering.*?\n      \}'

new_kpi_render = """// Large Fluid KPI Cards Grid Rendering (5 Responsive Cards)
      var summaryEl = document.getElementById("tkSummaryBadges");
      if (summaryEl) {
        var reqTk = summary && summary.totalReqTk !== undefined ? summary.totalReqTk : items.reduce(function(s, x){ return s + (parseInt(x.req_tk)||0); }, 0);
        var tkJuni = summary && summary.totalJuni !== undefined ? summary.totalJuni : items.reduce(function(s, x){ return s + (parseInt(x.tk_juni)||0); }, 0);
        var kekurangTK = reqTk - tkJuni;

        summaryEl.innerHTML = '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Kebun</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + items.length + ' <span class="text-xs font-bold text-slate-500">Kebun</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Luas</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + (summary && summary.totalLuas ? summary.totalLuas : 0).toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Ha</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Kebutuhan Tenaga Panen</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + reqTk.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Orang</span></div>' +
          '</div>' +
          '<div class="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">TK Juni (Cut Off Juni)</span>' +
          '<div class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">' + tkJuni.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-500">Orang</span></div>' +
          '</div>' +
          '<div class="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-all duration-300">' +
          '<span class="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Kekurangan Tenaga Panen</span>' +
          '<div class="text-xl md:text-2xl font-black text-white mt-1">' + kekurangTK.toLocaleString('id-ID') + ' <span class="text-xs font-bold text-slate-300">Orang</span></div>' +
          '</div>';
      }
    }"""

login_code = re.sub(old_kpi_render, new_kpi_render, login_code, flags=re.DOTALL)

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_code)

print("Updated login.html KPI cards grid with new formulas!")


# 3. UPDATE LAPORAN_PRODUKSI.HTML REACT COMPONENT IF PRESENT
lap_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(lap_path, 'r', encoding='utf-8') as f:
    lap_code = f.read()

old_react_kpi = r'// TK Summary Badges.*?\</div>\s+\</div>'

new_react_kpi = """{/* TK Summary Badges Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
            <div className="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
              <span className="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Kebun</span>
              <div className="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">{items.length} <span className="text-xs font-bold text-slate-500">Kebun</span></div>
            </div>
            <div className="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
              <span className="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Luas</span>
              <div className="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">{summary.totalLuas || 0} <span className="text-xs font-bold text-slate-500">Ha</span></div>
            </div>
            <div className="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
              <span className="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">Kebutuhan Tenaga Panen</span>
              <div className="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">{summary.totalReqTk || 0} <span className="text-xs font-bold text-slate-500">Orang</span></div>
            </div>
            <div className="bg-white dark:bg-slate-900 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
              <span className="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">TK Juni (Cut Off Juni)</span>
              <div className="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">{summary.totalJuni || 0} <span className="text-xs font-bold text-slate-500">Orang</span></div>
            </div>
            <div className="bg-slate-900 text-white dark:bg-slate-800 border-2 border-slate-900 dark:border-slate-700 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
              <span className="text-[11px] font-black text-slate-300 dark:text-slate-400 uppercase tracking-wider">Kekurangan Tenaga Panen</span>
              <div className="text-xl md:text-2xl font-black text-white mt-1">{(summary.totalReqTk || 0) - (summary.totalJuni || 0)} <span className="text-xs font-bold text-slate-300">Orang</span></div>
            </div>
          </div>"""

lap_code = re.sub(old_react_kpi, new_react_kpi, lap_code, flags=re.DOTALL)

with open(lap_path, 'w', encoding='utf-8') as f:
    f.write(lap_code)

print("Updated laporan_produksi.html React component!")
