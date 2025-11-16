# Agent-Assisted Development Log

This document tracks significant changes and improvements to the Auspicious Times project that were made with the assistance of AI agents and automated tools.

## Overview

Auspicious Times is a Python-based Vedic astrology tool for finding auspicious times (muhurta) for various occasions. The project includes planetary calculations, divisional charts (vargas), strength calculations (shadBala), panchang computations, and muhurta yoga analysis.

---

## 2025-08-03: Initial Project Setup with Unit Tests

**Agent:** Codex  
**Commit:** `0bda06c` - "Introduced unit tests with the help of Codex."

### Summary
Complete project initialization with comprehensive test coverage. This marks the first commit establishing the entire codebase structure with unit tests for core functionality.

### Key Components Added

#### Core Modules
- **Core Library** (`core/`): Fundamental astrological calculations
  - `helpers.py`: Circular arithmetic, sign calculations, and utility functions
  - `constants.py`: Astrological constants and reference data
  - `sweHelpers.py`: Swiss Ephemeris integration for planetary positions
  - `varga.py`: Divisional chart (varga) calculations
  - `dignity.py`: Planet dignity calculations
  - `planetaryPositions.py`: Planet position computations
  - `planetQuality.py`: Planet strength and quality analysis
  - `specialPositions.py`: Special astrological points
  - `karakas.py`: Karaka (significator) calculations
  - `Cached.py`: Caching decorator for performance optimization

#### Calculation Modules
- **ShadBala** (`shadBala/`): Six-fold strength calculations for planets
  - Complete shadBala implementation
  - `cheshtaBala.py`: Motional strength calculations
  
- **Ashtakavarga** (`ashtakavarga/`): Ashtakavarga point system
  - CSV data files for bindu calculations
  
- **Dasha** (`dasha/`): Planetary period (dasha) calculations

- **Panchang** (`panchang/`): Hindu calendar calculations
  - Tithi, nakshatra, yoga, karana computations
  - `getMuhurtaYoga.py`: Muhurta yoga identification
  - `muhurtaYogaEffects.csv`: Database of 1479+ yoga effects

#### Application Structure
- **Main** (`main.py`): Entry point with config-based execution
- **Read/Write** (`readWrite/`): Configuration and output handling
  - `readConfig.py`: YAML config parser with preset system
  - `output.py`: Result formatting and export
  - `getDefaultConfig.py`: Default configuration loader

- **Chart** (`chart/`): Chart generation utilities
- **Varga** (`varga/`): Divisional chart system

#### Testing
- **Unit Tests** (`tests/test_core_helpers.py`): 108 lines of test coverage
  - Tests for circular value normalization
  - Distance calculations in circles
  - Sign distance and longitude conversions
  - Utility function tests (fold, select)
  - Parametrized tests for comprehensive coverage

#### Configuration System
- **Presets** (`presets/`): 13 preset configurations for different use cases
  - `biz.yml`, `bizUltra.yml`: Business muhurta
  - `education.yml`: Educational activities
  - `panchang.yml`: Panchang output
  - `peak.yml`, `weekly.yml`, `yearly.yml`: Time-based analyses
  - `amkADL.yml`, `amkDL.yml`: Specialized calculations
  - `eventBalas.yml`: Event strength analysis
  - Regional presets (e.g., `inTNJambukeswarar.yml`)

- **Examples** (`examples/`): Sample configurations
  - `config.yml`: Basic usage example
  - `composite.yml`: Composite configuration
  - `presetExtensions.yml`: Preset extension example

#### Development Infrastructure
- **VS Code Configuration** (`.vscode/`)
  - Debug launch configurations
  - Editor settings for Python development
  
- **Git Hooks** (`.githooks/`)
  - Pre-commit: Code quality checks
  - Pre-push: Additional validation
  
- **Code Quality**
  - `ruff.toml`: Ruff linter configuration (77 lines)
  - `pytest.ini`: Pytest configuration
  - `.editorconfig`: Editor consistency rules

- **Dependencies** (`requirements.txt`)
  - Swiss Ephemeris (pyswisseph)
  - Testing frameworks
  - YAML processing
  - Other scientific computing libraries

#### Tools
- **generateCombos.py** (`tools/`): 361-line combo generator for muhurta analysis
- **Trial Scripts** (`trial/`): Experimental implementations

### Technical Highlights

1. **Swiss Ephemeris Integration**: Planetary calculations using the highly accurate Swiss Ephemeris library with configurable ayanamsa (Raman ayanamsa preferred for accuracy)

2. **Modular Architecture**: Clear separation between calculation engines (core, shadBala, ashtakavarga), application logic (main, tools), and I/O (readWrite)

3. **Flexible Configuration**: YAML-based config system with preset layering - configs on the right have higher priority

4. **Test Coverage**: Comprehensive unit tests for core helper functions with pytest framework

5. **Performance Optimization**: Caching decorator implementation for expensive calculations

6. **Data-Driven Approach**: CSV files for complex lookup tables (ashtakavarga, muhurta yogas)

### Documentation
- Comprehensive README with:
  - Setup and usage instructions
  - Technical notes on accuracy and limitations
  - Extensive TODO list for future development
  - Development log with timestamps
  - Glossary and references
  - Acknowledgments to reference software (Jagannatha Hora, JyotishApp, JyotishyaMitra)

### Known Limitations Documented
- Ayanamsa choice affects calculation accuracy
- AbdaBala and MaasaBala calculations have known precision issues
- Polar region calculations may be imprecise
- Some calculation methods differ from reference software

### Statistics
- **Files Added**: 61 files
- **Lines Added**: 6,627 lines
- **Test Files**: 1 test module with comprehensive coverage
- **Data Files**: 2 CSV databases (ashtakavarga, muhurta yogas)
- **Preset Configurations**: 13 presets + 3 examples

---

## Future Work

Based on the README TODO section, planned improvements include:
- Enhanced Python 3.11 compatibility in setup
- True Pushya Paksha Ayanamsa exploration
- Chart visualization for trend analysis
- Improved date/time configuration options
- DMS notation support for coordinates
- Better tithi calculation accuracy
- Personal natal chart integration
- Additional panchang values (Abhijit Muhurta, Rahu Kaala)
- Package management improvements

---

## Notes

- This project demonstrates extensive knowledge of Vedic astrology principles
- The codebase shows careful consideration of accuracy vs. reference implementations
- Active development log indicates ongoing refinements and discoveries
- Test-driven approach from the initial commit
- Clear acknowledgment of reference implementations and sources

