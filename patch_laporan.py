import re

file_path = r'd:\AGRINAS PALMA NUSANTARA\AGRIPAM\laporan_produksi.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add NavItem in Sidebar component
nav_target = '<NavItem icon="calendar" label="RENCANA & REALISASI" active={activeNav === \'rencana-realisasi\'} onClick={() => handleNavClick(\'rencana-realisasi\')} collapsed={collapsed} isMobile={mobileOpen} />'
nav_replacement = nav_target + '\n                <NavItem icon="users" label="TK PANEN" active={activeNav === \'tk-panen\'} onClick={() => handleNavClick(\'tk-panen\')} collapsed={collapsed} isMobile={mobileOpen} />'

if nav_target in content and 'label="TK PANEN"' not in content:
    content = content.replace(nav_target, nav_replacement)
    print("Added TK PANEN to Sidebar nav in laporan_produksi.html")

# 2. Add TKPanenView component before ROOT APP
tk_view_code = '''
    // ============================================================
    // TK PANEN VIEW (Realisasi Tenaga Kerja Panen Kebun Juli & Agustus)
    // ============================================================
    function TKPanenView() {
      const [kebunData, setKebunData] = useState([]);
      const [loading, setLoading] = useState(true);
      const [saving, setSaving] = useState(false);
      const [selectedRegion, setSelectedRegion] = useState('ALL');
      const [searchQuery, setSearchQuery] = useState('');
      const [edits, setEdits] = useState({});
      const [summary, setSummary] = useState({});
      const [toastMsg, setToastMsg] = useState(null);

      const sessionRaw = sessionStorage.getItem("agripam_session");
      const session = sessionRaw ? JSON.parse(sessionRaw) : null;
      const userRegion = session ? session.region : 'ALL';
      const isAdmin = userRegion === 'ADMIN';

      const fetchKebunData = async (reg) => {
        setLoading(true);
        try {
          const reqReg = reg || (isAdmin ? 'ALL' : userRegion);
          const res = await fetch(`/api/kebunTK?action=getKebun&region=${encodeURIComponent(reqReg)}&_t=${Date.now()}`);
          const json = await res.json();
          if (json.success) {
            setKebunData(json.data || []);
            setSummary(json.summary || {});
          } else {
            setKebunData([]);
          }
        } catch (err) {
          console.error("Error fetching kebun TK data:", err);
          setKebunData([]);
        } finally {
          setLoading(false);
        }
      };

      useEffect(() => {
        fetchKebunData(selectedRegion);
      }, [selectedRegion]);

      const handleInputChange = (id, field, value) => {
        const valNum = Math.max(0, parseFloat(value) || 0);
        setEdits(prev => ({
          ...prev,
          [id]: {
            ...prev[id],
            [field]: valNum
          }
        }));
      };

      const handleSave = async () => {
        const editKeys = Object.keys(edits);
        if (editKeys.length === 0) {
          setToastMsg({ type: 'warning', text: 'Tidak ada perubahan data yang dibuat.' });
          setTimeout(() => setToastMsg(null), 3000);
          return;
        }

        setSaving(true);
        try {
          const editPayload = editKeys.map(id => ({
            id: parseInt(id, 10),
            ...edits[id]
          }));

          const res = await fetch('/api/kebunTK', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              action: 'updateTK',
              region: userRegion,
              token: session ? session.token : '',
              edits: editPayload
            })
          });

          const json = await res.json();
          if (json.success) {
            setToastMsg({ type: 'success', text: json.message || 'Data TK Panen berhasil disimpan!' });
            setEdits({});
            fetchKebunData(selectedRegion);
          } else {
            setToastMsg({ type: 'error', text: json.message || 'Gagal menyimpan data TK Panen.' });
          }
        } catch (err) {
          console.error("Error saving TK data:", err);
          setToastMsg({ type: 'error', text: 'Terjadi kesalahan saat menyimpan data.' });
        } finally {
          setSaving(false);
          setTimeout(() => setToastMsg(null), 4000);
        }
      };

      const filteredKebun = kebunData.filter(item => {
        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return (
          (item.nama_kebun && item.nama_kebun.toLowerCase().includes(q)) ||
          (item.name_tag && item.name_tag.toLowerCase().includes(q)) ||
          (item.region && item.region.toLowerCase().includes(q)) ||
          (item.cro && item.cro.toLowerCase().includes(q))
        );
      });

      const hasEdits = Object.keys(edits).length > 0;

      return (
        <div className="flex flex-col gap-6 w-full">
          {toastMsg && (
            <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded-xl shadow-xl border text-sm font-semibold flex items-center gap-2 animate-bounce ${
              toastMsg.type === 'success' ? 'bg-emerald-500 text-white border-emerald-600' :
              toastMsg.type === 'warning' ? 'bg-amber-500 text-white border-amber-600' :
              'bg-rose-500 text-white border-rose-600'
            }`}>
              <Icon name={toastMsg.type === 'success' ? 'check-circle' : 'alert-circle'} size={18} />
              <span>{toastMsg.text}</span>
            </div>
          )}

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-800 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-700 shadow-sm">
            <div>
              <div className="flex items-center gap-2.5">
                <span className="p-2 bg-emerald-100 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 rounded-xl">
                  <Icon name="users" size={20} />
                </span>
                <h1 className="text-xl font-extrabold text-slate-800 dark:text-slate-100">
                  Fitur Pengisian TK Panen
                </h1>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Input & Monitoring Realisasi Tenaga Kerja Panen Kebun (Bulan Juli & Agustus)
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              {isAdmin && (
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-slate-500">Filter Regional:</span>
                  <select
                    value={selectedRegion}
                    onChange={(e) => setSelectedRegion(e.target.value)}
                    className="px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="ALL">Semua Regional (23 Region)</option>
                    <option value="Aceh">Aceh</option>
                    <option value="Sumut 1">Sumut 1</option>
                    <option value="Sumut 2">Sumut 2</option>
                    <option value="Riau 1">Riau 1</option>
                    <option value="Riau 2">Riau 2</option>
                    <option value="Riau 3">Riau 3</option>
                    <option value="Riau 4">Riau 4</option>
                    <option value="Babel">Bangka Belitung</option>
                    <option value="Jambi">Jambi</option>
                    <option value="Sumbar">Sumatera Barat</option>
                    <option value="Sumsel">Sumatera Selatan</option>
                    <option value="Kalbar 1">Kalbar 1</option>
                    <option value="Kalbar 2">Kalbar 2</option>
                    <option value="Kalsel 1">Kalsel 1</option>
                    <option value="Kalsel 2">Kalsel 2</option>
                    <option value="Kaltara">Kaltara</option>
                    <option value="Kaltim">Kaltim</option>
                    <option value="Kalteng 1">Kalteng 1</option>
                    <option value="Kalteng 2">Kalteng 2</option>
                    <option value="Kalteng 3">Kalteng 3</option>
                    <option value="Sulteng">Sulteng</option>
                    <option value="Sultra">Sultra</option>
                    <option value="Papua Selatan">Papua Selatan</option>
                  </select>
                </div>
              )}

              <button
                onClick={handleSave}
                disabled={saving || !hasEdits}
                className={`px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 shadow-md transition-all ${
                  hasEdits
                    ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-500/20 active:scale-95'
                    : 'bg-slate-200 dark:bg-slate-700 text-slate-400 cursor-not-allowed'
                }`}
              >
                {saving ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                    <span>Menyimpan...</span>
                  </>
                ) : (
                  <>
                    <Icon name="save" size={16} />
                    <span>Simpan Data TK Panen {hasEdits ? `(${Object.keys(edits).length})` : ''}</span>
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            <div className="bg-white dark:bg-slate-800 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Jumlah Kebun</span>
              <div className="text-base font-extrabold text-slate-800 dark:text-slate-100 mt-1">{filteredKebun.length} Kebun</div>
            </div>
            <div className="bg-white dark:bg-slate-800 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Total Luas</span>
              <div className="text-base font-extrabold text-slate-800 dark:text-slate-100 mt-1">{formatRibuan(summary.totalLuas || 0)} Ha</div>
            </div>
            <div className="bg-white dark:bg-slate-800 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Realisasi Mei</span>
              <div className="text-base font-extrabold text-slate-800 dark:text-slate-100 mt-1">{formatRibuan(summary.totalMei || 0)} TK</div>
            </div>
            <div className="bg-white dark:bg-slate-800 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Realisasi Juni</span>
              <div className="text-base font-extrabold text-slate-800 dark:text-slate-100 mt-1">{formatRibuan(summary.totalJuni || 0)} TK</div>
            </div>
            <div className="bg-amber-50 dark:bg-amber-950/30 p-3.5 rounded-xl border border-amber-200 dark:border-amber-800/50">
              <span className="text-[10px] font-bold text-amber-700 dark:text-amber-400 uppercase">Target Juli (K)</span>
              <div className="text-base font-extrabold text-amber-800 dark:text-amber-300 mt-1">{formatRibuan(summary.totalJuliTgt || 0)} TK</div>
            </div>
            <div className="bg-red-50 dark:bg-red-950/30 p-3.5 rounded-xl border border-red-200 dark:border-red-800/50">
              <span className="text-[10px] font-bold text-red-700 dark:text-red-400 uppercase">TK Panen Juli (I)</span>
              <div className="text-base font-extrabold text-red-800 dark:text-red-300 mt-1">{formatRibuan(summary.totalJuliAct || 0)} TK</div>
            </div>
            <div className="bg-red-50 dark:bg-red-950/30 p-3.5 rounded-xl border border-red-200 dark:border-red-800/50">
              <span className="text-[10px] font-bold text-red-700 dark:text-red-400 uppercase">TK Panen Ags (J)</span>
              <div className="text-base font-extrabold text-red-800 dark:text-red-300 mt-1">{formatRibuan(summary.totalAgustAct || 0)} TK</div>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700 overflow-hidden shadow-sm">
            <div className="p-4 border-b border-slate-100 dark:border-slate-700/80 flex flex-wrap items-center justify-between gap-3">
              <div className="relative flex-1 min-w-[240px]">
                <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400">
                  <Icon name="search" size={16} />
                </span>
                <input
                  type="text"
                  placeholder="Cari kebun, tag kebun, atau regional..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div className="text-xs text-slate-500 font-medium">
                Menampilkan <span className="font-bold text-slate-800 dark:text-slate-200">{filteredKebun.length}</span> dari {kebunData.length} akun kebun
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 dark:bg-slate-900/80 text-[11px] font-bold text-slate-500 uppercase tracking-wider border-b border-slate-200 dark:border-slate-700">
                    <th className="py-3 px-3 text-center w-12">No</th>
                    <th className="py-3 px-3">CRO</th>
                    <th className="py-3 px-3">Regional</th>
                    <th className="py-3 px-4 min-w-[200px]">Nama Kebun / PT</th>
                    <th className="py-3 px-3">Tag Kebun</th>
                    <th className="py-3 px-3 text-right">Luas (Ha)</th>
                    <th className="py-3 px-3 text-right">Req TK</th>
                    <th className="py-3 px-3 text-right">TK Mei</th>
                    <th className="py-3 px-3 text-right">TK Juni</th>
                    <th className="py-3 px-3 text-right bg-amber-500/10 text-amber-700 dark:text-amber-400">Target Jul</th>
                    <th className="py-3 px-3 text-right bg-amber-500/10 text-amber-700 dark:text-amber-400">Target Ags</th>
                    <th className="py-3 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-x border-red-300 dark:border-red-800">
                      🟥 TK PANEN JULI (COL I)
                    </th>
                    <th className="py-3 px-4 text-center bg-red-500/20 text-red-700 dark:text-red-300 font-extrabold border-r border-red-300 dark:border-red-800">
                      🟥 TK PANEN AGUSTUS (COL J)
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700/50 text-xs">
                  {loading ? (
                    <tr>
                      <td colSpan="13" className="py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center gap-2">
                          <span className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></span>
                          <span>Memuat data kebun...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredKebun.length === 0 ? (
                    <tr>
                      <td colSpan="13" className="py-12 text-center text-slate-400">
                        Tidak ada data kebun yang sesuai.
                      </td>
                    </tr>
                  ) : (
                    filteredKebun.map((item, idx) => {
                      const itemEdit = edits[item.id] || {};
                      const valJuli = itemEdit.tk_juli !== undefined ? itemEdit.tk_juli : (item.tk_juli || 0);
                      const valAgs = itemEdit.tk_agustus !== undefined ? itemEdit.tk_agustus : (item.tk_agustus || 0);
                      const isEdited = edits[item.id] !== undefined;

                      return (
                        <tr key={item.id} className={`hover:bg-slate-50/80 dark:hover:bg-slate-700/30 transition-colors ${isEdited ? 'bg-emerald-50/50 dark:bg-emerald-950/20' : ''}`}>
                          <td className="py-2.5 px-3 text-center text-slate-400 font-medium">{idx + 1}</td>
                          <td className="py-2.5 px-3 font-semibold text-slate-700 dark:text-slate-300">{item.cro}</td>
                          <td className="py-2.5 px-3 font-medium text-slate-600 dark:text-slate-400">{item.region}</td>
                          <td className="py-2.5 px-4 font-bold text-slate-800 dark:text-slate-100">{item.nama_kebun}</td>
                          <td className="py-2.5 px-3 font-mono text-[11px] text-slate-500">{item.name_tag || '-'}</td>
                          <td className="py-2.5 px-3 text-right font-medium">{formatRibuan(item.luasan)}</td>
                          <td className="py-2.5 px-3 text-right font-medium">{formatRibuan(item.req_tk)}</td>
                          <td className="py-2.5 px-3 text-right font-medium text-slate-600 dark:text-slate-400">{formatRibuan(item.tk_mei)}</td>
                          <td className="py-2.5 px-3 text-right font-medium text-slate-600 dark:text-slate-400">{formatRibuan(item.tk_juni)}</td>
                          <td className="py-2.5 px-3 text-right font-semibold text-amber-700 dark:text-amber-400 bg-amber-500/5">{formatRibuan(item.target_juli)}</td>
                          <td className="py-2.5 px-3 text-right font-semibold text-amber-700 dark:text-amber-400 bg-amber-500/5">{formatRibuan(item.target_agustus)}</td>
                          
                          <td className="py-2.5 px-4 text-center bg-red-500/10 border-x border-red-200 dark:border-red-800/60">
                            <input
                              type="number"
                              min="0"
                              value={valJuli}
                              onChange={(e) => handleInputChange(item.id, 'tk_juli', e.target.value)}
                              className="w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm"
                            />
                          </td>

                          <td className="py-2.5 px-4 text-center bg-red-500/10 border-r border-red-200 dark:border-red-800/60">
                            <input
                              type="number"
                              min="0"
                              value={valAgs}
                              onChange={(e) => handleInputChange(item.id, 'tk_agustus', e.target.value)}
                              className="w-24 px-2 py-1 bg-white dark:bg-slate-900 border-2 border-red-400 dark:border-red-600 rounded-lg text-center font-bold text-red-700 dark:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 shadow-sm"
                            />
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      );
    }
'''

# Insert TKPanenView component before the ROOT APP comment if not already present
root_app_marker = '// ============================================================\n    // ROOT APP'
if 'function TKPanenView' not in content and root_app_marker in content:
    content = content.replace(root_app_marker, tk_view_code.strip() + '\n\n    ' + root_app_marker)
    print("Added TKPanenView component to laporan_produksi.html")

# 3. Add TKPanenView route in App component
tk_route_target = "activeNav === 'rencana-realisasi' && <RencanaRealisasiView />"
tk_route_replacement = tk_route_target + "\n              {activeNav === 'tk-panen' && <TKPanenView />}"

if tk_route_target in content and "'tk-panen' && <TKPanenView" not in content:
    content = content.replace(tk_route_target, tk_route_replacement)
    print("Added TKPanenView route in App component")

# Write patched file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("patch_laporan.py completed successfully.")
