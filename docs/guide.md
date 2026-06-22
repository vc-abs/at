# Guide

## Table of Contents

- [What This Tool Does](#what-this-tool-does)
- [Basic Usage](#basic-usage)
- [Query Language Notes](#query-language-notes)

## What This Tool Does

`at` helps identify auspicious times for selected activities using Vedic astrology inputs and configurable presets.

## Basic Usage

- Setup environment: `sh ./setup.sh`
- Run with config: `python3 main.py ./examples/config.yml`
- Run validation: `./scripts/validate.sh`

## Query Language Notes

- The YAML `query` value is evaluated using `pandas.DataFrame.query(...)`.
- String contains checks are supported through vectorized string accessors, e.g.:
  - `nakshatra.str.contains('Rohini', na=False)`
  - `nakshatra.str.contains('rohini', case=False, na=False)`
- Use `na=False` for robust behavior when a string column may contain nulls.
