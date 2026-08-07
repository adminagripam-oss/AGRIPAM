import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the Filter Bar section
filter_bar_old = """        <!-- Filter Bar -->
        <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
          <div class="flex items-center space-x-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-4">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            <span>Filter Tampilan Data</span>
          </div>
          <div class="grid grid-cols-4 gap-4">
            <div class="relative">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">CRO</label>
              <div class="border border-gray-200 rounded-lg px-3 py-2 flex items-center justify-between bg-gray-50 text-gray-500 text-xs cursor-not-allowed">
                <span>Semua CRO</span>
              </div>
            </div>
            <div class="relative">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">REGIONAL</label>
              <div class="border border-gray-200 rounded-lg px-3 py-2 flex items-center justify-between bg-gray-50 text-gray-500 text-xs cursor-not-allowed">
                <span>Nasional</span>
              </div>
            </div>
            <div class="relative">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">RENTANG WAKTU</label>
              <div class="border border-gray-200 rounded-lg px-3 py-2 flex items-center justify-between bg-gray-50 text-gray-500 text-xs cursor-not-allowed">
                <span>Tanggal Tunggal</span>
              </div>
            </div>
            <div class="relative">
              <label class="absolute -top-2 left-3 px-1 bg-white text-[9px] font-bold text-gray-400">TANGGAL</label>
              <div class="border border-gray-200 rounded-lg px-3 py-2 flex items-center justify-between bg-gray-50 text-gray-500 text-xs cursor-not-allowed">
                <span>16/07/2026</span>
              </div>
            </div>
          </div>
        </section>"""

filter_bar_new = """        <!-- Filter Bar -->
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

content = content.replace(filter_bar_old, filter_bar_new)

# 2. Add javascript helper functions at the end of the script tag (before </body>)
js_helpers = """
      // Helper functions for Date Filtering in Regional View
      function getFilterDates() {
        var mode = document.getElementById("filterDateMode").value;
        var refDate = document.getElementById("filterTanggalStart").value;
        var start = refDate;
        var end = refDate;
        
        if (!refDate) return { start: "", end: "" };
        
        if (mode === "TUNGGAL") {
          start = refDate;
          end = refDate;
        } else if (mode === "SD_HARI_INI") {
          var d = new Date(refDate);
          var yyyy = d.getFullYear();
          var MM = String(d.getMonth() + 1).padStart(2, '0');
          start = yyyy + "-" + MM + "-01";
          end = refDate;
        } else if (mode === "SD_BULAN_INI") {
          var d = new Date(refDate);
          start = d.getFullYear() + "-01-01";
          end = refDate;
        } else if (mode === "KUSTOM") {
          start = refDate;
          end = document.getElementById("filterTanggalEnd").value || refDate;
        }
        return { start: start, end: end };
      }

      function onFilterDateModeChange() {
        var mode = document.getElementById("filterDateMode").value;
        var endContainer = document.getElementById("filterTanggalEndContainer");
        var labelStart = document.getElementById("labelTanggalStart");
        
        if (mode === "KUSTOM") {
          if (endContainer) endContainer.classList.remove("hidden");
          if (labelStart) labelStart.textContent = "DARI TANGGAL";
        } else {
          if (endContainer) endContainer.classList.add("hidden");
          if (labelStart) labelStart.textContent = "TANGGAL";
        }
        
        checkAccumulation();
        updateRunningText();
      }

      function onFilterTanggalChange() {
        checkAccumulation();
        updateRunningText();
      }
