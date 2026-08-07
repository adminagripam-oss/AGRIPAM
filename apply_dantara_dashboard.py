import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the head styles and Tailwind CDN
head_insert = """
    <!-- Tailwind CSS v3 & Fonts (Dantara Indonesia Theme) -->
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f6f9;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        .sidebar-active {
            position: relative;
            background-color: #f0fdf4 !important;
            color: #16a34a !important;
            border-left: 4px solid #16a34a;
            border-top-left-radius: 0 !important;
            border-bottom-left-radius: 0 !important;
        }
        @keyframes ticker-anim {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .ticker-track {
            display: flex;
            white-space: nowrap;
            animation: ticker-anim 38s linear infinite;
        }
        .ticker-track:hover {
            animation-play-state: paused;
        }
        @keyframes pulse2 {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .animate-pulse2 {
            animation: pulse2 2s ease-in-out infinite;
        }
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>"""

# Replace the previous CDN head area up to </head>
start_head_idx = content.find('    <!-- Tailwind CSS & Fonts (Precision Ag Theme) -->')
if start_head_idx == -1:
    start_head_idx = content.find('  <!-- Tailwind CSS CDN -->')
end_head_idx = content.find('</head>')

if start_head_idx != -1 and end_head_idx != -1:
    content = content[:start_head_idx] + head_insert + content[end_head_idx+7:]

