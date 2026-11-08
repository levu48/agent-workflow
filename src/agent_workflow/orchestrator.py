from .models import Review, passes

MAX_REVISION_CYCLES = 3

def next_action(review: Review, revision_cycle: int) -> str:
    if passes(review):
        return "human_approval"
    if revision_cycle >= MAX_REVISION_CYCLES:
        return "human_triage"
    return "request_revision"
