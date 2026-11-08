import os
from github import Github

def get_repository():
    return Github(os.environ["GITHUB_TOKEN"]).get_repo(os.environ["GITHUB_REPOSITORY"])

def get_pull_request():
    repo = get_repository()
    pr = repo.get_pull(int(os.environ["PR_NUMBER"]))
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