"""

# Append JS helpers inside the main <script> tag
# Let's locate the ending of the script before </script>
content = content.replace('    </script>\n  </div>', js_helpers + '    </script>\n  </div>')
if js_helpers not in content:
    # If the marker wasn't exactly that:
    content = content.replace('    </script>\n</div>', js_helpers + '    </script>\n</div>')

# 3. Update checkAccumulation to use getFilterDates()
check_accumulation_old_start = """    function checkAccumulation(isSilent) {
        var tanggal = document.getElementById("tanggal").value;
        var s = loadSession();"""

check_accumulation_new_start = """    function checkAccumulation(isSilent) {
        var filterDates = getFilterDates();
        var tanggal = filterDates.start;
        var tanggal_akhir = filterDates.end;
        var s = loadSession();"""

content = content.replace(check_accumulation_old_start, check_accumulation_new_start)

# Replace jsonp calls inside checkAccumulation
# { action: "getData", tanggal: tanggal, region: region } -> { action: "getData", tanggal: tanggal, tanggal_akhir: tanggal_akhir, region: region }
getData_old = '{ action: "getData", tanggal: tanggal, region: region }'
getData_new = '{ action: "getData", tanggal: tanggal, tanggal_akhir: tanggal_akhir, region: region }'
content = content.replace(getData_old, getData_new)

# { action: "getEstimasi", tanggal: tanggal, region: region, token: s.token } -> { action: "getEstimasi", tanggal: tanggal, tanggal_akhir: tanggal_akhir, region: region, token: s.token }
getEstimasi_old = '{ action: "getEstimasi", tanggal: tanggal, region: region, token: s.token }'
getEstimasi_new = '{ action: "getEstimasi", tanggal: tanggal, tanggal_akhir: tanggal_akhir, region: region, token: s.token }'
content = content.replace(getEstimasi_old, getEstimasi_new)

# 4. Update updateRunningText to use getFilterDates()
running_text_old_logic = """      function updateRunningText() {
        var container = document.getElementById("runningTextContainer");
        var content = document.getElementById("runningTextContent");
  
        // Safety check: ensure DOM elements exist
        if (!container || !content) return;
  
        // Check if we are on the login page or don't have a session. If so, hide and abort.
        var loginSection = document.getElementById("loginSection");
        var s = loadSession();
        if (!s || (loginSection && loginSection.style.display !== "none")) {
          container.style.display = "none";
          return;
        }
  
        // Hide running text when infografisSection is currently visible (active iframe page)
        var infografisSec = document.getElementById("infografisSection");
        if (infografisSec && infografisSec.style.display !== "none") {
          container.style.display = "none";
          return;
        }
  
        // Get today's date in WIB (UTC+7) as fallback
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var wibTime = new Date(utc + (7 * 3600000));
        var yyyy = wibTime.getFullYear();
        var MM = String(wibTime.getMonth() + 1).padStart(2, '0');
        var dd = String(wibTime.getDate()).padStart(2, '0');
        var todayDateStr = yyyy + "-" + MM + "-" + dd;
        var tanggal = todayDateStr;
  
        // If user has selected a date in the form, use that instead
        var tanggalEl = document.getElementById("tanggal");
        if (tanggalEl && tanggalEl.value) {
          tanggal = tanggalEl.value;
        }"""

running_text_new_logic = """      function updateRunningText() {
        var container = document.getElementById("runningTextContainer");
        var content = document.getElementById("runningTextContent");
  
        // Safety check: ensure DOM elements exist
        if (!container || !content) return;
  
        // Check if we are on the login page or don't have a session. If so, hide and abort.
        var loginSection = document.getElementById("loginSection");
        var s = loadSession();
        if (!s || (loginSection && loginSection.style.display !== "none")) {
          container.style.display = "none";
          return;
        }
  
        // Hide running text when infografisSection is currently visible (active iframe page)
        var infografisSec = document.getElementById("infografisSection");
        if (infografisSec && infografisSec.style.display !== "none") {
          container.style.display = "none";
          return;
        }
  
        // Use filter dates for marquee text
        var filterDates = getFilterDates();
        var tanggal = filterDates.start;
        var tanggal_akhir = filterDates.end;"""

content = content.replace(running_text_old_logic, running_text_new_logic)

# Replace the JSONP call in running text:
running_fetch_old = '{ action: "getRunningTextData", tanggal: tanggal, region: "ALL" }'
running_fetch_new = '{ action: "getRunningTextData", tanggal: tanggal, tanggal_akhir: tanggal_akhir, region: "ALL" }'
content = content.replace(running_fetch_old, running_fetch_new)

# 5. Initialize the filter inputs on login success
init_tgl_old = """            var tglInput = document.getElementById("tanggal");
            if (!tglInput.value) {
              var now = new Date();
              var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
              var wibTime = new Date(utc + (7 * 3600000));
              var yyyy = wibTime.getFullYear();
              var MM = String(wibTime.getMonth() + 1).padStart(2, '0');
              var dd = String(wibTime.getDate()).padStart(2, '0');
              tglInput.value = yyyy + "-" + MM + "-" + dd;
            }"""

init_tgl_new = """            var tglInput = document.getElementById("tanggal");
            var filterTglStart = document.getElementById("filterTanggalStart");
            var filterTglEnd = document.getElementById("filterTanggalEnd");
            
            var now = new Date();
            var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            var wibTime = new Date(utc + (7 * 3600000));
            var yyyy = wibTime.getFullYear();
            var MM = String(wibTime.getMonth() + 1).padStart(2, '0');
            var dd = String(wibTime.getDate()).padStart(2, '0');
            var todayWib = yyyy + "-" + MM + "-" + dd;

            if (!tglInput.value) {
              tglInput.value = todayWib;
            }
            if (filterTglStart && !filterTglStart.value) {
              filterTglStart.value = todayWib;
            }
            if (filterTglEnd && !filterTglEnd.value) {
              filterTglEnd.value = todayWib;
            }"""

content = content.replace(init_tgl_old, init_tgl_new)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Filters update applied successfully.")
