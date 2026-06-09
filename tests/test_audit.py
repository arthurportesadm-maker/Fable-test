import json

from tracerail.audit import AuditLog, redact


def make_log(tmp_path, n=3):
    log = AuditLog(str(tmp_path / "audit.jsonl"))
    for i in range(n):
        log.append(session="s", tool=f"tool_{i}", arguments={"i": i}, decision="allow", policy="p")
    return log


def test_chain_verifies_clean(tmp_path):
    log = make_log(tmp_path)
    status = log.verify_chain()
    assert status.ok and status.records == 3


def test_tampering_with_contents_detected(tmp_path):
    log = make_log(tmp_path)
    lines = open(log.path).read().splitlines()
    record = json.loads(lines[1])
    record["arguments"]["i"] = 999  # rewrite history
    lines[1] = json.dumps(record)
    open(log.path, "w").write("\n".join(lines) + "\n")
    status = log.verify_chain()
    assert not status.ok and "record 1" in status.error


def test_deleting_a_record_detected(tmp_path):
    log = make_log(tmp_path)
    lines = open(log.path).read().splitlines()
    del lines[1]
    open(log.path, "w").write("\n".join(lines) + "\n")
    assert not log.verify_chain().ok


def test_append_resumes_existing_chain(tmp_path):
    make_log(tmp_path)
    log = AuditLog(str(tmp_path / "audit.jsonl"))  # reopen
    log.append(session="s", tool="late", arguments={}, decision="allow", policy="p")
    status = log.verify_chain()
    assert status.ok and status.records == 4


def test_interleaved_writers_keep_chain_intact(tmp_path):
    # Two handles to the same file (e.g. proxy + CLI processes) interleaving.
    path = str(tmp_path / "audit.jsonl")
    a, b = AuditLog(path), AuditLog(path)
    for i, log in enumerate([a, b, a, b, b, a]):
        log.append(session="s", tool=f"t{i}", arguments={}, decision="allow", policy="p")
    status = a.verify_chain()
    assert status.ok and status.records == 6


def test_redact_is_recursive():
    args = {"password": "hunter2", "nested": [{"api_key": "k", "ok": 1}]}
    cleaned = redact(args, ["password", "api_key"])
    assert cleaned == {"password": "[REDACTED]", "nested": [{"api_key": "[REDACTED]", "ok": 1}]}
    assert args["password"] == "hunter2"  # original untouched
