"""
Cathedral-Engine Integrated HTTP REST API Server Daemon.
Zero-dependency implementation serving:
- GET /api/health
- GET /api/rpg/state
- GET /api/rpg/chamber?id=5
- POST /api/oracle/draw
- GET /api/codex/book?id=X
- POST /api/codex/scaffold
- POST /api/codex/batch-all
- POST /api/wargame/run
- GET /api/diagnostics/trikey
- GET /api/audit/merkle
"""

from __future__ import annotations
import os
import json
import time
import math
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from .models import Spectral, BelnapValue, ChamberVLayout, ChamberNode
from .database import DatabaseManager
from .codex_generator import CodexGenerator
from .oracle_deck import OracleDeckManager
from .merkle_verifier import MerkleVerifier
from .wargame import DialetheicWargameEngine
from .batch_codex import BatchCodexCompiler
from .trikey_diagnostics import TriKeyDiagnosticSuite

db_manager = DatabaseManager()
codex_gen = CodexGenerator(db_manager)
oracle_deck = OracleDeckManager(db_manager)
merkle_verifier = MerkleVerifier(db_manager)
wargame_engine = DialetheicWargameEngine(db_manager)
batch_codex = BatchCodexCompiler(db_manager)
trikey_suite = TriKeyDiagnosticSuite(db_manager)

# Engine Runtime State
runtime_state = {
    "turn": 1,
    "tau_pol": 0.44,
    "rho_res": 0.38,
    "delta_fac": 0.35,
    "sigma_coh": 0.72,
    "carrier_hz": 130.81,
    "flux_dphi_dt": 0.428,
    "active_spectral": Spectral.RED.value,
    "active_chamber_id": 5,
    "era_name": "Era of Kinetic Remaking & Lithic Calibration"
}

def generate_chamber_v_layout() -> ChamberVLayout:
    """Constructs the dynamic 8x8 spatial grid for Chamber V."""
    layout = ChamberVLayout(
        chamber_id=5,
        designation="Chamber V: The Rupture & Altar of Lithic Athanor",
        grid_size=8,
        carrier_hz=runtime_state["carrier_hz"],
        flux_dphi_dt=runtime_state["flux_dphi_dt"],
        active_spectral=Spectral(runtime_state["active_spectral"]),
        nodes=[]
    )

    for y in range(8):
        for x in range(8):
            # Portals (North, South, East, West threshold apertures)
            if (y == 0 and x in (3, 4)):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="portal", node_id=f"portal_north_{x}",
                    spectral=Spectral.TEAL, load_bearing=False,
                    carrier_hz=130.81, flux_dphi_dt=0.15,
                    metadata={"designation": "North Aperture / Mandala Threshold", "spectral_gate": "Teal"}
                ))
            elif (y == 7 and x in (3, 4)):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="portal", node_id=f"portal_south_{x}",
                    spectral=Spectral.RED, load_bearing=False,
                    carrier_hz=130.81, flux_dphi_dt=0.55,
                    metadata={"designation": "South Exhaust / Rupture Gate", "spectral_gate": "Red"}
                ))
            elif (x == 0 and y in (3, 4)):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="portal", node_id=f"portal_west_{y}",
                    spectral=Spectral.NULL, load_bearing=False,
                    carrier_hz=0.0, flux_dphi_dt=0.0,
                    metadata={"designation": "West Threshold / Null Cartography", "spectral_gate": "Obsidian"}
                ))
            elif (x == 7 and y in (3, 4)):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="portal", node_id=f"portal_east_{y}",
                    spectral=Spectral.GOLD, load_bearing=False,
                    carrier_hz=130.81, flux_dphi_dt=0.20,
                    metadata={"designation": "East Colonnade / Axiomatic Wall", "spectral_gate": "Gold"}
                ))
            # Load-Bearing Pillars (Harmonic Scar X-Columns)
            elif (x, y) in [(2, 2), (2, 5), (5, 2), (5, 5)]:
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="pillar", node_id=f"pillar_harmonic_{x}_{y}",
                    spectral=Spectral.BLUE, load_bearing=True,
                    carrier_hz=130.81, flux_dphi_dt=0.08,
                    metadata={"designation": f"X-Pillar Harmonic Scar #{x}{y}", "triz_cost": 0.28, "asymmetry": "Obsidian-Gold Skin"}
                ))
            # Altar: Lithic Athanor (3, 3)
            elif (x, y) == (3, 3):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="altar", node_id="altar_lithic_athanor",
                    spectral=Spectral.RED, load_bearing=True,
                    carrier_hz=130.81, flux_dphi_dt=0.85,
                    metadata={"designation": "The Lithic Athanor / Compression Furnace", "temp_f": 2500, "phase": "Martensitic"}
                ))
            # Oculus: Heart-Oculus Sensor Node (4, 4)
            elif (x, y) == (4, 4):
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="oculus", node_id="heart_oculus_core",
                    spectral=Spectral.GOLD, load_bearing=True,
                    carrier_hz=130.81, flux_dphi_dt=0.428,
                    metadata={"designation": "36-Chambered Bio-Silicate Heart-Oculus", "rings": [12, 12, 12]}
                ))
            # Perimeter Walls
            elif x == 0 or x == 7 or y == 0 or y == 7:
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="wall", node_id=f"wall_{x}_{y}",
                    spectral=Spectral.NULL, load_bearing=True,
                    carrier_hz=130.81, flux_dphi_dt=0.0,
                    metadata={"material": "Polished Cyclopean Basalt"}
                ))
            # Floor Cells
            else:
                layout.nodes.append(ChamberNode(
                    x=x, y=y, node_type="floor", node_id=f"floor_{x}_{y}",
                    spectral=Spectral.TEAL, load_bearing=False,
                    carrier_hz=130.81, flux_dphi_dt=0.12,
                    metadata={"material": "Etched Granite Tile", "resonance": "1.5 Hz Somatic Sink"}
                ))
    return layout

class CathedralAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: Any, status_code: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/health":
            self._send_json({
                "status": "OPERATIONAL",
                "service": "Cathedral-Engine Master Daemon",
                "doctrine": "Never-Overwrite (Book III)",
                "active_chamber": runtime_state["active_chamber_id"],
                "carrier_hz": runtime_state["carrier_hz"],
                "timestamp": time.time()
            })
        elif path == "/api/rpg/state":
            t = time.time()
            runtime_state["flux_dphi_dt"] = round(0.428 + 0.05 * math.sin(t * 1.5), 4)
            self._send_json(runtime_state)
        elif path == "/api/rpg/chamber":
            layout = generate_chamber_v_layout()
            self._send_json(layout.to_dict())
        elif path == "/api/codex/book":
            book_id = int(query.get("id", [1])[0])
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM codex_strata WHERE book_id = ?", (book_id,))
                row = cursor.fetchone()
                if not row:
                    self._send_json({"error": "Book not found"}, 404)
                    return
                cursor.execute("SELECT chapter_id, chapter_designation, core_thesis, content_hash FROM codex_chapters WHERE book_id = ?", (book_id,))
                chapters = [dict(r) for r in cursor.fetchall()]
                book_data = dict(row)
                book_data["chapters"] = chapters
                self._send_json(book_data)
        elif path == "/api/diagnostics/trikey":
            diag = trikey_suite.audit_tri_key_governance()
            loop_res = trikey_suite.execute_9_stage_reduction_loop()
            diag["reduction_loop_result"] = loop_res
            self._send_json(diag)
        elif path == "/api/audit/merkle":
            res = merkle_verifier.verify_ledger_chain()
            self._send_json(res)
        else:
            self._send_json({"error": "Not Found", "path": path}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            data = json.loads(body_raw.decode("utf-8")) if body_raw else {}
        except Exception:
            data = {}

        if path == "/api/oracle/draw":
            spectrum_mode = data.get("spectrum_mode", "Gold-Obsidian")
            active_spec_str = data.get("active_spectrum", runtime_state["active_spectral"])
            active_spec = Spectral(active_spec_str)
            player_assert_str = data.get("player_assertion", "T")
            player_assert = BelnapValue(player_assert_str)
            card_id = data.get("card_id", None)

            draw_res = oracle_deck.draw(
                spectrum_mode=spectrum_mode,
                active_spectrum=active_spec,
                player_assertion=player_assert,
                card_id=card_id
            )

            # Mutate engine telemetry
            runtime_state["turn"] += 1
            deltas = draw_res["net_telemetry_delta"]
            runtime_state["tau_pol"] = round(max(0.0, min(1.0, runtime_state["tau_pol"] + deltas["tau_delta"] * 0.05)), 3)
            runtime_state["rho_res"] = round(max(0.0, min(1.0, runtime_state["rho_res"] + deltas["rho_delta"] * 0.05)), 3)
            runtime_state["delta_fac"] = round(max(0.0, min(1.0, runtime_state["delta_fac"] + deltas["delta_delta"] * 0.05)), 3)
            runtime_state["sigma_coh"] = round(max(0.0, min(1.0, runtime_state["sigma_coh"] + deltas["sigma_delta"] * 0.05)), 3)
            runtime_state["active_spectral"] = draw_res["card"]["spectral"]

            block_payload = {
                "event": "ORACLE_CARD_DRAW",
                "turn": runtime_state["turn"],
                "card_id": draw_res["card"]["card_id"],
                "card_name": draw_res["card"]["name"],
                "belnap_resolution": draw_res["belnap_resolution"],
                "state_after": {
                    "tau_pol": runtime_state["tau_pol"],
                    "rho_res": runtime_state["rho_res"],
                    "delta_fac": runtime_state["delta_fac"],
                    "sigma_coh": runtime_state["sigma_coh"]
                }
            }
            block = db_manager.append_ash_block(event_type="ORACLE_DRAW", payload=block_payload)
            draw_res["ash_block_hash"] = block.block_hash
            draw_res["ash_block_index"] = block.index

            self._send_json(draw_res)

        elif path == "/api/wargame/run":
            rounds = data.get("rounds", 4)
            w_res = wargame_engine.run_wargame(rounds=rounds)
            self._send_json(w_res)

        elif path == "/api/codex/batch-all":
            b_res = batch_codex.compile_all_40_books()
            self._send_json(b_res)

        elif path == "/api/codex/scaffold":
            book_id = data.get("book_id", 5)
            chapter_num = data.get("chapter_num", 1)
            chapter = codex_gen.scaffold_chapter(book_id=book_id, chapter_num=chapter_num)
            self._send_json({
                "chapter_id": chapter.chapter_id,
                "chapter_designation": chapter.chapter_designation,
                "core_thesis": chapter.core_thesis,
                "content_hash": chapter.content_hash,
                "merkle_proof": chapter.merkle_proof,
                "parent_ledger_hash": chapter.parent_ledger_hash,
                "full_monograph": chapter.full_monograph
            })
        else:
            self._send_json({"error": "Not Found", "path": path}, 404)

    def log_message(self, format, *args):
        pass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def run_server(port: int = 5000):
    server = ThreadedHTTPServer(("0.0.0.0", port), CathedralAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    run_server()
