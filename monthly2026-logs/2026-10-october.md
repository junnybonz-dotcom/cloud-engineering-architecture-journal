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

# Everday Stuff like documentation on everything tbh 

## October 1 (Day 71) Storage fundamentals — what "storage" means at the infrastructure level, object vs block storage defined side by side (how each is addressed, mutability, typical size). +15 min: what "time complexity" even measures, O(1) vs O(n) as concepts.

**Definition:**

**Cloud storage — what "storage" means at the infrastructure level**

* At the infrastructure level, "storage" is just: where do bytes physically live, and what's the *interface* for reading/writing them. Different interfaces suit different problems — that's the whole reason object and block storage both exist instead of one universal type.

**Object storage**

* Stores data as discrete, whole **objects** (a file, a blob), each with a unique key/identifier, inside a **bucket** (a flat container — no real folder hierarchy, even though consoles fake one with `/` in key names).
* **Addressed by key**, over HTTP — you ask for bucket/path/to/file.jpg and get the whole object back. There's no "open this file and edit byte 400" — you replace the *entire* object to change it.
* **Immutable in practice:** an update is really "upload a new object with the same key," not an in-place edit.
* Typical size: anywhere from a few KB to many GB/TB per object — scales to enormous volumes (petabytes) with no practical ceiling. AWS S3, Azure Blob Storage, GCP Cloud Storage.

**Block storage**

* Stores data as fixed-size **blocks**, each with a raw numeric address, attached to a machine like a regular hard disk.
* **Addressed by block number**, at a much lower level than object storage — the OS puts a filesystem (ext4, NTFS) on top, and *that's* what gives you folders/files. The storage layer itself has no concept of "files."
* **Mutable** — you can modify a tiny piece in place (change block #4821) without touching anything else, exactly like editing a few bytes in the middle of a file on your laptop's disk.
* Typical size: provisioned in GB/TB chunks, attached to one VM at a time (usually) — AWS EBS, Azure Managed Disks, GCP Persistent Disks.

**Side by side**

|	Object storage	Block storage
Addressed by	key (string)	block number
Unit	whole object	fixed-size block
Mutability	replace the whole object	edit in place
Access	HTTP API	attached like a disk, needs a filesystem
Good for	backups, images, logs, static files, huge archives	a VM's root disk, databases needing fast random read/write |

**Big-O intuition — what "time complexity" measures**

* Time complexity isn't a stopwatch measurement — it's a description of **how the number of operations grows as the input grows**, independent of hardware speed.
* `O(1)` ("constant time") — the number of operations stays the same no matter how big the input is.
* `O(n)` ("linear time") — the number of operations grows directly proportional to the input size `n`. Double the input, roughly double the work.
* The "O" is shorthand for "order of" — it describes the *shape* of the growth curve, not an exact count.

