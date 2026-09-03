# StarCut v0.1.0-rc.1 候选发布版

StarCut 是一套可移植的 Agent Skill，用于导演和剪辑真人口播、AI 科普、Vlog、产品讲解与观点类竖屏视频。

GitHub：<https://github.com/haoxiaolong1102/starcut-video-editor>

下载：[最新发布页](https://github.com/haoxiaolong1102/starcut-video-editor/releases/latest) · [通用 Agent Skill 压缩包](https://github.com/haoxiaolong1102/starcut-video-editor/releases/download/v0.1.0-rc.1/starcut-video-editor.zip) · [WorkBuddy 手动安装包](https://github.com/haoxiaolong1102/starcut-video-editor/releases/download/v0.1.0-rc.1/starcut-video-editor-workbuddy-manual.zip)

它会把最终口播文案、真人视频或配音，以及可选的录屏、截图、图片和 B-roll，整理为：连续口播粗剪、字级时间轴、语义分段、Hook 判断、SHOTBOOK、真实证据优先的视觉规划、字幕、克制动效、可选的仅磨皮处理，以及经过 QA 的 9:16 成片。

StarCut 不是单一渲染器，也不是给第三方项目改名。离线 ZIP 只包含 StarCut 原创的导演规则、数据结构、验证脚本、模板和适配器协议；FFmpeg、Whisper、HyperFrames、Remotion、OpenChatCut、人脸模型、图片生成器和音乐服务均为外部依赖。

## 快速使用

1. 下载并解压 `starcut-video-editor.zip`。
2. Codex 项目级安装：`python3 scripts/install_starcut.py --agent codex --scope project --project /你的项目路径`。
3. WorkBuddy 用户级安装：`python3 scripts/install_starcut.py --agent workbuddy --scope user`。
4. 执行 `python3 scripts/starcut_doctor.py` 和 `python3 scripts/detect_adapters.py`。
5. 告诉 Agent 使用 `starcut-video-editor`，并提供最终文案和素材路径。
6. 先确认口播粗剪和 SHOTBOOK，再渲染完整视频。

没有 Skill 导入功能的平台，请使用 `adapters/generic-agent/` 内的 `MASTER_PROMPT.md`、`WORKFLOW.md` 和 `INSTALL_GUIDE.md`。

`BUNDLE_MANIFEST.md` 记录了 ZIP 内实际包含的能力，以及 OpenChatCut 等外部项目的合规接入边界。

## 核心原则

- RAW 永远只读，所有处理均生成派生文件。
- 真实证据 > 真实录屏 > 真实截图 > 信息图 > 原创生成视觉 > 纯装饰动画。
- 先理解语义，再决定视觉；删掉不会降低理解的动画。
- 音乐不是硬依赖，未配置合法音乐时自动使用 `NO_MUSIC`。
- 默认 `SMOOTH_HIGH` 只做皮肤区域磨皮，不改肤色、脸型和五官。
- 不伪造截图、录屏、数据、来源、音乐或渲染成功。

## 当前状态

`0.1.0-rc.1` 已完成格式、路由、结构、验证器、打包器和三类代表性流程夹具验证。不同机器上的第三方渲染器与 API 仍需在正式发布前分别做冒烟测试。
