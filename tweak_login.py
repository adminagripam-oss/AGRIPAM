import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Tailwind config to include keyframes and animations for ticker
tailwind_insert = """
              },
              keyframes: {
                ticker: {
                  '0%': { transform: 'translateX(100%)' },
                  '100%': { transform: 'translateX(-100%)' },
                },
                pulse2: {
                  '0%, 100%': { opacity: '1' },
                  '50%': { opacity: '0.5' },
                }
              },
              animation: {
                ticker: 'ticker 38s linear infinite',
                pulse2: 'pulse2 2s ease-in-out infinite',
              }
"""
content = content.replace('              }', tailwind_insert, 1)

# 2. Add .ticker-track css
style_insert = """
        .ticker-track {
            display: flex;
            white-space: nowrap;
            animation: ticker 38s linear infinite;
        }
        .ticker-track:hover {
            animation-play-state: paused;
        }
"""
content = content.replace('    <style>', '    <style>' + style_insert)

# 3. Add Side track to Monitoring
monitoring_orig = 'class="flex items-center gap-3 px-4 py-3 bg-secondary-container text-on-secondary-container font-semibold rounded-lg font-label-md text-label-md hover:bg-surface-container-high transition-colors" href="#" onclick="bukaDashboard()"'
monitoring_new = 'class="flex items-center gap-3 px-4 py-3 bg-secondary-container text-on-secondary-container font-semibold rounded-r-lg font-label-md text-label-md hover:bg-surface-container-high transition-colors border-l-4 border-primary" href="#" onclick="bukaDashboard()"'
content = content.replace(monitoring_orig, monitoring_new)

# 4. Change Estimation to Infografis
estimation_orig = """<span class="material-symbols-outlined">query_stats</span>
                    Estimation"""
estimation_new = """<span class="material-symbols-outlined">query_stats</span>
                    Infografis"""
content = content.replace(estimation_orig, estimation_new)

# 5. Change Reports to SAP
reports_orig = """<li>
                <a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#">
                    <span class="material-symbols-outlined">description</span>
                    Reports
                </a>
            </li>"""
reports_new = """<li>
                <a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface rounded-lg font-label-md text-label-md transition-colors" href="#" onclick="bukaSAP()" id="btnOpenSAP">
                    <span class="material-symbols-outlined">mail</span>
                    SAP
                    <span id="sapNotifBadge" class="hidden ml-auto">
                        <span class="flex h-3 w-3 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                        </span>
                    </span>
                </a>
            </li>"""
content = content.replace(reports_orig, reports_new)

# 6. Add running text at the very bottom of main content
running_text_html = """
        <!-- Running Text -->
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
        </div>
"""
content = content.replace('    </main>', running_text_html + '\n    </main>')

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Changes applied successfully.")
