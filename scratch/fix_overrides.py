with open('shadcn_overrides.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """  if (status === 'APPROVED') {
    return `
      <div class="relative w-full rounded-xl border border-emerald-200 bg-emerald-50 dark:border-emerald-900/50 dark:bg-emerald-950/50 p-4 text-left shadow-sm flex items-center gap-3 text-emerald-900 dark:text-emerald-200 mb-4 transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-emerald-600 dark:text-emerald-500 shrink-0"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
    } else if (input.disabled || input.readOnly) {
      input.classList.add('bg-slate-50', 'cursor-not-allowed', 'opacity-70');
    }
  });
};"""

replacement = """  if (status === 'APPROVED') {
    return `
      <div class="relative w-full rounded-xl border border-emerald-200 bg-emerald-50 dark:border-emerald-900/50 dark:bg-emerald-950/50 p-4 text-left shadow-sm flex items-center gap-3 text-emerald-900 dark:text-emerald-200 mb-4 transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-emerald-600 dark:text-emerald-500 shrink-0"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <div>
          <h5 class="font-semibold leading-none tracking-tight text-emerald-800 dark:text-emerald-300">Success! All good</h5>
          <div class="text-sm opacity-90 mt-1">Akses revisi tanggal ini${formattedDate ? ' (' + formattedDate + ')' : ''} telah disetujui Admin</div>
        </div>
      </div>
    `;
  }
  return '';
};"""

if target in text:
    text = text.replace(target, replacement)
    with open('shadcn_overrides.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESSFULLY REPLACED")
else:
    print("TARGET NOT MATCHED")
