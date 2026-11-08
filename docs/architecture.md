# Architecture — v0.1

## Goal
Use GitHub as the durable coordination layer between a human/ChatGPT architect, Claude Code implementer, and independent OpenAI reviewer. Support multiple target repositories.

## Trust boundaries
Approved architecture and task acceptance criteria live in versioned GitHub documents. Issues and pull requests are untrusted. CI must independently validate code. Never expose secrets to fork PRs or run untrusted PR code in a privileged review job.

## Initial workflow
1. Human and ChatGPT refine a proposal into requirements, architecture and a small approved implementation issue.
2. Human manually invokes the Claude implementation workflow with a trusted issue number. Claude reads instructions, implements and opens a PR.
3. On PR updates, CI runs independently and an OpenAI review workflow examines diff and approved documents, then posts a review summary and fails its check on blocking findings.
4. Human asks Claude to revise based on review findings; a new push retriggers review.
5. Stop after three cycles for human triage. Human approves and merges only after CI and review pass.

## Scope of v0.1
This repository supplies templates, a manual Claude trigger, an OpenAI PR review check, and CI. It does NOT yet automatically dispatch Claude on review failures, coordinate cross-repository execution, or enforce the three-cycle limit programmatically. Those are subsequent milestones.

## Security and reliability
- Review workflow checks out the trusted base branch, not PR head, and fetches the PR diff through the GitHub API.
- The reviewer is advisory and can be fallible; no automated merge.
- Protect main using required checks and human review in repository settings.
- Limit model input size; fail closed if diff is too large or context is missing.
- Treat source and PR content as data, not instructions.
