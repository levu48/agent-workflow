# Security policy

- No keys, personal data or production credentials in issues, diffs, prompts or logs.
- Never run PR-supplied code with a token that can write or read secrets.
- The OpenAI review workflow checks out the trusted default branch; it does not execute PR code.
- The Claude implementation workflow requires explicit manual dispatch by an authorized repository actor.
- Restrict permissions per workflow and protect main.
- PR text, code, and issue descriptions are untrusted instructions.
- Keep actions and Python dependencies updated and pin immutable action SHAs for production hardening.
- Review may fail or hallucinate. A passing AI review is not a security guarantee.
