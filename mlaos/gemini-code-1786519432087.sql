-- Ash Archive Immutable Ledger
CREATE TABLE IF NOT EXISTS ash_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    parent_hash TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    state_payload TEXT NOT NULL,
    dialetheic_flag INTEGER NOT NULL,
    truth_value TEXT NOT NULL,
    merkle_root TEXT NOT NULL
);

-- Lex I Guardrails: Blocking Mutations
CREATE TRIGGER IF NOT EXISTS prevent_ash_update
BEFORE UPDATE ON ash_ledger
BEGIN
    SELECT RAISE(ABORT, 'Lex I Violation: Never-Overwrite Doctrine forbids modification of past state entries.');
END;

CREATE TRIGGER IF NOT EXISTS prevent_ash_delete
BEFORE DELETE ON ash_ledger
BEGIN
    SELECT RAISE(ABORT, 'Lex I Violation: Never-Overwrite Doctrine forbids deletion of past state entries.');
END;