// ==========================================
// Shadcn Alert Toast System
// ==========================================
window.showAlert = function (variant, title, message) {
  let container = document.getElementById('custom-alert-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'custom-alert-container';
    document.body.appendChild(container);
  }
  const alertEl = document.createElement('div');
  alertEl.className = 'shadcn-alert shadcn-alert-' + variant;
  let iconSvg = '';
  if (variant === 'success' || variant === 'invert') {
    iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-success"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>';
  } else if (variant === 'warning') {
    iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>';
  } else {
    iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>';
  }
  alertEl.innerHTML = iconSvg + '<h5 class="shadcn-alert-title">' + (title || 'Notification!') + '</h5><div class="shadcn-alert-desc">' + message + '</div>';
  container.appendChild(alertEl);
  setTimeout(function () {
    alertEl.classList.add('hiding');
    setTimeout(function () { alertEl.remove(); }, 300);
  }, 4000);
};

// Override native alert globally!
window.nativeAlert = window.alert;
window.alert = function (msg) {
  if (typeof msg === 'object') {
    try { msg = JSON.stringify(msg); } catch (e) { }
  }
  const lower = String(msg).toLowerCase();
  let variant = 'invert';
  let title = 'Notification!';

  if (lower.includes('berhasil') || lower.includes('sukses') || lower.includes('disetujui') || lower.includes('dihapus')) {
    variant = 'invert';
    title = 'Notification!';
  } else if (lower.includes('gagal') || lower.includes('error') || lower.includes('kesalahan') || lower.includes('tidak ditemukan') || lower.includes('tidak valid') || lower.includes('berakhir') || lower.includes('ditutup')) {
    variant = 'destructive';
    title = 'Error!';
  } else if (lower.includes('peringatan') || lower.includes('warning') || lower.includes('di luar batas')) {
    variant = 'warning';
    title = 'Warning!';
  }

  window.showAlert(variant, title, msg);
};


