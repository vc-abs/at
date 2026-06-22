# Auspicious Times

	A simple tool to find auspicious times for various occasions and endeavors.

# Stack
* Python 3.11.6
* VS Code.

# Usage
*Activate the VENV before running setup and other commands.*

```console
$ # Setup.
$ sh ./setup.sh

$ # Simple run.
$ python3 main.py ./examples/config.yml

$ # Validate code: lint (src only) + tests with coverage.
$ ./scripts/validate.sh

$ # Open readable HTML coverage report.
$ xdg-open ./temp/coverage/index.html

$ # Pre-commit blocks direct `.pdf` commits.
$ # Prefer keeping only immediately used text artifacts in repo.
$ # If a PDF must be retained locally, track it with DVC:
$ ./scripts/addPdfToDvc.sh ./references/texts/muhurta/<book>.pdf
$ dvc push

$ # Using presets. Configs to the right have more priority.
$ python3 main.py ./presets/biz.yml ./examples/presetExtensions.yml
```

## Config Constants

You can define reusable root-level config constants and reference them from `query` and string-valued `customColumns` expressions.

```yml
constants:
  marketingWeekdayWeights:
    wednesday: 30
    friday: 24
    thursday: 22
    sunday: 18
  marketingMinHouses:
    - h3
    - h5
    - h7
    - h10
    - h11

query: >-
  weekdayScore > 0 and
  marketingMin >= 24

customColumns:
  weekdayScore: >-
    vaara.map(constants.marketingWeekdayWeights).fillna(0)
  marketingMin:
    min: constants.marketingMinHouses
```

Notes:
- author-facing config syntax uses `constants.foo`
- constants can hold reusable lists, thresholds, and mapping/weight dictionaries
- internally, expression evaluation rewrites that to pandas-compatible external-variable access only at the evaluation boundary
- constants remain available on merged runtime config as `config['constants']`
- constants are not exported as output columns unless you explicitly derive a custom output column from them

## Thanks To
* [Jagannatha Hora](https://www.vedicastrologer.org/jh/), a vedic astrology software by P. V. R. Narasimmha Rao.
* [JyotishApp](https://play.google.com/store/apps/details?id=com.vishdroid.jyotisha), an android app by Vishnuvardhana SV.
* [JyotishyaMitra](https://github.com/VicharaVandana/jyotishyamitra/), a python package by Shyam Bhat.

## Notes
* Accuracy of the computations are affected by the chosen Ayanamsa.
* The preferred ayanamsa is "raman" as it's closer to the Pushya at 16Cn, suggested by PVN Rao.
* Jagannatha Hora seems to be more stable in handling higher latitudes than JyotishApp.
* Astrology software in general seem to have at least a few minor bugs in handling sunrise and sunset times at higher latitudes.
* Some names are in English and other in Sanskrit. This is a temporary situation for operational efficiency.
* AbdaBala and MaasaBala calculations doesn't seem to be precise, as the length of an year (based Jupiter's movement across signs) is considered to be 360 days, instead of ~361.08333 days. The same anchors are used for computing MaasaBala too. This might render the values incorrect. This might need some new calculation methods by analyzing Astro Data Banks.
* Rise and Set calculations of polar regions could be imprecise.

## Backlog
- ToDo items were migrated to [`backlog.md`](./backlog.md) as part of deliberate-dev initialization.

## References
* [ShadBala Calculations by Dr Mahesh Joshi](https://www.youtube.com/watch?v=d7GX4Jm39Is)

## Findings
* Krakacha yoga is formed when tithi + vaara = 13.
* Amritasiddhi Muhurtayoga is a subset of Sarvarthasiddhi yoga.

## Glossary
* **JH**: Jagannatha Hora.
* **JA**: JyotishApp.

## 	Log
* 2406250100 - Found out that the difference between the Saptavargaja Calculation of JH and JA are due the differences in calculating D2 chart. JH by default doesn't use the traditional Parasara Hora. And also found out that there are many systems of calculating divisional charts.
* 2406250100 - The varga computation used here ended up to be really closer the the Custom Divisional Chart from JH.
* 2406270340 - Got the Saptavargaja calculation right, after a long struggle due to not understanding some fundamental concepts.
* 2406300355 - Discovered that there are some minute differences in the positions of fast moving planets between JA and siderealib, when the ayanamsa is set to BV. Raman.
* 2407250725 - Decided not to use the Chesta Bala computation used in JH and JA as the anchor date of 01-01-1900 seems arbitrary and changing the anchor impacts the balas of fast moving planets, significantly.
