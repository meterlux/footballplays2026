# Olsson's Play Trainer 2026 (v0.2)

A browser game for memorizing the Gridiron Elite playbook (Coach Olsson's offense and defense playbooks, emailed Nov 6, 2026).

**Open it:** https://raw.githack.com/meterlux/footballplays2026/claude/hopeful-shannon-b0xy1z/index.html

## How it works

1. Open a group (Formations, Run plays, Pass plays, Defense) and pick a play.
2. **Step 1:** tap your position, either the dot on the field or the button with your position name.
3. **Step 2:** drag your dot along your route. For formations, drag from the huddle to where you line up.
4. **Step 3:** get a score and tips (break depth, motion, wrong way, finish spot, zone), with your route drawn over the playbook route.

- **Reveal** shows every route. **Run** animates the play with a SET / HIT! cadence, players accelerating at position speed, linemen firing out, and the ball following the snap and handoff. **Learn / Real** sets the speed.
- **Quick drill:** 5 random plays with a report card.
- **Add to Home Screen:** the link on the start screen plays a short guide for iPhone (Safari) and Android (Chrome).

## v0.2 changes

- Renamed to Olsson's Play Trainer 2026.
- Intro animation with Start and an "Add to Home Screen" guide.
- Collapsible play groups.
- Step 1-2-3 bar, plus position buttons for picking your spot.
- More lifelike movement: acceleration, position speeds, cadence, and linemen's first step.
- Home-screen icon and web app manifest.

## Files

| Path | What it is |
|---|---|
| `index.html` | Built standalone page (what the link above serves) |
| `icon-*.png`, `manifest.webmanifest` | Home-screen icon and app manifest |
| `dist/artifact.html` | Same page without the HTML wrapper (claude.ai artifact) |
| `src/template.html` | App source (UI, drawing, animation, grading) |
| `src/build.py` | Converts play data to yards and builds the pages and icons |
| `data/*.json` | Play data in source-image pixel coordinates plus an anchor per play |
| `tools/offense_transcription.py` | Hand transcription of the offense diagrams (raster images in the PDF) |
| `tools/defense_extract.py` | Automatic extraction of the defense diagrams (vector PDF) |
| `tools/grid.py`, `tools/check.py` | Grid overlay and draw-back check images used to verify transcriptions |

## Rebuild

```
python3 tools/offense_transcription.py   # only if the offense data changed
python3 src/build.py
```

## Nicer link (optional)

In GitHub: Settings → Pages → Deploy from a branch → `claude/hopeful-shannon-b0xy1z`, folder `/ (root)`. The app will then also be at https://meterlux.github.io/footballplays2026/
