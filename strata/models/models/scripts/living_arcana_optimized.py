#!/usr/bin/env python3
"""
Living Arcana Engine - Optimized Spectral Sampler & SQLite WAL Storage
"""
import sqlite3
import numpy as np

class OptimizedArcanaEngine:
    def __init__(self, db_path: str = "ash_archive.db"):
        self.db = sqlite3.connect(db_path)
        self._init_sqlite_pragmas()
        self.cards = []
        self.card_vectors_normalized = None

    def _init_sqlite_pragmas(self):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA temp_store = MEMORY;")
        cursor.execute("PRAGMA mmap_size = 268435456;") # 256MB memory map
        self.db.commit()

    def load_cards(self, raw_card_list: list):
        self.cards = raw_card_list
        raw_vectors = np.array([c["vector4d"] for c in raw_card_list], dtype=np.float32)
        norms = np.linalg.norm(raw_vectors, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        self.card_vectors_normalized = raw_vectors / norms

    def draw_by_resonance(self, inquiry_vector: list, beta: float = 2.5, count: int = 3) -> list:
        u = np.array(inquiry_vector, dtype=np.float32)
        u_norm = np.linalg.norm(u)
        if u_norm == 0.0:
            u_norm = 1.0
        u_unit = u / u_norm

        cosine_scores = np.dot(self.card_vectors_normalized, u_unit)
        exp_scores = np.exp(beta * (cosine_scores - np.max(cosine_scores)))
        probs = exp_scores / np.sum(exp_scores)

        selected_indices = np.random.choice(len(self.cards), size=count, replace=False, p=probs)
        return [self.cards[i] for i in selected_indices]
