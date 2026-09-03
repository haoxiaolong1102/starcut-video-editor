# Generic Agent Workflow

1. Inventory final script, primary media, optional assets, rights, brand rules, and output.
2. Probe media and preserve RAW.
3. Create word timestamps; run `prepare_speech_edit.py`, resolve blockers, render the reversible cut list, and listen to the clean narration master.
4. Segment semantic roles and judge the Hook.
5. Build `shotbook.json` using `references/shotbook-schema.md`.
6. Apply `references/visual-router.md`; load specialist references only when needed.
7. Detect external adapters from the real project root; run `build_render_plan.py` and execute selected Remotion shots with receipts.
8. Fit captions to explicit design boxes, assemble, optionally smooth skin, add sparse SFX, and default to no music.
9. Render a proof for new/high-risk capabilities, then the final 9:16 master.
10. Run `validate_production.py`, then complete `QA_REPORT.md`; blockers prevent delivery.
