import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Using regex to target checkAccumulation function definition exactly
pattern = r'(function checkAccumulation\(isSilent\) \{\s*)var tanggal = document\.getElementById\("tanggal"\)\.value;'

# Replace with getFilterDates version
replacement = r'\1var filterDates = getFilterDates();\n      var tanggal = filterDates.start;\n      var tanggal_akhir = filterDates.end;'

new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)

if count > 0:
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully replaced checkAccumulation start block ({count} occurrences).")
else:
    # Fallback to direct lines replacement
    print("Regex match failed, let's do a direct lines replacement.")
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "function checkAccumulation" in line:
            print(f"Found function checkAccumulation on line {idx + 1}")
            if "var tanggal =" in lines[idx+1]:
                lines[idx+1] = "      var filterDates = getFilterDates();\n      var tanggal = filterDates.start;\n      var tanggal_akhir = filterDates.end;"
                print("Replaced successfully!")
                break
    with open('login.html', 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
