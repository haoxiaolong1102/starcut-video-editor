# Transcription adapter

StarCut accepts any external word-timestamp engine that returns UTF-8 tokens with `start`, `end`, `text`, and optional `confidence`. OpenAI Whisper is one compatible option and is not bundled; models remain external.

The transcript must be aligned against the final script before cutting. Low-confidence words, overlapping speech, and quiet syllables require manual/audio review. If no word timeline exists, do not automate word-level dialogue removal.
