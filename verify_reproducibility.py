"""Verify package integrity and recompute the supplied case-level results."""

from pathlib import Path
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
CSV_ROWS = {
    "analysis_cases.csv": 33,
    "historical_search_passes.csv": 2,
    "population_verification.csv": 33,
    "prospective_search_log.csv": 83,
    "source_verification.csv": 111,
    "prospective_change_ledger.csv": 31,
    "final_adjudication.csv": 1,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    hashes = {}
    for line in (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        require(Path(name).name == name, "Manifest paths must be flat filenames")
        require(name not in hashes, "Duplicate manifest filename")
        require(len(digest) == 64, "Invalid SHA-256 length")
        path = ROOT / name
        require(path.is_file(), f"Missing package file: {name}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                f"SHA-256 mismatch: {name}")
        hashes[name] = digest
    required = set(CSV_ROWS) | {
        "analysis_summary.json", "generate_figures.py", "verify_reproducibility.py",
        "README.md", "DATA_DICTIONARY.md", "RIGHTS_NOTICE.md",
        "requirements.txt", "CITATION.cff", "LICENSE_CODE_MIT.txt", "LICENSE_DATA_CC_BY_4.0.md",
    }
    require(set(hashes) == required, "Manifest differs from the release allowlist")

    records = {}
    for name, expected in CSV_ROWS.items():
        with (ROOT / name).open(encoding="utf-8", newline="") as handle:
            records[name] = list(csv.DictReader(handle))
        require(len(records[name]) == expected, f"Unexpected row count: {name}")
    cases = records["analysis_cases.csv"]
    ids = [r["stable_id"] for r in cases]
    expected_ids = {f"A{i:02d}" for i in range(1, 35) if i != 19}
    require(len(set(ids)) == 33 and set(ids) == expected_ids, "Case ID set differs")
    require({r["stable_id"] for r in records["population_verification.csv"]} == expected_ids,
            "Population crosswalk ID set differs")
    for name in ("prospective_search_log.csv", "source_verification.csv",
                 "prospective_change_ledger.csv", "final_adjudication.csv"):
        require(all(r["stable_id"] in expected_ids for r in records[name]),
                f"Unknown case key in {name}")
    for row in cases:
        for prefix, links in (("primary", range(1, 9)), ("record_linked", range(5, 9)),
                              ("baseline_primary", range(1, 9)),
                              ("baseline_strict", range(5, 9))):
            require(all(row[f"{prefix}_L{i}"] in ("E", "P", "NPD") for i in links),
                    f"Invalid categorical state for {row['stable_id']}")
    correction = records["final_adjudication.csv"][0]
    require((correction["stable_id"], correction["analysis"], correction["link"],
             correction["before"], correction["after"]) == ("A08", "primary", "L5", "P", "E"),
            "Final correction differs")

    reference = json.loads((ROOT / "analysis_summary.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="faigri_eagle_reproduction_") as directory:
        scratch = Path(directory)
        for name in ("analysis_cases.csv", "generate_figures.py"):
            shutil.copy2(ROOT / name, scratch / name)
        environment = dict(os.environ)
        environment["MPLBACKEND"] = "Agg"
        result = subprocess.run([sys.executable, str(scratch / "generate_figures.py")],
                                cwd=scratch, env=environment, capture_output=True,
                                text=True, encoding="utf-8", check=True)
        observed = json.loads((scratch / "analysis_summary.json").read_text(encoding="utf-8"))
        require(observed == reference, "Full derived JSON differs from the supplied reference")
        require(json.loads(result.stdout) == {k: observed[k] for k in ("primary", "record_linked")},
                "Printed summaries differ from derived JSON")
        for name in ("figure1_aggregate_traceability.pdf", "figure1_aggregate_traceability.png",
                     "figure2_first_break.pdf", "figure2_first_break.png"):
            path = scratch / "figures" / name
            require(path.is_file() and path.stat().st_size > 0, f"Missing generated figure: {name}")

    expected_primary = {
        "L1": (19, 14, 0), "L2": (33, 0, 0), "L3": (33, 0, 0), "L4": (11, 22, 0),
        "L5": (15, 10, 8), "L6": (13, 12, 8), "L7": (11, 12, 10), "L8": (9, 13, 11),
    }
    expected_record = {"L5": (11, 14, 8), "L6": (11, 14, 8),
                       "L7": (8, 15, 10), "L8": (6, 16, 11)}
    for key, expected in (("primary", expected_primary), ("record_linked", expected_record)):
        require(observed[key]["n"] == 33, f"Denominator differs: {key}")
        actual = {link: tuple(counts[state] for state in ("E", "P", "NPD"))
                  for link, counts in observed[key]["links"].items()}
        require(actual == expected, f"Link counts differ: {key}")
    require(observed["primary"]["downstream_profiles"] == {"All E": 8, "No E": 18, "Mixed": 7},
            "Primary profiles differ")
    require(observed["record_linked"]["downstream_profiles"] == {"All E": 6, "No E": 22, "Mixed": 5},
            "Record-linked profiles differ")
    require(observed["primary"]["first_non_explicit"] ==
            {"L5": 18, "L6": 2, "L7": 3, "L8": 2, "All E": 8}, "Primary first-link partition differs")
    require(observed["record_linked"]["first_non_explicit"] ==
            {"L5": 22, "L6": 0, "L7": 3, "L8": 2, "All E": 6}, "Record-linked first-link partition differs")
    require(observed["countries"] == {"United States": 28, "United Kingdom": 2,
                                      "Australia": 1, "Canada": 1, "Singapore": 1},
            "Country counts differ")
    require(observed["all_eight_primary_explicit_ids"] == ["A18"], "All-eight-E case differs")
    require(len(observed["record_linked_changes"]) == 12 and
            observed["record_linked_changed_case_count"] == 4, "Sensitivity restrictions differ")
    print(json.dumps({"verified_package_files": len(hashes), "csv_rows": CSV_ROWS,
                      "full_derived_json_equal": True, "cases": 33,
                      "primary_downstream_profiles": observed["primary"]["downstream_profiles"],
                      "record_linked_downstream_profiles": observed["record_linked"]["downstream_profiles"],
                      "generated_figure_files": 4}, indent=2))


if __name__ == "__main__":
    main()
