# Original effect library

These are behavior contracts, not copied recipes. Implement them with the selected renderer's native primitives.

## Complexity levels

- **LEVEL 0** — presenter and captions.
- **LEVEL 1** — keyword emphasis, compact card, screenshot, simple PiP.
- **LEVEL 2** — semantic Screen Focus, data animation, process diagram, multi-stage kinetic type, parallax.
- **LEVEL 3** — explanatory morph, mask composite, 3D, shader, complex multi-layer transition.

Default to the lowest level that explains the sentence. One video may mix levels.

## Capabilities

| Capability | Use when | Guardrail | Class |
|---|---|---|---|
| Kinetic typography | wording itself is the concept | animate phrases, not every glyph | default/conditional |
| Data motion | change, ranking, probability, progress | show scale/source and stable final value | default |
| Evidence tour | several parts of one real source matter | one focus at a time; hold to read | default |
| Screen Focus | a software target is too small on mobile | semantic targets only | default |
| Flow/relationship | order or dependency is the lesson | progressive reveal; no PPT grid | default |
| PiP/reframe | screen is primary but presenter anchors trust | do not cover controls or captions | default |
| Parallax/depth | layers clarify scene or hierarchy | slow movement, small depth range | conditional |
| Mask/reveal | occlusion or continuity explains a transition | preserve subject edges | conditional |
| Morph/match | A becomes B or one state continues | match a real shared property | conditional |
| Picturebook/collage | story lacks real footage | continuity bible required | conditional |
| Lottie | standard licensed icon/UI motion is needed | verify file license | conditional |
| Map | location or route is factual content | accurate labels/source | conditional |
| Audio visualization | sound itself is discussed | reflect real audio | conditional |
| Advanced media | crop, split-screen, freeze, speed or time remap explains timing | preserve sync and label altered time | conditional |
| 3D | spatial structure cannot be shown clearly in 2D | no decorative 3D | rare |
| Shader/pixel effect | a conceptual climax or state change benefits | short, restrained, tested | rare |

## Motion language

- Use smooth, predictable easing and stable end states.
- Prefer one continuous camera intention per shot.
- Prevent screen flash, fast bounce, whip-pan, constant zoom, and cursor chasing.
- Transitions must express continuity, contrast, causality, or chapter change.
- Preserve 9:16 safe areas and render deterministic frames.
