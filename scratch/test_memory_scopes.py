# test_memory_scopes.py — Unit test for isolated memory scopes
import sys, os, glob
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import gnom_hub.db
import gnom_hub.memory.soul_retrieval as soul_retrieval
from gnom_hub.memory.embeddings import SoulEmbedder
from gnom_hub.memory.smr.smr_retrieve import retrieve_similar_sync

def cleanup():
    # Remove index files
    for path in glob.glob("data/*coderag*") + glob.glob("data/*writerag*"):
        try: os.remove(path)
        except Exception: pass
    with gnom_hub.db.get_db_conn() as conn:
        with conn:
            conn.execute("DELETE FROM soul_memory WHERE LOWER(agent) IN ('coderag', 'writerag')")
            conn.execute("DELETE FROM soul_memory WHERE key = 'global_user_name_test'")

def seed_facts():
    # Save with priority="high" to ensure they bubble up in _fetch_recent
    gnom_hub.db.save_soul_fact("coder_rule_test", "Use python 3.11 for coding tasks and always check typing.", agent="CoderAG", priority="high")
    gnom_hub.db.save_soul_fact("writer_rule_test", "The tone of the user-facing articles should be polite and formal.", agent="WriterAG", priority="high")
    gnom_hub.db.save_soul_fact("global_user_name_test", "The user's first name is Alexander.", agent="SoulAG", priority="high")

def run_retrieval_tests():
    # 1. CoderAG querying coder-related stuff via _fetch_recent (short query)
    coder_facts = soul_retrieval.retrieve_relevant_facts("typing Python", agent_name="CoderAG", top_k=5)
    print("CoderAG (short query) facts:", coder_facts)
    assert any("python 3.11" in f.lower() for f in coder_facts), "CoderAG should retrieve its own CoderAG facts"
    assert not any("polite" in f.lower() for f in coder_facts), "CoderAG should NOT retrieve WriterAG facts"

    # 2. WriterAG querying coder-related stuff via _fetch_recent (should NOT get CoderAG facts)
    writer_coder_facts = soul_retrieval.retrieve_relevant_facts("typing Python", agent_name="WriterAG", top_k=5)
    print("WriterAG (short query) facts:", writer_coder_facts)
    assert not any("python 3.11" in f.lower() for f in writer_coder_facts), "WriterAG should NOT retrieve CoderAG facts"

    # 3. WriterAG querying tone-related stuff
    writer_facts = soul_retrieval.retrieve_relevant_facts("tone and articles", agent_name="WriterAG", top_k=5)
    print("WriterAG (short query) tone facts:", writer_facts)
    assert any("polite" in f.lower() for f in writer_facts), "WriterAG should retrieve its own WriterAG facts"
    assert not any("python 3.11" in f.lower() for f in writer_facts), "WriterAG should NOT retrieve CoderAG facts"

    # 4. Global fact retrieval check
    coder_global = soul_retrieval.retrieve_relevant_facts("Alexander user name", agent_name="CoderAG", top_k=5)
    print("CoderAG global facts:", coder_global)
    assert any("Alexander" in f for f in coder_global), "CoderAG should retrieve global facts"

def test_similarity_queries():
    # Long query that bypasses _fetch_recent and uses similarity search
    # Fact: "Use python 3.11 for coding tasks and always check typing."
    query = "Use python 3.11 for coding tasks and always check typing."
    
    coder_res = soul_retrieval.retrieve_relevant_facts(query, agent_name="CoderAG", top_k=5)
    print("CoderAG similarity facts:", coder_res)
    assert any("python 3.11" in f.lower() for f in coder_res), "CoderAG should match its own Python fact via similarity matcher"

    writer_res = soul_retrieval.retrieve_relevant_facts(query, agent_name="WriterAG", top_k=5)
    print("WriterAG similarity facts:", writer_res)
    assert not any("python 3.11" in f.lower() for f in writer_res), "WriterAG should NOT match CoderAG Python fact via similarity matcher"

def test_fallback_queries():
    # Test SMR fallback directly with exact query to hit similarity threshold > 0.60
    query = "Use python 3.11 for coding tasks and always check typing."
    coder_smr = retrieve_similar_sync(query, agent_name="CoderAG", top_k=5)
    print("CoderAG SMR fallback:", coder_smr)
    assert any("python 3.11" in f.lower() for f in coder_smr)
    assert not any("polite" in f.lower() for f in coder_smr)

    writer_smr = retrieve_similar_sync(query, agent_name="WriterAG", top_k=5)
    print("WriterAG SMR fallback:", writer_smr)
    assert not any("python 3.11" in f.lower() for f in writer_smr)

def main():
    print("--- STARTING ISOLATED MEMORY SCOPES UNIT TESTS ---")
    gnom_hub.db.init_db()
    cleanup()
    try:
        seed_facts()
        run_retrieval_tests()
        test_similarity_queries()
        test_fallback_queries()
        print("🎉 ALL ISOLATED MEMORY SCOPE TESTS PASSED SUCCESSFULLY!")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
