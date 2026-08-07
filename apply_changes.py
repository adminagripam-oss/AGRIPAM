import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove #themeToggleBtn completely
# Sun/Moon icons inside body wrapper
theme_btn_pattern = re.compile(r'  <button id="themeToggleBtn".*?</button>\s*', re.DOTALL)
content = theme_btn_pattern.sub('', content)

# 2. Remove the duplicate marquee appended inside #loginSection > main
duplicate_marquee = """        <!-- Running Text -->
        <div class="w-full bg-[#0f172a] border-t border-slate-700/50 flex items-center h-10 overflow-hidden relative shadow-[0_-4px_10px_rgba(0,0,0,0.1)] flex-shrink-0 z-10 mt-auto rounded-xl mb-2">
            <div class="absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-[#0f172a] to-transparent z-10 pointer-events-none"></div>
            <div class="flex items-center gap-2 px-4 z-20 bg-[#0f172a] border-r border-slate-700/50 shadow-[4px_0_10px_rgba(0,0,0,0.2)]">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse2"></span>
                <span class="text-[11px] font-bold text-white tracking-wider whitespace-nowrap">LIVE UPDATE</span>
            </div>
            <div class="flex-1 overflow-hidden relative h-full flex items-center group">
                <div class="ticker-track flex items-center w-full">
                    <span class="text-[13px] text-slate-300 font-medium whitespace-nowrap px-4" id="marqueeText">
                        Mengambil data hasil produksi...
                    </span>
                </div>
            </div>
            <div class="absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-[#0f172a] to-transparent z-10 pointer-events-none"></div>
        </div>"""

content = content.replace(duplicate_marquee, "")

# 3. Modify Filter Bar block layout (removing absolute collision)
filter_bar_old_block = """        <!-- Filter Bar -->
        <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
          <div class="flex items-center space-x-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-4">
            <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            <span>Filter Tampilan Data</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="filterBarGrid">
            <!-- Rentang Waktu -->
            <div class="relative">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">RENTANG WAKTU</label>
              <select id="filterDateMode" onchange="onFilterDateModeChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
                <option value="TUNGGAL" selected>Tanggal Tunggal</option>
                <option value="SD_HARI_INI">s.d. Hari Ini</option>
                <option value="SD_BULAN_INI">s.d. Bulan Ini</option>
                <option value="KUSTOM">Rentang Kustom</option>
              </select>
            </div>
            <!-- Tanggal (Dari) -->
            <div class="relative" id="filterTanggalStartContainer">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400" id="labelTanggalStart">TANGGAL</label>
              <input type="date" id="filterTanggalStart" onchange="onFilterTanggalChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
            </div>
            <!-- Tanggal Akhir (Sampai) -->
            <div class="relative hidden" id="filterTanggalEndContainer">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">SAMPAI TANGGAL</label>
              <input type="date" id="filterTanggalEnd" onchange="onFilterTanggalChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
            </div>
          </div>
        </section>"""

filter_bar_new_block = """        <!-- Filter Bar -->
        <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
          <div class="flex items-center space-x-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
            <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            <span>Filter Tampilan Data</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="filterBarGrid">
            <!-- Rentang Waktu -->
            <div class="flex flex-col">
              <label class="text-[10px] font-bold text-slate-400 mb-1 uppercase tracking-wider">Rentang Waktu</label>
              <select id="filterDateMode" onchange="onFilterDateModeChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
                <option value="TUNGGAL" selected>Tanggal Tunggal</option>
                <option value="SD_HARI_INI">s.d. Hari Ini</option>
                <option value="SD_BULAN_INI">s.d. Bulan Ini</option>
                <option value="KUSTOM">Rentang Kustom</option>
              </select>
            </div>
            <!-- Tanggal (Dari) -->
            <div class="flex flex-col" id="filterTanggalStartContainer">
              <label class="text-[10px] font-bold text-slate-400 mb-1 uppercase tracking-wider" id="labelTanggalStart">Tanggal</label>
              <input type="date" id="filterTanggalStart" onchange="onFilterTanggalChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
            </div>
            <!-- Tanggal Akhir (Sampai) -->
            <div class="flex flex-col hidden" id="filterTanggalEndContainer">
              <label class="text-[10px] font-bold text-slate-400 mb-1 uppercase tracking-wider">Sampai Tanggal</label>
              <input type="date" id="filterTanggalEnd" onchange="onFilterTanggalChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500 bg-white">
            </div>
          </div>
        </section>"""

