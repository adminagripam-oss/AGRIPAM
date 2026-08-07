import sys
import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Fonts, Material Symbols, and Tailwind config provided by user
tailwind_head_snippet = """
    <!-- Google Fonts: Hanken Grotesk -->
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700&display=swap" rel="stylesheet"/>
    <!-- Material Symbols -->
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: ['class', '[data-theme="dark"]'],
            corePlugins: { preflight: false },
            theme: {
                extend: {
                    "colors": {
                        "on-tertiary": "#ffffff",
                        "inverse-primary": "#64de87",
                        "on-background": "#191c1e",
                        "on-error-container": "#93000a",
                        "inverse-on-surface": "#eff1f3",
                        "surface-tint": "#006d34",
                        "on-primary-fixed": "#00210b",
                        "tertiary-fixed": "#d7e2ff",
                        "tertiary-container": "#2372df",
                        "on-surface-variant": "#3e4a3e",
                        "tertiary-fixed-dim": "#acc7ff",
                        "secondary": "#b7102a",
                        "error-container": "#ffdad6",
                        "surface": "#f7f9fb",
                        "outline": "#6e7a6d",
                        "surface-variant": "#e0e3e5",
                        "surface-dim": "#d8dadc",
                        "error": "#ba1a1a",
                        "on-tertiary-fixed-variant": "#004492",
                        "outline-variant": "#bdcabb",
                        "on-primary-fixed-variant": "#005225",
                        "on-primary": "#ffffff",
                        "secondary-container": "#db313f",
                        "surface-container-lowest": "#ffffff",
                        "surface-container-high": "#e6e8ea",
                        "primary-fixed": "#81fba1",
                        "on-secondary": "#ffffff",
                        "surface-container": "#eceef0",
                        "surface-bright": "#f7f9fb",
                        "secondary-fixed": "#ffdad8",
                        "secondary-fixed-dim": "#ffb3b1",
                        "on-tertiary-fixed": "#001a40",
                        "surface-container-low": "#f2f4f6",
                        "on-error": "#ffffff",
                        "primary-fixed-dim": "#64de87",
                        "inverse-surface": "#2d3133",
                        "tertiary": "#0059ba",
                        "on-surface": "#191c1e",
                        "on-secondary-container": "#fffbff",
                        "primary": "#006b32",
                        "background": "#f7f9fb",
                        "surface-container-highest": "#e0e3e5",
                        "on-tertiary-container": "#fefcff",
                        "primary-container": "#008741",
                        "on-secondary-fixed-variant": "#92001c",
                        "on-primary-container": "#f7fff3",
                        "on-secondary-fixed": "#410007"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.25rem",
                        "lg": "0.5rem",
                        "xl": "0.75rem",
                        "full": "9999px"
                    },
                    "spacing": {
                        "stack-md": "1.5rem",
                        "margin-mobile": "1rem",
                        "stack-sm": "0.5rem",
                        "gutter-md": "1rem",
                        "inset-squish": "0.75rem 1rem"
                    },
                    "fontFamily": {
                        "headline-md": ["Hanken Grotesk"],
                        "button-text": ["Hanken Grotesk"],
                        "body-md": ["Hanken Grotesk"],
                        "body-lg": ["Hanken Grotesk"],
                        "metric-display": ["Hanken Grotesk"],
                        "headline-lg": ["Hanken Grotesk"],
                        "label-caps": ["Hanken Grotesk"]
                    },
                    "fontSize": {
                        "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                        "button-text": ["14px", {"lineHeight": "20px", "fontWeight": "600"}],
                        "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                        "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                        "metric-display": ["28px", {"lineHeight": "34px", "fontWeight": "700"}],
                        "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                        "label-caps": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600"}]
                    }
                },
            },
        }
    </script>
    <style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .pulse-live {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse-ring {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>"""

# Replace the previous block from <!-- Tailwind CSS CDN --> to </head>
start_head_idx = content.find('  \n    <!-- Tailwind CSS CDN -->')
if start_head_idx == -1:
    start_head_idx = content.find('    <!-- Tailwind CSS CDN -->')

end_head_idx = content.find('</head>')

if start_head_idx != -1 and end_head_idx != -1:
    content = content[:start_head_idx] + tailwind_head_snippet + content[end_head_idx + 7:]

# 2. Replace mainSection
with open(r'C:\Users\JOI\.gemini\antigravity-ide\brain\0e64d8f8-2cd6-477e-9621-3208d72c564c\scratch\new_main_section.html', 'r', encoding='utf-8') as f:
    new_section = f.read()

start_marker = '  <!-- ===================== HALAMAN UTAMA ===================== -->'
end_marker = '  <!-- ===================== INFOGRAFIS ESTIMASI PANEN ===================== -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_section + '\n' + content[end_idx:]
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully updated login.html')
else:
    print('Could not find markers in login.html')
