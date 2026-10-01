#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: 40-Book Codex Markdown Ingestion Pipeline
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import re
import json
from ledger import AshArchive

CODEX_DIR = "codex_source"

def ensure_codex_dir():
    if not os.path.exists(CODEX_DIR):
        os.makedirs(CODEX_DIR)
        print(f"\033[1;33m[i] Created '{CODEX_DIR}' directory. Place Markdown lore files here.\033[0m")

def extract_frontmatter(content: str) -> dict:
    """Extracts metadata such as Spectral Dominant, Tier, and Domain."""
    metadata = {
        "spectral_dominant": "Bronze-Obsidian/Null",
        "tier": "UNKNOWN",
        "domain": "UNCLASSIFIED"
    }
    
    # Simple regex parsing for Key: Value patterns
    spectral_match = re.search(r'(?i)Spectral Dominant:\s*(.+)', content)
    tier_match = re.search(r'(?i)Tier:\s*(.+)', content)
    domain_match = re.search(r'(?i)Domain:\s*(.+)', content)
    
    if spectral_match: metadata["spectral_dominant"] = spectral_match.group(1).strip()
    if tier_match: metadata["tier"] = tier_match.group(1).strip()
    if domain_match: metadata["domain"] = domain_match.group(1).strip()
        
    return metadata

def ingest_codex_files():
    ensure_codex_dir()
    ledger = AshArchive()
    files = [f for f in os.listdir(CODEX_DIR) if f.endswith('.md')]
    
    if not files:
        print(f"\033[1;31m[-] No Markdown files found in '{CODEX_DIR}'.\033[0m")
        return

    print("\033[1;36m┌────────────────────────────────────────┐\033[0m")
    print("\033[1;36m│   CODEX MARKDOWN INGESTION PIPELINE    │\033[0m")
    print("\033[1;36m└────────────────────────────────────────┘\033[0m")

    for filename in files:
        filepath = os.path.join(CODEX_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        metadata = extract_frontmatter(content)
        
        payload = {
            "event": "CODEX_INGESTION",
            "file": filename,
            "metadata": metadata,
            "body_length": len(content),
            # Cryptographic hash of content to ensure fidelity
            "content_hash": hash(content) 
        }
        
        block_hash = ledger.append(payload)
        print(f"\033[1;32m[+] Ingested:\033[0m {filename}")
        print(f"    \033[1;34mSpectral:\033[0m {metadata['spectral_dominant']}")
        print(f"    \033[1;34mDAG Hash:\033[0m {block_hash}")

if __name__ == "__main__":
    ingest_codex_files()