content = content.replace(filter_bar_old_block, filter_bar_new_block)

# 4. Remove edit_note and lock reporting date to today, disable it
reporting_card_old = """          <!-- Input Form Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
            <div>
              <h2 class="text-base font-bold text-slate-800 mb-4 flex items-center gap-2">
                <span class="material-symbols-outlined text-green-600">edit_note</span>
                Input Laporan Panen
              </h2>
              <form id="panenForm" onsubmit="return false;" class="space-y-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Tanggal Laporan</label>
                  <input type="date" id="tanggal" name="tanggal" required onchange="onTanggalChange()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500">
                </div>"""

reporting_card_new = """          <!-- Input Form Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
            <div>
              <h2 class="text-base font-bold text-slate-800 mb-4">
                Input Laporan Panen
              </h2>
              <form id="panenForm" onsubmit="return false;" class="space-y-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Tanggal Laporan</label>
                  <input type="date" id="tanggal" name="tanggal" readonly disabled class="w-full border border-gray-200 bg-gray-100 rounded-lg p-2 text-sm text-slate-500 cursor-not-allowed">
                </div>"""

content = content.replace(reporting_card_old, reporting_card_new)

# 5. Delete MidSectionGrid completely
mid_grid_pattern = re.compile(r'        <!-- MidSectionGrid \(Contribution & Leaderboard\) -->.*?<!-- RealizationVsEstimation -->', re.DOTALL)
content = mid_grid_pattern.sub('        <!-- RealizationVsEstimation -->', content)

# 6. Update RealizationVsEstimation section to host the canvas chart
realization_section_old = """        <!-- RealizationVsEstimation -->
        <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
          <div class="flex justify-between items-start mb-8">
            <div>
              <h2 class="text-base font-bold text-slate-800">Realisasi vs Estimasi Panen — Nasional</h2>
              <p class="text-xs text-gray-400">Perbandingan pencapaian vs target</p>
            </div>
            <div class="flex items-center space-x-6">
              <div class="flex items-center space-x-4">
                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3 h-3 bg-blue-100 border border-blue-600 rounded-sm mr-2"></span>
                  Estimasi Panen
                </div>
                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3 h-3 bg-green-500 rounded-sm mr-2"></span>
                  Realisasi Panen
                </div>
              </div>
            </div>
          </div>
          <div class="h-64 relative w-full">
            <div class="absolute inset-0 flex flex-col justify-between text-[10px] text-gray-400">
              <div class="border-b border-dashed border-gray-100 pb-1">6.000,00</div>
              <div class="border-b border-dashed border-gray-100 pb-1">4.000,00</div>
              <div class="border-b border-dashed border-gray-100 pb-1">2.000,00</div>
              <div class="pb-1">0,00</div>
            </div>
            <div class="absolute inset-0 pl-14 pt-2 flex items-end justify-between overflow-x-auto pb-6 scrollbar-hide">
              <div class="flex flex-col items-center min-w-[60px] group">
                <div class="flex items-end space-x-1">
                  <div class="w-4 h-2 bg-blue-100 border border-blue-500 rounded-sm relative"></div>
                  <div class="w-4 h-1 bg-green-500 rounded-sm relative"></div>
                </div>
                <span class="mt-2 text-[9px] font-bold text-gray-400 uppercase">Aceh</span>
              </div>
            </div>
          </div>
        </section>"""

