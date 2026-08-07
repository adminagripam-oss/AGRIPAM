import os
import re

filepath = r'supabase/schema.sql'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Jambi password
content = re.sub(
    r"\('Jambi',\s*crypt\('ROJambi',\s*gen_salt\('bf',\s*10\)\)\),",
    r"('Jambi',                       crypt('ROJ4mb1',     gen_salt('bf', 10))),",
    content
)

# Replace Kalimantan Barat 1
content = re.sub(
    r"\('Kalimantan Barat 1',\s*crypt\('ROKalbar1',\s*gen_salt\('bf',\s*10\)\)\),",
    r"('Kalimantan Barat 1A',         crypt('ROKalbar1a',  gen_salt('bf', 10))),\n  ('Kalimantan Barat 1B',         crypt('ROKalbar1B',  gen_salt('bf', 10))),",
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {filepath}")
