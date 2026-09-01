# Codex installation

## Project-level (recommended for one repository)

Unzip/copy the complete `starcut-video-editor` directory to:

```text
<project>/.agents/skills/starcut-video-editor/
```

The final path must contain `SKILL.md` directly. Start a new Codex task or reload Skill discovery, then ask:

```text
Use $starcut-video-editor to inspect my script and RAW video, create a clean narration edit and SHOTBOOK, and wait for review before the full render.
```

## User-level

If the Codex installation supports user skills, place the folder under its configured user Skill directory (commonly `~/.codex/skills/starcut-video-editor/`). Project-level installation remains the most portable choice.

Run `python3 scripts/starcut_doctor.py` from the installed Skill folder. Do not upload the Skill through an API unless the user explicitly asks for that distribution method.
