import sys
from pathlib import Path
from .github_client import get_pull_request, get_diff
from .models import passes
from .openai_reviewer import review_code

def main() -> int:
    try:
        _, pr = get_pull_request()
        diff = get_diff(pr)
        architecture = Path("docs/architecture.md").read_text(encoding="utf-8")
        context = f"PR title: {pr.title}\nPR description: {pr.body or ''}"
        result = review_code(diff, architecture, context)
        findings = "\n".join(
            f"- **{f.severity.upper()}** `{f.file}`: {f.explanation} Fix: {f.suggested_fix}"
            for f in result.findings
        ) or "No findings."
        body = (
            f"## Independent OpenAI review\n\n**Decision:** {result.decision}\n\n"
            f"{result.summary}\n\n### Findings\n{findings}\n\n"
            f"Reviewed commit: `{pr.head.sha}`. This is an automated review, not a substitute for CI or human approval."
        )
        pr.create_issue_comment("<!-- agent-workflow-review -->\n" + body)
        return 0 if passes(result) else 1
    except Exception as exc:
        print(f"Review failed closed: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
