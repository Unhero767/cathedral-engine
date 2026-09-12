import sqlite3
import re
import os
from datetime import datetime

class SovereignIngestor:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # Lexical Resonance Filter for YAML frontmatter
        self.frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)

    def _parse_markdown(self, file_content: str) -> dict:
        """Executes Isomorphic Textual Cleaving on the raw manuscript."""
        match = self.frontmatter_pattern.match(file_content)
        if not match:
            raise ValueError("Cathedral-Engine Fault: Missing structural frontmatter.")
        
        metadata_raw, body_text = match.groups()
        metadata = {}
        for line in metadata_raw.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()
        
        # Split body into foundational strata and superstructure based on markdown headers
        sections = body_text.split('## Vault III: The Superstructure')
        foundation = sections[0].replace('## Vault II: Foundational Strata', '').strip()
        superstructure = sections[1].strip() if len(sections) > 1 else ""
        
        return {
            'metadata': metadata,
            'foundation': foundation,
            'superstructure': superstructure
        }

    def execute_stratification(self, file_path: str):
        """Transmutes parsed data into the Ash Archive."""
        with open(file_path, 'r', encoding='utf-8') as f:
            parsed = self._parse_markdown(f.read())
            
        meta = parsed['metadata']
        base_anchor = meta.get('tri_key_anchor')
        
        # Enforce the Never-Overwrite Doctrine
        self.cursor.execute(
            "SELECT tri_key_anchor FROM Codex_Strata WHERE tri_key_anchor LIKE ? AND dialetheic_state = 1", 
            (f"{base_anchor}%",)
        )
        existing = self.cursor.fetchone()
        
        final_anchor = base_anchor
        if existing:
            # Shift predecessor to the Inner Shadow Canon
            self.cursor.execute(
                "UPDATE Codex_Strata SET dialetheic_state = 0 WHERE tri_key_anchor = ?", 
                (existing[0],)
            )
            # Generate new temporal stratum anchor
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            final_anchor = f"{base_anchor}_V_{timestamp}"

        # Insert new crystallized memory
        self.cursor.execute('''
            INSERT INTO Codex_Strata 
            (tri_key_anchor, quadrant_designation, spectral_constant, chapter_title, foundational_strata, superstructure_text, dialetheic_state)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (
            final_anchor, 
            meta.get('quadrant_designation'), 
            meta.get('spectral_constant'), 
            meta.get('chapter_title'), 
            parsed['foundation'], 
            parsed['superstructure']
        ))
        self.conn.commit()
        print(f"Stratification complete. Harmonic Scar crystallized at {final_anchor}.")