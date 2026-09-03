# End-to-end workflow

1. **Ingest** — preserve RAW, probe files, record provenance and output assumptions.
2. **Speech edit** — transcribe to word timestamps, run `prepare_speech_edit.py`, resolve its blockers, remove silence/stumbles/repeats, render and listen to clean narration. Visual work cannot begin before this gate passes.
3. **Semantic map** — divide complete ideas and label hook, claim, evidence, demonstration, comparison, process, data, story, opinion, warning, recap, or CTA.
4. **Hook review** — make the first three seconds promise a useful answer, conflict, result, or curiosity gap.
5. **SHOTBOOK** — assign one primary visual treatment, evidence source, motion level, presenter mode, fallback, and rationale per semantic segment.
6. **Asset pass** — resolve real recordings/screenshots first; generate only missing explanatory assets and record provenance.
7. **Assembly** — detect adapters from the actual project root, run `build_render_plan.py`, use detected eligible Remotion for selected Level 2/3 shots, keep actual render receipts, and run caption box-fit calibration before typesetting.
8. **Finish** — skin-only smoothing if configured, sparse SFX, optional licensed music, loudness and encoding.
9. **QA** — run `validate_production.py`, then technical, editorial, semantic, visual, face, audio, and provenance checks. A blocker remains a blocker.
10. **Delivery** — final master, editable sources, SHOTBOOK, manifest, and QA report. Temporary cleanup requires explicit approval.

Approval gates should occur after the clean speech edit and after the SHOTBOOK when the user asks for review. A request for autonomous completion authorizes normal in-scope execution, but never external publication.
