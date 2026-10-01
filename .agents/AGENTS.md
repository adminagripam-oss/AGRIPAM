### Linktree and Portal Page Design Rule
**When building or modifying linktree, portal, or dashboard-entry pages, you MUST:**
1. **Apply Scroll-Reveal Animations:** Use Intersection Observer to trigger staggered fade-and-slide-in animations as elements scroll into view.
2. **Implement Advanced Hover Effects:** Add interactive 3D tilt effects to clickable cards/elements that react dynamically to the mouse cursor position.
3. **Use Premium Aesthetics:** Default to a modern, dynamic aesthetic (like Sci-Fi / Cosmic HUD or Glassmorphism as appropriate) with vibrant accents, glowing borders, and micro-animations to create a "wow" factor, unless the user specifies otherwise.

### TK Panen Data Structure & KPI Cut-Off Rule
**When working on or modifying TK Panen tables, modals, or KPI cards in `laporan_produksi.html` and `login.html`, AI agents MUST:**
1. **Default KPI Cut-Off Month:** Always use **September** (`tk_september` / `September`) as the default cut-off month for KPI card calculations and summary metrics.
2. **Ketersediaan TK Panen Sub-Columns (9 Columns):** 
   - TK Juni, TK Juli, Trend (Jul vs Jun), TK Ags, Trend (Ags vs Jul), **TK Sep**, **Trend (Sep vs Ags)**, SD Ags, SD Sep.
3. **Rencana Pemenuhan TK Panen Sub-Columns (4 Columns):**
   - Rencana Jul, Rencana Ags, Rencana Sep, **Rencana Okt**.
4. **Synchronized Persistence:** Ensure both `addKebun` and `updateTK` handlers in `api/kebunTK.js` and all modal forms (Edit Kebun & Tambah Kebun) read, validate, and save `tk_september` and `target_oktober`.