# 2. Main content update
main_section_html = """
  <!-- ===================== HALAMAN UTAMA ===================== -->
  <div id="mainSection" style="display:none;" class="h-screen w-full flex overflow-hidden">
    <!-- LeftSidebar -->
    <aside class="w-16 bg-white border-r border-gray-200 flex flex-col items-center py-4 space-y-8 flex-shrink-0 z-20">
      <nav class="flex flex-col space-y-6">
        <!-- Button 1: Monitoring -->
        <button onclick="tutupSAP(); tutupEstimasiModal(); setActiveSidebar(0);" class="p-2 rounded-lg transition-colors sidebar-active bg-green-50 text-green-600" data-purpose="nav-item" title="Monitoring">
          <svg class="w-6 h-6" fill="currentColor" viewbox="0 0 20 20"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
        </button>
        <!-- Button 2: Infografis -->
        <button id="btnOpenInfografis" onclick="bukaInfografis(); setActiveSidebar(1);" class="p-2 text-gray-400 hover:bg-gray-50 rounded-lg transition-colors" data-purpose="nav-item" title="Infografis">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
        </button>
        <!-- Button 3: SAP -->
        <button id="btnOpenSAP" onclick="bukaSAP(); setActiveSidebar(2);" class="p-2 text-gray-400 hover:bg-gray-50 rounded-lg transition-colors relative" data-purpose="nav-item" title="SAP">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span id="sapNotifBadge" class="hidden absolute top-0 right-0">
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
          </span>
        </button>
      </nav>
      <!-- Admin Dropdown placeholder so JS doesn't crash -->
      <div id="adminRegionSelectContainer" style="display:none;">
          <select id="adminRegionSelect" onchange="onAdminRegionChange()"></select>
          <select id="adminCROSelect" onchange="onAdminCROChange()"></select>
          <button onclick="onAdminTotalAllClick()">Total</button>
      </div>
      <div class="mt-auto pb-4">
        <div class="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center text-[10px] font-bold" id="sidebarInitial">AD</div>
      </div>
    </aside>

    <!-- MainContentContainer -->
    <main class="flex-1 overflow-y-auto p-6 bg-[#f8fafc] custom-scrollbar flex flex-col justify-between">
      <div>
        <!-- TopHeader / Header Section -->
        <header class="bg-white border border-gray-200 rounded-xl px-6 py-3 flex items-center justify-between z-10 mb-6 shadow-sm">
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <img alt="Logo Dantara" class="h-10 w-auto" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDHtM49SF3kBAznE4ZpjpGfr2Az2yv8szygcpLu9AXnhpHScCpqu-_cfNfWCXTZBfUsvh0wcMOVxrTjoDI-JpA_JvGNKcxGBMlyJK-E3p6S7Fpp-UWnlTI0ULv_xJbb5tMYDjC1gkIIA8qs7-to2fuCfyuxevJkMJ8gZeJ2ctBvGg20wnFltlCugkfs3tQd4eV3UIhPelyuZGXHhECU77yP1w2_ZoPyEpBTvINx5kM1axhQhIChVt1PgDmEMrpQKNXYHDK5cEjBOhk0"/>
              <div>
                <h1 class="text-base font-bold leading-none text-slate-800">Danantara</h1>
                <p class="text-xs font-semibold text-slate-500 leading-none mt-1" id="displayRegionText">Indonesia</p>
              </div>
            </div>
            <div class="h-8 w-px bg-gray-300 mx-2"></div>
            <div class="flex items-center space-x-2">
              <img alt="Logo Agrinas" class="h-8 w-auto" src="https://lh3.googleusercontent.com/aida-public/AB6AXuA9In2fU8tbiU_BpEpuMcFLABTp9qK2wAvbSda_i2Bo0BrxpQwvRWiutWSy5VMHgrjc9fv5VEu4vTF_7huCBr5Li2cMohibACmNKZvvG8kg6jfjcH50HQ2AYl3OMfnbCK4J_28Nb5FvysUN7QBHwk7p_6JkQ7zBWbmHBUVuz2Ggo5ng3uHvzDcQINidi9H2uOtr7wooNYND3s_L8ZyEaqNA0Y6bHNcEgwjStfuw8Ix6a6oWTqK68pfAn_NGuJTKXBDE33HL5Hfc8vri"/>
              <div class="text-[9px] font-bold text-green-700 leading-tight">
                AGRINAS PALMA<br/>NUSANTARA
              </div>
            </div>
            <span class="text-gray-400 text-xs ml-4" id="wibClockDate">Tanggal</span>
          </div>
          <div class="flex items-center space-x-6">
            <div class="flex items-center bg-green-50 text-green-600 px-3 py-1 rounded-full text-xs font-bold border border-green-200">
              <span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              LIVE
            </div>
            <div class="text-right">
              <div class="text-lg font-bold text-slate-800 tabular-nums" id="wibClockTime">--:--:--</div>
              <div class="text-[9px] text-gray-400 font-medium">WIB</div>
            </div>
          </div>
        </header>

        <!-- Filter Bar -->
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
        </section>

        <!-- ProductionTrends & Input Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <!-- Chart Area -->
          <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col">
            <div class="flex justify-between items-start mb-6">
              <div>
                <h2 class="text-base font-bold text-slate-800" id="chartTitle">Tren Produksi Per Jam</h2>
                <p class="text-xs text-gray-400">Tonnes harvested</p>
              </div>
              <div class="text-right">
                <div class="flex items-center justify-end">
                  <span class="text-xl font-bold text-green-600 mr-2" id="compCardRealisasi">0.00 ton</span>
                  <div class="bg-red-50 text-red-600 text-[10px] font-bold px-2 py-0.5 rounded border border-red-100 flex items-center">
                    <span id="compCardPercentage">+0.00%</span>
                  </div>
                </div>
                <div class="text-[10px] text-gray-400">dari est. <span id="compCardEstimasi">0.00</span> ton</div>
              </div>
            </div>
            <!-- Chart Container -->
            <div id="chartContainer" class="h-64 relative w-full flex-grow">
              <canvas id="realisasiChart"></canvas>
            </div>
          </div>

          <!-- Input Form Card -->
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
                </div>
                
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Jam Laporan</label>
                  <select id="jam" name="jam" required onchange="updateJamHint()" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500">
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
                  <small class="text-[10px] text-slate-400 block mt-1" id="jamHint"></small>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Realisasi (Ton)</label>
                  <input type="number" step="0.01" id="tonase" name="tonase" class="w-full border border-gray-200 rounded-lg p-2 text-sm text-slate-700 focus:outline-none focus:border-green-500" placeholder="0.00">
                </div>

                <input type="hidden" id="akumulasi" value="0">

                <div class="flex gap-2 pt-2">
                  <button type="button" id="submitBtn" onclick="handleInsert()" class="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg text-sm transition-colors">
                    Kirim Data
                  </button>
                  <button type="button" id="deleteBtn" onclick="handleDelete()" class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-3 rounded-lg text-sm transition-colors" title="Hapus Jam">
                    Hapus
                  </button>
                  <button type="button" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-3 rounded-lg text-sm transition-colors" onclick="checkAccumulation()" title="Refresh Akumulasi">
                    <span class="material-symbols-outlined text-[18px]">refresh</span>
                  </button>
                </div>
              </form>
            </div>
            <p id="status" class="text-xs text-center mt-2 font-semibold"></p>
          </div>
        </div>

        <!-- MidSectionGrid (Contribution & Leaderboard) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <!-- RegionalContribution -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col">
            <h2 class="text-base font-bold text-slate-800 mb-1">Kontribusi Panen Tiap Regional</h2>
            <p class="text-xs text-gray-400 mb-6">Proporsi realisasi nasional s.d. jam ini</p>
            <div class="flex-1 flex flex-col items-center justify-center relative">
              <div class="w-48 h-48 rounded-full border-[18px] border-slate-100 relative flex items-center justify-center">
                <div class="absolute inset-0 rounded-full" style="background: conic-gradient(#16a34a 0% 40%, #2563eb 40% 60%, #ea580c 60% 75%, #ca8a04 75% 100%); mask: radial-gradient(circle, transparent 58%, black 60%);"></div>
                <div class="text-center">
                  <div class="text-2xl font-black text-slate-800 leading-none">100%</div>
                  <div class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">Ton Total</div>
                </div>
              </div>
              <div class="w-full mt-8 space-y-2">
                <div class="flex justify-between items-center text-xs">
                  <div class="flex items-center">
                    <span class="w-3 h-3 bg-green-600 rounded-sm mr-2"></span>
                    <span class="text-slate-600">Aceh</span>
                  </div>
                  <div class="flex space-x-4">
                    <span class="font-semibold text-slate-800">2,50 ton</span>
                    <span class="text-gray-400">0.1%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- RegionalLeaderboard -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 lg:col-span-2">
            <h2 class="text-base font-bold text-slate-800 mb-1">Leaderboard Regional</h2>
            <p class="text-xs text-gray-400 mb-6">Ranking berdasarkan data s.d. jam saat ini</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <div class="flex items-center space-x-2 text-xs font-bold text-green-700 mb-4">
                  <svg class="w-4 h-4" fill="currentColor" viewbox="0 0 20 20"><path clip-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.789l1.599.8L9 4.323V3a1 1 0 011-1z" fill-rule="evenodd"></path></svg>
                  <span>Top 5 Output Panen</span>
                </div>
                <div class="space-y-4">
                  <div class="flex items-center">
                    <div class="w-6 h-6 rounded-full bg-orange-400 text-white flex items-center justify-center text-[10px] font-bold mr-3 shrink-0">1</div>
                    <div class="flex-1">
                      <div class="flex justify-between items-baseline mb-1">
                        <span class="text-xs font-bold text-slate-700">Aceh</span>
                        <span class="text-xs font-bold text-slate-900">2.50 <span class="text-[10px] font-medium text-gray-400">ton</span></span>
                      </div>
                      <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-green-500 h-full rounded-full" style="width: 100%;"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <div class="flex items-center space-x-2 text-xs font-bold text-orange-700 mb-4">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewbox="0 0 24 24"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                  <span>Top 5 Restan Hari Ini</span>
                </div>
                <div class="space-y-4">
                  <div class="flex items-center">
                    <div class="w-6 h-6 rounded-full bg-orange-400 text-white flex items-center justify-center text-[10px] font-bold mr-3 shrink-0">1</div>
                    <div class="flex-1">
                      <div class="flex justify-between items-baseline mb-1">
                        <span class="text-xs font-bold text-slate-700">Aceh</span>
                        <span class="text-xs font-bold text-slate-900">0.00 <span class="text-[10px] font-medium text-gray-400">ton</span></span>
                      </div>
                      <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-orange-600 h-full rounded-full" style="width: 0%;"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RealizationVsEstimation -->
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
        </section>
      </div>

      <!-- Ticker Row & Footer -->
      <div>
        <!-- Running Text Ticker (Exactly like Admin) -->
        <section id="runningTextContainer" class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex-shrink-0 mb-6" style="display: none;">
          <div class="flex items-stretch">
            <div class="bg-red-600 flex items-center gap-2 px-4 py-2.5 flex-shrink-0">
              <div class="w-1.5 h-1.5 rounded-full bg-white animate-pulse2"></div>
              <span class="text-[11px] font-bold text-white uppercase tracking-wider whitespace-nowrap">AGRIPAM</span>
            </div>
            <div class="flex-1 overflow-hidden bg-red-50">
              <div class="ticker-track py-2.5">
                <span class="text-[12.5px] text-red-800 font-medium px-8" id="runningTextContent">Mengambil data hasil produksi...</span>
              </div>
            </div>
          </div>
        </section>

        <footer class="flex flex-col items-center justify-center pb-6">
          <p id="sessionInfo" class="text-[10px] text-slate-400 mb-2"></p>
          <span class="text-[9px] font-bold text-slate-400 tracking-[0.2em] uppercase">Patriot - Loyal - Profesional</span>
        </footer>
      </div>
    </main>
    <script>
      function setActiveSidebar(index) {
        const buttons = document.querySelectorAll('[data-purpose="nav-item"]');
        buttons.forEach((btn, idx) => {
          if (idx === index) {
            btn.classList.add('sidebar-active', 'bg-green-50', 'text-green-600');
            btn.classList.remove('text-gray-400', 'hover:bg-gray-50');
          } else {
            btn.classList.remove('sidebar-active', 'bg-green-50', 'text-green-600');
            btn.classList.add('text-gray-400', 'hover:bg-gray-50');
          }
        });
      }
    </script>
  </div>
"""

# Replace mainSection
start_marker = '  <!-- ===================== HALAMAN UTAMA ===================== -->'
end_marker = '  <!-- ===================== INFOGRAFIS ESTIMASI PANEN ===================== -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + main_section_html + '\n' + content[end_idx:]

# 3. Modify tutupSAP and tutupEstimasiModal inside JS to set active sidebar to 0
# Let's search and replace inside javascript functions
tutup_sap_target = """    function tutupSAP() {
      var sapSec = document.getElementById("sapSection");"""
tutup_sap_replacement = """    function tutupSAP() {
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
      var sapSec = document.getElementById("sapSection");"""

tutup_estimasi_target = """    function tutupEstimasiModal() {
      var estimasiSec = document.getElementById("estimasiSection");"""
tutup_estimasi_replacement = """    function tutupEstimasiModal() {
      if (typeof setActiveSidebar === 'function') setActiveSidebar(0);
      var estimasiSec = document.getElementById("estimasiSection");"""

content = content.replace(tutup_sap_target, tutup_sap_replacement)
content = content.replace(tutup_estimasi_target, tutup_estimasi_replacement)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Dantara Indonesia theme changes applied successfully.")
