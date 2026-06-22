# Muhurta Source Authority (Draft)

Status: draft (to be finalized with domain review)

## Purpose

Define canonical source authority and citation workflow for muhurta-yoga rules and severities,
so `muhurtaYogaEffects.csv` can evolve from an operational rule table into a text-auditable baseline.

## Authority model (dual-track)

Active source artifacts are listed in `references/texts/muhurta/manifest.json`.

### 1) Implementation authority (fast, practical)

- Primary implementation source: **Muhurtha or Electional Astrology (B. V. Raman)**
  - Active artifact:
    `references/texts/muhurta/text/muhurthaOrElectionalAstrologyRamanDli2015128092.archiveDjvu.txt`

### 2) Support sources (higher text quality/readability)

- Active support artifacts:
  - `references/texts/muhurta/text/vedicAstroTextbookSupport.txt`
  - `references/texts/muhurta/text/muhurtaJyotisVedicAstrology.txt`

### 3) Audit authority links (for future retrieval/validation)

- Muhurta Chintamani (1907 Nirnay Sagar):
  https://archive.org/details/muhurta-chintamani-1907-nirnay-sagar-press-from-residence-of-ashok-ji-kashmir
- Muhurta Chintamani (DLI scan):
  https://archive.org/details/in.ernet.dli.2015.487104
- Shri Muhurta Martanda (DLI scan):
  https://archive.org/details/in.ernet.dli.2015.312516

### Conflict policy

- If Raman and Sanskrit audit texts agree: mark row as `text-verified`.
- If they differ: keep Raman behavior as operational default, mark row provisional, and
  open a reconciliation note in provenance (`notes` + citation details).

> This model enables fast implementation while preserving a path to text-auditable rigor.

## Normalization conventions

- Weekdays (`vaara`) normalized to lowercase English: sunday..saturday
- Nakshatras normalized to repository spellings used in `src/at/panchang/muhurtaYogaEffects.csv`
- Alias spellings tracked in `data/muhurtaYogaProvenance.csv` (`aliases` column)

## Data files and responsibilities

- `src/at/panchang/muhurtaYogaEffects.csv`
  - Runtime rule matrix used by code (`getMuhurtaYogas`).
  - Defines which combinations of `tithi`, `vaara`, `nakshatra` activate each yoga.
  - Scoring inputs are `impact` and `effect`; weighted effect = `impact * effect`.
  - This is the operational dataset (what the tool currently computes).

- `data/yogaWeightPolicy.yml`
  - Audit/guardrail policy for expected weighted severities per yoga.
  - Used by tests to ensure CSV severities stay consistent with agreed policy.

- `data/muhurtaYogaProvenance.csv`
  - Citation tracking layer for textual verification and weight appropriateness review.
  - Records row-specific primary/corroborating sources, review status, confidence, and weight support status.
  - Not used at runtime for yoga calculation.

## Citation workflow

For each yoga/class:

1. Capture source record in `data/muhurtaYogaProvenance.csv`
   - `primarySourceText`, `corroboratingSources`, `sourceText`, `chapter`, `verse`, `evidenceSnippet`, `tradition`
2. Set `reviewStatus`
   - `unverified` -> `reviewed` -> `text-verified`
3. Record reviewer metadata
   - `reviewedBy`, `reviewedAt`, `confidence`
4. Ensure severity band aligns with `data/yogaWeightPolicy.yml`

## Current limitations

- Canonical Sanskrit audit citations are not yet fully captured per yoga.
- Provenance now contains real evidence snippets/page candidates in `evidenceSnippet`; `verse` is reserved for confirmed verse citations and is currently mostly empty.
- Existing tests validate mechanics and schema, not textual correctness.