realization_section_new = """        <!-- RealizationVsEstimation -->
        <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h2 class="text-base font-bold text-slate-800">Realisasi vs Estimasi Panen — Nasional</h2>
              <p class="text-xs text-gray-400">Tren akumulasi harian dari awal bulan s.d. hari ini</p>
            </div>
            <div class="flex items-center space-x-6">
              <div class="flex items-center space-x-4">
                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3.5 h-3.5 bg-blue-500 rounded-sm mr-2 opacity-70"></span>
                  Estimasi Panen
                </div>
                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3.5 h-3.5 bg-green-500 rounded-sm mr-2 opacity-70"></span>
                  Realisasi Panen
                </div>
              </div>
            </div>
          </div>
          <div class="h-72 relative w-full" id="dailyChartContainer">
            <canvas id="realisasiVsEstimasiChart"></canvas>
          </div>
        </section>"""

content = content.replace(realization_section_old, realization_section_new)

# 7. Hide the sessionInfo text at the bottom footer of main content
session_info_old = """        <footer class="flex flex-col items-center justify-center pb-6">
          <p id="sessionInfo" class="text-[10px] text-slate-400 mb-2"></p>
          <span class="text-[9px] font-bold text-slate-400 tracking-[0.2em] uppercase">Patriot - Loyal - Profesional</span>
        </footer>"""

session_info_new = """        <footer class="flex flex-col items-center justify-center pb-6">
          <p id="sessionInfo" style="display: none;"></p>
          <span class="text-[9px] font-bold text-slate-400 tracking-[0.2em] uppercase">Patriot - Loyal - Profesional</span>
        </footer>"""

content = content.replace(session_info_old, session_info_new)

