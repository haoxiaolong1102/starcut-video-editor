# Install StarCut

StarCut is distributed as one portable ZIP. It includes the complete original director workflow and adapter contracts. Third-party engines are detected after installation and remain separately installed.

## 1. Unzip

Unzip `starcut-video-editor.zip`, then enter the extracted directory.

## 2. Install for your Agent

### Codex — current project

```bash
python3 scripts/install_starcut.py --agent codex --scope project --project /path/to/your/project
```

### Codex — current user

```bash
python3 scripts/install_starcut.py --agent codex --scope user
```

### WorkBuddy — current user

```bash
python3 scripts/install_starcut.py --agent workbuddy --scope user
```

### Generic Agent or custom directory

```bash
python3 scripts/install_starcut.py --agent generic --dest /path/to/agent/skills
```

The installer refuses to overwrite an existing installation. Pass `--backup-existing` to move the old copy to a timestamped backup before installing.

## 3. Check capabilities

```bash
python3 scripts/starcut_doctor.py
python3 scripts/detect_adapters.py
```

FFmpeg/FFprobe are required for actual media output. OpenChatCut, HyperFrames, Remotion, transcription, smoothing, image generation, and music are optional external adapters. Missing optional adapters never produce fake success.

## 4. Verify discovery

Restart or reload the Agent, then request:

```text
Use $starcut-video-editor to inspect my final script and RAW media. Create the clean speech edit and SHOTBOOK before the full render.
```

For platforms without Skill-folder discovery, follow `adapters/generic-agent/INSTALL_GUIDE.md`.
