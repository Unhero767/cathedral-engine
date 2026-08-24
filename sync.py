import os
import time

cwd = os.getcwd()
if os.path.basename(cwd) == "cathedral_integration_pipeline":
    base_dir = cwd
else:
    base_dir = os.path.join(cwd, "cathedral_integration_pipeline")

nb_dir = os.path.join(base_dir, "notebooklm_packs")
os.makedirs(nb_dir, exist_ok=True)

# 1. Write Local Monograph
mono_path = os.path.join(base_dir, "MASTER_REPORT_SOVEREIGN_TRANSDUCTION_PIPELINE.md")
monograph_text = """# MASTER REPORT: THE MLAOS SOVEREIGN TRANSDUCTION PIPELINE

Chain: AUTHOR -> TRANSDUCE -> RUNTIME -> PRESERVE -> AUDIT

1. Chamber I (Author): Recipe JSONs in recipes/ define genotype.
2. Chamber II (Transduce): ComfyUI diffusion formats phenotype.
3. Chamber III (Runtime): Godot 4 scene drives dialogue and shader physics.
4. Chamber IV (Preserve): Ash Archive commits Layer 11 scars via J_hash.
5. Chamber V (Audit): NotebookLM reconciles corpus.

CANON_(n+1) = RECONCILE(CANON_n + EXPERIENCE_n)
DELETE(BASE) = FALSE and HISTORY_PRESERVED = TRUE
"""

with open(mono_path, "w", encoding="utf-8") as f:
    f.write(monograph_text)

# 2. Write NotebookLM Corpus Pack
corpus_path = os.path.join(nb_dir, "MLAOS_Cathedral_Master_Corpus.md")
date_str = time.strftime("%Y-%m-%d")
header = f"---\ntitle: MLAOS-Prime Master Corpus\ngenerated: {date_str}\ntarget: NotebookLM\n---\n\n"

with open(corpus_path, "w", encoding="utf-8") as f:
    f.write(header + monograph_text)

print("Sync complete. Local files verified.")
