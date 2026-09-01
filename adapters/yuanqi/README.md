# Tencent Yuanqi adapter

No one-click Agent Skill import is claimed. Use Yuanqi's current custom instructions/knowledge/workflow features to reproduce only capabilities the product actually exposes.

- Place the content of `../generic-agent/MASTER_PROMPT.md` in the Agent instruction.
- Add `../generic-agent/WORKFLOW.md` and relevant StarCut references as knowledge documents if supported.
- Connect only authorized tools; video file processing and local render commands may need an external service/workflow.
- Keep RAW, keys, and user media outside public knowledge bases.
- Verify real output rather than claiming local FFmpeg/renderer execution.
