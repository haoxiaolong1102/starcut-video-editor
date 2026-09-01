# SCREEN FOCUS SYSTEM

The director follows semantic importance, not raw cursor coordinates.

## States

### FULL VIEW

Show the complete interface when entering software, switching pages, or establishing where an item lives. Hold long enough to understand the layout.

### FOCUS ZOOM

Use only for a key button, important prompt, critical text/result, setting, data, or error. Typical scale:

- ordinary target: 1.25–1.45x
- small text: 1.5–1.8x
- very small code/parameters: at most 2x by default

Compute the crop from the actual source dimensions. Verify the target lands inside the visible safe region; if not, remove the highlight rather than draw a wrong box.

### FOCUS HOLD

After the move completes, hold about 1–2 seconds or long enough to read. The cursor moves first and pauses before an important click. The camera follows more slowly and never tracks every cursor movement.

### RETURN

After the explanation, ease back to FULL VIEW. Before changing pages: return, cut to the new page, establish full view, then focus. Avoid fast local-to-local jumps.

## Cursor and emphasis

- Cursor remains visible when it carries meaning.
- Use a restrained ripple, subtle scale response, or brief highlight—not a default large yellow circle.
- Continuous small clicks, scrolling, and ordinary navigation do not trigger zoom.
- Do not cover native controls, result text, captions, or presenter PiP.

## Quality test

Review four keyframes: full view, focus arrival, hold, return. Confirm target accuracy at original resolution and on a phone-sized preview. Remove any inaccurate focus box.
