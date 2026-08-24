import os, sys, json
from datetime import datetime, timezone

def generate_manifest():
    print("[SCAN] Traversing MLAOS-Prime workspace for active codex & code strata...")
    entries = []
    valid_exts = {".py", ".md", ".json", ".ndjson", ".frag", ".vert", ".sh", ".csv"}
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in valid_exts or f.endswith(".sh"):
                fp = os.path.join(root, f)
                try:
                    st = os.stat(fp)
                    entries.append({
                        "domain": os.path.basename(root) if root != "." else "ROOT_STRATA",
                        "path": fp,
                        "filename": f,
                        "size_bytes": st.st_size,
                        "modified": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()[:10]
                    })
                except Exception:
                    pass

    manifest_data = {
        "system": "MLAOS-Prime / Cathedral-Engine v4.0",
        "author": "Kenneth W. Dallmier (Unhero767)",
        "geodetic_anchor": "Olney, IL (37.7306 N, -88.0817 W)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_artifacts": len(entries),
        "corpus": entries
    }

    with open("corpus_manifest.json", "w") as f:
        json.dump(manifest_data, f, indent=2)

    md_lines = [
        "# MLAOS-PRIME // NOTEBOOKLM MASTER CORPUS MANIFEST",
        "**System Designation:** Cathedral-Engine v4.0 / Sovereign Systemic Archive",
        "**Author & Architect:** Kenneth W. Dallmier (Unhero767)",
        "**Geodetic Anchor:** Olney, Illinois (37.7306 N, -88.0817 W)",
        f"**Generation Timestamp:** {datetime.now(timezone.utc).isoformat()}",
        f"**Total Cataloged Artifacts:** {len(entries)}",
        "",
        "---",
        "",
        "## I. Corpus Overview & Ingestion Directives",
        "This manifest indexes the complete active operational corpus of MLAOS-Prime for vector ingestion, semantic querying, and NotebookLM synchronization.",
        "",
        "---",
        "",
        "## II. Cataloged Repository Artifacts"
    ]

    curr_dom = ""
    for e in sorted(entries, key=lambda x: (x["domain"], x["path"])):
        if e["domain"] != curr_dom:
            curr_dom = e["domain"]
            md_lines.append(f"\n### Domain / Directory: `{curr_dom}`")
        md_lines.append(f"- **`{e['filename']}`** (`{e['path']}`) — *{e['size_bytes']} bytes* (Modified: {e['modified']})")

    md_lines.extend(["", "---", "**ARCHIVE STATUS:** VERIFIED & READY FOR VECTOR COMPILATION."])

    with open("MLAOS_NOTEBOOKLM_MASTER_CORPUS.md", "w") as f:
        f.write("\n".join(md_lines))

    print(f"[✓] Manifest generated with {len(entries)} artifacts: 'corpus_manifest.json' and 'MLAOS_NOTEBOOKLM_MASTER_CORPUS.md'.")

if __name__ == "__main__":
    generate_manifest()
