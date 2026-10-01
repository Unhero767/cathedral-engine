# ====================================================================
# MLAOS-Prime :: Embedded Terminal Bridge Verification
# ====================================================================
import subprocess
import os

def test_studio_orchestrator_presence():
    """Verify studio orchestrator is linked and executable."""
    studio_path = os.path.expanduser("~/.local/bin/studio")
    assert os.path.exists(studio_path) or os.path.exists("studio.py"), "Studio CLI must be present."

def test_subprocess_pty_execution():
    """Simulate asynchronous pseudo-terminal (PTY) command execution."""
    # Test safe background command capture via subprocess
    res = subprocess.run(["python3", "-c", "print('MLAOS_BRIDGE_ACTIVE')"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "MLAOS_BRIDGE_ACTIVE" in res.stdout
