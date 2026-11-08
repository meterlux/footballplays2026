# Cal's Play Trainer

A browser game for memorizing the Gridiron Elite playbook (offense and defense playbooks emailed Nov 6, 2026).

- Pick a play from the menu. The players show up as color-coded dots.
- **Reveal** shows every route. **Run** animates the play. **Learn / Real** sets the speed.
- **Drill:** tap the dot for your position, then drag it along your route with your finger. You get a score, tips (break depth, motion, wrong way, finish spot, zone), and your route drawn over the playbook route.
- **Formations:** drag from the huddle to your alignment spot.
- **Quick drill:** 5 random plays with a report card at the end.

Open `index.html` in any browser. It's one self-contained file with no install.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Built standalone page |
| `dist/artifact.html` | Same page without the HTML wrapper (published as a claude.ai artifact) |
| `src/template.html` | App source (UI, drawing, animation, grading) |
| `src/build.py` | Converts play data to yards and builds both pages |
| `data/*.json` | Play data in source-image pixel coordinates plus an anchor per play |
| `tools/offense_transcription.py` | Hand transcription of the offense diagrams (raster images in the PDF) |
| `tools/defense_extract.py` | Automatic extraction of the defense diagrams (vector PDF) |
| `tools/grid.py`, `tools/check.py` | Grid overlay and draw-back check images used to verify transcriptions |

## Rebuild

```
python3 tools/offense_transcription.py   # only if the offense data changed
python3 src/build.py
```

If the coach sends a new playbook: extract diagram images with `pdfimages -png -p`, update the transcription, run `tools/check.py` to overlay it on the source, then rebuild.
