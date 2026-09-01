# Security

## Trust boundary

StarCut can instruct an Agent to read local media, execute FFmpeg and optional renderers, and call separately configured providers. Install only from a release you trust, review `SKILL.md` and scripts, and begin with non-sensitive sample media.

The official package does not contain API keys, tokens, browser state, external repositories, model files, media, fonts, music, binaries, or `node_modules`.

## Reporting

Until a dedicated security contact is published, use a private GitHub security advisory on the StarCut repository. Do not disclose user media, credentials, private paths, or exploit details in a public issue.

## Safe defaults

- RAW inputs are read-only.
- External publishing requires explicit authorization.
- Optional adapter absence produces a visible fallback.
- Music defaults to `NO_MUSIC`.
- Existing Skill installs are never overwritten without a recoverable timestamped backup.
