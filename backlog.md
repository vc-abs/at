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
- Standardize naming conventions across languages (for example, avoid mixing Wednesday and Budha).

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
- Make Rahu/Ketu exaltation handling configurable by tradition/school.

## Muhurta/Yoga Domain Coverage

- Explore True [Pushya Nakshatra Ayanamsa by PVRNR](https://astrorigin.com/pyswisseph/sphinx/ephemerides/sidereal/suryasiddhanta_and_aryabhata.html#true-pushya-paksha-ayanamsha) (`swe.SIDM_TRUE_PUSHYA`).
- Check whether muhurta-yoga effects depend on Paksha/Tithi combinations.
- Try adding more muhurta-yoga combinations.
- Find the correct name for the muhurta yoga recorded as `apaduddharaka`.
- Handle tripushkara/tripushkara yogas appropriately.
- Improve the accuracy of Tithi calculations.
- Add individual impacts of weekdays, tithis, and nakshatras to muhurta effects.
- Bring in effects of additional time scales: maasa, yoga, karana, chowgadiya, hora, etc.
- Introduce panchang values like Abhijit Muhurta, Rahu Kaala, etc.
- Make `panchang.vaara` return Vedic vaara.
- When possible, include personal natal charts to find muhurta fitment.

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

## Data and Validation

- Introduce a yoga definition registry (YAML/CSV + Python handlers where needed) with metadata, dimensions, polarity, and rule definitions.
- Validate presets with domain experts.
- Get popular reference locations across regions from experts.
- Fine tune analysis with input from https://astrologerjolly.tripod.com/muhurtha.htm.
- Understand the impact of altitude on charts (sunrise shifts).

## Documentation and Examples

- Write a proper example for events (refer: `panchang.yml`).
