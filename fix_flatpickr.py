import re

with open('shadcn_overrides.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_event = "input.dispatchEvent(new Event('change', { bubbles: true }));"
new_event = "input.dispatchEvent(new Event('change', { bubbles: true }));\n          input.dispatchEvent(new Event('input', { bubbles: true }));"

if old_event in js and new_event not in js:
    js = js.replace(old_event, new_event)
    with open('shadcn_overrides.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed Flatpickr events")
else:
    print("Already fixed or not found")
