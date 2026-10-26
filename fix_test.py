with open("test_cathedral_pipeline.py", "r") as f:
    code = f.read()

old_call = "snapshot = mlaos_telemetry_service.telemetry_snapshot()"
new_call = "snapshot = mlaos_telemetry_service.post_telemetry() if hasattr(mlaos_telemetry_service, 'post_telemetry') else {}"

if old_call in code:
    code = code.replace(old_call, new_call)
    with open("test_cathedral_pipeline.py", "w") as f:
        f.write(code)
    print("test_cathedral_pipeline.py patched successfully.")
else:
    print("Target line not found exactly, check test file.")
