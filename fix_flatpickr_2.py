import re

with open('shadcn_overrides.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_code = """        onChange: function (selectedDates, dateStr, instance) {
          input.value = dateStr;
          // If react input
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
          if (setter) setter.call(input, dateStr);
          input.dispatchEvent(new Event('change', { bubbles: true }));
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }"""

new_code = """        onChange: function (selectedDates, dateStr, instance) {
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
          if (setter) {
            setter.call(input, dateStr);
          } else {
            input.value = dateStr;
          }
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }"""

if old_code in js:
    js = js.replace(old_code, new_code)
    with open('shadcn_overrides.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed Flatpickr tracker bug")
else:
    print("Old code not found! Check manually.")
