# Remotion optional adapter

Remotion is never bundled. Before use, the user must install it separately and confirm that the current Remotion License covers the person/organization and intended production use.

Use it when React-based composition materially helps: advanced data, Screen Focus keyframes, masks, meaningful morphs, multilayer parallax, 3D, or complex media timing. Do not default to high complexity.

Run adapter detection with `--project-root` pointing to the actual Remotion project, not the installed Skill directory. After eligibility is confirmed, run `scripts/build_render_plan.py ... --remotion-license eligible`. In `auto` mode, selected Level 2/3 shots then route to Remotion.

For every selected shot, retain a receipt containing the shot ID, `renderer: remotion`, `status: success`, real output path, and exact project/command. `scripts/validate_production.py` rejects a final delivery when this proof is absent.

Fallback: HyperFrames, a simpler renderer, or a renderer-neutral SHOTBOOK.
