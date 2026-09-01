# Audio, SFX, and music

## Priority

1. intelligible, continuous narration
2. clean edit joins and stable loudness
3. sparse semantic SFX
4. optional background music

## SFX

Use at meaningful state changes, confirmation, reveal, or a clearly motivated interaction. Avoid constant whooshes, electronic buzzing, sci-fi noise beds, and a sound on every caption.

## Music adapter contract

The adapter returns:

```json
{
  "status": "ready|no_music|unavailable|error",
  "provider": "local|mureka|minimax|atlas|sonilo|none",
  "file": null,
  "license_or_permission": null,
  "duration": null,
  "notes": ""
}
```

Supported future providers are capability names, not bundled integrations. A valid `ready` response requires an existing audio file and license/permission record.

If there is no API key or licensed local track, return `no_music` and continue. Never synthesize random tones as a substitute and never claim a provider generated a track when it did not.

## Mix

Duck music under speech, use gentle fades, and inspect beginning/end transitions. Check that music never masks consonants and that loudness remains comfortable across phone speakers. If it does, deliver `NO_MUSIC`.
