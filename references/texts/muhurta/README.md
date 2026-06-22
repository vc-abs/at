# Muhurta Text References

This folder stores active text references used for muhurta/yoga verification work.

## Active source artifacts (currently used)

- `text/muhurthaOrElectionalAstrologyRamanDli2015128092.archiveDjvu.txt`
  - Extracted OCR text from archive item:
    https://archive.org/details/in.ernet.dli.2015.128092
- `text/vedicAstroTextbookSupport.txt`
  - Local extracted text from `/home/vc/Downloads/vedic-astro-textbook.pdf`
- `text/muhurtaJyotisVedicAstrology.txt`
  - OCR text from archive item:
    https://archive.org/details/MuhurtaJyotisVedicAstrology

## Retained future reference PDFs (not active inputs)

- `futureReferences/bphs1RSanthanam.pdf` (DVC-tracked)
- `futureReferences/jyotishVidyaSageParasara.pdf` (DVC-tracked)
- `vedicAstroTextbookSupport.pdf` (DVC-tracked source for the active support text)

## Source and derived artifacts relationship

- **Manifest**: `manifest.json` is the canonical index of currently retained source artifacts.
- **Derived text artifacts**: files under `text/` are used for search and citation candidate discovery.
- **Provenance mapping**: `data/muhurtaYogaProvenance.csv` links yoga rows to evidence snippets/page candidates.
  - `primarySourceText` identifies the best current supporting source for a yoga row.
  - `corroboratingSources` captures additional supporting English references when available.
  - `weightSupportStatus` summarizes how well the current weight is supported by English evidence.
  - `verse` is reserved for confirmed verse citations.
  - `evidenceSnippet` holds current English-source supporting text.

In short: `manifest.json` declares active source artifacts; `text/` holds searchable evidence;
`muhurtaYogaProvenance.csv` records per-yoga validation evidence state.

## Notes

- Always verify rights and reuse permissions before redistribution.
- For textual verification, populate chapter/verse/page citations in `data/muhurtaYogaProvenance.csv` and migrate provisional English evidence from `evidenceSnippet` where appropriate.
- Large PDF binaries were dropped from this folder because they are not immediately used.
  Backlog retains source links for future retrieval/validation.
