# FAIGRI-EAGLE admissions recourse: data and calculation package

Companion to *Human Review Is Not Recourse: Auditing Challenge and Remedy in Operational AI-Assisted University Admissions*.

Package version: 1.0.0. Manuscript snapshot: R30-2026-09-26. The evidence states and calculations are unchanged from the manuscript's final local candidate dated 26 September 2026.

## Repository and citation

Repository: <https://github.com/shaikhamalkawi-ux/faigri-eagle-admissions-recourse>.

Version 1.0.0 archive: <https://doi.org/10.5281/zenodo.22975754>.

`CITATION.cff` supplies the title, version, DOI, release date, and five authors in manuscript order. Please cite this data and calculation package when using it. The deposit is not a journal article or manuscript preprint, and its release does not imply journal acceptance. Its creator and repository-owner metadata identify authors, so these are not anonymous reviewer-access links.

## Contents

All package files are in one directory. CSV files use UTF-8, a header row, and standard CSV quoting.

| File | Role |
|---|---|
| `analysis_cases.csv` | Current primary and record-linked states for 33 pathways, preserved baseline states, source URLs, dates, and rationales |
| `analysis_summary.json` | Reference calculation output derived from that matrix |
| `generate_figures.py` | Unmodified manuscript calculation and figure-generation script |
| `historical_search_passes.csv` | Two recovered historical summary-pass records, not the full historical screening trail |
| `population_verification.csv` | Population, decision-stage, mechanism, and access assessments for all 33 cases |
| `prospective_search_log.csv` | 83 executed queries from the 25 September verification round |
| `source_verification.csv` | 111 source-access records, brief attributed excerpts, and interpretations |
| `prospective_change_ledger.csv` | 31 cell transitions in the prospective verification round |
| `final_adjudication.csv` | One separately dated UNC-Chapel Hill L5 correction |
| `DATA_DICTIONARY.md` | Field meanings, coding definitions, and interpretation limits |
| `requirements.txt` | Tested calculation dependencies |
| `verify_reproducibility.py` | Integrity, record-count, and exact calculation-output checks |
| `SHA256SUMS.txt` | SHA-256 hashes of all other package files |
| `CITATION.cff` | Author, version, date, and DOI citation metadata |
| `RIGHTS_NOTICE.md` | License scopes and third-party exceptions |
| `LICENSE_CODE_MIT.txt` | MIT license for the two Python scripts |
| `LICENSE_DATA_CC_BY_4.0.md` | CC BY 4.0 grant for original data and documentation, excluding third-party material |

## Licenses

`generate_figures.py` and `verify_reproducibility.py` are licensed under the [MIT License](https://opensource.org/license/mit). The authors' original data compilation, interpretations, and other package documentation are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Brief quoted source excerpts and other third-party material are excluded from these grants and remain subject to their respective rights. This is a component-specific allocation, not a choice to apply either license to any file. See `RIGHTS_NOTICE.md` and the two license files for scope and terms.

## Reproduce

Tested with Python 3.12.14, NumPy 2.3.5, and Matplotlib 3.11.2. In a clean environment with the package extracted:

```text
python -m pip install -r requirements.txt
python verify_reproducibility.py
```

The test checks the manifest, CSV row counts and IDs, and categorical states. It runs the exact generator in a temporary directory and compares the entire derived JSON object with `analysis_summary.json`. It confirms the 33-case denominator, both eight-/four-link tables, downstream profiles, first-non-explicit partitions, country counts, and the 12 E-to-P record-linkage restrictions. Temporary outputs are removed automatically after the test.

To generate the results and figures in the extracted directory:

```text
python generate_figures.py
```

This command regenerates `analysis_summary.json` and creates four files in `figures/`: PDF and PNG versions of the aggregate-state chart and first-non-explicit-link chart. Those binaries are not needed as inputs and are not included in the deposit. The script does not change the input CSV or update manuscript prose or tables. JSON comparison is semantic and exact; PDF binary hashes may vary with creation timestamps or software versions.

## Scope and limits

The unit is an institution by AI-enabled function by admissions pathway or population, not every operation of an institution. There are 33 source-qualified pathways: 28 United States, two United Kingdom, and one each Australia, Canada, and Singapore. The historical 52-country search frame is not the analyzed sample or a prevalence denominator.

The primary downstream L5-L8 profiles are eight all-E, 18 no-E, and seven mixed. The exploratory record-linked restriction gives six all-E, 22 no-E, and five mixed. E/P/NPD are categorical documentary states, not numerical scores. General applicable admissions procedures can qualify in the primary analysis; the record-linked analysis asks an additional connection-to-record-domain question and is one-sided by construction. It does not independently validate a deficit or demonstrate successful recourse in practice.

The 31-row prospective change ledger remains distinct from the later one-row correction and from differences against the oldest baseline. The latter correction changes only A08 primary L5 from P to E. All source and query dates are retained; access limitations are not erased by the fact that a query was executed.

The full historical 317-row candidate/exclusion register, individual historical executed-query trail, and complete immutable source archive were not recovered. Two historical summary passes and the newly executed verification queries do not reconstruct that missing record. Reproducing these calculations is not independent validation of the underlying documentary judgments.

This minimal package deliberately excludes the manuscript and Supplement, title page, cover letter, the full evidence workbook, contextual correspondence summaries, raw emails, attachments, personal contact information, and internal QA/handoff records. The admissions data use public institutional/provider sources rather than non-public student-level records. Public links can change after their recorded retrieval dates. Source excerpts remain attributed to their original sources; consult `RIGHTS_NOTICE.md` before reuse.
