import os
from github import Github

def get_repository():
    name = os.environ["GITHUB_REPOSITORY"]
    return Github(os.environ["GITHUB_TOKEN"]).get_repo(name)

def get_pull_request():
    number = int(os.environ["PR_NUMBER"])
    repo = get_repository()
    pr = repo.get_pull(number)
    if pr.head.repo is None or pr.head.repo.full_name != repo.full_name:
        raise ValueError("Only same-repository pull requests may be reviewed")
    return repo, pr

def get_diff(pr, max_chars: int = 100_000) -> str:
    chunks = []
    total = 0
    for f in pr.get_files():
        if f.patch is None:
            raise ValueError(f"Missing textual patch for {f.filename}; manual review required")
        part = f"FILE: {f.filename}\nSTATUS: {f.status}\n{f.patch}\n"
        total += len(part)
        if total > max_chars:
            raise ValueError("PR diff exceeds review size limit; manual review required")
        chunks.append(part)
    if not chunks:
        raise ValueError("Empty PR diff")
    return "\n".join(chunks)

def post_review_comment(pr, body: str):
    marker = "<!-- agent-workflow-review -->"
    for comment in pr.get_issue_comments():
        if marker in comment.body and comment.user.login == pr._requester.requestJsonAndCheck.__self__.auth.get_user().login:
            comment.edit(marker + "\n" + body)
            return
    pr.create_issue_comment(marker + "\n" + body)
