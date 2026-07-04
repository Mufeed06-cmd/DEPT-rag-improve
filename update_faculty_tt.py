import json

# ─────────────────────────────────────────────────────────────────────────────
# Column-shift bug fixes — confirmed against source PDF (2026-07-03)
#
# Bug: during original extraction, empty cells were skipped instead of
# preserved, shifting all subsequent values in that row one column left.
#   - Mamatha Mon:       PROJECT duplicate at 11-12; IDS shifted into lunch col
#   - Venkateswarlu Mon: same pattern with NLP
#   - Venkateswarlu Tue: NLP duplicated at 11-12 (single-slot shifted)
#   - Prasanth Tue:      DL LAB appeared at 3-4 instead of correct Wed slots
#
# Only the three affected faculty are listed.
# All other 10 faculty verified clean by diagnostic scan.
# S.V. Chiranjeevi Tue BD/DV LAB span + Sat DL_CO: NEEDS MANUAL VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

new_tt = {

    # ── Dr. S. Mamatha ────────────────────────────────────────────────────────
    # Mon 11-12: "PROJECT (IV-II AI_DS-B)" → "IDS II-II AI_DS-A"  (shift artefact)
    # Mon 12-1:  "IDS II-II AI_DS-A"       → "L"                  (was shifted NLP)
    "Dr. S. Mamatha": {
        "Mon": {
            "9:00-10:00":  "",
            "10:00-11:00": "PROJECT (IV-II AI_DS-B)",
            "11:00-12:00": "IDS II-II AI_DS-A",
            "12:00-1:00":  "L",
            "1:00-2:00":   "",
            "2:00-3:00":   "",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Tue": {
            "9:00-10:00":  "",
            "10:00-11:00": "IDS II-II AI_DS-A",
            "11:00-12:00": "",
            "12:00-1:00":  "U",
            "1:00-2:00":   "IDS LAB (II-II AI_DS-A)",
            "2:00-3:00":   "IDS LAB (II-II AI_DS-A)",
            "3:00-4:00":   "IDS LAB (II-II AI_DS-A)",
            "4:00-5:00":   "",
        },
        "Wed": {
            "9:00-10:00":  "",
            "10:00-11:00": "IDS LAB (II-II AI_DS-B)",
            "11:00-12:00": "IDS LAB (II-II AI_DS-B)",
            "12:00-1:00":  "N",
            "1:00-2:00":   "",
            "2:00-3:00":   "IDS II-II AI_DS-B",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Thu": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "",
            "12:00-1:00":  "C",
            "1:00-2:00":   "FULL STACK DEVELOPEMENT LAB (II-II AI_DS-B)",
            "2:00-3:00":   "FULL STACK DEVELOPEMENT LAB (II-II AI_DS-B)",
            "3:00-4:00":   "FULL STACK DEVELOPEMENT LAB (II-II AI_DS-B)",
            "4:00-5:00":   "",
        },
        "Fri": {
            "9:00-10:00":  "",
            "10:00-11:00": "IDS II-II AI_DS-B",
            "11:00-12:00": "",
            "12:00-1:00":  "H",
            "1:00-2:00":   "",
            "2:00-3:00":   "",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Sat": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "IDS II-II AI_DS-B",
            "12:00-1:00":  "BREAK",
            "1:00-2:00":   "",
            "2:00-3:00":   "IDS II-II AI_DS-A",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
    },

    # ── A. Venkateswarlu ──────────────────────────────────────────────────────
    # Mon 11-12: "PROJECT (IV-II AI_DS-A)" → "NLP III-II AI_DS-B"  (shift artefact)
    # Mon 12-1:  "NLP III-II AI_DS-B"      → "L"
    # Tue 11-12: "NLP III-II AI_DS-A"      → ""  (single-slot shifted duplicate)
    "A. Venkateswarlu": {
        "Mon": {
            "9:00-10:00":  "",
            "10:00-11:00": "PROJECT (IV-II AI_DS-A)",
            "11:00-12:00": "NLP III-II AI_DS-B",
            "12:00-1:00":  "L",
            "1:00-2:00":   "",
            "2:00-3:00":   "",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Tue": {
            "9:00-10:00":  "",
            "10:00-11:00": "NLP III-II AI_DS-A",
            "11:00-12:00": "",
            "12:00-1:00":  "U",
            "1:00-2:00":   "BD and DV LAB (III-II AI_DS-A)",
            "2:00-3:00":   "BD and DV LAB (III-II AI_DS-A)",
            "3:00-4:00":   "BD and DV LAB (III-II AI_DS-A)",
            "4:00-5:00":   "",
        },
        "Wed": {
            "9:00-10:00":  "NLP III-II AI_DS-B",
            "10:00-11:00": "",
            "11:00-12:00": "NLP III-II AI_DS-A",
            "12:00-1:00":  "N",
            "1:00-2:00":   "AI LAB (II-II AI_DS-A)",
            "2:00-3:00":   "AI LAB (II-II AI_DS-A)",
            "3:00-4:00":   "AI LAB (II-II AI_DS-A)",
            "4:00-5:00":   "",
        },
        "Thu": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "",
            "12:00-1:00":  "C",
            "1:00-2:00":   "NLP III-II AI_DS-A",
            "2:00-3:00":   "",
            "3:00-4:00":   "NLP III-II AI_DS-B",
            "4:00-5:00":   "",
        },
        "Fri": {
            "9:00-10:00":  "NLP III-II AI_DS-A",
            "10:00-11:00": "",
            "11:00-12:00": "NLP III-II AI_DS-B",
            "12:00-1:00":  "H",
            "1:00-2:00":   "",
            "2:00-3:00":   "",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Sat": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "",
            "12:00-1:00":  "BREAK",
            "1:00-2:00":   "Tutorial I-II AI_DS-A",
            "2:00-3:00":   "Tutorial I-II AI_DS-A",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
    },

    # ── P. Penchala Prasanth ──────────────────────────────────────────────────
    # Tue 3-4: "DL LAB (III-II AI_DS-B)" → ""  (misplaced; correct slots are Wed 2-3 and 3-4)
    "P. Penchala Prasanth": {
        "Mon": {
            "9:00-10:00":  "",
            "10:00-11:00": "PROJECT (IV-II IT)",
            "11:00-12:00": "PROJECT (IV-II IT)",
            "12:00-1:00":  "L",
            "1:00-2:00":   "",
            "2:00-3:00":   "BDA III-II AI_DS-A",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Tue": {
            "9:00-10:00":  "",
            "10:00-11:00": "BD and DV LAB (III-II AI_DS-B)",
            "11:00-12:00": "BD and DV LAB (III-II AI_DS-B)",
            "12:00-1:00":  "U",
            "1:00-2:00":   "BD and DV LAB (III-II AI_DS-A)",
            "2:00-3:00":   "BD and DV LAB (III-II AI_DS-A)",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Wed": {
            "9:00-10:00":  "BDA III-II AI_DS-A",
            "10:00-11:00": "",
            "11:00-12:00": "BDA III-II AI_DS-B",
            "12:00-1:00":  "N",
            "1:00-2:00":   "",
            "2:00-3:00":   "DL LAB (III-II AI_DS-B)",
            "3:00-4:00":   "DL LAB (III-II AI_DS-B)",
            "4:00-5:00":   "",
        },
        "Thu": {
            "9:00-10:00":  "BDA III-II AI_DS-B",
            "10:00-11:00": "",
            "11:00-12:00": "BDA III-II AI_DS-A",
            "12:00-1:00":  "C",
            "1:00-2:00":   "",
            "2:00-3:00":   "BDA III-II AI_DS-B",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Fri": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "",
            "12:00-1:00":  "H",
            "1:00-2:00":   "",
            "2:00-3:00":   "BDA III-II AI_DS-A",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
        "Sat": {
            "9:00-10:00":  "",
            "10:00-11:00": "",
            "11:00-12:00": "",
            "12:00-1:00":  "BREAK",
            "1:00-2:00":   "",
            "2:00-3:00":   "",
            "3:00-4:00":   "",
            "4:00-5:00":   "",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Merge into aids_faculty_data.json
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = "aids_faculty_data.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    faculty_data = json.load(f)

updated, added = [], []
for name, tt in new_tt.items():
    found = False
    for record in faculty_data:
        if record.get("name", "").lower() == name.lower():
            record["timetable"] = tt
            updated.append(name)
            found = True
            break
    if not found:
        faculty_data.append({"name": name, "timetable": tt})
        added.append(name)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(faculty_data, f, indent=2, ensure_ascii=False)

print(f"Patched {DATA_FILE}")
print(f"  Updated : {updated}")
print(f"  Added   : {added}")
print(f"  Total records: {len(faculty_data)}")

# ── Post-write verification ───────────────────────────────────────────────────
print("\n── Post-write verification ─────────────────────────────────────────────")
LUNCH_VALS = {"L","U","N","C","H","BREAK",""}
LUNCH_SLOT = "12:00-1:00"

with open(DATA_FILE) as f:
    data = json.load(f)

issues = 0
for fac in data:
    tt = fac.get("timetable", {})
    for day in ["Mon","Tue","Wed","Thu","Fri","Sat"]:
        val = tt.get(day, {}).get(LUNCH_SLOT, "")
        if val not in LUNCH_VALS:
            print(f"  STILL BROKEN: {fac['name']} {day} 12:00-1:00 = {repr(val)}")
            issues += 1

if issues == 0:
    print("  All 12:00-1:00 columns clean across all faculty. OK")
