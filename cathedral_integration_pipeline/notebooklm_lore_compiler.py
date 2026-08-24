"""
Module 4: 40-Book Codex & NotebookLM Synthesis Exporter
Compiles narrative manifests, stratum databases, and character recipes into high-density Markdown packs.
"""
import os
import json
import time

class NotebookLMLoreCompiler:
    def __init__(self, pipeline_dir: str = ""):
        self.pipeline_dir = pipeline_dir or os.path.dirname(os.path.abspath(__file__))

    def compile_research_pack(self, output_pack_path: str) -> str:
        recipes_dir = os.path.join(self.pipeline_dir, "recipes")
        manifest_path = os.path.join(self.pipeline_dir, "narrative_manifest.json")
        ledger_path = os.path.join(self.pipeline_dir, "ash_ledger.json")

        lines = [
            "---",
            "title: MLAOS-Prime & Cathedral-Engine High-Density Master Lore Corpus",
            f"generated_utc: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
            "compilation_target: NotebookLM / Vector Ingestion Pack",
            "stratum: Multi-Stratum Concordance (Books I through XL)",
            "foundational_axiom: 'Emotion = Physics = Magic = Biology = Architecture'",
            "---",
            "",
            "# 1. MAGISTERIAL ONTOLOGY & SPECTRAL CONSTANTS",
            "The universe operates on an immutable six-spectral substrate plus lightless Null space:",
            "* **Theta (585nm Burnished Gold)**: Joy and Divine Law. High-coherence laminate, unbreakable vanguard authority.",
            "* **Psi (490nm Matte Teal)**: Curiosity and Algorithmic Recursion. Caelen's Lemma, invariant load-bearing lattice.",
            "* **Delta (440nm Oxford Blue)**: Sorrow and Archiving. Zero information decay, the Ash Archive, JBP Merkle ledgers.",
            "* **Phi (680nm Crimson)**: Anger and Kinetic Remaking. Deimos's Variable, thermal combustion, dynamic entropy.",
            "* **Omega (405nm Dark Violet)**: Fear and Shadow Adaptation. Edge-walking non-indexed space in the Glitch-Wastes.",
            "* **Epsilon (520nm Emerald)**: Love and Healing. Restorative living resonance filaments.",
            "* **Null (0nm Lightless Obsidian)**: Void and Anti-Resonance. Absolute negative space.",
            "",
            "# 2. ACTIVE CANONICAL ARCHETYPE SPECIFICATIONS"
        ]

        if os.path.exists(recipes_dir):
            for r_file in sorted(os.listdir(recipes_dir)):
                if r_file.endswith(".json"):
                    with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
                        r_data = json.load(f)
                    lines.extend([
                        f"## Archetype: {r_data.get('archetype')} ({r_data.get('title', '')})",
                        f"- **Spectral Constant**: {r_data.get('spectral_constant')}",
                        f"- **Ego Density (rho)**: {r_data.get('ego_density')} (Baseline: 8.30)",
                        f"- **A-Field Potency**: {r_data.get('afield_potency')}",
                        f"- **Dialetheic State**: {r_data.get('dialetheic_state')}",
                        f"- **Armor Architecture**: {r_data.get('somatic_properties', {}).get('armor', 'N/A')}",
                        f"- **Weathering Index**: {r_data.get('somatic_properties', {}).get('weathering_index', 0.50)}",
                        ""
                    ])

        lines.extend(["# 3. NARRATIVE PROLOGUE & DIALOGUE RECITATIONS"])

        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                n_data = json.load(f)
            for conv_id, c_info in n_data.get("conversations", {}).items():
                lines.append(f"### Chamber Recitation: {c_info.get('title')} (`{conv_id}`)")
                for n_id, n_node in c_info.get("nodes", {}).items():
                    speaker = n_node.get("speaker")
                    text = n_node.get("text")
                    lines.append(f"* **{speaker}**: \"{text}\"")
                lines.append("")

        lines.extend([
            "# 4. ASH ARCHIVE IMMUTABLE HISTORICAL LEDGER",
            "Under the Never-Overwrite Doctrine (Book III), all past trauma and events are committed to Layer 11:"
        ])

        if os.path.exists(ledger_path):
            with open(ledger_path, "r", encoding="utf-8") as f:
                l_data = json.load(f)
            for entry in l_data.get("entries", []):
                lines.append(f"* `Entry #{entry.get('index')}` [{entry.get('j_hash')[:16]}...]: **{entry.get('archetype_id')}** -> {entry.get('telemetry')}")

        full_doc = "\n".join(lines)
        os.makedirs(os.path.dirname(os.path.abspath(output_pack_path)), exist_ok=True)
        with open(output_pack_path, "w", encoding="utf-8") as f:
            f.write(full_doc)

        return full_doc
