
<div align="center">

# ☁️ Cloud & Systems Engineering

### Building. Automating. Learning by Doing.

I'm a BSIT student building hands-on projects in **Linux, Python, AWS, and cloud automation**.

I document not just what works, but also the problems I encounter, how I troubleshoot them, and what I learn along the way.

<br>

<a href="https://github.com/junnybonz-dotcom">
  <img src="https://img.shields.io/badge/GitHub-View%20My%20Work-181717?style=for-the-badge&logo=github" alt="GitHub">
</a>
<img src="https://img.shields.io/badge/Focus-Cloud%20%26%20Platform%20Engineering-2563eb?style=for-the-badge" alt="Cloud and Platform Engineering">
<img src="https://img.shields.io/badge/Approach-Hands--On%20Learning-15803d?style=for-the-badge" alt="Hands-on learning">

</div>

---

## 👨‍💻 About Me

I'm developing my foundations in cloud and systems engineering through practical projects rather than studying tools in isolation.

My current work focuses on:

- **Linux & Automation** — command-line tools, Python scripts, and cron jobs.
- **Cloud Infrastructure** — AWS EC2, IAM permissions, and AWS service integrations.
- **Data & Monitoring** — APIs, JSON, SQLite, SQL queries, and log analysis.
- **Engineering Habits** — troubleshooting, documenting failures, and making projects reproducible.

My long-term goal is to grow toward a career in **cloud, platform, or DevOps engineering**.

## 🚀 Featured Project

### 🌦️ Weather Logger — Automated Data Pipeline

An AWS-hosted Python application that collects live weather data from the Open-Meteo API, stores timestamped readings in SQLite, and runs automatically using Linux cron.

**The pipeline**

`Open-Meteo API` → `Python` → `SQLite` → `Cron Automation`

**What I built**
- Fetches temperature and wind-speed data from a public API.
- Stores readings in a structured SQLite database.
- Handles API and database failures with specific exceptions.
- Runs on an Ubuntu EC2 instance using a scheduled job.
- Uses SQL queries to summarize readings and calculate hourly averages.

**Technologies:** Python · AWS EC2 · Linux · Requests · SQLite · SQL · Cron

[**Explore the Weather Logger repository →**](https://github.com/junnybonz-dotcom/weather-logger-capstone)

[View the rebuild and gap analysis →](https://github.com/junnybonz-dotcom/weather-logger-capstone/tree/main/capstone/redo-oct21)

---

## 🛠️ Project Showcase

### 01 / Log Scanner

**Python · Bash · Filesystem Operations**

A command-line tool that recursively inventories files and summarizes matching error lines in log files.

What it demonstrates:
- File traversal and metadata collection.
- Text matching and log summaries.
- Command-line arguments and basic exception handling.

[**View project and documentation →**](https://github.com/junnybonz-dotcom/log-scanner-capstone)

---

### 02 / AWS Inventory Report

**Python · Boto3 · S3 · EC2 · STS**

A read-only reporting script that retrieves S3 bucket information and EC2 instance details, identifies the AWS caller, and reports service errors.

What it demonstrates:
- AWS SDK integration.
- EC2 pagination and inventory reporting.
- Credential and permission troubleshooting.
- Read-only access and IAM security practices.

[**Read the Boto3 project documentation →**](boto3-inventory/README.md)

> Note: The source scripts currently reside in my AWS VM workspace and have not yet been packaged into this journal repository.

---

### 03 / Weather Logger — Guided Rebuild

**Python · SQLite · Error Handling · Git**

A separate rebuild of the Weather Logger, accompanied by a comparison file and an honest record of what required assistance.

The goal was to identify the difference between recognizing code and being able to recreate and explain it independently.

[**Explore the rebuild and gap report →**](https://github.com/junnybonz-dotcom/weather-logger-capstone/tree/main/capstone/redo-oct21)

---

### 04 / API Logger

**Python · Requests · JSON · Cron**

A mini-project that retrieves public GitHub repository statistics and records timestamped results.

[**View API Logger repository →**](https://github.com/junnybonz-dotcom/api-logger)

---

## 🧰 Technologies I'm Practicing

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux">
<img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white" alt="AWS">
<img src="https://img.shields.io/badge/Bash-121011?style=flat-square&logo=gnubash&logoColor=white" alt="Bash">
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">

</div>

These technologies reflect my current learning and project experience, not professional certifications or mastery of every tool.

## 📚 Learning Journal

My journal documents the exercises, troubleshooting sessions, and lessons behind my projects.


- [July 2026 — Study Log](monthly2026-logs/2026-07-july.md)
- [August 2026 — Study Log](monthly2026-logs/2026-08-august.md)
- [September 2026 — Study Log](monthly2026-logs/2026-09-september.md)
- [October 2026 — Study Log](monthly2026-logs/2026-10-october.md)

## 🎯 What I'm Working Toward

My goal is to graduate with more than theoretical knowledge: practical projects, better Linux and Python fundamentals, AWS experience, and the ability to investigate and explain technical problems independently.

I'm documenting the journey as I build toward that goal, one project at a time.

---

<div align="center">

*Learn the fundamentals. Build real things. Understand what breaks. Improve.*

</div>
