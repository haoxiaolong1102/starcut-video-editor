# WorkBuddy adapter package

This directory is a **manual compatibility package**, not a silent one-click installer. Current WorkBuddy guides describe local Skill package import, but the exact menu and validation behavior can change between versions.

1. In WorkBuddy's Skills manager, choose the current “import local Skill/package” action and select `starcut-video-editor-workbuddy-manual.zip`.
2. Verify that the imported root is `starcut-video-editor/` and contains `SKILL.md` directly.
3. If the installed version has no package import, unzip the folder under `~/.workbuddy/skills/starcut-video-editor/`, then reload Skills or restart WorkBuddy.
4. Run the dependency doctor and a non-sensitive fixture before granting access to real media.

If the installed WorkBuddy build cannot load Agent Skill folders, use the generic workflow instead:

1. Create a custom Agent/workflow in WorkBuddy.
2. Use `../generic-agent/MASTER_PROMPT.md` as the primary instruction.
3. Attach `../generic-agent/WORKFLOW.md` plus the relevant StarCut references.
4. Configure local command/file permissions explicitly.
5. Run the three fixtures or an equivalent test before production media.

Do not claim that import succeeded until WorkBuddy lists `starcut-video-editor` and can read the referenced files.
