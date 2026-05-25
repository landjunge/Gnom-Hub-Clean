# test_capabilities.py — Test capability system and caching
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import gnom_hub.db
import gnom_hub.gatekeeper
import gnom_hub.router
from gnom_hub.capability_manager import request_capability, check_capability, cleanup_expired

def test_capabilities():
    print("--- STARTING CAPABILITIES UNIT TESTS ---")
    gnom_hub.db.init_db()

    # Clear previous capabilities
    with gnom_hub.db.get_db_conn() as conn:
        with conn: conn.execute("DELETE FROM capabilities")

    # 1. Test basic grant and check
    agent = {"name": "CoderAG", "role": "coder"}
    res = "test_script.py"
    
    assert not check_capability("CoderAG", "WRITE", res)
    assert request_capability("CoderAG", "WRITE", res, "SecurityAG", ttl_min=5)
    assert check_capability("CoderAG", "WRITE", res)

    # 2. Test expiration and cleanup
    assert request_capability("CoderAG", "WRITE", "old_script.py", "SecurityAG", ttl_min=-1) # Already expired
    cleanup_expired()
    assert not check_capability("CoderAG", "WRITE", "old_script.py")
    assert check_capability("CoderAG", "WRITE", res) # Still active

    # 3. Test verification bypass
    # Mock ask_router to verify it is NOT called when capability is cached
    called = False
    def mock_ask_router(*args, **kwargs):
        nonlocal called
        called = True
        return "APPROVED"
    original_ask_router = gnom_hub.router.ask_router
    gnom_hub.router.ask_router = mock_ask_router

    try:
        # First verification should bypass router because capability exists
        assert gnom_hub.gatekeeper.verify_write(agent, res, "print('hello')", "/tmp", []) is True
        assert not called, "Router was incorrectly called even though capability was active!"

        # Verification on a new resource should call the router
        assert gnom_hub.gatekeeper.verify_write(agent, "new_script.py", "print('world')", "/tmp", []) is True
        assert called, "Router should have been called for a new resource!"
    finally:
        gnom_hub.router.ask_router = original_ask_router

    print("Capabilities system verified successfully!")

if __name__ == "__main__":
    test_capabilities()
