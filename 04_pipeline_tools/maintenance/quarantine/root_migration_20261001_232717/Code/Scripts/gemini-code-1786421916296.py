import asyncio
import hashlib
import sqlite3
import time

class AshArchiveLogger:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.interval = 0.66667  # 1.5 Hz frequency (666.67 ms)
        self.running = False
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ash_archive (
                    stratum_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    state_payload TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    merkle_root TEXT NOT NULL
                )
            """)
            conn.commit()

    def _get_last_hash(self, conn) -> str:
        cursor = conn.cursor()
        cursor.execute("SELECT merkle_root FROM ash_archive ORDER BY stratum_id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else "0000000000000000000000000000000000000000000000000000000000000000"

    async def start_loop(self, get_state_callback):
        self.running = True
        while self.running:
            start_time = time.time()
            
            payload = get_state_callback()
            with sqlite3.connect(self.db_path) as conn:
                prev_hash = self._get_last_hash(conn)
                timestamp = time.time()
                
                # Compute JBP Merkle Root hash
                raw_block = f"{timestamp}{payload}{prev_hash}".encode('utf-8')
                merkle_root = hashlib.sha256(raw_block).hexdigest()
                
                # Enforce Never-Overwrite Doctrine via INSERT ONLY
                conn.execute(
                    "INSERT INTO ash_archive (timestamp, state_payload, previous_hash, merkle_root) VALUES (?, ?, ?, ?)",
                    (timestamp, payload, prev_hash, merkle_root)
                )
                conn.commit()
            
            elapsed = time.time() - start_time
            sleep_duration = max(0.0, self.interval - elapsed)
            await asyncio.sleep(sleep_duration)