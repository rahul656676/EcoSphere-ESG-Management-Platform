import re

with open('frontend/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_charts = '''function drawLineChart(canvasId, points) {
    const ctx = document.getElementById(canvasId).getContext("2d");
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(34, 197, 94, 0.4)');
    gradient.addColorStop(1, 'rgba(34, 197, 94, 0.05)');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: points.map((_, i) => Month ),
        datasets: [{
          label: 'Carbon Emissions',
          data: points.map(p => p.total_co2),
          borderColor: '#22C55E',
          backgroundColor: gradient,
          borderWidth: 3,
          pointBackgroundColor: '#22C55E',
          pointBorderColor: '#111827',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          fill: true,
          tension: 0.4
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        plugins: { 
          legend: { display: false }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#94A3B8' }, border: { display: false } },
          y: { grid: { color: '#334155', borderDash: [5, 5] }, ticks: { color: '#94A3B8' }, border: { display: false } }
        }
      }
    });
  }

  function drawBarChart(canvasId, bars) {
    const ctx = document.getElementById(canvasId).getContext("2d");
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: bars.map(b => b.department_name),
        datasets: [{
          label: 'ESG Score',
          data: bars.map(b => b.total_score),
          backgroundColor: '#3B82F6',
          borderRadius: 6,
          barThickness: 16
        }]
      },
      options: { 
        indexAxis: 'y',
        responsive: true, 
        maintainAspectRatio: false, 
        plugins: { 
          legend: { display: false }
        },
        scales: {
          x: { grid: { color: '#334155', borderDash: [5, 5] }, ticks: { color: '#94A3B8' }, border: { display: false } },
          y: { grid: { display: false }, ticks: { color: '#F8FAFC' }, border: { display: false } }
        }
      }
    });
  }'''

content = re.sub(r'function drawLineChart.*?\}\n\s*\}', new_charts, content, flags=re.DOTALL)
content = content.replace('o\"', '<i data-lucide=\"activity\" style=\"width:14px; height:14px; vertical-align:middle; margin-right:4px;\"></i>')
with open('frontend/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Charts updated!")
