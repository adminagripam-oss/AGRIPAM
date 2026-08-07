import sys
import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the head with new Tailwind config and fonts
tailwind_head_snippet = """
    <!-- Tailwind CSS & Fonts (Precision Ag Theme) -->
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "tertiary-fixed-dim": "#ffb95f",
                      "on-error": "#ffffff",
                      "on-primary-container": "#80bea6",
                      "on-error-container": "#93000a",
                      "inverse-surface": "#213145",
                      "tertiary-fixed": "#ffddb8",
                      "surface-dim": "#cbdbf5",
                      "on-secondary-fixed": "#002113",
                      "tertiary": "#442800",
                      "on-primary": "#ffffff",
                      "inverse-on-surface": "#eaf1ff",
                      "primary-fixed": "#b0f0d6",
                      "tertiary-container": "#623c00",
                      "primary-container": "#064e3b",
                      "on-tertiary": "#ffffff",
                      "on-primary-fixed-variant": "#0b513d",
                      "on-secondary-fixed-variant": "#005236",
                      "background": "#f8f9ff",
                      "surface": "#f8f9ff",
                      "surface-container-highest": "#d3e4fe",
                      "on-surface": "#0b1c30",
                      "primary": "#003527",
                      "on-background": "#0b1c30",
                      "surface-container": "#e5eeff",
                      "on-primary-fixed": "#002117",
                      "primary-fixed-dim": "#95d3ba",
                      "inverse-primary": "#95d3ba",
                      "surface-container-high": "#dce9ff",
                      "outline-variant": "#bfc9c3",
                      "on-tertiary-fixed": "#2a1700",
                      "on-secondary-container": "#00714d",
                      "secondary-container": "#6cf8bb",
                      "secondary": "#006c49",
                      "error": "#ba1a1a",
                      "on-secondary": "#ffffff",
                      "on-tertiary-fixed-variant": "#653e00",
                      "surface-container-lowest": "#ffffff",
                      "surface-variant": "#d3e4fe",
                      "surface-bright": "#f8f9ff",
                      "surface-tint": "#2b6954",
                      "on-tertiary-container": "#f69f0d",
                      "error-container": "#ffdad6",
                      "secondary-fixed-dim": "#4edea3",
                      "secondary-fixed": "#6ffbbe",
                      "on-surface-variant": "#404944",
                      "outline": "#707974",
                      "surface-container-low": "#eff4ff"
              },
              "borderRadius": {
                      "DEFAULT": "0.25rem",
                      "lg": "0.5rem",
                      "xl": "0.75rem",
                      "full": "9999px"
              },
              "spacing": {
                      "container-margin": "1rem",
                      "stack-gap": "1rem",
                      "card-padding": "1.25rem",
                      "inline-gap": "0.5rem",
                      "section-padding": "1.5rem"
              },
              "fontFamily": {
                      "label-md": ["Inter"],
                      "display-lg": ["Inter"],
                      "stat-value": ["Inter"],
                      "headline-sm": ["Inter"],
                      "headline-md": ["Inter"],
                      "body-lg": ["Inter"],
                      "body-md": ["Inter"]
              }
            }
          }
        }
    </script>
    <style>
        .glass-panel {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>"""

# Find current head injection and replace
start_head_idx = content.find('  <!-- Tailwind CSS CDN -->')
end_head_idx = content.find('</head>')

if start_head_idx != -1 and end_head_idx != -1:
    content = content[:start_head_idx] + tailwind_head_snippet + '\n' + content[end_head_idx+7:]

