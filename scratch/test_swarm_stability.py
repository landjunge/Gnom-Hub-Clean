# test_swarm_stability.py — Test swarm stability, mention depth cascades, and pulse timeout watcher
import sys, os, json, time
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import gnom_hub.db
from gnom_hub.agents.entities import Agent
from gnom_hub.db.agent_repo import SQLiteAgentRepository
from gnom_hub.agents.swarm.swarm_comms import process_swarm_mentions
from gnom_hub.infrastructure.pulse import pulse_janitor
from gnom_hub.core.utils.preset_service import handle_preset_change

def test_swarm_stability():
    print("--- STARTING SWARM STABILITY TESTS ---")
    gnom_hub.db.init_db()
    repo = SQLiteAgentRepository()

    # 1. Test Mention Depth Limit
    # Set mock agents online
    agent_id = "22345678-1234-5678-1234-567812345678"
    a = Agent(
        id=agent_id, name="TestCoderAG", port=0, description="Test",
        status="online", capabilities=["CODER"], role="normal"
    )
    repo.save(a)

    print("Checking mention depth limit...")
    # Trigger at depth=3 (this will increment to 4 and must abort)
    from gnom_hub.db.legacy_db import get_chat_history, get_active_project
    
    # Process mentions with depth=3
    process_swarm_mentions("GeneralAG", "@TestCoderAG build it", depth=3)
    
    # Check if a new message was posted to System warning about loop
    history = get_chat_history(get_active_project(), limit=5)
    warning_found = any("Limit überschritten" in m.get("content", "") for m in history)
    assert warning_found, "Mention depth loop prevention did not abort at depth > 3!"
    print("Mention depth limit verified successfully!")

    # 2. Test pulse_janitor timeout watcher
    print("Checking pulse timeout watcher...")
    # Set CoderAG as busy and set last_seen to 6 minutes in the past
    coder = repo.get_by_name("TestCoderAG")
    assert coder is not None
    coder.status = "busy"
    coder.last_seen = datetime.now(timezone.utc) - timedelta(minutes=6)
    repo.save(coder)
    
    # Trigger pulse_janitor
    pulse_janitor()
    
    # Reload and check status
    coder_after = repo.get_by_name("TestCoderAG")
    assert coder_after.status == "online", f"Agent status was not reset! Still: {coder_after.status}"
    assert coder_after.active_job is None, "Agent active job was not cleared!"
    
    # Check if chat message was posted
    history_after = get_chat_history(get_active_project(), limit=5)
    timeout_msg_found = any("automatisch freigegeben" in m.get("content", "") for m in history_after)
    assert timeout_msg_found, "System timeout release chat message was not posted!"
    print("Pulse timeout watcher verified successfully!")

    # 3. Test Preset transactional change
    print("Checking preset change transactional safety...")
    handle_preset_change("Web Development")
    assert gnom_hub.db.get_state_value("active_preset") == "Web Development"
    print("Preset transactional change verified successfully!")

    # Clean up mock agent
    repo.delete(agent_id)
    print("All stability tests passed successfully!")

if __name__ == "__main__":
    test_swarm_stability()
