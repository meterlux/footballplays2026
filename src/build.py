"""Build the play trainer.

Reads the transcribed playbook diagrams in data/*.json (pixel coordinates of the
source images plus an anchor per play), converts them to yards measured from the
center on the line of scrimmage, and writes:

  dist/artifact.html  page body for the claude.ai artifact (no <html> skeleton)
  index.html          standalone page (open in any browser / GitHub Pages)

Usage: python3 src/build.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FILES = ["offense_runs.json", "offense_pass.json", "defense.json"]
CAT_ORDER = {"Formation": 0, "Run": 1, "Pass": 2, "Defense": 3}

SOURCE = {
    "label": "Gridiron Elite offense + defense · playbooks sent Nov 6, 2026",
    "detail": "the Gridiron Elite offensive and defensive playbooks emailed Nov 6, 2026",
}


def conv(play):
    a = play["anchor"]
    k = 5.0 / a["yard5"]

    def P(x, y):
        return [round((x - a["cx"]) * k, 2), round((y - a["losY"]) * k, 2)]

    players = []
    for p in play["players"]:
        team = p.get("team", "off")
        label = p.get("label", p["id"])
        pid = p["id"] if team != "opp" else "o_" + p["id"]
        q = {"id": pid, "label": label, "team": team}
        q["x"], q["y"] = P(p["x"], p["y"])
        if p.get("motion"):
            q["motion"] = [P(*m) for m in p["motion"]]
        if p.get("path"):
            q["path"] = [P(*m) for m in p["path"]]
            q["end"] = p.get("end", "arrow")
            if p.get("dashed"):
                q["dashed"] = True
        if p.get("carrier"):
            q["carrier"] = True
        players.append(q)
    out = {
        "id": play["id"],
        "name": play["name"],
        "cat": play["category"],
        "note": play.get("note", ""),
        "page": play.get("page"),
        "players": players,
    }
    if play.get("num"):
        out["num"] = play["num"]
    zones = []
    for z in play.get("zones", []):
        x, y = P(z["x"], z["y"])
        owner = z.get("owner")
        zones.append({"x": x, "y": y, "r": round(z["r"] * k, 2), "color": z.get("color", "teal"), "owner": owner})
    if zones:
        out["zones"] = zones
    return out


def main():
    plays = []
    for f in FILES:
        path = os.path.join(DATA, f)
        if not os.path.exists(path):
            print("missing", f)
            continue
        plays += [conv(p) for p in json.load(open(path))]
    # keep playbook order: offense by page, defense by play number
    plays.sort(key=lambda p: (CAT_ORDER[p["cat"]], p.get("num") or 0, p.get("page") or 0))
    tpl = open(os.path.join(ROOT, "src", "template.html")).read()
    body = tpl.replace("/*__PLAYS__*/[]", json.dumps(plays, separators=(",", ":"))).replace(
        "/*__SOURCE__*/{}", json.dumps(SOURCE)
    )
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    open(os.path.join(ROOT, "dist", "artifact.html"), "w").write(body)
    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    counts = {}
    for p in plays:
        counts[p["cat"]] = counts.get(p["cat"], 0) + 1
    print("built", len(plays), "plays", counts)


if __name__ == "__main__":
    main()
