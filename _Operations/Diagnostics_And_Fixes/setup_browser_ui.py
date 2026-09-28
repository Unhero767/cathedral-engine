import os

HTML_CODE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cathedral-Engine | Sovereign Interface</title>
    <style>
        :root {
            --bg-obsidian: #0a0a0e;
            --panel-bg: #121218;
            --gold-primary: #d4af37;
            --gold-glow: rgba(212, 175, 55, 0.3);
            --teal-accent: #00e5ff;
            --text-main: #e0e0e8;
            --border-color: #2a2a38;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
        body { background: var(--bg-obsidian); color: var(--text-main); padding: 20px; }
        header { border-bottom: 2px solid var(--gold-primary); padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        h1 { color: var(--gold-primary); font-size: 1.4rem; letter-spacing: 2px; text-transform: uppercase; }
        .tag { font-size: 0.8rem; background: #1a1a24; padding: 4px 8px; border: 1px solid var(--border-color); color: var(--teal-accent); }
        .grid-container { display: grid; grid-template-columns: 360px 1fr; gap: 20px; }
        .panel { background: var(--panel-bg); border: 1px solid var(--border-color); padding: 15px; border-radius: 4px; }
        .panel h2 { font-size: 0.95rem; color: var(--gold-primary); margin-bottom: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }
        .matrix-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; margin-bottom: 15px; }
        .cell { width: 38px; height: 38px; background: #0e0e14; border: 1px solid #1f1f2c; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
        .cell:hover { border-color: var(--teal-accent); background: #161622; }
        .cell.player { background: var(--gold-glow); border-color: var(--gold-primary); color: #fff; font-weight: bold; }
        .cell.entity { border-color: var(--teal-accent); color: var(--teal-accent); }
        .controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; max-width: 180px; margin: 0 auto 15px auto; }
        button { background: #1a1a24; color: var(--text-main); border: 1px solid var(--border-color); padding: 8px 12px; cursor: pointer; font-size: 0.85rem; }
        button:hover { background: var(--gold-primary); color: #000; }
        .log-box { height: 320px; overflow-y: auto; background: #08080c; border: 1px solid #1a1a24; padding: 10px; font-size: 0.8rem; color: #a0a0b0; }
        .log-entry { margin-bottom: 6px; line-height: 1.4; border-left: 2px solid var(--gold-primary); padding-left: 6px; }
        .telemetry-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.85rem; }
        .telemetry-val { color: var(--gold-primary); }
    </style>
</head>
<body>
    <header>
        <h1>Cathedral-Engine // Sovereign Console</h1>
        <span class="tag" id="freq-tag">Carrier: 130.81 Hz</span>
    </header>

    <div class="grid-container">
        <div>
            <div class="panel" style="margin-bottom: 20px;">
                <h2>Spatial Matrix (Chamber V)</h2>
                <div class="matrix-grid" id="grid"></div>
                <div class="controls">
                    <div></div><button onclick="move(0, -1)">▲</button><div></div>
                    <button onclick="move(-1, 0)">◀</button><button onclick="interact()">Ω</button><button onclick="move(1, 0)">▶</button>
                    <div></div><button onclick="move(0, 1)">▼</button><div></div>
                </div>
            </div>

            <div class="panel">
                <h2>Substrate Telemetry</h2>
                <div class="telemetry-row"><span>Position:</span><span class="telemetry-val" id="tele-pos">(7, 4)</span></div>
                <div class="telemetry-row"><span>Chamber:</span><span class="telemetry-val">Chamber V (Sanctum Apex)</span></div>
                <div class="telemetry-row"><span>Spectrum:</span><span class="telemetry-val" id="tele-spec">Prismatic-Obsidian</span></div>
                <div class="telemetry-row"><span>Truth Value:</span><span class="telemetry-val">BOTH (Dialetheic)</span></div>
                <div class="telemetry-row"><span>dΦ/dt Flux:</span><span class="telemetry-val">1.618</span></div>
            </div>
        </div>

        <div class="panel">
            <h2>Ash Archive & Event Telemetry</h2>
            <div class="log-box" id="log">
                <div class="log-entry">[SYSTEM] Sovereign interface online. Transcendent Oculus engaged.</div>
                <div class="log-entry">[AXIOM] EMOTION = PHYSICS = MAGIC = BIOLOGY = ARCHITECTURE</div>
            </div>
        </div>
    </div>

    <script>
        let px = 7, py = 4;
        const entities = {
            '0,4': 'W', '2,1': 'α', '2,7': 'β', '4,4': 'Ω', '6,4': 'T', '7,4': 'O'
        };

        function renderGrid() {
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            for(let y = 0; y < 8; y++) {
                for(let x = 0; x < 8; x++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    const key = `${x},${y}`;
                    if (x === px && y === py) {
                        cell.classList.add('player');
                        cell.innerText = '@';
                    } else if (entities[key]) {
                        cell.classList.add('entity');
                        cell.innerText = entities[key];
                    }
                    cell.onclick = () => { px = x; py = y; syncMove(); };
                    grid.appendChild(cell);
                }
            }
            document.getElementById('tele-pos').innerText = `(${px}, ${py})`;
        }

        async function syncMove() {
            renderGrid();
            try {
                const res = await fetch(`/api/rpg/move?x=${px}&y=${py}&chamber=5`);
                const data = await res.json();
                addLog(`[MOVE] Stepped to (${px}, ${py}) | Status: ${data.status}`);
            } catch(e) {
                addLog(`[MOVE] Position updated to (${px}, ${py})`);
            }
        }

        function move(dx, dy) {
            px = Math.max(0, Math.min(7, px + dx));
            py = Math.max(0, Math.min(7, py + dy));
            syncMove();
        }

        async function interact() {
            const key = `${px},${py}`;
            const target = entities[key] || 'floor_tile';
            try {
                const res = await fetch(`/api/rpg/interact?target_uid=${target}&x=${px}&y=${py}&action=EXAMINE`);
                const data = await res.json();
                addLog(`[INTERACT] (${px}, ${py}) -> ${data.status || 'RECORDED'}`);
            } catch(e) {
                addLog(`[INTERACT] Triggered construct at (${px}, ${py})`);
            }
        }

        function addLog(msg) {
            const box = document.getElementById('log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerText = msg;
            box.appendChild(entry);
            box.scrollTop = box.scrollHeight;
        }

        renderGrid();
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CODE)

print("[✓] index.html written to engine directory.")
