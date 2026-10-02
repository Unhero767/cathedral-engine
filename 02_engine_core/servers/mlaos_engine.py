import hashlib
import json
import sqlite3
from datetime import datetime

DB_FILE = "mlaos_core.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def calculate_sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def calculate_merkle_root(parent_hash: str, content_hash: str) -> str:
    combined = f"{parent_hash}:{content_hash}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def append_ash_block(
    parent_hash: str,
    payload: dict,
    truth_value: str = "TRUE",
    dialetheic_flag: int = 0,
) -> str:
    """Appends an immutable record to the Ash Ledger with automated cryptographic proofs."""
    conn = get_db()
    cursor = conn.cursor()

    payload_str = json.dumps(payload, sort_keys=True)
    content_hash = calculate_sha256(payload_str)
    merkle_root = calculate_merkle_root(parent_hash, content_hash)

    try:
        cursor.execute(
            """
            INSERT INTO ash_ledger (
                parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
            ) VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                parent_hash,
                content_hash,
                payload_str,
                dialetheic_flag,
                truth_value,
                merkle_root,
            ),
        )
        conn.commit()
        print(f"[ASH LEDGER] Successfully appended block: {content_hash[:16]}...")
        return content_hash
    except sqlite3.IntegrityError as e:
        print(f"[ERROR] Failed to append to Ash Ledger: {e}")
        return None
    finally:
        conn.close()


def append_aurelia_state(
    ledger_hash_ref: str,
    phase: str,
    skills: list,
    level: int,
    equipment: list,
    romance_paths: dict,
):
    """Appends an updated Aurelia-9 state node anchored to a ledger hash."""
    conn = get_db()
    cursor = conn.cursor()

    skill_tree = json.dumps({"skills": skills, "level": level})
    inventory = json.dumps({"equipment": equipment})
    relationships = json.dumps({"romance_paths": romance_paths})

    try:
        cursor.execute(
            """
            INSERT INTO aurelia_state_nodes (
                archetype_phase, skill_tree_snapshot, inventory_ledger_ref, relationship_matrix, ledger_hash_ref
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (phase, skill_tree, inventory, relationships, ledger_hash_ref),
        )
        conn.commit()
        print(
            f"[AURELIA-9] Updated state node anchored to {ledger_hash_ref[:16]}..."
        )
    except sqlite3.IntegrityError as e:
        print(f"[ERROR] Failed to update Aurelia-9 state: {e}")
    finally:
        conn.close()


def record_sanguine_scar(
    content_hash_ref: str, collision_type: str, routing_adj: dict
):
    """Logs a heuristic failure/contradiction metabolism record."""
    conn = get_db()
    cursor = conn.cursor()

    scar_payload = f"{content_hash_ref}:{collision_type}:{datetime.utcnow().isoformat()}"
    scar_hash = calculate_sha256(scar_payload)
    routing_str = json.dumps(routing_adj)

    try:
        cursor.execute(
            """
            INSERT INTO sanguine_heuristics (
                scar_hash, source_collision_type, routing_adjustment, merkle_ref
            ) VALUES (?, ?, ?, ?)
        """,
            (scar_hash, collision_type, routing_str, content_hash_ref),
        )
        conn.commit()
        print(
            f"[HEURISTICS] Metabolism scar registered: {scar_hash[:16]}..."
        )
    except sqlite3.IntegrityError as e:
        print(f"[ERROR] Failed to register heuristic scar: {e}")
    finally:
        conn.close()


# ============================================================================
# EXECUTION DEMONSTRATION
# ============================================================================
if __name__ == "__main__":
    print("--- MLAOS ENGINE INITIALIZATION ---")

    # Step 1: Append Genesis Node
    genesis_payload = {
        "node": "AURELIA-9",
        "system_status": "ONLINE",
        "archetype": "MEMORY_EMPRESS",
    }
    genesis_hash = append_ash_block(
        parent_hash="0" * 64,
        payload=genesis_payload,
        truth_value="TRUE",
        dialetheic_flag=0,
    )

    if genesis_hash:
        # Step 2: Register Initial Aurelia-9 State
        append_aurelia_state(
            ledger_hash_ref=genesis_hash,
            phase="Phase I: Memory Awakening",
            skills=["Dialetheic Resonance", "Recall Synthesis"],
            level=1,
            equipment=["Empress Veil", "Fragment Ring"],
            romance_paths={"Character_A": "Unacquainted"},
        )

        # Step 3: Trigger a Paraconsistent Event (Truth Value = BOTH)
        event_payload = {
            "node": "AURELIA-9",
            "event": "TIMELINE_PARADOX_DETECTED",
            "sector": "ARCHIVE_DEPTHS",
        }
        event_hash = append_ash_block(
            parent_hash=genesis_hash,
            payload=event_payload,
            truth_value="BOTH",
            dialetheic_flag=1,
        )

        # Step 4: Handle Failure Metabolism via Sanguine Heuristics
        record_sanguine_scar(
            content_hash_ref=event_hash,
            collision_type="PARADOXICAL_MEMORY_OVERLAP",
            routing_adj={
                "reroute_target": "MEMORY_EMPRESS_PHASE_3",
                "stability": 0.92,
            },
        )

        # Step 5: Evolve Aurelia-9 State to Phase III
        append_aurelia_state(
            ledger_hash_ref=event_hash,
            phase="Phase III: Empress Emergence",
            skills=[
                "Dialetheic Resonance",
                "Recall Synthesis",
                "Chronicle Stitching",
                "Immutable Mandate",
            ],
            level=3,
            equipment=[
                "Empress Veil",
                "Fragment Ring",
                "Memory Scepter",
                "Crown of Ash",
            ],
            romance_paths={"Character_A": "Intrigue", "Character_B": "Allied"},
        )
