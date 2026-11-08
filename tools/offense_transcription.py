"""Offense playbook transcription (Gridiron Elite Playbook, emailed Nov 6, 2026).

Every coordinate is in pixels of the diagram image extracted from the PDF with
`pdfimages -png -p` (file names like o-020-010.png = PDF page 20, image 10).
The anchor gives the center/LOS pixel position and the 5-yard line spacing so
src/build.py can convert to yards.

Run:  python3 tools/offense_transcription.py   -> writes data/offense_runs.json, data/offense_pass.json
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OL = ["LT", "LG", "C", "RG", "RT"]


def play(pid, page, file, name, cat, note, los, ol, yard5, skill):
    """ol = x of LT, LG, C, RG, RT (all on the LOS). skill = {id: (x, y, {extras})}."""
    players = [{"id": k, "x": x, "y": los} for k, x in zip(OL, ol)]
    for k, v in skill.items():
        x, y = v[0], v[1]
        p = {"id": k, "x": x, "y": y}
        if len(v) > 2:
            p.update(v[2])
        players.append(p)
    unit = (ol[-1] - ol[0]) / 4 if ol else 0
    return {"id": pid, "page": page, "file": file, "name": name, "category": cat, "note": note,
            "anchor": {"cx": ol[2] if ol else 0, "losY": los, "unit": unit, "yard5": yard5}, "players": players}


def R(path, end="arrow", **kw):
    d = {"path": path, "end": end}
    d.update(kw)
    return d


QB_NOTE_DROP = "drop"

F = "Formation"
formations = [
    play("f-right", 9, "o-009-000.png", "Right", F, "Base formation. TE and Z right, X left.", 271, [472, 541, 610, 680, 748], 129.5,
         {"X": (197, 271), "TE": (817, 271), "h": (410, 336), "Q": (610, 336), "Z": (1024, 337), "H": (610, 466)}),
    play("f-flex-right", 10, "o-010-001.png", "Flex Right", F, "", 268, [473, 542, 611, 680, 749], 130,
         {"X": (198, 268), "TE": (818, 268), "Q": (611, 335), "h": (880, 332), "Z": (1025, 335), "H": (611, 463)}),
    play("f-slot-right", 11, "o-011-002.png", "Slot Right", F, "", 242, [413, 479, 545, 610, 676], 123.5,
         {"X": (150, 242), "TE": (742, 242), "Q": (545, 305), "h": (865, 304), "Z": (979, 302), "H": (545, 429)}),
    play("f-twins-right", 12, "o-012-003.png", "Twins Right", F, "", 244, [424, 490, 556, 621, 687], 123,
         {"X": (160, 244), "Z": (962, 244), "TE": (744, 291), "h": (914, 293), "Q": (556, 306), "H": (556, 431)}),
    play("f-deuce-right", 13, "o-013-004.png", "Deuce Right", F, "", 271, [472, 541, 610, 680, 748], 129.5,
         {"X": (185, 271), "Z": (1040, 271), "h": (240, 339), "Q": (610, 337), "TE": (978, 336), "H": (610, 467)}),
    play("f-ace-right", 14, "o-014-005.png", "Ace Right", F, "", 273, [472, 541, 610, 680, 748], 130,
         {"X": (337, 273), "TE": (929, 273), "Q": (610, 340), "h": (874, 340), "Z": (984, 343), "H": (610, 468)}),
    play("f-double-right", 15, "o-015-006.png", "Double Right", F, "", 271, [472, 541, 610, 680, 748], 129.5,
         {"h": (396, 271), "TE": (817, 271), "X": (207, 338), "Q": (610, 336), "Z": (1024, 338), "H": (610, 442)}),
    play("f-i-right", 16, "o-016-007.png", "I Right", F, "", 270, [472, 541, 610, 680, 748], 130,
         {"X": (197, 270), "TE": (817, 270), "Q": (610, 336), "Z": (1024, 336), "h": (610, 424), "H": (610, 484)}),
    play("f-deuce-right-tight", 17, "o-017-008.png", "Deuce Right Tight", F,
         "Tight can be tagged to any formation. Maintain 1.5 ft splits at all positions.", 271, [472, 541, 610, 680, 748], 129.5,
         {"X": (343, 271), "Z": (882, 272), "h": (410, 336), "Q": (610, 336), "TE": (816, 336), "H": (610, 466)}),
    play("f-right-gun", 18, "o-018-009.png", "Right Gun", F,
         "Gun: QB heels 4 yards behind ball. RB toes to QB heel, shade to inside shoulder of guard.", 270, [472, 541, 610, 680, 748], 130,
         {"X": (197, 270), "TE": (817, 270), "h": (410, 334), "Z": (1024, 337), "Q": (610, 389), "H": (678, 389)}),
]

U = "Run"
runs = [
    play("zone-right", 20, "o-020-010.png", "Right to Pig Right Zone Right", U,
         "Inside zone with motion to point of attack to add blocker.", 260, [418, 486, 555, 623, 692], 129,
         {"X": (140, 260), "TE": (761, 260), "Z": (968, 326),
          "h": (355, 328, {"motion": [[655, 328]], **R([[660, 282]], dashed=True)}),
          "Q": (553, 322, R([[602, 370]], "handoff")),
          "H": (555, 455, R([[602, 370], [640, 308]], carrier=True))}),
    play("stretch-right", 21, "o-021-011.png", "Right to Pig Right Stretch Right", U,
         "Outside zone with motion to point of attack to add blocker.", 262, [398, 467, 537, 605, 674], 129.5,
         {"X": (122, 262), "TE": (743, 262), "Z": (950, 330),
          "h": (337, 335, {"motion": [[640, 332]], **R([[795, 297]], "block", dashed=True)}),
          "Q": (535, 323, R([[585, 374]], "handoff")),
          "H": (537, 458, R([[585, 374], [598, 352], [750, 317]], carrier=True))}),
    play("sweep-right", 22, "o-022-012.png", "Deuce Right Tight to Flex Right Sweep Right", U,
         "Sweep with motion to point of attack to add blocker.", 265, [409, 478, 547, 616, 685], 130,
         {"X": (281, 265), "Z": (819, 265),
          "h": (348, 328, {"motion": [[905, 326]], **R([[882, 243]], "block", dashed=True)}),
          "TE": (752, 330, R([[940, 262], [940, 218]], "block", alt="solid to the edge, short dashed climb")),
          "Q": (547, 328, R([[520, 368], [640, 433]], "handoff")),
          "H": (547, 460, R([[640, 433], [688, 420], [848, 343]], carrier=True))}),
    play("zone-right-counter", 23, "o-023-013.png", "Right to Pig Right Zone Right Counter", U,
         "Inside zone look with motion to point of attack, with counter action.", 263, [411, 480, 549, 618, 687], 129.5,
         {"X": (135, 263), "TE": (756, 263), "Z": (963, 329),
          "h": (349, 334, {"motion": [[650, 331]], **R([[470, 290]], dashed=True)}),
          "Q": (548, 323, R([[598, 374], [578, 391]], "handoff")),
          "H": (549, 457, R([[597, 407], [578, 391], [457, 303]], carrier=True))}),
    play("sweep-right-counter", 24, "o-024-014.png", "Right to Pig Right Sweep Right Counter", U,
         "Sweep action with motion to point of attack, counter to motion back.", 265, [407, 476, 545, 614, 683], 130,
         {"X": (131, 265), "TE": (752, 265), "Z": (958, 335),
          "h": (345, 337, {"motion": [[652, 335]], **R([[592, 313], [570, 300], [505, 260]], carrier=True)}),
          "Q": (545, 325, R([[520, 370], [582, 405], [592, 316]], "handoff", alt="reverse out, fake to H, last part dashed back to the mesh")),
          "H": (545, 459, R([[730, 420], [805, 367]]))}),
    play("dive-left", 25, "o-025-015.png", "Right Dive Left", U, "Inside run to A gap.", 242, [382, 449, 513, 580, 645], 123,
         {"X": (119, 242), "TE": (710, 242), "h": (323, 312), "Z": (907, 305),
          "Q": (512, 302, R([[484, 307]], "handoff")),
          "H": (513, 427, R([[486, 307], [477, 218]], carrier=True))}),
    play("dive-left-counter", 26, "o-026-016.png", "Right Dive Left Counter", U, "Fake dive left to sweep action right.", 262, [394, 462, 532, 601, 669], 129.5,
         {"X": (118, 262), "TE": (738, 262), "Z": (945, 330),
          "Q": (530, 322, R([[548, 357], [516, 366]], "handoff")),
          "H": (532, 457, R([[516, 366], [492, 236]], dashed=True, alt="dashed = dive fake")),
          "h": (331, 337, R([[405, 363], [663, 356], [805, 314]], carrier=True))}),
    play("jet-right", 27, "o-027-017.png", "Right to Pig Left Jet Right", U, "Motion into Jet Sweep.", 260, [400, 469, 539, 607, 676], 129.5,
         {"X": (125, 260), "TE": (745, 260), "Z": (952, 326), "H": (539, 457),
          "h": (343, 328, {"motion": [[410, 330]], **R([[505, 338], [710, 340], [818, 284]], carrier=True)}),
          "Q": (538, 316, R([[500, 316], [505, 338]], "handoff"))}),
    play("gun-jet-right", 28, "o-028-018.png", "Double Left Tight Gun Jet Right", U, "Jet Sweep from tight formation.", 262, [382, 451, 520, 589, 658], 129,
         {"TE": (304, 262), "h": (731, 262), "H": (445, 386),
          "Z": (237, 328, R([[520, 326], [688, 325], [850, 289]], carrier=True)),
          "Q": (522, 384, R([[520, 328]], "handoff")),
          "X": (800, 328, R([[832, 232]], "block", dashed=True))}),
]

P = "Pass"
DROP = "drop"
PRO = dict(dashed=True)  # H dashed = pass protection
passes = [
    play("rub-right", 30, "o-030-019.png", "Deuce Right Tight Rub Right", P,
         "In tight formation: play side inside receiver rubs to out. Backside X rubs to cross.", 488, [403, 472, 541, 610, 679], 129,
         {"X": (273, 489, R([[264, 358], [568, 355]])),
          "Z": (812, 490, R([[812, 230], [905, 140]])),
          "h": (341, 550, R([[330, 217], [466, 36]])),
          "TE": (746, 550, R([[830, 403], [836, 353], [998, 353]])),
          "Q": (541, 552, R([[553, 598], [575, 627], [613, 647]], DROP)),
          "H": (541, 683, R([[697, 566]], "block", **PRO))}),
    play("slants", 31, "o-031-020.png", "Right Slants", P,
         "Outside slants, inside seams. Check safeties, get the ball out quick.", 390, [420, 489, 558, 627, 696], 129.5,
         {"X": (133, 390, R([[133, 313], [268, 262]])),
          "h": (358, 455, R([[358, 92]])),
          "TE": (765, 390, R([[765, 30]])),
          "Z": (993, 453, R([[993, 374], [862, 320]])),
          "Q": (558, 455, R([[562, 503]], DROP)),
          "H": (558, 585, R([[412, 474]], "block", **PRO))}),
    play("sticks", 32, "o-032-021.png", "Right Sticks", P, "Outside fades, inside sticks.", 385, [398, 467, 537, 605, 674], 129,
         {"X": (123, 385, R([[123, 22]])),
          "h": (337, 450, R([[337, 177], [296, 177]])),
          "TE": (743, 387, R([[741, 175], [783, 176]])),
          "Z": (966, 434, R([[966, 72]])),
          "Q": (538, 514, R([[538, 562]], DROP)),
          "H": (466, 512, R([[382, 448]], "block", **PRO))}),
    play("swing-right", 33, "o-033-022.png", "Flex Right Swing Right", P, "Block edge like a sweep. Spy WRs running off. 5 step drop.", 368, [403, 468, 534, 600, 665], 123,
         {"X": (140, 368, R([[128, 345], [110, 300], [100, 250], [97, 180], [97, 68]])),
          "Z": (958, 432, R([[975, 380], [990, 300], [995, 200], [997, 66]], "block", alt="fade that ends in a T (stalk/run-off)")),
          "TE": (731, 368, R([[752, 330]], "block")),
          "h": (790, 430, R([[822, 352], [805, 340]], "block")),
          "Q": (534, 432),
          "H": (534, 555, R([[700, 547], [790, 541], [828, 530], [870, 505], [910, 478]]))}),
    play("hawk-right", 34, "o-034-023.png", "Right Hawk Right", P,
         "Inside receivers out/cross towards play side. Outside fade/post towards play side.", 378, [392, 461, 530, 599, 668], 129,
         {"X": (116, 378, R([[116, 118], [210, 28]])),
          "h": (330, 442, R([[330, 196], [578, 194]])),
          "TE": (736, 378, R([[731, 176], [993, 177]])),
          "Z": (944, 445, R([[944, 82]])),
          "Q": (530, 445, R([[556, 520], [586, 543], [622, 547]], DROP)),
          "H": (530, 572, R([[690, 437]], "block", **PRO))}),
    play("zone-left-hawk-right", 35, "o-035-024.png", "Right Zone Left Hawk Right", P,
         "SELL THE FAKE, peek the seek, hit open man.", 368, [380, 446, 512, 578, 644], 123.5,
         {"X": (117, 368, R([[118, 120], [206, 35]])),
          "h": (321, 430, R([[321, 193], [556, 193]])),
          "TE": (708, 368, R([[704, 175], [953, 176]])),
          "Z": (906, 432, R([[906, 84]])),
          "Q": (512, 432, R([[495, 460], [490, 490], [510, 520], [558, 540]], DROP)),
          "H": (512, 553, R([[388, 433]], "block", dashed=True, alt="zone-left fake, then protect"))}),
    play("hawk-left", 36, "o-036-025.png", "Right Hawk Left", P,
         "Inside receivers out/cross towards play side. Outside fade/post towards play side.", 380, [423, 492, 561, 630, 698], 129,
         {"X": (147, 380, R([[147, 18]])),
          "h": (360, 445, R([[358, 188], [36, 188]])),
          "TE": (768, 380, R([[770, 206], [458, 206]])),
          "Z": (975, 445, R([[975, 186], [882, 97]])),
          "Q": (561, 445, R([[548, 490], [520, 545], [490, 565], [466, 568]], DROP)),
          "H": (561, 575, R([[397, 438]], "block", **PRO))}),
    play("flex-hawk-right", 37, "o-037-026.png", "Right to Flex Right Hawk Right", P,
         "When we bring a 3rd receiver to Hawk, Smash, Flood, Wheel, he runs a skinny post across the safety's face.", 368, [371, 437, 503, 568, 634], 123,
         {"X": (108, 368, R([[108, 122], [196, 36]])),
          "h": (312, 430, {"motion": [[757, 430]], **R([[760, 190], [738, 38]])}),
          "TE": (700, 368, R([[695, 176], [945, 177]])),
          "Z": (927, 428, R([[945, 350], [948, 250], [950, 68]])),
          "Q": (503, 430, R([[528, 505], [558, 525], [592, 528]], DROP)),
          "H": (503, 553, R([[657, 427]], "block", **PRO))}),
    play("tight-zone-hawk-right", 38, "o-038-027.png", "Deuce Right Tight Zone Right Hawk Right", P,
         "Inside receivers out/cross towards play side. Outside fade/post towards play side.", 370, [363, 429, 495, 560, 626], 123.5,
         {"X": (231, 370, R([[231, 122], [320, 36]])),
          "h": (299, 423, R([[302, 202], [472, 200]])),
          "TE": (697, 416, R([[698, 215], [935, 215]])),
          "Z": (770, 372, R([[790, 320], [798, 250], [800, 170], [802, 50]])),
          "Q": (495, 433, R([[518, 505], [550, 527], [583, 530]], DROP)),
          "H": (495, 555, R([[648, 428]], "block", **PRO))}),
    play("smash-right", 39, "o-039-028.png", "Right Smash Right", P,
         "Outside receivers out/cross towards play side. Inside receivers corner/post towards play side. We can tag a route to the play side WR (whip, comeback, curl, slant).", 373, [406, 475, 544, 613, 682], 129.5,
         {"X": (130, 373, R([[137, 246], [464, 242]])),
          "h": (344, 436, R([[344, 177], [436, 86]])),
          "TE": (750, 373, R([[751, 112], [843, 22]])),
          "Z": (958, 438, R([[958, 179], [1090, 179]])),
          "Q": (544, 437, R([[576, 509], [628, 547], [665, 550]], DROP)),
          "H": (544, 568, R([[712, 445]], "block", **PRO))}),
    play("smash-left", 40, "o-040-029.png", "Right Smash Left", P,
         "Outside receivers out/cross towards play side. Inside receivers corner/post towards play side. We can tag a route to the play side WR (whip, comeback, curl, slant).", 391, [462, 531, 600, 669, 738], 129.5,
         {"X": (187, 391, R([[187, 184], [48, 186]])),
          "h": (400, 455, R([[399, 128], [304, 18]])),
          "TE": (807, 391, R([[807, 131], [715, 42]])),
          "Z": (1014, 458, R([[996, 262], [572, 253]])),
          "Q": (600, 456, R([[592, 500], [570, 546], [538, 568], [489, 574]], DROP)),
          "H": (600, 586, R([[444, 466]], "block", **PRO))}),
    play("flex-smash-right", 41, "o-041-030.png", "Right to Flex Right Smash Right", P,
         "When we bring a 3rd receiver to Hawk, Smash, Flood, Wheel, he runs a skinny post across the safety's face.", 367, [375, 441, 507, 572, 637], 123.5,
         {"X": (112, 367, R([[119, 246], [428, 242]])),
          "h": (315, 428, {"motion": [[777, 424]], **R([[777, 118], [740, 36]])}),
          "TE": (703, 367, R([[708, 165], [815, 106]])),
          "Z": (900, 430, R([[900, 182], [1027, 182]])),
          "Q": (505, 430, R([[537, 496], [588, 534], [621, 536]], DROP)),
          "H": (505, 551, R([[673, 430]], "block", **PRO))}),
    play("flood-right", 42, "o-042-031.png", "Right Flood Right", P,
         "Comeback as deep as needed. Maintain levels on backside drags.", 389, [359, 428, 497, 566, 634], 129.5,
         {"X": (82, 389, R([[92, 365], [138, 232], [185, 182], [240, 134], [270, 121], [310, 111], [493, 109]])),
          "h": (296, 453, R([[303, 425], [320, 339], [366, 284], [440, 253], [655, 252]])),
          "TE": (704, 389, R([[704, 130], [797, 40]])),
          "Z": (934, 450, R([[935, 105], [998, 157]])),
          "Q": (497, 454), "H": (497, 585)}),
    play("wheel-right", 43, "o-043-032.png", "Right Wheel Right", P,
         "Post and wheel on play side, drag play side and backside dig.", 387, [353, 422, 490, 559, 628], 129,
         {"X": (77, 387, R([[77, 128], [210, 128]])),
          "h": (291, 452, R([[295, 375], [303, 342], [320, 315], [360, 290], [420, 270], [480, 260], [560, 256], [670, 256]])),
          "TE": (697, 387, R([[720, 381], [800, 370], [880, 350], [940, 325], [985, 290], [1002, 250], [1008, 200], [1015, 42]])),
          "Z": (904, 454, R([[904, 192], [813, 102]])),
          "Q": (490, 452), "H": (490, 582)}),
    play("wheel-left", 44, "o-044-033.png", "Right Wheel Left", P,
         "Post and wheel on play side, drag play side and backside dig.", 382, [430, 499, 568, 637, 706], 129.5,
         {"X": (155, 382, R([[155, 123], [246, 32]])),
          "h": (369, 447, R([[280, 415], [180, 375], [140, 355], [90, 305], [65, 260], [50, 200], [40, 120], [38, 62]])),
          "TE": (775, 382, R([[768, 330], [740, 290], [700, 262], [640, 245], [560, 239], [320, 236]])),
          "Z": (983, 449, R([[967, 120], [770, 115]])),
          "Q": (568, 447, R([[548, 513], [520, 550], [490, 567], [463, 568]], DROP)),
          "H": (568, 577, R([[420, 451]], "block", **PRO))}),
]

DUO_NOTE = "H breaks Fade, Z breaks slant under H on each combo. Each route combo looks the same at first."


def duo(pid, file, name, los, zx, zy, hx, hy, hpath, zpath, yard5=123):
    return {"id": pid, "page": 46, "file": file, "name": name, "category": P, "note": DUO_NOTE,
            "anchor": {"cx": zx - 70, "losY": los, "unit": 0, "yard5": yard5},
            "players": [{"id": "Z", "x": zx, "y": zy, "path": zpath, "end": "arrow"},
                        {"id": "h", "x": hx, "y": hy, "path": hpath, "end": "arrow"}]}


duos = [
    duo("duo-fade-post", "o-046-034.png", "Duo: Fade Post", 368, 188, 368, 140, 416,
        [[132, 385], [126, 305], [138, 280], [180, 245], [210, 195], [225, 140], [235, 95]],
        [[205, 305], [108, 275], [108, 143], [25, 48]]),
    duo("duo-comeback-slant", "o-046-035.png", "Duo: Comeback Slant", 366, 191, 367, 144, 413,
        [[136, 385], [130, 315], [140, 285], [175, 255], [205, 205], [225, 140], [238, 80], [309, 128]],
        [[210, 300], [67, 230]]),
    duo("duo-dig-whip", "o-046-036.png", "Duo: Dig Whip", 367, 185, 368, 138, 412,
        [[134, 385], [130, 325], [130, 290], [150, 265], [175, 230], [190, 180], [193, 120], [192, 82], [180, 72], [140, 70], [75, 72]],
        [[200, 300], [85, 225], [240, 225]]),
    duo("duo-out-jerk", "o-046-037.png", "Duo: Out Jerk", 357, 185, 358, 138, 405,
        [[130, 385], [120, 285], [145, 250], [165, 215], [185, 162], [260, 162]],
        [[203, 295], [95, 206], [118, 206], [102, 228], [43, 228]], yard5=122),
]

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    json.dump(formations + runs, open(os.path.join(ROOT, "data", "offense_runs.json"), "w"), indent=1)
    json.dump(passes + duos, open(os.path.join(ROOT, "data", "offense_pass.json"), "w"), indent=1)
    print(len(formations), "formations,", len(runs), "runs,", len(passes), "passes,", len(duos), "duo combos")
