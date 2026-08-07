import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace broken Tailwind script tag
content = re.sub(
    r'<!-- TailwindCSS -->\s*<script src="https://cdn\.tailwindcss\.com">\s*</script>\s*<script>',
    '<!-- TailwindCSS -->\n  <script src="https://cdn.tailwindcss.com"></script>\n  <script>',
    content
)

# Put window.checkCurrentRoute inside script tag
window_route_code = """
    // Global Route detector for /login.html/TKPanen or /TKPanen
    window.checkCurrentRoute = function() {
      var path = window.location.pathname || '';
      var hash = window.location.hash || '';
      if (path.includes('TKPanen') || path.includes('tk-panen') || hash === '#TKPanen') {
        if (typeof bukaTKPanenSection === 'function') {
          bukaTKPanenSection();
        }
      }
    };
    window.addEventListener('popstate', function() { if (typeof window.checkCurrentRoute === 'function') window.checkCurrentRoute(); });
    window.addEventListener('load', function() { if (typeof window.checkCurrentRoute === 'function') window.checkCurrentRoute(); });
"""

if 'window.checkCurrentRoute = function()' not in content:
    content = content.replace("  <!-- TailwindCSS -->\n  <script src=\"https://cdn.tailwindcss.com\"></script>\n  <script>", "  <!-- TailwindCSS -->\n  <script src=\"https://cdn.tailwindcss.com\"></script>\n  <script>" + window_route_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("CLEANED UP login.html FINAL!")
