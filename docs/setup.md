# Setup

1. Review and merge the initial scaffold PR.
2. Under Settings → Secrets and variables → Actions, add repository secrets `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`.
3. Add repository variable `OPENAI_REVIEW_MODEL` (for example `gpt-4.1-mini`; confirm model access and pricing).
4. Enable GitHub Actions. Review the permissions requested by each workflow.
5. Configure main branch protection / ruleset: require CI and OpenAI Review, disallow direct pushes, and require human PR approval. This cannot be configured by this scaffold.
6. Create a small implementation issue with explicit acceptance criteria and approved spec links.
7. Run Actions → Claude Implementation → Run workflow with the issue number. Inspect its PR.
8. On PR updates, CI and OpenAI Review run; ask Claude for revisions manually if necessary.

Important: GitHub Actions secrets are not available to fork PRs. The reviewer only processes same-repository PRs. The initial Claude workflow is manual, and its ability to create PRs depends on the installed Claude GitHub action and repository token permissions.

Costs: OpenAI API, Anthropic API, and GitHub Actions usage can be separately billed.