# 2. Extract new section HTML from user snippet
new_section = """
  <!-- ===================== HALAMAN UTAMA ===================== -->
  <div id="mainSection" style="display:none;" class="w-full flex min-h-screen bg-surface text-on-surface">
    <!-- SideNavBar -->
    <nav class="hidden md:flex fixed left-0 top-0 h-full z-50 flex-col p-4 w-64 bg-surface dark:bg-surface-dim transition-all duration-200 ease-in-out">
        <div class="mb-8 px-4 flex items-center gap-3">
            <img alt="Organization Logo" class="w-10 h-10 rounded-full bg-surface-container-high object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDC68ZpnvokNJBL4p-wrWScMYW9xQpdoNpibmmmv0EaFVT6LrXshAE2IEWwnRszI79pU3aqKcNP4ymPn0k313Vi_CfK1m5zYkqQ63Q040MZDjL-mHvwKfMXMc9qKbORf94bXaTSX_y7EZsCRExpkVPB0MDdlpz_lhRDxvu1cMATm6YVmYh1V-asYB0pfMbZWp4T5OtRIGu8LG-8nofOn_fsG8nKw_YtaKJiUSB-BGY93rXeD0CBWTcc9pePk0Sj-YBbyM1YOhvOg2k"/>
            <div>
                <h1 class="font-headline-sm text-headline-sm text-primary">Precision Ag</h1>
                <p class="font-label-md text-label-md text-on-surface-variant" id="displayRegionText">Regional Operations</p>
            </div>
        </div>
        <ul class="flex flex-col gap-2 flex-grow">
            <li>
                <a class="flex items-center gap-3 px-4 py-3 bg-secondary-container text-on-secondary-container font-semibold rounded-lg font-label-md text-label-md hover:bg-surface-container-high transition-colors" href="#" onclick="bukaDashboard()">
                    <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">analytics</span>
                    Monitoring
                </a>
            </li>
            <li>
                <a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#" id="btnOpenSAP" onclick="bukaSAP()">
                    <span class="material-symbols-outlined">fact_check</span>
                    Data Validation
                </a>
            </li>
            <li>
                <a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#" onclick="bukaInfografis()">
                    <span class="material-symbols-outlined">query_stats</span>
                    Estimation
                </a>
            </li>
            <li>
                <a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#">
                    <span class="material-symbols-outlined">description</span>
                    Reports
                </a>
            </li>
        </ul>
        <!-- Admin Dropdown placeholder so JS doesn't crash -->
        <div id="adminRegionSelectContainer" style="display:none;">
            <select id="adminRegionSelect" onchange="onAdminRegionChange()"></select>
            <select id="adminCROSelect" onchange="onAdminCROChange()"></select>
            <button onclick="onAdminTotalAllClick()">Total</button>
        </div>
        <div class="mt-auto border-t border-outline-variant/30 pt-4">
            <ul class="flex flex-col gap-2">
                <li>
                    <a class="flex items-center gap-3 px-4 py-2 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#">
                        <span class="material-symbols-outlined">help</span>
                        Help Center
                    </a>
                </li>
                <li>
                    <a class="flex items-center gap-3 px-4 py-2 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#" onclick="prosesLogout()">
                        <span class="material-symbols-outlined">logout</span>
                        Logout
                    </a>
                </li>
            </ul>
        </div>
    </nav>
    
    <!-- Main Content Area -->
    <main class="flex-grow md:ml-64 p-section-padding flex flex-col gap-stack-gap h-screen overflow-y-auto bg-background">
        <header class="flex justify-between items-center mb-4">
            <div>
                <div class="flex items-center gap-3 mb-1">
                    <h2 class="font-display-lg text-display-lg text-primary">Monitoring Panen</h2>
                    <span class="bg-secondary/10 text-secondary font-label-md text-label-md px-2 py-1 rounded-full border border-secondary/20 flex items-center gap-1">
                        <span class="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
                        LIVE
                    </span>
                </div>
                <p class="font-body-md text-body-md text-on-surface-variant" id="wibClockDate">Real-time agricultural yield tracking - 24 Okt 2023</p>
            </div>
            <div class="flex gap-inline-gap">
                <button class="w-10 h-10 rounded-full bg-surface-container-lowest shadow-sm flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high transition-colors">
                    <span class="material-symbols-outlined">notifications</span>
                </button>
            </div>
        </header>
        
        <!-- Filter Bar -->
        <div class="flex gap-inline-gap overflow-x-auto pb-2 scrollbar-hide">
            <div class="glass-panel px-4 py-2 rounded-full flex items-center gap-2 flex-shrink-0 cursor-pointer hover:border-primary transition-colors focus-within:border-primary">
                <span class="font-label-md text-label-md text-on-surface-variant">CRO:</span>
                <select class="bg-transparent font-body-md text-body-md text-on-surface outline-none border-none focus:ring-0 p-0 pr-6">
                    <option>All CROs</option>
                </select>
            </div>
            <div class="glass-panel px-4 py-2 rounded-full flex items-center gap-2 flex-shrink-0 cursor-pointer hover:border-primary transition-colors focus-within:border-primary">
                <span class="font-label-md text-label-md text-on-surface-variant">Regional:</span>
                <select class="bg-transparent font-body-md text-body-md text-on-surface outline-none border-none focus:ring-0 p-0 pr-6">
                    <option>National</option>
                </select>
            </div>
            <div class="glass-panel px-4 py-2 rounded-full flex items-center gap-2 flex-shrink-0 cursor-pointer hover:border-primary transition-colors focus-within:border-primary">
                <span class="font-label-md text-label-md text-on-surface-variant">Time:</span>
                <select class="bg-transparent font-body-md text-body-md text-on-surface outline-none border-none focus:ring-0 p-0 pr-6">
                    <option>Today</option>
                </select>
            </div>
        </div>

        <!-- Main Dashboard Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-stack-gap">
            <!-- Main Chart Area -->
            <div class="lg:col-span-2 glass-panel rounded-xl p-card-padding flex flex-col" id="chartCard">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h3 class="font-headline-md text-headline-md text-primary" id="chartTitle">Tren Produksi Per Jam</h3>
                        <p class="font-body-md text-body-md text-on-surface-variant">Tonnes harvested</p>
                    </div>
                    <!-- KPI Card within main area -->
                    <div class="bg-surface-container-lowest rounded-lg p-3 border border-outline-variant/30 flex items-center gap-4">
                        <div>
                            <p class="font-label-md text-label-md text-on-surface-variant">Total Kumulatif</p>
                            <p class="font-stat-value text-stat-value text-on-surface"><span id="compCardRealisasi">0.00</span><span class="font-body-md text-body-md text-on-surface-variant ml-1">Ton</span></p>
                        </div>
                        <div class="flex items-center text-secondary bg-secondary/10 px-2 py-1 rounded font-label-md text-label-md">
                            <span class="material-symbols-outlined text-sm">trending_up</span>
                            <span id="compCardPercentage">+0%</span>
                        </div>
                    </div>
                </div>
                
                <!-- Chart Canvas instead of fake bars -->
                <div id="chartContainer" class="flex-grow min-h-[300px] bg-surface-container-lowest rounded-lg border border-outline-variant/20 p-4 relative overflow-hidden">
                    <canvas id="realisasiChart"></canvas>
                </div>
            </div>

            <!-- Secondary Widgets Column -->
            <div class="flex flex-col gap-stack-gap">
                <!-- Kontribusi Regional -->
                <div class="glass-panel rounded-xl p-card-padding flex-1">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface mb-4">Input Data</h3>
                    
                    <form id="panenForm" onsubmit="return false;" class="space-y-3">
                        <div>
                            <label class="font-label-md text-on-surface-variant">Tanggal Laporan</label>
                            <input type="date" id="tanggal" name="tanggal" required onchange="onTanggalChange()" class="w-full mt-1 border-outline-variant rounded-md text-sm p-2 bg-surface">
                        </div>
                        <div>
                            <label class="font-label-md text-on-surface-variant">Jam Laporan</label>
                            <select id="jam" name="jam" required onchange="updateJamHint()" class="w-full mt-1 border-outline-variant rounded-md text-sm p-2 bg-surface">
                                <option value="" disabled selected>Pilih Jam...</option>
                                <option value="06.00">06.00</option>
                                <option value="07.00">07.00</option>
                                <option value="08.00">08.00</option>
                                <option value="09.00">09.00</option>
                                <option value="10.00">10.00</option>
                                <option value="11.00">11.00</option>
                                <option value="12.00">12.00</option>
                                <option value="13.00">13.00</option>
                                <option value="14.00">14.00</option>
                                <option value="15.00">15.00</option>
                                <option value="16.00">16.00</option>
                                <option value="17.30">17.30</option>
                            </select>
                            <small id="jamHint" class="text-[10px] text-on-surface-variant"></small>
                        </div>
                        <div>
                            <label class="font-label-md text-on-surface-variant">Realisasi (Ton)</label>
                            <input type="number" step="0.01" id="tonase" name="tonase" class="w-full mt-1 border-outline-variant rounded-md text-sm p-2 bg-surface">
                        </div>
                        <input type="hidden" id="akumulasi" value="0">
                        <div class="flex gap-2 pt-2">
                            <button type="button" id="submitBtn" onclick="handleInsert()" class="flex-1 bg-primary text-white text-sm py-2 rounded-md hover:bg-primary-container transition-colors">Kirim</button>
                            <button type="button" id="deleteBtn" onclick="handleDelete()" class="bg-error text-white text-sm py-2 px-3 rounded-md hover:bg-red-800 transition-colors">Hapus</button>
                        </div>
                        <p id="status" class="text-xs text-center font-bold mt-1 text-on-surface-variant"></p>
                    </form>

                </div>

                <!-- Leaderboard Widget -->
                <div class="glass-panel rounded-xl p-card-padding flex-1 overflow-hidden flex flex-col">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface mb-4">Estimasi Rencana</h3>
                    <div class="flex flex-col gap-3 flex-grow justify-center items-center">
                        <span class="font-stat-value text-3xl text-on-surface" id="compCardEstimasi">0.00 Ton</span>
                        <p id="sessionInfo" class="text-xs text-on-surface-variant mt-4"></p>
                    </div>
                </div>
            </div>
        </div>
    </main>
  </div>
"""

start_marker = '  <!-- ===================== HALAMAN UTAMA ===================== -->'
end_marker = '  <!-- ===================== INFOGRAFIS ESTIMASI PANEN ===================== -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_section + '\n' + content[end_idx:]
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully applied Precision Ag snippet.')
else:
    print('Could not find markers in login.html')
