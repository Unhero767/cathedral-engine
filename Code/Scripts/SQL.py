import sqlite3
from typing import List, Tuple

DB_PATH = "mlaos_catalog.db"

def initialize_database(db_path: str = DB_PATH) -> None:
    """Initializes tables, indexes, and views with foreign key enforcement."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Enforce foreign key constraints in SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Table Definitions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            strata TEXT NOT NULL,
            clearance_level INTEGER NOT NULL DEFAULT 1 CHECK (clearance_level BETWEEN 1 AND 10),
            spectral_resonance REAL NOT NULL CHECK (spectral_resonance >= 0.0)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            author_id INTEGER NOT NULL,
            strata_classification TEXT NOT NULL CHECK (
                strata_classification IN (
                    'Prime Foundations',
                    'Inner Mandala',
                    'Outer Choirs',
                    'Inner Shadow Canon'
                )
            ),
            spectral_frequency REAL NOT NULL CHECK (spectral_frequency >= 0.0),
            word_count INTEGER NOT NULL CHECK (word_count > 0),
            publication_year INTEGER NOT NULL CHECK (publication_year >= 2020),
            FOREIGN KEY (author_id) REFERENCES authors (id) ON DELETE CASCADE
        );
        """)

        # B-Tree Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_strata ON books(strata_classification);")

        # Views
        cursor.execute("DROP VIEW IF EXISTS v_codex_catalog;")
        cursor.execute("""
        CREATE VIEW v_codex_catalog AS
        SELECT 
            b.id AS book_id,
            b.title,
            a.name AS author_name,
            a.clearance_level,
            b.strata_classification,
            b.spectral_frequency,
            b.word_count,
            b.publication_year
        FROM books b
        JOIN authors a ON b.author_id = a.id;
        """)

        cursor.execute("DROP VIEW IF EXISTS v_strata_metrics;")
        cursor.execute("""
        CREATE VIEW v_strata_metrics AS
        SELECT 
            strata_classification,
            COUNT(id) AS total_books,
            SUM(word_count) AS total_words,
            ROUND(AVG(spectral_frequency), 2) AS avg_spectral_freq
        FROM books
        GROUP BY strata_classification;
        """)

        conn.commit()
        print("[+] Schema, indexes, and views initialized successfully.")


def seed_database(db_path: str = DB_PATH) -> None:
    """Populates database using parameterized queries to prevent SQL injection."""
    authors_data: List[Tuple[str, str, int, float]] = [
        ('Kenneth Dallmier', 'Prime Foundations', 10, 432.0),
        ('Archon Scribe Vaelen', 'Inner Mandala', 8, 528.5),
        ('Chamber Keeper Kaelen', 'Outer Choirs', 5, 639.1)
    ]

    books_data: List[Tuple[str, int, str, float, int, int]] = [
        ('Book I: Genesis of the Ontological Core', 1, 'Prime Foundations', 432.5, 46500, 2025),
        ('Book XI: The Inner Resonance Chamber', 2, 'Inner Mandala', 528.5, 38000, 2025),
        ('Book XXI: Echoes of the Outer Choirs', 3, 'Outer Choirs', 639.1, 41200, 2026),
        ('Book XXXI: Shadow Canon Thresholds', 1, 'Inner Shadow Canon', 741.2, 52000, 2026)
    ]

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Parameterized queries using '?' placeholders
            cursor.executemany("""
            INSERT OR IGNORE INTO authors (name, strata, clearance_level, spectral_resonance)
            VALUES (?, ?, ?, ?);
            """, authors_data)

            cursor.executemany("""
            INSERT OR IGNORE INTO books (title, author_id, strata_classification, spectral_frequency, word_count, publication_year)
            VALUES (?, ?, ?, ?, ?, ?);
            """, books_data)

            conn.commit()
            print("[+] Sample records inserted into database.")
    except sqlite3.Error as err:
        print(f"[-] Database operation failed: {err}")


def fetch_summary_reports(db_path: str = DB_PATH) -> None:
    """Queries views and aggregate metrics."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        print("\n=== Author Aggregations ===")
        cursor.execute("""
        SELECT 
            a.name AS author,
            COUNT(b.id) AS total_books,
            COALESCE(SUM(b.word_count), 0) AS total_words,
            ROUND(AVG(b.spectral_frequency), 2) AS avg_spectral_frequency
        FROM authors a
        LEFT JOIN books b ON a.id = b.author_id
        GROUP BY a.id, a.name
        ORDER BY total_words DESC;
        """)
        for row in cursor.fetchall():
            print(f"Author: {row[0]} | Books: {row[1]} | Words: {row[2]:,} | Avg Freq: {row[3]}")

        print("\n=== Strata Metrics (v_strata_metrics) ===")
        cursor.execute("SELECT * FROM v_strata_metrics;")
        for row in cursor.fetchall():
            print(f"Strata: {row[0]} | Books: {row[1]} | Words: {row[2]:,} | Avg Freq: {row[3]}")


if __name__ == "__main__":
    initialize_database()
    seed_database()
    fetch_summary_reports()