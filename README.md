# Cloud Engineering & Systems Learning Journal

**A record of my BSIT studies and four-year self-study journey toward Cloud, Platform, and DevOps Engineering.**

This repository documents how I learn: study notes, practical exercises, project retrospectives, assessments, troubleshooting records, and lessons from building systems.

It is the **learning journal**, not the home for every project's source code. Standalone projects have their own repositories so their code, setup instructions, tests, and future improvements can be maintained independently.

---

## 👨‍💻 About This Journal

I'm a BSIT student developing foundations in:

- **Linux & Systems** — command-line workflows, processes, permissions, services, and troubleshooting.
- **Python & Automation** — scripts, APIs, file handling, error handling, and command-line tools.
- **Cloud Infrastructure** — AWS identity and access management, EC2, S3, and Boto3.
- **Data & Databases** — JSON, SQLite, SQL queries, and data handling.
- **Engineering Practice** — Git, documentation, testing, debugging, and learning from mistakes.

My goal is to build strong fundamentals and graduate with practical projects and the ability to explain, troubleshoot, and improve the systems I build.


## 🚀 Standalone Projects

The repositories below contain the source code, setup instructions, tests, and documentation for each project.

### 1. 🌦️ Weather Logger — Automated Data Pipeline

[![Weather Logger CI](https://github.com/junnybonz-dotcom/weather-logger-capstone/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/weather-logger-capstone/actions/workflows/tests.yml)

[**View Repository →**](https://github.com/junnybonz-dotcom/weather-logger-capstone)

A Python weather data pipeline deployed on an Ubuntu AWS EC2 instance. It retrieves current temperature and wind-speed data from the Open-Meteo API, validates the response, stores timestamped readings in SQLite, and runs automatically every 15 minutes through Linux cron.

**Demonstrates:**
- Python and REST API integration
- HTTP error handling and JSON validation
- SQLite database operations and parameterized SQL
- Linux administration and cron scheduling
- Automated testing and GitHub Actions CI

### 2. ☁️ AWS Inventory Report — Boto3

[![AWS Inventory Report CI](https://github.com/junnybonz-dotcom/aws-inventory-report/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/aws-inventory-report/actions/workflows/tests.yml)

[**View Repository →**](https://github.com/junnybonz-dotcom/aws-inventory-report)

A read-only Python command-line tool built with Boto3 to inventory Amazon S3 buckets and EC2 instances. It verifies the active AWS identity through STS, uses shared region configuration, handles paginated API responses, and provides actionable AWS error messages.

**Demonstrates:**
- Python automation with Boto3
- AWS S3, EC2, STS, and IAM concepts
- AWS authentication and region configuration
- Pagination and exception handling
- Offline unit testing with mocked AWS clients
- GitHub Actions CI

### 3. 🖥️ Log Scanner — Python CLI Tool

[![Log Scanner CI](https://github.com/junnybonz-dotcom/log-scanner-capstone/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/log-scanner-capstone/actions/workflows/tests.yml)

[**View Repository →**](https://github.com/junnybonz-dotcom/log-scanner-capstone)

A Python command-line utility that recursively inventories files and summarizes matching lines in `.log` files. It supports configurable text searches, regular expressions, case-sensitive and case-insensitive matching, file metadata, and human-readable file sizes.

**Demonstrates:**
- Python CLI development with argparse
- Filesystem traversal and file metadata
- Text processing and regular expressions
- Exception handling and exit codes
- Automated testing with temporary files
- GitHub Actions CI

### 4. 🔗 API Logger — GitHub Repository Statistics

[![API Logger CI](https://github.com/junnybonz-dotcom/api-logger/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/api-logger/actions/workflows/tests.yml)

[**View Repository →**](https://github.com/junnybonz-dotcom/api-logger)

A Python command-line application that retrieves public GitHub repository statistics through the GitHub REST API and appends timestamped records to a JSON Lines file. It supports configurable repositories, output paths, and request timeouts, with response validation and structured error handling.

**Demonstrates:**
- Python REST API integration
- HTTP requests and response validation
- JSON serialization and JSONL file handling
- UTC timestamps and command-line arguments
- Dependency injection and mocked API testing
- GitHub Actions CI

---

## 📚 Learning Records

These files document the work behind the projects and the wider study roadmap.

### Monthly study logs

- [July 2026](monthly2026-logs/2026-07-july.md)
- [August 2026](monthly2026-logs/2026-08-august.md)
- [September 2026](monthly2026-logs/2026-09-september.md)
- [October 2026](monthly2026-logs/2026-10-october.md)

### November study records

- [November 2026 Weekly Study Log](WEEKLY-LOG.md)
- [November Baseline Assessment](assessments/baseline.md)
- [Linux Command Practice Cheat Sheet](notes/linux-task-cheatsheet.md)
- [Errors and Troubleshooting Journal](ERRORS.md)

### Project rebuild and reflection

The Weather Logger's earlier implementation and guided rebuild are preserved as learning records:

- [Original implementation snapshot](capstone/original/)
- [October guided rebuild](capstone/redo-oct21/)
- [Rebuild gap report](capstone/redo-oct21/GAPS.md)
- [Rebuild documentation](capstone/redo-oct21/README.md)
- [Original-versus-rebuild comparison](capstone/redo-oct21/COMPARISON.patch)

The rebuild notes distinguish what I could recall, where I needed guidance, and what I still need to practice independently.

## 🗂️ Repository Organization

| Location | Purpose |
|---|---|
| `monthly2026-logs/` | Monthly study history |
| `WEEKLY-LOG.md` | Current weekly study record |
| `assessments/` | Baseline and future assessment records |
| `notes/` | Technical reference notes and task cheat sheets |
| `ERRORS.md` | Troubleshooting and lessons learned |
| `capstone/` | Historical project snapshots and guided rebuild records |
| `boto3-inventory/` | Migration notice pointing to the standalone AWS Inventory Report repository |

### Why projects have separate repositories

The journal preserves the learning process and history. Each standalone project repository is the source of truth for that project's code, requirements, usage instructions, tests, and future development.

The AWS Inventory Report was moved out of this journal into its own repository:

➡️ [Open the standalone AWS Inventory Report](https://github.com/junnybonz-dotcom/aws-inventory-report)

The old `boto3-inventory/` directory is retained only as a migration pointer; it is not a second copy of the project source code.

## 🧰 Technologies I'm Practicing

**Languages:** Python, SQL, Bash

**Cloud:** AWS EC2, S3, IAM, STS, Boto3

**Systems:** Linux, Ubuntu, Windows

**Data:** SQLite, JSON, REST APIs

**Tools:** Git, GitHub, VS Code

These reflect my current learning and hands-on project experience, not professional certifications or mastery of every tool.

## 🎯 Direction

I'm working toward a career in cloud, platform, or DevOps engineering. My focus is to strengthen the fundamentals, build useful projects, document problems honestly, and become more independent at designing, troubleshooting, and explaining technical solutions.

---

*Learn the fundamentals. Build real things. Understand what breaks. Improve.*
