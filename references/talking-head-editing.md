# Talking-head and narration editing

## Rough cut order

1. Transcribe with word timestamps and confidence.
2. Align the approved script to spoken words; mark deviations.
3. Remove clear non-speaking gaps except intentional dramatic pauses.
4. Remove filler, false starts, duplicated phrases, misreads, and abandoned takes.
5. Audition every join in context. Keep short natural breaths and consonant tails.
6. Use short equal-power audio crossfades when a hard cut clicks or sounds mechanical.
7. Export the cleaned narration map before visual timing.

Amplitude/VAD detects candidates, not final edits. A quiet syllable, breath, room-noise change, or plosive must not be mistaken for silence.

## Pacing

- Optimize continuity, not maximum speed.
- Keep pauses that signal a concept change, suspense, or emotional beat.
- Remove empty pauses that feel like the presenter stopped working.
- Do not time-stretch by default. If the user requests a speed change, preserve pitch and report the exact factor.

## Framing

The presenter is the human anchor, not necessarily full-screen. For low-gesture delivery, use a stable cropped panel, designed window, or restrained PiP. The eyes and mouth must remain large enough to read on a phone. Do not use rapid punch-ins to manufacture energy.

## Edit manifest

Record every kept segment as `source_in`, `source_out`, `timeline_in`, `timeline_out`, and `reason`. This keeps the rough cut reversible and allows later renderer replacement.

After listening review, `scripts/render_cutlist.py` can assemble video/audio keep segments with external FFmpeg. It refuses to overwrite the input. Render to an intermediate master, listen again, and correct any clipped syllable or unnatural join before visual work.

## Mandatory executable gate

Use `scripts/prepare_speech_edit.py` on every spoken project. It runs FFmpeg silence detection, protects detected word spans, lists adjacent repeated words/phrases, and writes both `speech-analysis.json` and a reversible cut list.

Default starting thresholds are `-38 dB`, `0.35 s` minimum silence, and `0.08 s` edge padding. Treat them as a starting point, not a universal acoustic truth. A noisy room may require calibration from a short sample.

The command blocks visual assembly when:

- word timestamps are missing and VAD-only cutting was not explicitly accepted;
- a proposed removal overlaps a recognized word;
- a detected repeated phrase has not been reviewed against the approved script.

`--allow-vad-only` is an explicit degraded mode for material without word timestamps; it must not become the silent default. `--repeats-reviewed` may be used only after choosing the correct take and updating the edit manifest where necessary. `scripts/render_cutlist.py` refuses a cut list whose `review.status` is not `PASS`.
