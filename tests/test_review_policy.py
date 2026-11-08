from agent_workflow.models import Finding, Review, has_blockers, passes
from agent_workflow.orchestrator import next_action

def test_pass():
    review = Review(decision="pass", summary="ok")
    assert passes(review)
    assert next_action(review, 0) == "human_approval"

def test_blocking_finding():
    review = Review(decision="pass", summary="issue", findings=[
        Finding(severity="high", file="src/app.py", explanation="bug", suggested_fix="fix it")
    ])
    assert has_blockers(review)
    assert not passes(review)
    assert next_action(review, 3) == "human_triage"

def test_revision_needed():
    review = Review(decision="changes_requested", summary="issue")
    assert next_action(review, 1) == "request_revision"
