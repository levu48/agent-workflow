from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low"]

class Finding(BaseModel):
    severity: Severity
    file: str
    explanation: str
    suggested_fix: str

class Review(BaseModel):
    decision: Literal["pass", "changes_requested"]
    summary: str
    findings: list[Finding] = Field(default_factory=list)

def has_blockers(review: Review) -> bool:
    return any(f.severity in ("critical", "high") for f in review.findings)

def passes(review: Review) -> bool:
    return review.decision == "pass" and not has_blockers(review)
