import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace updateEstimasiComparison to remove card dependencies
comparison_old = """    function updateEstimasiComparison() {
      var card = document.getElementById("estimasiComparisonCard");
      var compEstimasi = document.getElementById("compCardEstimasi");
      var compRealisasi = document.getElementById("compCardRealisasi");
      var compPercentage = document.getElementById("compCardPercentage");

      if (!card || !compEstimasi || !compRealisasi || !compPercentage) return;

      var tanggal = document.getElementById("tanggal").value;
      var s = loadSession();

      if (!tanggal || !s) {
        card.style.display = "none";
        return;
      }

      var totalRealisasi = parseFloat(document.getElementById("akumulasi").value) || 0;

      card.style.display = "block";
      compRealisasi.textContent = formatNumberId(totalRealisasi) + " Ton";

      if (currentEstimasiPanen > 0) {
        compEstimasi.textContent = formatNumberId(currentEstimasiPanen) + " Ton";
        var pct = (totalRealisasi / currentEstimasiPanen) * 100;
        compPercentage.textContent = formatNumberId(pct) + "%";

        if (pct >= 100) {
          compPercentage.style.color = "#28a745"; // Green
        } else if (pct >= 80) {
          compPercentage.style.color = "#ffa600"; // Orange
        } else {
          compPercentage.style.color = "#dc3545"; // Red
        }
      } else {
        compEstimasi.textContent = "0,00 Ton";
        compPercentage.textContent = "0,00%";
        compPercentage.style.color = "var(--text-muted)";
      }
      updateChart();
    }"""

comparison_new = """    function updateEstimasiComparison() {
      var compEstimasi = document.getElementById("compCardEstimasi");
      var compRealisasi = document.getElementById("compCardRealisasi");
      var compPercentage = document.getElementById("compCardPercentage");

      if (!compEstimasi || !compRealisasi || !compPercentage) return;

      var tanggal = document.getElementById("tanggal").value;
      var s = loadSession();

      if (!tanggal || !s) {
        return;
      }

      var totalRealisasi = parseFloat(document.getElementById("akumulasi").value) || 0;

      compRealisasi.textContent = formatNumberId(totalRealisasi) + " Ton";

      if (currentEstimasiPanen > 0) {
        compEstimasi.textContent = formatNumberId(currentEstimasiPanen) + " Ton";
        var pct = (totalRealisasi / currentEstimasiPanen) * 100;
        compPercentage.textContent = formatNumberId(pct) + "%";

        if (pct >= 100) {
          compPercentage.style.color = "#28a745"; // Green
        } else if (pct >= 80) {
          compPercentage.style.color = "#ffa600"; // Orange
        } else {
          compPercentage.style.color = "#dc3545"; // Red
        }
      } else {
        compEstimasi.textContent = "0,00 Ton";
        compPercentage.textContent = "0,00%";
        compPercentage.style.color = "var(--text-muted)";
      }
      updateChart();
    }"""

content = content.replace(comparison_old, comparison_new)

# 2. Update updateDailyNationalChart to filter by s.region instead of "ALL"
daily_fetch_old = """        // Fetch realisasi data
        jsonpRequest(
          { action: "getData", tanggal: startOfMonth, tanggal_akhir: todayWib, region: "ALL" },
          function (res) {
            realRecords = (res && res.success) ? (res.allRecords || []) : [];
            realisasiLoaded = true;
            drawChart();
          },
          function () {
            realisasiLoaded = true;
            drawChart();
          }
        );

        // Fetch estimasi data
        jsonpRequest(
          { action: "getEstimasi", tanggal: startOfMonth, tanggal_akhir: todayWib, region: "ALL", token: s.token },"""

daily_fetch_new = """        // Fetch realisasi data
        jsonpRequest(
          { action: "getData", tanggal: startOfMonth, tanggal_akhir: todayWib, region: s.region },
          function (res) {
            realRecords = (res && res.success) ? (res.allRecords || []) : [];
            realisasiLoaded = true;
            drawChart();
          },
          function () {
            realisasiLoaded = true;
            drawChart();
          }
        );

        // Fetch estimasi data
        jsonpRequest(
          { action: "getEstimasi", tanggal: startOfMonth, tanggal_akhir: todayWib, region: s.region, token: s.token },"""

content = content.replace(daily_fetch_old, daily_fetch_new)

# 3. Dynamic Chart Title inside applyUserRoleUI
role_ui_old = """        if (adminContainer) adminContainer.style.display = "none";
        if (panenInputFields) panenInputFields.style.display = "block";
      }
    }"""

role_ui_new = """        if (adminContainer) adminContainer.style.display = "none";
        if (panenInputFields) panenInputFields.style.display = "block";

        var chartTitle = document.getElementById("chartTitle");
        if (chartTitle) {
          chartTitle.textContent = "Grafik Realisasi Tiap Jam - " + s.region;
        }
      }
    }"""

content = content.replace(role_ui_old, role_ui_new)

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Logic fix applied successfully.")