// ==========================================
// Shadcn Custom Select
// ==========================================
window.initShadcnSelect = function (selectId) {
  const selectEl = document.getElementById(selectId);
  if (!selectEl) return;
  if (selectEl.parentElement && selectEl.parentElement.classList.contains('shadcn-wrapper')) return;

  const wrapper = document.createElement('div');
  wrapper.className = 'relative w-full shadcn-wrapper';
  selectEl.parentNode.insertBefore(wrapper, selectEl);
  wrapper.appendChild(selectEl);
  selectEl.style.display = 'none';

  const trigger = document.createElement('button');
  trigger.type = 'button';
  trigger.className = 'custom-shadcn-trigger flex h-10 w-full items-center justify-between rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:cursor-not-allowed disabled:opacity-50 text-slate-700 hover:bg-slate-50 transition-colors text-left';

  const triggerText = document.createElement('span');
  triggerText.className = 'truncate pointer-events-none';
  triggerText.textContent = selectEl.options[selectEl.selectedIndex]?.text || 'Select...';

  const icon = document.createElement('div');
  icon.className = 'pointer-events-none opacity-50';
  icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down"><path d="m6 9 6 6 6-6"/></svg>';

  trigger.appendChild(triggerText);
  trigger.appendChild(icon);

  const popover = document.createElement('div');
  popover.className = 'custom-shadcn-popover-panel absolute z-[9999] mt-2 w-full min-w-[8rem] overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl hidden flex-col transition-all opacity-0 translate-y-[-5px]';

  const scrollArea = document.createElement('div');
  scrollArea.className = 'overflow-y-auto max-h-72 p-2 shadcn-scroll flex flex-col divide-y divide-gray-50 custom-shadcn-divide';

  popover.appendChild(scrollArea);

  const updateCheckmarks = () => {
    Array.from(scrollArea.children).forEach(child => {
      const val = child.getAttribute('data-value');
      const checkspan = child.querySelector('.check-container');
      if (val === selectEl.value) {
        checkspan.innerHTML = '<svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600"><path d="M11.4669 3.72684C11.7558 3.91574 11.8369 4.30308 11.648 4.59198L7.39799 11.092C7.29783 11.2452 7.13556 11.3467 6.95402 11.3699C6.77247 11.3931 6.58989 11.3355 6.45446 11.2124L3.70446 8.71241C3.44905 8.48022 3.43023 8.08494 3.66242 7.82953C3.89461 7.57412 4.28989 7.55529 4.5453 7.78749L6.75292 9.79441L10.6018 3.90792C10.7907 3.61902 11.178 3.53795 11.4669 3.72684Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path></svg>';
        child.classList.add('bg-green-50/50', 'text-green-700', 'font-medium');
      } else {
        checkspan.innerHTML = '';
        child.classList.remove('bg-green-50/50', 'text-green-700', 'font-medium');
      }
    });
  };

  Array.from(selectEl.options).forEach(opt => {
    if (opt.disabled && opt.value === "") return;

    const item = document.createElement('div');
    item.className = 'custom-shadcn-item relative flex w-full cursor-default select-none items-center rounded-lg py-2.5 pl-8 pr-2 text-sm outline-none hover:bg-gray-100 transition-colors text-slate-700';
    item.setAttribute('data-value', opt.value);

    const checkmark = document.createElement('span');
    checkmark.className = 'check-container absolute left-2 flex h-3.5 w-3.5 items-center justify-center';

    const itemText = document.createElement('span');
    itemText.textContent = opt.text;

    item.appendChild(checkmark);
    item.appendChild(itemText);

    item.addEventListener('click', (e) => {
      e.stopPropagation();
      selectEl.value = opt.value;
      triggerText.textContent = opt.text;

      popover.classList.remove('opacity-100', 'translate-y-0');
      popover.classList.add('opacity-0', 'translate-y-[-5px]');
      setTimeout(() => popover.classList.add('hidden'), 150);

      updateCheckmarks();
      selectEl.dispatchEvent(new Event('change'));
    });

    scrollArea.appendChild(item);
  });

  updateCheckmarks();

  wrapper.appendChild(trigger);
  wrapper.appendChild(popover);

  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    const isHidden = popover.classList.contains('hidden');

    document.querySelectorAll('.custom-shadcn-popover-panel').forEach(p => {
      if (p !== popover) {
        p.classList.remove('opacity-100', 'translate-y-0');
        p.classList.add('opacity-0', 'translate-y-[-5px]');
        setTimeout(() => p.classList.add('hidden'), 150);
      }
    });

    if (isHidden) {
      popover.classList.remove('hidden');
      requestAnimationFrame(() => {
        popover.classList.remove('opacity-0', 'translate-y-[-5px]');
        popover.classList.add('opacity-100', 'translate-y-0');
      });
    } else {
      popover.classList.remove('opacity-100', 'translate-y-0');
      popover.classList.add('opacity-0', 'translate-y-[-5px]');
      setTimeout(() => popover.classList.add('hidden'), 150);
    }
  });

  document.addEventListener('click', (e) => {
    if (!wrapper.contains(e.target)) {
      popover.classList.remove('opacity-100', 'translate-y-0');
      popover.classList.add('opacity-0', 'translate-y-[-5px]');
      setTimeout(() => popover.classList.add('hidden'), 150);
    }
  });

  selectEl.addEventListener('change', () => {
    if (selectEl.selectedIndex >= 0) {
      triggerText.textContent = selectEl.options[selectEl.selectedIndex].text;
      updateCheckmarks();
    }
  });

  // Expose update function for dynamically added options
  selectEl._rebuildShadcn = function () {
    scrollArea.innerHTML = '';
    Array.from(selectEl.options).forEach(opt => {
      if (opt.disabled && opt.value === "") return;
      const item = document.createElement('div');
      item.className = 'custom-shadcn-item relative flex w-full cursor-default select-none items-center rounded-lg py-2.5 pl-8 pr-2 text-sm outline-none hover:bg-gray-100 transition-colors text-slate-700';
      item.setAttribute('data-value', opt.value);
      const checkmark = document.createElement('span');
      checkmark.className = 'check-container absolute left-2 flex h-3.5 w-3.5 items-center justify-center';
      const itemText = document.createElement('span');
      itemText.textContent = opt.text;
      item.appendChild(checkmark);
      item.appendChild(itemText);
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        selectEl.value = opt.value;
        triggerText.textContent = opt.text;
        popover.classList.remove('opacity-100', 'translate-y-0');
        popover.classList.add('opacity-0', 'translate-y-[-5px]');
        setTimeout(() => popover.classList.add('hidden'), 150);
        updateCheckmarks();
        selectEl.dispatchEvent(new Event('change'));
      });
      scrollArea.appendChild(item);
    });
    updateCheckmarks();
    triggerText.textContent = selectEl.options[selectEl.selectedIndex]?.text || 'Select...';
  };
};

