with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update legend HTML
legend_old = """                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3.5 h-3.5 bg-blue-500 rounded-sm mr-2 opacity-70"></span>
                  Estimasi Panen
                </div>"""

legend_new = """                <div class="flex items-center text-[10px] font-semibold text-slate-500">
                  <span class="w-3.5 h-3.5 bg-yellow-500 rounded-sm mr-2 opacity-70"></span>
                  Estimasi Panen
                </div>"""

content = content.replace(legend_old, legend_new)

# 2. Update gradient and dataset color config in updateDailyNationalChart
gradient_old = """          var gradientEst = chartCtx.createLinearGradient(0, 0, 0, 300);
          gradientEst.addColorStop(0, 'rgba(37, 99, 235, 0.2)'); // Blue
          gradientEst.addColorStop(1, 'rgba(37, 99, 235, 0.0)');"""

gradient_new = """          var gradientEst = chartCtx.createLinearGradient(0, 0, 0, 300);
          gradientEst.addColorStop(0, 'rgba(234, 179, 8, 0.3)'); // Yellow
          gradientEst.addColorStop(1, 'rgba(234, 179, 8, 0.0)');"""

content = content.replace(gradient_old, gradient_new)

dataset_old = """                {
                  label: 'Estimasi Panen (Ton)',
                  data: estimasiData,
                  borderColor: '#2563eb',
                  backgroundColor: gradientEst,
                  fill: true,
                  tension: 0.3,
                  borderWidth: 2,
                  pointRadius: 3,
                  pointBackgroundColor: '#2563eb'
                }"""

dataset_new = """                {
                  label: 'Estimasi Panen (Ton)',
                  data: estimasiData,
                  borderColor: '#eab308',
                  backgroundColor: gradientEst,
                  fill: true,
                  tension: 0.3,
                  borderWidth: 2,
                  pointRadius: 3,
                  pointBackgroundColor: '#eab308'
                }"""

content = content.replace(dataset_old, dataset_new)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Chart colors updated to Green (Realisasi) and Yellow (Estimasi) successfully.")
