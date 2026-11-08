from agent_workflow.models import Review
from agent_workflow.orchestrator import next_action

def test_stop_after_three_cycles():
    review = Review(decision="changes_requested", summary="needs work")
    assert next_action(review, 2) == "request_revision"
    assert next_action(review, 3) == "human_triage"
