# tests/test_iam_logging_sanitization.py

import json
from fastapi.testclient import TestClient

from cathedral_engine.app.main import app

client = TestClient(app)


def test_role_change_event_is_logged_and_sanitized(caplog):
    with caplog.at_level("INFO", logger="ash_archive.ledger"):
        resp = client.patch(
            "/users/user_12345/role",
            json={"new_role": "administrator", "password": "SHOULD_NOT_LEAK"},
        )

    assert resp.status_code == 200

    ledger_records = [
        r for r in caplog.records if r.name == "ash_archive.ledger"
    ]
    assert ledger_records, "no ash archive logs captured for IAM event"

    all_messages = " ".join(r.getMessage() for r in ledger_records)

    assert "SHOULD_NOT_LEAK" not in all_messages

    found_iam_event = False
    for r in ledger_records:
        msg = r.getMessage()
        if "ASH_ARCHIVE_BLOCK_COMMITTED:" not in msg:
            continue
        _, json_part = msg.split("ASH_ARCHIVE_BLOCK_COMMITTED:", 1)
        event = json.loads(json_part.strip())
        if event.get("event_type") == "iam.role.updated":
            assert event["actor_user_id"] == "admin_99"
            assert event["target_user_id"] == "user_12345"
            assert event["previous_role"] == "standard_user"
            assert event["new_role"] == "administrator"
            body = event["metadata"]["body"]
            if "password" in body:
                assert body["password"] == "[REDACTED]"
            found_iam_event = True
            break

    assert found_iam_event, "expected at least one iam.role.updated event in Ash Archive"
