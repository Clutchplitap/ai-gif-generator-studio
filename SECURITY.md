# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security only |
| < 0.5   | no        |

## Reporting a vulnerability

Do not open a public issue for security problems. Email
`security@ai-gif-studio.dev` with a description, a repro, and the affected
version. We aim to acknowledge within 72 hours.

## Scope notes

- This is a **local desktop tool**. It does not phone home by default.
- Model checkpoints are downloaded from user-configured mirrors. Verify the
  SHA-256 recorded in `models/manifest.toml` before loading.
- The optional render daemon (`ai_gif_studio.server`) binds to `127.0.0.1`
  only. Do not expose it to a LAN without a reverse proxy and auth.
- Report any path-traversal or arbitrary-file-write issue in the export
  pipeline with the highest priority.