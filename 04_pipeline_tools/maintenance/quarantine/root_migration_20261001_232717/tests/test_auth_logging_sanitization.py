# tests/test_auth_logging_sanitization.py

import json

from fastapi.testclient import TestClient

from cathedral_engine.app.main import app  # adjust if needed


client = TestClient(app)


def test_auth_logs_do_not_contain_plaintext_password(caplog):
    test_password = "SUPER_SECRET_TEST_PASSWORD"

    with caplog.at_level("INFO", logger="ash_archive.ledger"):
        resp = client.post(
            "/auth/login",
            json={"username": "someone", "password": test_password},
        )

    # we expect a 401 from the fake auth
    assert resp.status_code == 401

    # find ledger log lines
    ledger_records = [
        r for r in caplog.records if r.name == "ash_archive.ledger"
    ]
    assert ledger_records, "no ash archive logs captured"

    # concatenate all messages as one string for simple search
    all_messages = " ".join(r.getMessage() for r in ledger_records)

    # plaintext password must not appear
    assert test_password not in all_messages

    # but we should see a redacted field in the JSON
    found_redacted = False
    for r in ledger_records:
        if "ASH_ARCHIVE_BLOCK_COMMITTED:" not in r.getMessage():
            continue
        _, json_part = r.getMessage().split("ASH_ARCHIVE_BLOCK_COMMITTED:", 1)
        event = json.loads(json_part.strip())
        body = event["metadata"]["body"]
        if "password" in body and body["password"] == "[REDACTED]":
            found_redacted = True
            break

    assert found_redacted, "expected password field to be [REDACTED] in metadata.body"
