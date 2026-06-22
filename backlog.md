# Backlog

## Table of Contents

- [Tooling and Developer Experience](#tooling-and-developer-experience)
- [Architecture and Refactoring](#architecture-and-refactoring)
- [Configuration and Input Model](#configuration-and-input-model)
- [Muhurta/Yoga Domain Coverage](#muhurtayoga-domain-coverage)
- [Performance and Scalability](#performance-and-scalability)
- [Output and Explainability](#output-and-explainability)
- [Data and Validation](#data-and-validation)
- [Documentation and Examples](#documentation-and-examples)

## Tooling and Developer Experience

- Make `setup.sh` work well with Python 3.11.
- Remove hacky fixes.
- Introduce proper package management.
- Choose a testing framework and write tests for core modules and workflows.
- Increase automated test coverage toward high-confidence levels (70%+ to start).
- Add more integration/smoke coverage for real runtime paths, especially Chart/ShadBala preset-driven execution.
- Standardize naming conventions across languages (for example, avoid mixing Wednesday and Budha).
- Normalize file naming conventions across docs/data/references to snake_case (tests already follow snake_case), and update any recently introduced non-snake-case paths.

## Architecture and Refactoring

- Think of moving computations to Julian Dates for simplicity and consistency.
- Try to depend on chart objects, rather than Python `datetime`, for weekday calculations.
- Prefer numbers over strings for calculations; add a translation layer at output time.

## Configuration and Input Model

- Make configuration more human-readable.
- Support DMS notation for latitudes and longitudes.
- Introduce `endTime` as an option to allow skipping explicit period config.
- Introduce `startDate`, `startTime`, `endDate`, and `endTime` configs.
- Replace `periods` with a single `period` config with values aligned to `frequency` type.
- Make Rahu/Ketu exaltation handling configurable by tradition/school after correcting the current exaltation logic.

## Muhurta/Yoga Domain Coverage

- Explore True [Pushya Nakshatra Ayanamsa by PVRNR](https://astrorigin.com/pyswisseph/sphinx/ephemerides/sidereal/suryasiddhanta_and_aryabhata.html#true-pushya-paksha-ayanamsha) (`swe.SIDM_TRUE_PUSHYA`).
- Check whether muhurta-yoga effects depend on Paksha/Tithi combinations.
- Try adding more muhurta-yoga combinations.
- Find the correct name for the muhurta yoga recorded as `apaduddharaka`.
- Handle tripushkara/tripushkara yogas appropriately.
- Improve the accuracy of Tithi calculations.
- Add individual impacts of weekdays, tithis, and nakshatras to muhurta effects.
- Bring in effects of additional time scales: maasa, yoga, karana, chowgadiya, hora, etc.
- Introduce panchang values like Abhijit Muhurta, Rahu Kaala, Gowri Panchangam, etc.
- Add lower-priority Choghadiya support as a separate/duplicate field set only if we later confirm the repo should expose it distinctly from Gowri rather than treating it as a naming-layer concern.
- Make `panchang.vaara` return Vedic vaara.
- When possible, include personal natal charts to find muhurta fitment.

## Data and Validation

- Refine ShadBala further against manual comparison evidence while keeping BPHS as rule authority, especially around Drik/Drig Bala, Mercury Paksha Bala branch behavior, and remaining component-level divergences.
- Introduce a yoga definition registry (YAML/CSV + Python handlers where needed) with metadata, dimensions, polarity, and rule definitions.
- Reconcile Amritadi/Anandadi yoga provenance and runtime scope using trusted scanned sources, and determine whether the current implementation mixes Siddha-yoga, Anandadi, and incompletely sourced Amritadi-style rules.
  - Confirm which named systems are actually present in trustworthy sources: Siddha Yoga, Amrita Siddha, Anandadi, any separately attested Amritadi/Amritadhi family, and the Tamil-style 3-type weekday–nakshatra system.
  - Model the Tamil-style 3 yoga types as a **separate rule family**, rather than folding them into Anandadi or generic Siddha-yoga data.
  - Define the Tamil 3-type family explicitly in backlog terminology and later implementation surfaces, including its canonical names, aliases/transliterations, polarity, and how it should be exposed at runtime independently of other yoga families.
  - Build a classification matrix for all relevant runtime rows: `repo yoga name -> claimed/traditional system -> source(s) -> confidence -> keep/rename/remove/defer`.
  - Verify whether `siddha` and `siddhi` are truly distinct in source material or are being conflated in the current implementation.
  - Verify whether `mrityu`, `kana`, `subha`, `amrita`, `utpata`, and related rows align with the Anandadi sequence found in *Muhurta Chintamani*.
  - Separately verify which currently implemented rows, if any, actually belong to the Tamil 3-type system (for example an `amrita` / `siddha` / `marana|mrityu` style grouping) and should be split away from Anandadi handling.
  - Determine whether `nasa`, `subhaMadhyam`, `sri`, and `suta` belong to a trustworthy source-backed system or should be marked provisional / unsupported.
  - Compare the runtime combinations and names in `src/at/panchang/muhurtaYogaEffects.csv` against trusted scan sources before changing weights or severities.
  - Record exact citations, source snippets, and page/scan references for each accepted mapping in `data/muhurtaYogaProvenance.csv`.
  - Decide remediation per row/family:
    - keep as-is with stronger provenance,
    - rename rows and/or add aliases,
    - split mixed systems into separate rule families/registries,
    - introduce a dedicated Tamil 3-type family with separate runtime naming/output where warranted,
    - remove or defer unsupported rows from runtime scoring.
  - After reconciliation, update all impacted surfaces together:
    - `src/at/panchang/muhurtaYogaEffects.csv`
    - `data/muhurtaYogaProvenance.csv`
    - `data/yogaWeightPolicy.yml`
    - related tests and source-authority docs.
  - Preferred sources for this audit:
    - *Muhurta Chintamani of Daivagya Ramacharya – Mahidhar Sharma*: https://archive.org/details/muhurta-chintamani-of-daivagya-ramacharya-mahidhar-sharma
    - *Shri Muhurta Martanda*: https://archive.org/details/in.ernet.dli.2015.312516
    - existing retained English support texts already tracked in the repository for Siddha / Amita Siddha and operational comparisons.
- Complete `data/muhurtaYogaProvenance.csv` from evidence-candidate status to citation-complete status:
  - Current file now includes row-specific provenance fields for weight review:
    - `primarySourceText`
    - `corroboratingSources`
    - `weightSupportStatus` (`unsupportedEnglish`, `singleEnglishSource`, `corroboratedEnglish`)
    - `weightAssessmentNotes`
    - `evidenceSnippet`
  - `verse` is intentionally reserved for confirmed verse citations and should remain empty until actually verified.
  - `evidenceSnippet` currently stores English-source support text from active sources; do not treat it as a verse citation.
  - `sourceText` currently lists the active English source pool, but `primarySourceText` and `corroboratingSources` are the row-level fields to trust when reviewing a specific yoga.
  - Fill chapter/verse/pageRef with confirmed citations for all tracked yogas.
  - Promote reviewStatus from `unverified` to `reviewed` and `text-verified` only after source checks.
  - When resuming, inspect these active files first:
    - `data/muhurtaYogaProvenance.csv`
    - `references/texts/muhurta/manifest.json`
    - `references/texts/muhurta/text/muhurthaOrElectionalAstrologyRamanDli2015128092.archiveDjvu.txt`
    - `references/texts/muhurta/text/vedicAstroTextbookSupport.txt`
    - `references/texts/muhurta/text/muhurtaJyotisVedicAstrology.txt`
  - Current English-support picture to continue from:
    - `corroboratedEnglish`: `amritSiddhi`, `amrita`, `generalRestrictions`, `mrityu`, `siddha`
    - `singleEnglishSource`: `asubha`, `guruPushya`, `raviPushya`, `visha`, `yamaghanta`, `subha`
    - many remaining yogas are still `unsupportedEnglish`
  - The immediate follow-up question is not “is the yoga present?” but “does the current weight have enough support?”
    Use `weightSupportStatus` + `evidenceSnippet` + `pageRef` to drive that review.
- Keep active source footprint minimal: retain only immediately used text artifacts and remove inactive local binaries.
- Keep future-reference links and retained reference PDFs synchronized:
  - Retained (DVC): `references/texts/muhurta/futureReferences/bphs1RSanthanam.pdf`
  - Retained (DVC): `references/texts/muhurta/futureReferences/jyotishVidyaSageParasara.pdf`
  - BPHS source path: `/home/vc/Downloads/BPHS - 1 RSanthanam.pdf`
  - Jyotish Vidya source path: `/home/vc/Downloads/Jyotish-vidya-sage-Parasara.pdf`
  - Muhurta Chintamani (1907 Nirnay Sagar): https://archive.org/details/muhurta-chintamani-1907-nirnay-sagar-press-from-residence-of-ashok-ji-kashmir
  - Muhurta Chintamani (DLI scan): https://archive.org/details/in.ernet.dli.2015.487104
  - Shri Muhurta Martanda (DLI scan): https://archive.org/details/in.ernet.dli.2015.312516
  - Kalaprakashika: https://archive.org/details/Kalaprakashika
  - Additional English candidates to evaluate:
    - Muhurta Jyotis Vedic Astrology: https://archive.org/details/MuhurtaJyotisVedicAstrology (promoted to active text support)
    - Muhurtha or Electional Astrology (B. V. Raman, alternate item): https://archive.org/details/bwb_P9-EAH-659
    - Electional Astrology (Vivian Robson): https://archive.org/details/in.ernet.dli.2015.128090 (tested, no useful current coverage)
    - Robson, Vivian, Electional Astrology: https://archive.org/details/robson-vivian-electional-astrology
- Validate presets with domain experts.
- Get popular reference locations across regions from experts.
- Fine tune analysis with input from https://astrologerjolly.tripod.com/muhurtha.htm.
- Verify Gowri/Choghadiya relationship and provenance later as a lower-priority follow-up:
  - determine whether Choghadiya should be exposed as a separate field set or just as an alternate label layer over the same segment logic,
  - verify whether Gowri and Choghadiya differ only by labels or also by weekday schedule semantics,
  - if needed later, add provenance/verification material during that verification cycle rather than carrying it in runtime data.
- Keep active English source set documented and reproducible:
  - Raman OCR text
    - Source (Archive item): https://archive.org/details/in.ernet.dli.2015.128092
    - Source OCR text: https://archive.org/download/in.ernet.dli.2015.128092/2015.128092.Muhurtha-Or-Electional-Astrology_djvu.txt
    - Local text target: `references/texts/muhurta/text/muhurthaOrElectionalAstrologyRamanDli2015128092.archiveDjvu.txt`
  - Vedic Astrology Textbook support text
    - Local source PDF path: `/home/vc/Downloads/vedic-astro-textbook.pdf`
    - Local text target: `references/texts/muhurta/text/vedicAstroTextbookSupport.txt`
  - Muhurta Jyotis Vedic Astrology support text
    - Source (Archive item): https://archive.org/details/MuhurtaJyotisVedicAstrology
    - Source OCR text: https://archive.org/download/MuhurtaJyotisVedicAstrology/Muhurta%20JyotisVedic%20Astrology_djvu.txt
    - Local text target: `references/texts/muhurta/text/muhurtaJyotisVedicAstrology.txt`
- Defer full Sanskrit OCR/model conversion for primary audit texts pending pipeline readiness and budget sign-off:
  - Muhurta Chintamani (1907 Nirnay Sagar): https://archive.org/details/muhurta-chintamani-1907-nirnay-sagar-press-from-residence-of-ashok-ji-kashmir
  - Muhurta Chintamani (DLI scan): https://archive.org/details/in.ernet.dli.2015.487104
  - Shri Muhurta Martanda (DLI scan): https://archive.org/details/in.ernet.dli.2015.312516
  - Reason: large scans + Devanagari OCR uncertainty; requires model-assisted extraction with confidence gates and manual citation review.
- Understand the impact of altitude on charts (sunrise shifts).

## Performance and Scalability

- Profile runtime hotspots (Swiss ephemeris calls, chart loops, pandas operations) and prioritize optimizations from measured bottlenecks.
- Evaluate vectorized/pandas extensions for bulk runs.
- If profiling confirms Python limits, move hotspot modules to a faster language (for example Rust/C++).

## Output and Explainability

- Introduce charts to analyze trends.
- Introduce `planetaryYogas` as a field set with a string output listing active planetary yogas.
- Score active yogas on Dharma, Artha, Kama, and Moksha dimensions and expose cumulative scores.
- Add positive/negative yoga balance fields such as `positiveYogaCount`, `negativeYogaCount`, and `yogaNetScore`.
- Add event-fit yoga scores such as `bizYogaScore`, `educationYogaScore`, `marriageYogaScore`, `travelYogaScore`, and `spiritualYogaScore`.
- Add explainability fields such as `yogaHighlights` and `yogaTopContributors` alongside `planetaryYogas`.

## Documentation and Examples

- Write a proper example for events (refer: `panchang.yml`).
