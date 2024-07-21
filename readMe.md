# Auspicious Times

	A simple tool to find auspicious times for various occasions and endeavors.

# Usage
```console
$ # Simple run.
$ python3 main.py ./examples/config.yml

$ # Using presets. Configs to the right have more priority.
$ python3 main.py ./presets/biz.yml ./examples/presetExtensions.yml
```

## Thanks To
* [Jagannatha Hora](https://www.vedicastrologer.org/jh/), a vedic astrology software by P. V. R. Narasimmha Rao.
* [JyotishApp](https://play.google.com/store/apps/details?id=com.vishdroid.jyotisha), an android app by Vishnuvardhana SV.
* [JyotishyaMitra](https://github.com/VicharaVandana/jyotishyamitra/), a python package by Shyam Bhat.

## Notes
* Some computations might be off by a few minutes.
* The preferred ayanamsa is "ay_raman" as it's closer to the Pushya at 16Cn, suggested by PVN Rao.
* Jagannatha Hora seems to be more stable in handling higher latitudes than JyotishApp.
* Astrology software in general seem to have at least a few minor bugs in handling sunrise and sunset times at higher latitudes.
* Some names are in English and other in Sanskrit. This is a temporary situation for operational efficiency.
* AbdaBala and MaasaBala calculations doesn't seem to be precise, as the length of an year (based Jupiter's movement across signs) is considered to be 360 days, instead of ~361.08333 days. The same anchors are used for computing MaasaBala too. This might render the values incorrect. This might need some new calculation methods by analyzing Astro Data Banks.
* Rise and Set calculations of polar regions could be imprecise.

## ToDo
* Create CSV-s for storing all possible data in the constants file.
* Explore True [Pushya Nakshatra Ayanamsa by PVRNR](https://astrorigin.com/pyswisseph/sphinx/ephemerides/sidereal/suryasiddhanta_and_aryabhata.html#true-pushya-paksha-ayanamsha) (swe.SIDM_TRUE_PUSHYA).
* Think about having the start time as the default time.
* Use planetary short forms (IE: Me, Ju, etc) as the default.
* Try using [Pyswisseph](https://github.com/astrorigin/pyswisseph) instead of depending on sideralib, as the former has become essential for comparatively complex calculations.
* Replace periods with a single period config, with values with same type as frequency.
* Check whether muhurtaYoga effects depend upon Pakshatithis.
* Validate the presets with experts.
* Get popular reference locations cross regions, from experts.
* Try adding more muhurta yoga combinations.
* Introduce proper package management.
* Make the configuration a bit more human readable.
* Support DMS notation for latitudes and longitudes.
* Improve the accuracy of Tithi Calculations.
* Try to depend on chart objects, rather than python datetime for weekday calculations.
* Prefer numbers over strings for calculations. Have a translation layer at the tail to make things readable. This could be done as a part of performance improvements, post initial development. This could lead to moving some data dependent decisions to calculations.
* Standardize naming conventions across languages. IE: Don't use Wednesday and Budha together.
* Find the correct name for the muhurta yoga recorded as apaduddharaka.
* Handle dvipushkara and tripushkara yogas appropriately.
* Add individual impacts of weekdays, tithis and nakshatras to muhurta effects. Refer: https://www.astrojyoti.com/naksatratithiyogainfo.htm
* Bring in the effects of other time scales like maasa, yoga, karana, chowgadiya, hora etc. These might need a different CSV file as the format is different, as their effects are not tied to other scales.
* When possible include personal natal charts to find muhurta fitment.
* Fine tune the analysis with input from: https://astrologerjolly.tripod.com/muhurtha.htm
* Understand the impact of altitude on charts, as the sunrise time would be different.

## References
* [ShadBala Calculations by Dr Mahesh Joshi](https://www.youtube.com/watch?v=d7GX4Jm39Is)

## Findings
* Krakacha yoga is formed when tithi + vaara = 13.
* Amritsiddhi Muhurtayoga is a subset of Sarvarthasiddhi yoga.

## Glossary
* **JH**: Jagannatha Hora.
* **JA**: JyotishApp.

## 	Log
* 2406250100 - Found out that the difference between the Saptavargaja Calculation of JH and JA are due the differences in calculating D2 chart. JH by default doesn't use the traditional Parasara Hora. And also found out that there are many systems of calculating divisional charts.
* 2406250100 - The varga computation used here ended up to be really closer the the Custom Divisional Chart from JH.
* 2406270340 - Got the Saptavargaja calculation right, after a long struggle due to not understanding some fundamental concepts.
* 2406300355 - Discovered that there are some minute differences in the positions of fast moving planets between JA and siderealib, when the ayanamsa is set to BV. Raman.
