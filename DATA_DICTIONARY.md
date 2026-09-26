# Data dictionary

## Shared conventions

The observational unit is institution by AI-enabled function by admissions pathway or population. `stable_id` joins case-level files. IDs A01-A18 and A20-A34 are intentionally retained: A19 is unused, not a missing row in this 33-case release. The integer `order` is presentation order, not a rank.

E means explicit documentary support for the relevant pathway and population. P means incomplete or indirect support, including unresolved scope or conflicting sources. NPD means not publicly documented within the assembled evidence, not proof of practical absence. These are categorical values with no numeric distance or weight.

| Link | Documentary proposition |
|---|---|
| L1 | An institution-hosted public source identifies the relevant AI-enabled admissions function or feature |
| L2 | The meaning or role of the AI-derived input is documented |
| L3 | A responsible human or institutional decision owner is identifiable |
| L4 | A person/institution can correct the relevant record, or a responsible human can depart from or override the AI output |
| L5 | An affected applicant has an identifiable route to question the record or consequence |
| L6 | The applicant can submit corrected information, supporting documentation, or other relevant evidence |
| L7 | The matter can be reconsidered on the merits, not just acknowledged administratively |
| L8 | An authority can alter, reopen, rescind, correct, or otherwise change the consequential outcome |

L1 measures source location, not source credibility or applicant awareness. Under the dated post-hoc harmonization, external-only provider/professional sources support P. L4 includes institution-side control and is not automatically an applicant remedy. An applicable general admissions procedure can support primary E at L5-L8 without naming AI. Record-linked E additionally requires a route reaching data processed by the particular AI function or its output. Missing linkage restricts selected primary E values to P; baseline P/NPD are retained. This does not establish correction or reprocessing of the original AI output.

CSV empty fields mean no value supplied for that field; they are not silently equivalent to zero, NPD, or proof of absence. Dates are ISO-formatted where available. Narrative evidence-date fields retain qualifications. UTC timestamps end in `Z`; `revision_local_date` refers to UTC+04:00. Some CSV cells contain serialized JSON arrays or objects; parse those with a JSON parser after CSV parsing.

## analysis_cases.csv

| Column or family | Meaning |
|---|---|
| `order`, `stable_id`, `institution` | Presentation order, stable case key, and institution name |
| `country` | Country of the included pathway |
| `function_cluster` | Descriptive transcript/academic-record versus other-admissions-function grouping |
| `activation_source_group` | Current direct-institution versus provider/professional source grouping; correlated with L1 by definition |
| `activation_source_class` | More detailed source-class description |
| `ena`, `ena_scope` | Retained baseline explicit-nonavailability metadata and its scope; separate from E/P/NPD and not an exhaustive current prevalence measure |
| `ai_mediated_role` | Concise description of the AI-enabled function |
| `primary_L1` ... `primary_L8` | Current primary categorical states |
| `record_linked_L5` ... `record_linked_L8` | Current record-domain sensitivity states |
| `baseline_primary_L1` ... `baseline_primary_L8` | Preserved earlier primary states, not current results |
| `baseline_strict_L5` ... `baseline_strict_L8` | Preserved earlier sensitivity states; historical field names retained |
| `activation_url` | Source locating the AI-assisted admissions function |
| `recourse_url`, `followup_url` | Retained recourse and follow-up source locators; may contain multiple locators |
| `baseline_checked`, `followup_checked` | Recorded evidence-check dates and qualifications, not proof every source was accessible |
| `record_link_rationale` | Reason for retaining or restricting record-linked states |

## population_verification.csv

`stable_id` and `institution` identify the case. `study_universe` states the bounded admissions scope. `activation_population` describes the population affected by the AI function; `recourse_population` describes who can use the documented route. `population_match` assesses their relation. `decision_stage` separates pre-decision updates, initial decisions, and later review objects. `mechanism_tags` is a JSON array of mechanism classifications. `verification_status` summarizes retrieval/verification status. `limitations` is a JSON array of explicit source/scope limitations. `adjudication` gives the resulting interpretation. `checked_utc` records the check timestamp.

## prospective_search_log.csv

`stable_id` and `institution` identify the case; `query_order` orders its searches, not result relevance. `checked_utc` records the check timestamp. `query_record` is a JSON object containing the executed `query`, its `status`, `executed_utc_date`, `selected_urls`, and the screening `disposition`. An empty selected-URL list is not a claim that there were no search hits. These 83 records are newly executed verification queries, not reconstructed historical searches.

## source_verification.csv

`stable_id`, `institution`, and `source_order` identify and order case/source records. `url` is the source locator. `role` describes its use in the verification. `status` records retrieval/access status, including failures or reliance on previously retained content. `page_date` gives a source date or explicit date limitation. `excerpt` is a brief attributed source extract, not a complete archived webpage. `interpretation` records the source's evidentiary use and limits. `checked_utc` is the check timestamp. A source record is not necessarily a unique URL or a successful retrieval.

## prospective_change_ledger.csv and final_adjudication.csv

Both retain `stable_id`, `institution`, `analysis`, `link`, `before`, `after`, `reason`, `source_urls`, and `checked_utc_date`. `analysis` distinguishes primary from record-linked states; `before`/`after` record categorical transitions. `reason` and `source_urls` explain the decision. Multiple source locators may be represented in a field.

The prospective file has 31 transitions across eight cases. The final file has the separate A08 primary L5 P-to-E correction and additionally records `checked_utc` and `revision_local_date`. The final correction's actual check was 25 September UTC and its revision date was 26 September in UTC+04:00. Do not add these row counts to the oldest-baseline difference: some states changed more than once.

## historical_search_passes.csv

The original column names are preserved. `Pass` is the historical record key; `Date` is its recorded date. `Search frame` and `Queries / families` describe broad search families, not individually executed queries. `New qualifying primary pathways` and `New substantive function class` preserve recorded outcomes, including their qualifications. `Pending leads retained`, `Outcome`, `Stopping-rule interpretation`, and `Notes` retain the original bounded status and caveats. Two pass summaries do not substitute for the missing full candidate register, hit histories, or query-level discovery trail.

## analysis_summary.json

`primary` summarizes L1-L8; `record_linked` summarizes L5-L8. Each contains `n`, per-link `links` counts for E/P/NPD, `downstream_profiles`, and `first_non_explicit`. Downstream profiles are `All E`, `No E`, or `Mixed` across L5-L8. `first_non_explicit` is the first non-E state in the fixed L5-to-L8 order, or `All E`; it is not a severity ranking.

`strata` repeats those summaries by activation-source group, function cluster, and country. `countries` gives case counts. `all_eight_primary_explicit_ids` lists complete primary pathways; `baseline_ena_ids` preserves historical flags. `record_linked_changes` lists current primary-to-record-linked E-to-P restrictions and `record_linked_changed_case_count` counts affected cases. `historical_to_revised_corrections` compares current states with the preserved baseline, not the number of editing actions. `reproducibility_limit` describes unavailable historical discovery materials. All these outputs are deterministically derived from the case CSV; no statistical reliability estimate is implied.
