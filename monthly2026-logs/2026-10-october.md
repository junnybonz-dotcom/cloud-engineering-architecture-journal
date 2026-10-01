# 📅 October 2026 — Cloud Architecture, SDK Automation & Semester Capstone Audit

## 🚀 Weekly Breakdown & Key Highlights

### Week 1 (Oct 1–7): Cloud Architecture & Big-O Intuition
* **Storage Paradigms:** Object Storage (S3) vs. Block Storage (EBS) and key usage criteria.
* **System Design:** Sketched a 3-tier cloud architecture blueprint (Web tier, Application tier, Database tier).
* **Data Structures & Algorithms:** Time/Space complexity fundamentals ($O(1)$ vs $O(N)$), evaluating why Hashmaps outpace linear array scans.

### Week 2 (Oct 8–14): Infrastructure Automation (`boto3`) & Cloud Security
* **AWS SDK Automation:** Programmatic resource discovery using `boto3` for S3 bucket enumeration (`list_buckets`) and EC2 instance state monitoring (`describe_instances`).
* **IAM & Least Privilege:** Hand-crafted scoped JSON IAM policies to replace over-privileged root credentials.
* **Shared Responsibility & Encryption:** Implemented client-side error handling for credentials and evaluated Encryption at Rest (S3 SSE, EBS) vs. Encryption in Transit (TLS/HTTPS).

### Week 3 (Oct 15–21): Cold Technical Audit & Capstone Re-execution
* **Self-Audit:** Rated confidence (1–5 scale) across all core topics since June (Linux CLI, Permissions, SQL JOINs, Python, boto3).
* **Targeted Weak-Spot Rebuilding:** Re-studied low-confidence areas from scratch and applied them in new, unscripted contexts.
* **Cold Capstone Redo:** Rebuilt the cloud VM API-to-SQLite pipeline completely from memory without referencing original repos; performed a diff analysis against the original codebase to isolate gaps.

### Week 4 (Oct 22–31): Academic Semester Wrap & Portfolio Polish
* **College Finals Execution:** Prioritized academic coursework and final examinations.
* **Repository & Portfolio Audit:** Standardized `README.md` files across all capstones for public demonstration.
* **Semester Close Snapshot:** Conducted final Git commits/pushes across repositories and documented the semester-long learning arc.

---

## 💡 In My Own Words

* **3-Tier Architecture separates concerns:** Keep web servers facing the user, app logic hidden behind private networking, and database tables isolated at the bottom.
* **SDK Automation turns manual work into code:** Running `boto3.client('s3').list_buckets()` allows me to programatically manage infrastructure without clicking through web consoles.
* **Least Privilege keeps cloud accounts safe:** Never run production automation with full Admin rights; scope IAM policies strictly to the specific actions and resources required.
* **Memory Diffing isolates true weaknesses:** Guessing what you know on paper is unreliable—rebuilding a project cold from memory and diffing it against original code reveals exact technical blind spots.

---

## 🛠️ How I Solved Problems (My Debugging Process)

* **AWS Access Denied Errors:** `boto3` calls threw authentication exceptions. Solved by configuring AWS credentials in `~/.aws/credentials` and swapping root keys with a scoped, read-only IAM policy.
* **Memory Redo Blocks:** Got stuck during the cold Capstone rebuild while wiring Python's `sqlite3` to `requests`. Solved by stepping back to map out the data pipeline schema on paper before writing code.
* **Handling Expired SDK Tokens:** Handled API failures by wrapping `boto3` connection blocks in `try/except ClientError` traps to log missing or invalid credentials cleanly.