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

### Region Naming & Aggregation Harmonization Rule
**When displaying, grouping, or filtering regional data for TK Panen in `laporan_produksi.html`, `login.html`, and backend APIs:**
1. **Standard Region Label:** Always use **`Sumut 2`** as the official region name for all 10 Sumut 2 gardens (including `Bukit Harapan I`).
2. **Modal Aggregation Grouping:** Normalize any incoming region name containing `"Sumatera Utara 2"` or `"Torganda"` to **`Sumut 2`** so that all Sumut 2 gardens aggregate into a single unified row under **CRO I** in `MonitorTKModal`.
3. **Authentication Mapping:** Maintain `'Sumut 2': 'ROSUMUT2'` in `LOCAL_REGIONS_MAP` (`api/auth.js`) for seamless login authentication.

### TK Panen New Month Column Expansion Rule
**When adding a new monthly column to the TK Panen feature (e.g., Oktober, November, or any future month) for Ketersediaan TK Panen or Rencana Pemenuhan, AI agents MUST follow this checklist in order:**

1. **Database First (Supabase ALTER TABLE):**
   - Before touching any frontend or API code, create an `ALTER TABLE` SQL migration script.
   - Column naming: `tk_<bulan>` for Ketersediaan (e.g., `tk_oktober`) and `target_<bulan>` for Rencana Pemenuhan (e.g., `target_november`).
   - Use `ADD COLUMN IF NOT EXISTS <col_name> INT DEFAULT 0` to prevent errors on re-run.
   - Present the script to the user and **do not proceed** until they confirm the columns exist in Supabase.

2. **Backend API (`api/kebunTK.js`) — Three Required Touch Points:**
   - **Supabase fetch mapping loop** (`supaData.map` block): add explicit mapping with JSON fallback — `new_col: k.new_col !== undefined && k.new_col !== null ? k.new_col : (fb.new_col || 0)`.
   - **`fullPayload`** in the `updateTK` Supabase update block: add `new_col: item.new_col`.
   - **`safePayload`** (fallback payload): add `new_col: item.new_col` — never silently drop it.

3. **Frontend UI (`login.html` and `laporan_produksi.html`) — Three Required Touch Points:**
   - **Table header**: add the new `<th>` in the correct column position.
   - **Table row rendering**: add the `<td>` with value display and inline-edit input.
   - **Edit/Add modal forms**: add input fields with correct `id` attributes (e.g., `id="editTKOktoberVal"` / `id="addTKOktoberVal"`).

4. **Data Persistence Verification:**
   - Enter a test value → restart the local dev server (`node dev-server.js`) → confirm the value still appears.
   - If it disappears, the Supabase column is missing or the API payload is still incomplete.

5. **Update AGENTS.md:**
   - Update the `TK Panen Data Structure & KPI Cut-Off Rule` Sub-Columns lists to include the new column.
   - Update the `Synchronized Persistence` item with the new field name.

