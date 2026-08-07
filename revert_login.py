import sys
import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Restore the old Tailwind config in the head
tailwind_head_snippet = """
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: ['class', '[data-theme="dark"]'],
      corePlugins: { preflight: false },
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'Trebuchet MS', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#f0fdf4',
              100: '#dcfce7',
              200: '#bbf7d0',
              400: '#4ade80',
              500: '#22c55e',
              600: '#16a34a',
              700: '#15803d',
              800: '#166534',
              900: '#14532d',
            },
          }
        },
      },
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>"""

# Replace the Hanken Grotesk block up to </head>
start_head_idx = content.find('    <!-- Google Fonts: Hanken Grotesk -->')
end_head_idx = content.find('</head>')

if start_head_idx != -1 and end_head_idx != -1:
    content = content[:start_head_idx] + tailwind_head_snippet + '\n' + content[end_head_idx:]

# 2. Replace mainSection with admin style
with open(r'C:\Users\JOI\.gemini\antigravity-ide\brain\0e64d8f8-2cd6-477e-9621-3208d72c564c\scratch\new_main_section_admin.html', 'r', encoding='utf-8') as f:
    new_section = f.read()

start_marker = '  <!-- ===================== HALAMAN UTAMA ===================== -->'
end_marker = '  <!-- ===================== INFOGRAFIS ESTIMASI PANEN ===================== -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_section + '\n' + content[end_idx:]
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully restored login.html to Admin style')
else:
    print('Could not find markers in login.html')