# 8. Add JS code for daily national chart
daily_chart_js = """
      var dailyNationalChart = null;

      function updateDailyNationalChart() {
        var s = loadSession();
        if (!s) return;

        // Calculate start of current month and today's date in WIB
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var wibTime = new Date(utc + (7 * 3600000));
        var yyyy = wibTime.getFullYear();
        var MM = String(wibTime.getMonth() + 1).padStart(2, '0');
        var dd = String(wibTime.getDate()).padStart(2, '0');
        var todayWib = yyyy + "-" + MM + "-" + dd;
        var startOfMonth = yyyy + "-" + MM + "-01";

        // Generate date list from 1st to today
        var dates = [];
        var labels = [];
        var d = new Date(yyyy, wibTime.getMonth(), 1);
        while (d <= wibTime) {
          var y = d.getFullYear();
          var m = String(d.getMonth() + 1).padStart(2, '0');
          var day = String(d.getDate()).padStart(2, '0');
          var dateStr = y + "-" + m + "-" + day;
          dates.push(dateStr);
          labels.push(day + "/" + m);
          d.setDate(d.getDate() + 1);
        }

        var realisasiData = Array(dates.length).fill(0);
        var estimasiData = Array(dates.length).fill(0);

        var realisasiLoaded = false;
        var estimasiLoaded = false;
        var realRecords = [];
        var estRecords = [];

        function drawChart() {
          if (!realisasiLoaded || !estimasiLoaded) return;

          // Group realisasi daily sum
          dates.forEach(function(dt, idx) {
            var sumReal = 0;
            realRecords.forEach(function(r) {
              if (r.tanggal === dt) {
                sumReal += parseFloat(r.tonase) || 0;
              }
            });
            realisasiData[idx] = sumReal;

            var sumEst = 0;
            estRecords.forEach(function(r) {
              if (r.tanggal === dt) {
                var estPanen = parseFloat(r.estimasi_panen_kg) || parseFloat(r.estimasi_kirim_kg) || 0;
                sumEst += estPanen / 1000;
              }
            });
            estimasiData[idx] = sumEst;
          });

          // Render Line Area Chart with gradient
          var ctx = document.getElementById("realisasiVsEstimasiChart");
          if (!ctx) return;

          if (dailyNationalChart) {
            dailyNationalChart.destroy();
          }

          var chartCtx = ctx.getContext("2d");
          var isDark = document.documentElement.getAttribute("data-theme") === "dark";

          // Create gradients
          var gradientReal = chartCtx.createLinearGradient(0, 0, 0, 300);
          gradientReal.addColorStop(0, 'rgba(34, 197, 94, 0.4)'); // Green
          gradientReal.addColorStop(1, 'rgba(34, 197, 94, 0.0)');

          var gradientEst = chartCtx.createLinearGradient(0, 0, 0, 300);
          gradientEst.addColorStop(0, 'rgba(37, 99, 235, 0.2)'); // Blue
          gradientEst.addColorStop(1, 'rgba(37, 99, 235, 0.0)');

          dailyNationalChart = new Chart(chartCtx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                {
                  label: 'Realisasi Panen (Ton)',
                  data: realisasiData,
                  borderColor: '#22c55e',
                  backgroundColor: gradientReal,
                  fill: true,
                  tension: 0.3,
                  borderWidth: 2,
                  pointRadius: 3,
                  pointBackgroundColor: '#22c55e'
                },
                {
                  label: 'Estimasi Panen (Ton)',
                  data: estimasiData,
                  borderColor: '#2563eb',
                  backgroundColor: gradientEst,
                  fill: true,
                  tension: 0.3,
                  borderWidth: 2,
                  pointRadius: 3,
                  pointBackgroundColor: '#2563eb'
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: false }
              },
              scales: {
                x: {
                  grid: { display: false },
                  ticks: {
                    color: isDark ? '#94a3b8' : '#64748b',
                    font: { size: 10 }
                  }
                },
                y: {
                  grid: { color: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' },
                  ticks: {
                    color: isDark ? '#94a3b8' : '#64748b',
                    font: { size: 10 }
                  }
                }
              }
            }
          });
        }

        // Fetch realisasi data
        jsonpRequest(
          { action: "getData", tanggal: startOfMonth, tanggal_akhir: todayWib, region: "ALL" },
          function (res) {
            realRecords = (res && res.success) ? (res.allRecords || []) : [];
            realisasiLoaded = true;
            drawChart();
          },
          function () {
            realisasiLoaded = true;
            drawChart();
          }
        );

        // Fetch estimasi data
        jsonpRequest(
          { action: "getEstimasi", tanggal: startOfMonth, tanggal_akhir: todayWib, region: "ALL", token: s.token },
          function (res) {
            estRecords = (res && res.success) ? (res.allRecords || []) : [];
            estimasiLoaded = true;
            drawChart();
          },
          function () {
            estimasiLoaded = true;
            drawChart();
          }
        );
      }
"""

content = content.replace('    </script>\n  </div>', daily_chart_js + '    </script>\n  </div>')
if daily_chart_js not in content:
    content = content.replace('    </script>\n</div>', daily_chart_js + '    </script>\n</div>')

# Call updateDailyNationalChart inside checkAccumulation
check_accumulation_call = """          updateJamHint();
          updateEstimasiComparison();"""

check_accumulation_call_new = """          updateJamHint();
          updateEstimasiComparison();
          if (typeof updateDailyNationalChart === 'function') {
            updateDailyNationalChart();
          }"""

content = content.replace(check_accumulation_call, check_accumulation_call_new)

# Force the disabled reporting date field to always lock to today
force_today_date_js = """            if (!tglInput.value) {
              tglInput.value = todayWib;
            }"""

force_today_date_js_new = """            // Force reporting form date to be strictly today
            tglInput.value = todayWib;"""

content = content.replace(force_today_date_js, force_today_date_js_new)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied UI and Daily Area Chart changes successfully.")
