import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Prepare new header block
new_header = """        <!-- Top Header -->
        <header class="flex-shrink-0 bg-white border-b border-slate-200 px-6 py-2.5 flex items-center justify-between transition-colors duration-300 mb-6 rounded-xl shadow-sm border">
          <div class="flex items-center gap-3">
            <img src="AGRINAS DANANTARA.png" alt="Agrinas Danantara" class="h-10 w-auto object-contain" />
            <p class="text-[12px] text-slate-400 leading-tight" id="wibClockDate">Tanggal</p>
          </div>
          <div class="flex items-center gap-4">
            <!-- Live indicator -->
            <div class="flex items-center gap-1.5 bg-green-50 border border-green-200 rounded-full px-3 py-1">
              <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span class="text-[11px] font-semibold text-green-700">LIVE</span>
            </div>
            <!-- Clock -->
            <div class="text-right hidden md:block">
              <div class="text-[15px] font-bold text-slate-700 tabular-nums" id="wibClockTime">--:--:--</div>
              <div class="text-[10px] text-slate-400">WIB</div>
            </div>
            <!-- Theme Toggle -->
            <button onclick="toggleTheme()" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100 transition-colors text-slate-500 ml-1">
               <svg class="sun-icon hidden" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
               <svg class="moon-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            </button>
          </div>
        </header>"""

# Replace the previous header block
header_pattern = re.compile(r'<!-- TopHeader / Header Section -->.*?<!-- Filter Bar -->', re.DOTALL)
if header_pattern.search(content):
    content = header_pattern.sub(new_header + '\n\n        <!-- Filter Bar -->', content)
else:
    # Try alternate match if the comment is slightly different
    header_pattern2 = re.compile(r'<header class="bg-white border border-gray-200 rounded-xl px-6 py-3.*?<!-- Filter Bar -->', re.DOTALL)
    content = header_pattern2.sub(new_header + '\n\n        <!-- Filter Bar -->', content)

# 2. Modify toggleTheme() to toggle class "hidden" for sun-icon and moon-icon
theme_func_target = """      function toggleTheme() {
        var currentTheme = document.documentElement.getAttribute("data-theme") || "light";
        var newTheme = currentTheme === "dark" ? "light" : "dark";
  
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("agripam_theme", newTheme);"""

theme_func_replacement = """      function toggleTheme() {
        var currentTheme = document.documentElement.getAttribute("data-theme") || "light";
        var newTheme = currentTheme === "dark" ? "light" : "dark";
  
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("agripam_theme", newTheme);

        var sunIcons = document.querySelectorAll(".sun-icon");
        var moonIcons = document.querySelectorAll(".moon-icon");
        if (newTheme === "dark") {
          sunIcons.forEach(function(el) { el.classList.remove("hidden"); });
          moonIcons.forEach(function(el) { el.classList.add("hidden"); });
        } else {
          sunIcons.forEach(function(el) { el.classList.add("hidden"); });
          moonIcons.forEach(function(el) { el.classList.remove("hidden"); });
        }"""

content = content.replace(theme_func_target, theme_func_replacement)

# Also ensure on page load theme icons are synced
onload_theme_sync = """      var savedTheme = localStorage.getItem("agripam_theme") || "light";
      document.documentElement.setAttribute("data-theme", savedTheme);"""

onload_theme_sync_replacement = """      var savedTheme = localStorage.getItem("agripam_theme") || "light";
      document.documentElement.setAttribute("data-theme", savedTheme);
      window.addEventListener('DOMContentLoaded', function() {
        var sunIcons = document.querySelectorAll(".sun-icon");
        var moonIcons = document.querySelectorAll(".moon-icon");
        if (savedTheme === "dark") {
          sunIcons.forEach(function(el) { el.classList.remove("hidden"); });
          moonIcons.forEach(function(el) { el.classList.add("hidden"); });
        } else {
          sunIcons.forEach(function(el) { el.classList.add("hidden"); });
          moonIcons.forEach(function(el) { el.classList.remove("hidden"); });
        }
      });"""

content = content.replace(onload_theme_sync, onload_theme_sync_replacement)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Header update applied successfully.")
