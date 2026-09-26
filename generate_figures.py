from pathlib import Path
import csv
import json
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


# Embed TrueType fonts in vector outputs so the submission PDF contains no
# Type 3 figure fonts.
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2F5597"
AMBER = "#D89216"
GREY = "#9AA0A6"
GRID = "#D9DDE3"


def finish(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def summarize(rows, prefix, links):
    """Derive categorical counts without assigning scores to E/P/NPD."""
    vectors = [[r[f"{prefix}_L{i}"] for i in links] for r in rows]
    downstream = [v[-4:] for v in vectors]
    first = Counter(next((f"L{i + 5}" for i, state in enumerate(v)
                          if state != "E"), "All E") for v in downstream)
    profiles = Counter("All E" if v.count("E") == 4 else
                       "No E" if "E" not in v else "Mixed"
                       for v in downstream)
    return {
        "n": len(rows),
        "links": {f"L{link}": {state: sum(v[i] == state for v in vectors)
                               for state in ("E", "P", "NPD")}
                  for i, link in enumerate(links)},
        "downstream_profiles": {v: profiles[v] for v in ("All E", "No E", "Mixed")},
        "first_non_explicit": {v: first[v] for v in ("L5", "L6", "L7", "L8", "All E")},
    }


def derive_analysis():
    with (ROOT / "analysis_cases.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len({r["stable_id"] for r in rows}) != len(rows):
        raise ValueError("Duplicate stable case ID")
    fields = ([f"primary_L{i}" for i in range(1, 9)] +
              [f"record_linked_L{i}" for i in range(5, 9)])
    if any(r[f] not in ("E", "P", "NPD") for r in rows for f in fields):
        raise ValueError("Invalid categorical state")
    changes = []
    corrections = []
    for r in rows:
        for i in range(5, 9):
            p, s = r[f"primary_L{i}"], r[f"record_linked_L{i}"]
            if p != s:
                if (p, s) != ("E", "P"):
                    raise ValueError("Record-linked sensitivity must be an E-to-P restriction")
                changes.append({"stable_id": r["stable_id"], "link": f"L{i}",
                                "primary": p, "record_linked": s})
        for label, baseline, current, links in (
            ("Primary", "baseline_primary", "primary", range(1, 9)),
            ("Record-linked", "baseline_strict", "record_linked", range(5, 9)),
        ):
            for i in links:
                before, after = r[f"{baseline}_L{i}"], r[f"{current}_L{i}"]
                if before != after:
                    corrections.append({"stable_id": r["stable_id"], "analysis": label,
                                        "link": f"L{i}", "before": before, "after": after})
    primary = summarize(rows, "primary", range(1, 9))
    record = summarize(rows, "record_linked", range(5, 9))
    strata = {}
    for field in ("activation_source_group", "function_cluster", "country"):
        strata[field] = {}
        for value in sorted({r[field] for r in rows}):
            selected = [r for r in rows if r[field] == value]
            strata[field][value] = {"primary": summarize(selected, "primary", range(1, 9)),
                                    "record_linked": summarize(selected, "record_linked", range(5, 9))}
    report = {
        "primary": primary, "record_linked": record, "strata": strata,
        "countries": dict(Counter(r["country"] for r in rows)),
        "all_eight_primary_explicit_ids": [r["stable_id"] for r in rows
                                           if all(r[f"primary_L{i}"] == "E" for i in range(1, 9))],
        "baseline_ena_ids": [r["stable_id"] for r in rows if r["ena"] == "Yes"],
        "record_linked_changes": changes,
        "record_linked_changed_case_count": len({x["stable_id"] for x in changes}),
        "historical_to_revised_corrections": corrections,
        "reproducibility_limit": "Two dated 19 September search-pass/query-family summaries were recovered from the historical register and preserved separately as historical_search_passes.csv. The full 317-row candidate register, individual executed queries, hit histories and complete exclusion records were not located. No complete search-frame reconstruction is claimed."
    }
    for analysis in (primary, record):
        assert all(sum(v.values()) == len(rows) for v in analysis["links"].values())
        assert sum(analysis["downstream_profiles"].values()) == len(rows)
        assert sum(analysis["first_non_explicit"].values()) == len(rows)
    (ROOT / "analysis_summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return primary, record


def aggregate_figure(primary):
    labels = [f"L{i}" for i in range(1, 9)]
    explicit = np.array([primary["links"][v]["E"] for v in labels])
    partial = np.array([primary["links"][v]["P"] for v in labels])
    npd = np.array([primary["links"][v]["NPD"] for v in labels])
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10.8, 5.2))
    ax.bar(x, explicit, color=BLUE, width=0.72, label="Explicit (E)")
    ax.bar(x, partial, bottom=explicit, color=AMBER, width=0.72,
           label="Partial or indirect (P)")
    ax.bar(x, npd, bottom=explicit + partial, color=GREY, width=0.72,
           label="Not publicly documented (NPD)")

    for i in range(len(labels)):
        values = (explicit[i], partial[i], npd[i])
        bottoms = (0, explicit[i], explicit[i] + partial[i])
        for value, bottom in zip(values, bottoms):
            if value:
                ax.text(i, bottom + value / 2, str(int(value)), ha="center",
                        va="center", fontsize=10, fontweight="bold",
                        color="white" if value >= 7 else "black")

    ax.axvline(3.5, color="#666666", linestyle="--", linewidth=1.2)
    ax.text(1.5, 34.4, "Disclosure, output and control", ha="center",
            va="bottom", fontsize=12, fontweight="bold")
    ax.text(5.5, 34.4, "Applicant-facing recourse", ha="center",
            va="bottom", fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Pathways (N = {primary['n']})")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 36)
    finish(ax)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3,
              frameon=False, fontsize=9.5)
    fig.tight_layout()
    fig.savefig(OUT / "figure1_aggregate_traceability.pdf", bbox_inches="tight")
    fig.savefig(OUT / "figure1_aggregate_traceability.png", dpi=220,
                bbox_inches="tight")
    plt.close(fig)


def first_break_figure(primary):
    labels = ["L5\nChallenge", "L6\nEvidence", "L7\nReconsideration",
              "L8\nRemedy", "Explicit\nthrough L8"]
    values = [primary["first_non_explicit"][v] for v in ("L5", "L6", "L7", "L8", "All E")]
    colors = [AMBER, BLUE, BLUE, BLUE, "#3B7D5A"]

    fig, ax = plt.subplots(figsize=(9.6, 4.7))
    bars = ax.bar(np.arange(len(labels)), values, color=colors, width=0.66)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.35, str(value),
                ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_ylabel(f"Pathways (N = {primary['n']})")
    ax.set_xticks(np.arange(len(labels)), labels)
    ax.set_ylim(0, max(values) + 3)
    finish(ax)
    fig.tight_layout()
    fig.savefig(OUT / "figure2_first_break.pdf", bbox_inches="tight")
    fig.savefig(OUT / "figure2_first_break.png", dpi=220,
                bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    primary, record = derive_analysis()
    aggregate_figure(primary)
    first_break_figure(primary)
    print(json.dumps({"primary": primary, "record_linked": record}, indent=2))
