# FHIR-CDA Interoperability Lab

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![FHIR](https://img.shields.io/badge/HL7-FHIR_R4-orange)](https://hl7.org/fhir/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green)](LICENSE)

> **Personal experimental workspace for clinical interoperability engineering.**  
> Exploring data transformation pipelines, resource mapping, and search patterns across European health data exchange standards.

---

## Overview

This repository is a hands-on laboratory for designing and validating interoperability workflows between **HL7 CDA** (Clinical Document Architecture) and **HL7 FHIR** (Fast Healthcare Interoperability Resources), with a focus on the European health data exchange context (ePrescription, Patient Summary, EHDS).

It includes modular components for parsing, transforming, persisting, and indexing clinical data—mimicking the architectural patterns found in national health gateway and cross-border interoperability projects.

---

## Architecture & Data Flow

The project is organized around a progressive pipeline that reflects real-world integration patterns:

```text
Clinical Documents (CDA)
        ↓
   CDA Parser / XML ingestion
        ↓
   FHIR Resource Mapper (R4)
        ↓
   Structured Data Store (SQL)
        ↓
   Search & Indexing Layer
        ↓
   Event-Driven Distribution (conceptual)
```

---

## Technology Stack

| Layer               | Technology                   | Purpose                                      |
|---------------------|------------------------------|----------------------------------------------|
| Core Language       | Python 3.12                  | Transformation logic, API clients            |
| Data Parsing        | `lxml`, `xml.etree`          | CDA document ingestion                       |
| FHIR Modeling       | `fhir.resources`, `pydantic` | Resource validation and construction         |
| Storage             | SQLite / PostgreSQL          | Relational persistence of mapped resources   |
| Search              | OpenSearch / Elasticsearch   | Full-text and structured search on FHIR data |
| Streaming (planned) | Apache Kafka (conceptual)    | Event-driven architecture patterns           |
| Environment         | Conda                        | Reproducible dependency management           |

---

## Project Structure

```text
fhir-cda-lab/
├── 00_python_basics/          # Core utilities and data-structure helpers
├── 01_interop_parsing/        # XML/CDA parsing and ingestion scripts
├── 02_sql_store/              # Database schemas and persistence layer
├── 03_fhir_resources/         # FHIR resource creation, validation, and API interaction
├── 04_cda_to_fhir/            # Transformation engine: CDA → FHIR mapping
├── 05_search_opensearch/      # Indexing and query DSL experiments
├── 06_event_driven/           # Event streaming architecture and patterns
├── docs/                      # Architecture diagrams and technical notes
└── README.md
```

---

## Getting Started

### 1. Clone and create environment

```bash
git clone https://github.com/<your-username>/fhir-cda-lab.git
cd fhir-cda-lab

conda env create -f environment.yml
conda activate fhir-lab
```

### 2. Verify setup

```bash
python --version
# Expected: Python 3.12.x
```

### 3. Run a module

```bash
# Example: run the parsing exercise
python 00_python_basics/exercises/01_data_structures.py
```

---

## Data & Compliance Notice

All clinical data used in this repository is **synthetic, anonymized, and manually crafted for testing purposes**. No real patient data (PHI/ePHI) is ever processed or stored here. This is an educational and engineering laboratory, not a production medical system.

---

## Status

🚧 **Experimental / Work in Progress** — Components are being built and validated iteratively. The codebase is not intended for production deployment.

---

## License

Apache 2.0 License — see [LICENSE](LICENSE) for details.