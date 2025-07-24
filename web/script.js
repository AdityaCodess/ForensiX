let allLogs = [];

function startBasicScan() {
  const drivePath = document.getElementById("drivePath").value;
  prepareScanUI();

  eel.start_basic_scan(drivePath)(handleScanResult);
}

function startSmartScan() {
  const drivePath = document.getElementById("drivePath").value;
  prepareScanUI();

  eel.start_smart_scan(drivePath)(handleScanResult);
}

function prepareScanUI() {
  document.getElementById("statusLog").innerText = "Starting scan...";
  document.getElementById("scan-results").innerHTML = "";
  document.getElementById("fullLog").innerHTML = "";
  allLogs = [];
  document.getElementById("smartBtn").disabled = true;
}

function handleScanResult(result) {
  document.getElementById("scan-results").innerHTML = '';
  result.files.forEach(file => {
    const line = `${file.flagged ? '⚠️ ' : ''}${file.name} (${file.size} KB)`;
    const el = document.createElement('p');
    el.textContent = line;
    if (file.flagged) el.style.color = 'red';
    document.getElementById('scan-results').appendChild(el);
  });

  result.log.forEach(log => {
    const logEl = document.createElement("p");
    logEl.textContent = String(log);
    document.getElementById("fullLog").appendChild(logEl);
  });

  document.getElementById("statusLog").innerText = "Scan completed.";
}

// Expose to Python
eel.expose(update_scan_progress);
function update_scan_progress(file) {
  let percent = 0;
  if (file.percent !== undefined && !isNaN(file.percent)) {
    percent = parseFloat(file.percent).toFixed(2);
  }

  document.getElementById("progress").innerText = `Scanning: ${percent}%`;

  const logLine = `${file.name} - ${file.size} KB`;
  allLogs.push(logLine);

  const logEntry = document.createElement("p");
  logEntry.textContent = logLine;
  document.getElementById("fullLog").appendChild(logEntry);

  if (file.flagged) {
    document.getElementById("scan-results").innerHTML += `<p style="color:red;"><strong>⚠️ ${logLine}</strong></p>`;
  }
}

eel.expose(scan_complete);
function scan_complete() {
  document.getElementById("progress").innerText = "✅ Scan complete.";
  document.getElementById("statusLog").innerText = "Scan finished successfully.";
  document.getElementById("smartBtn").disabled = false;
}

// Event Listeners
document.getElementById('basicBtn').addEventListener('click', startBasicScan);
document.getElementById('smartBtn').addEventListener('click', startSmartScan);
