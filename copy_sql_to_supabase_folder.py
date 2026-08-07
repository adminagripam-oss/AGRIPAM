import shutil
import os

source_sql = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\supabase_setup_data_kebun_tk.sql'
target_sql = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\supabase\setup_kebun_tk_table.sql'

os.makedirs(os.path.dirname(target_sql), exist_ok=True)
shutil.copyfile(source_sql, target_sql)

print(f"SUCCESSFULLY COPIED COMPLETE SQL SCRIPT TO: {target_sql}")
print(f"Target File Size: {os.path.getsize(target_sql)} bytes")