// ==========================================
// Shadcn Date Picker
// ==========================================
window.initShadcnDate = function () {
  if (typeof flatpickr === 'undefined') return;
  const dateInputs = document.querySelectorAll('input[type="date"], input[type="month"]');
  dateInputs.forEach(input => {
    if (input.parentElement && input.parentElement.classList.contains('shadcn-date-wrapper')) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'relative w-full shadcn-date-wrapper';
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const icon = document.createElement('div');
    icon.className = 'absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500 z-10';
    icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>';
    wrapper.appendChild(icon);

    input.classList.add('custom-shadcn-date');
    input.className = input.className.replace(/p-2/g, '').replace(/bg-gray-100/g, 'bg-white');
    input.classList.add('w-full', 'pl-10', 'pr-3', 'py-2', 'h-10', 'rounded-xl', 'border', 'border-gray-200', 'text-sm', 'font-medium', 'text-slate-700', 'transition-colors', 'focus:outline-none', 'focus:ring-2', 'focus:ring-green-500');

    // Hide native icon and convert to text to prevent internal shadow DOM from ignoring padding
    const isDate = input.type === 'date' || input.type === 'month';
    if (isDate) {
      input.setAttribute('type', 'text');
    }

    if (!input.disabled && !input.readOnly) {
      input.classList.add('cursor-pointer', 'hover:bg-slate-50');
      flatpickr(input, {
        dateFormat: "Y-m-d",
        disableMobile: true,
        allowInput: true,
        onChange: function (selectedDates, dateStr, instance) {
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
          if (setter) {
            setter.call(input, dateStr);
          } else {
            input.value = dateStr;
          }
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });
    } else if (input.disabled || input.readOnly) {
      input.classList.add('bg-slate-50', 'cursor-not-allowed', 'opacity-70');
    }
  });
};

// ==========================================
// Shadcn Alert Dialog (Confirm)
// ==========================================
window.showConfirm = function (title, description, type = 'destructive') {
  return new Promise((resolve) => {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'shadcn-dialog-overlay';

    // Create content box
    const dialog = document.createElement('div');
    dialog.id = 'shadcn-dialog-content';

    // Header
    const header = document.createElement('div');
    header.className = 'flex flex-col space-y-2 text-center sm:text-left';

    // Media / Icon wrapper
    const media = document.createElement('div');
    let iconHtml = '';

    if (type === 'success') {
      media.className = 'mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 sm:mx-0 sm:h-10 sm:w-10 dark:bg-emerald-900/20 dark:text-emerald-500 mb-2';
      iconHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>';
    } else {
      media.className = 'mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 text-red-600 sm:mx-0 sm:h-10 sm:w-10 dark:bg-red-900/20 dark:text-red-600 mb-2';
      iconHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>';
    }
    media.innerHTML = iconHtml;

    // Title
    const titleEl = document.createElement('h2');
    titleEl.className = 'text-lg font-semibold tracking-tight text-slate-900 dark:text-slate-50';
    titleEl.textContent = title;

    // Description
    const descEl = document.createElement('p');
    descEl.className = 'text-sm text-slate-500 dark:text-slate-400 mt-2 whitespace-pre-line';
    descEl.textContent = description;

    header.appendChild(media);
    header.appendChild(titleEl);
    header.appendChild(descEl);

    // Footer
    const footer = document.createElement('div');
    footer.className = 'flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 mt-6';

    // Cancel Button
    const btnCancel = document.createElement('button');
    btnCancel.className = 'mt-2 sm:mt-0 inline-flex h-10 items-center justify-center rounded-md border border-slate-200 bg-transparent px-4 py-2 text-sm font-semibold text-slate-900 transition-colors hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-100 dark:hover:bg-slate-800 dark:focus:ring-slate-400 dark:focus:ring-offset-slate-900';
    btnCancel.textContent = 'Batal';

    // Action Button
    const btnAction = document.createElement('button');
    if (type === 'success') {
      btnAction.className = 'inline-flex h-10 items-center justify-center rounded-md bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:hover:bg-emerald-700 dark:focus:ring-emerald-400 dark:focus:ring-offset-slate-900';
      btnAction.textContent = 'Lanjutkan';
    } else {
      btnAction.className = 'inline-flex h-10 items-center justify-center rounded-md bg-red-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:hover:bg-red-600 dark:focus:ring-red-400 dark:focus:ring-offset-slate-900';
      btnAction.textContent = 'Hapus';
    }

    footer.appendChild(btnCancel);
    footer.appendChild(btnAction);

    dialog.appendChild(header);
    dialog.appendChild(footer);

    document.body.appendChild(overlay);
    document.body.appendChild(dialog);

    const closeDialog = (result) => {
      overlay.classList.add('hiding');
      dialog.classList.add('hiding');
      setTimeout(() => {
        overlay.remove();
        dialog.remove();
        resolve(result);
      }, 200);
    };

    btnCancel.addEventListener('click', () => closeDialog(false));
    btnAction.addEventListener('click', () => closeDialog(true));
  });
};

// ==========================================
// Shadcn Inline Alerts (for form hints)
// ==========================================
window.renderInlineAlert = function (msg) {
  const lower = String(msg).toLowerCase();

  if (lower.includes('hanya dapat diisi') && lower.includes('waktu server anda saat ini')) {
    // Destructive Variant
    const cleanMsg = msg.replace('❌ Gagal: ', '').replace('Gagal: ', '');
    return `
      <div class="relative w-full rounded-lg border border-red-200 text-red-900 bg-red-50 dark:border-red-900/50 dark:text-red-200 dark:bg-red-950/50 p-4 text-left mt-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-4 top-4 h-5 w-5 text-red-600 dark:text-red-500"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <h5 class="mb-1 ml-8 font-medium leading-none tracking-tight text-red-800 dark:text-red-300">Error! Waktu Pengisian Ditolak</h5>
        <div class="text-sm ml-8 opacity-90 leading-relaxed">${cleanMsg}</div>
      </div>
    `;
  }

  if (lower.includes('waktu pengisian di luar batas')) {
    // Warning Variant
    const cleanMsg = msg.replace('⚠️ ', '');
    return `
      <div class="relative w-full rounded-lg border border-amber-200 text-amber-900 bg-amber-50 dark:border-amber-900/50 dark:text-amber-200 dark:bg-amber-950/50 p-4 text-left mt-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-4 top-4 h-5 w-5 text-amber-600 dark:text-amber-500"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        <h5 class="mb-1 ml-8 font-medium leading-none tracking-tight text-amber-800 dark:text-amber-300">Warning! Di Luar Batas</h5>
        <div class="text-sm ml-8 opacity-90 leading-relaxed">${cleanMsg}</div>
      </div>
    `;
  }

  // Invert Variant (Notification Alert)
  if (lower.includes('disetujui') || lower.includes('dihapus') || lower.includes('berhasil') || lower.includes('sukses') || lower.includes('notification')) {
    const cleanMsg = msg.replace('✅ ', '').replace('❌ ', '');
    return `
      <div class="relative w-full rounded-xl border border-slate-800 bg-slate-900 text-slate-50 p-4 text-left mt-2 shadow-lg dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-4 top-4 h-5 w-5 text-emerald-500"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <h5 class="mb-1 ml-8 font-semibold leading-none tracking-tight text-white">Notification!</h5>
        <div class="text-sm ml-8 text-slate-300 opacity-90 leading-relaxed">${cleanMsg}</div>
      </div>
    `;
  }

  return null;
};

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    // Automatically initialize dates
    window.initShadcnDate();

    // Automatically initialize custom selects (by ID)
    if (document.getElementById('loginRegion')) window.initShadcnSelect('loginRegion');
    if (document.getElementById('filterDateMode')) window.initShadcnSelect('filterDateMode');
    if (document.getElementById('jam')) window.initShadcnSelect('jam');
  }, 500);
});

