# Astrology Trial

	A trial of some existing astrology packages to find auspicious times.


## ToDO
* Try adding more muhurta yoga combinations.
* Introduce proper package management.
* Make the configuration a bit more human readable.
* Support DMS notation for latitudes and longitudes.
* Rename this package to Auspicious Times.
* Improve the accuracy of Tithi Calculations.
* Try to depend on chart objects, rather than python datetime for weekday calculations.
* Prefer numbers over strings for calculations. Have a translation layer at the tail to make things readable. This could be done as a part of performance improvements, post initial development. This could lead to moving some data dependent decisions to calculations.
* Standardize naming conventions across languages. IE: Don't use Wednesday and Budha together.

## Notes
* Some computations might be off by a few minutes.
* The preferred ayanamsa is "ay_raman" as it's closer to the Pushya at 16Cn, suggested by PVN Rao.
* Jagannatha Hora seems to be more stable in handling higher latitudes than JyotishApp.
* Astrology software in general seem to have at least a few minor bugs in handling sunrise and sunset times at higher latitudes.
* Some names are in English and other in Sanskrit. This is a temporary situation for operational efficiency.

## References
* Krakacha yoga is formed when tithi + vaara = 13.
* Amritsiddhi Muhurtayoga is a subset of Sarvarthasiddhi yoga.
