"""
RECORD CHECK - IT Server Capacity
=================================
Name  : [Sebastian]
Lane  : IT
Date  : [2026-11-08]

Run it: python template.py
"""

from pathlib import Path


# 1. FUNCTIONS

def parse_line(raw_line):
    """Clean one messy server record and return its values as a dictionary."""
    parts = [part.strip().lower() for part in raw_line.strip().split(",")]
    if len(parts) != 3 or not parts[0]:
        raise ValueError("Expected: hostname, used=number, total=number")

    fields = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"Missing '=' in {part!r}")
        key, value = [piece.strip() for piece in part.split("=", 1)]
        if key in fields or key not in ("used", "total"):
            raise ValueError(f"Unexpected or repeated field: {key!r}")
        fields[key] = float(value)

    if set(fields) != {"used", "total"}:
        raise ValueError("Record needs used and total fields")
    if fields["used"] < 0 or fields["total"] <= 0:
        raise ValueError("Used must be nonnegative and total must be positive")

    return {"hostname": parts[0], "used": fields["used"], "total": fields["total"]}


def status_of(record):
    """Classify a server as OVER LIMIT, WARNING, or OK by capacity usage."""
    percent = record["used"] / record["total"] * 100
    if percent > 100:
        return "OVER LIMIT"
    if percent >= 90:
        return "WARNING"
    return "OK"


# 2. INPUT: Load deliberately messy records from a text file.
# Use a path next to this script so it works from any terminal folder.
data_file = Path(__file__).with_name("it_messy_records.txt")
raw_records = []
with data_file.open("r", encoding="utf-8") as file:
    for line in file:
        if line.strip():
            raw_records.append(line)


# 3. PROCESS + OUTPUT
flagged = 0
valid = 0
errors = 0

for line_number, raw_record in enumerate(raw_records, start=1):
    try:
        record = parse_line(raw_record)
    except ValueError as error:
        errors += 1
        print(f"Line {line_number}: INVALID RECORD - {error}")
        continue

    valid += 1
    status = status_of(record)
    if status != "OK":
        flagged += 1
    print(f"{record} | {status}")

print(f"Summary: {valid} valid records, {flagged} flagged, {errors} invalid")


# 4. TESTING NOTES
# Tested with at least five records with inconsistent spacing and case.
# Example invalid value: "srv-07, used=abc, total=100"
# float('abc') raises ValueError: could not convert string to float: 'abc'
# The try/except above catches this and continues processing other records.
