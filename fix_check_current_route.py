file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\login.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define checkCurrentRoute globally on window object before anything else calls it
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
    window.addEventListener('popstate', function() { window.checkCurrentRoute(); });
    window.addEventListener('load', function() { window.checkCurrentRoute(); });
"""

# Replace any existing duplicate checkCurrentRoute definitions
content = content.replace("""    // Route detector for /login.html/TKPanen or /TKPanen on load and popstate
    function checkCurrentRoute() {
      var path = window.location.pathname || '';
      var hash = window.location.hash || '';
      if (path.includes('TKPanen') || path.includes('tk-panen') || hash === '#TKPanen') {
        bukaTKPanenSection();
      }
    }

    window.addEventListener('popstate', checkCurrentRoute);
    window.addEventListener('load', checkCurrentRoute);""", "")

content = content.replace("""    // Hash router listener for #TKPanen
    window.addEventListener('hashchange', function() {
      if (window.location.hash === '#TKPanen' || window.location.href.includes('TKPanen')) {
        bukaTKPanenSection();
      } else {
        tutupTKPanenSection();
      }
    });""", "")

# Insert window.checkCurrentRoute right after <script> tag on line 1842
target_head = '<script src="https://cdn.tailwindcss.com"></script>\n  <script>'
replacement_head = '<script src="https://cdn.tailwindcss.com"></script>\n  <script>' + window_route_code

if target_head in content:
    content = content.replace(target_head, replacement_head)
    print("Inserted window.checkCurrentRoute at top script head.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIXED checkCurrentRoute ReferenceError!")
