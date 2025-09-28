document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('checkForm');
  const modelInput = document.getElementById('model');
  const output = document.getElementById('output');
  const results = document.getElementById('results');
  const lastCheck = document.getElementById('lastCheck');
  const downloadBtn = document.getElementById('downloadCsv');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const model = modelInput.value.trim();
    if (!model) return;

    try {
      const res = await fetch(`/eos/${encodeURIComponent(model)}`);
      const data = await res.json();
      results.classList.remove('hidden');

      if (data.error) {
        output.textContent = `❌ ${data.error}`;
      } else {
        const record = Array.isArray(data) ? data[0] : data;
        output.textContent = `✅ ${record.part_number}
Software EOS: ${record.software_eos}
Hardware EOS: ${record.hardware_eos}`;
      }
    } catch (err) {
      output.textContent = '❌ Error fetching data';
    }
  });

  downloadBtn.addEventListener('click', () => {
    window.location.href = '/eos/csv';
  });

async function loadLastCheck() {
  try {
    const res = await fetch('/data/last-check.json');
    const json = await res.json();

    if (json.lastCheck) {
      let formatted = json.lastCheck;

      // Intentar parsear si parece una fecha ISO
      const d = new Date(json.lastCheck);
      if (!isNaN(d.getTime())) {
        const pad = (n) => String(n).padStart(2, '0');
        formatted = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
      }

      lastCheck.textContent = formatted;
    } else {
      lastCheck.textContent = 'Unknown';
    }
  } catch {
    lastCheck.textContent = 'Unavailable';
  }
}

  loadLastCheck();
});

