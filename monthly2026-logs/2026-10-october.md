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

**Worked examples:**
**Object vs. block, concretely**

Object storage (e.g. S3):
  PUT /my-bucket/photos/vacation.jpg   <- upload the whole file
  GET /my-bucket/photos/vacation.jpg   <- download the whole file
  ` to "edit" it: upload a new version under the same key, replacing it entirely`

Block storage (e.g. an EBS volume attached to your Day 55 VM):
  /dev/xvdf   <- the raw block device
  mkfs.ext4 /dev/xvdf   <- format it with a filesystem
  mount /dev/xvdf /data
  ` now it behaves like any normal disk — echo "x" >> /data/log.txt`
  ` appends ONE line, without rewriting the whole file`

**Picking one for a real scenario**

Storing user-uploaded profile pictures for a web app:
  → Object storage. Each picture is a discrete file, read far more often
    than written, and doesn't need in-place byte-level edits.

Storing the actual database files for your Day 65 weather_log:
  → Block storage. A database constantly modifies small pieces of its
    files (a single row update), and needs fast, low-latency random access —
    exactly what block storage is built for.

**Big-O — a hashmap lookup vs. a linear scan**

`python`
` O(n) — linear scan: has to check hostnames one by one, worst case ALL of them`
hostnames = ["web-01", "web-02", "db-primary", "db-replica", "cache-01"]

def find_linear(target):
    for host in hostnames:          ` Day 3's for loop`
        if host == target:
            return True
    return False
` 5 hostnames → up to 5 checks. 5 million hostnames → up to 5 million checks.`
`python`
` O(1) — hashmap (dict) lookup: computes where to look directly, doesn't scan`
hostnames_set = {"web-01", "web-02", "db-primary", "db-replica", "cache-01"}

def find_constant(target):
    return target in hostnames_set   ` Day 6's dict, used as a lookup table`
` 5 entries or 5 million entries — roughly the same number of operations either way`
`Why: a list is checked one item at a time (Day 3's for loop, literally).`
`A dict/set computes a hash of the key and jumps straight to where it`
`would be stored — it doesn't need to look at the other items at all.`

**Real-world use: Nearly every cloud architecture decision in Week 1 comes down to this one question first: "is this data a whole discrete thing I read/write as a unit, or do I need fast in-place edits to small pieces of it?" Logs, backups, user uploads, and your Day 70 capstone's README/screenshots are object-storage shaped. A database's underlying files, or a VM's own root filesystem, are block-storage shaped — which is exactly why your Day 55 VM has a block storage volume as its root disk, even though it's writing weather.db (itself just a file on that block device).                                                                                      Big-O intuition is what separates "this script works on my 100-row test table" from "this script still works when the table has 10 million rows" — a hidden O(n) scan inside a loop that itself runs n times becomes O(n²), which is the single most common reason code that was fast in testing becomes painfully slow in production. Recognizing "I'm checking membership in a list repeatedly" as a signal to reach for a set/dict instead is one of the highest-value habits in writing code that scales.**

## October 2 (Day 72) Object storage deep dive — buckets/keys, why it's built for static assets, backups, media; durability/scalability tradeoffs. +15 min: why a linear scan through a list is O(n) — walk through it mentally with a growing list.

**Definition:**

**Buckets & keys, more precisely**

* A **bucket** is the top-level container — globally unique name (on AWS S3, bucket names are unique across *all* AWS accounts, not just yours). Everything you store goes inside one.
* A **key** is the full string identifying an object inside a bucket — `photos/2026/vacation.jpg`. The `/` characters *look* like folders in the console, but the bucket is actually flat — there's no real directory structure underneath, just keys that happen to contain slashes.
* An object = key + the data itself + metadata (content type, size, last-modified, custom tags you set).

**Why it's built for static assets, backups, media**

* These workloads share a pattern: **write once (or rarely), read many times, whole-object access**. You don't need to tweak byte 4000 of a photo — you fetch the whole thing or you don't.
* Object storage trades away fine-grained in-place editing (block storage's strength) for massive horizontal scale and simplicity — exactly the right trade for files that are read far more than they're modified.

**Durability vs. availability — the tradeoff distinction that matters**

* **Durability** — the probability your data *still exists*, unharmed, over time. Commonly advertised as "11 nines" (99.999999999%) — meaning the odds of losing a given object in a year are vanishingly small. Achieved by automatically replicating every object across multiple physically separate data centers (often multiple AZs from Day 53).
* **Availability** — the probability you can successfully access it right now. Typically "only" 99.9%–99.99% — because a network blip or a brief service issue can make data temporarily unreachable even though it's perfectly intact.
* These are different numbers on purpose: your data can be 100% safe and still occasionally fail to answer a request for a few seconds.

**Scalability tradeoff**

* Object storage scales near-infinitely with no capacity planning on your part — you don't provision "how much storage" up front like you would with a block volume. The tradeoff: higher latency per request (it's an HTTP call, not a raw disk read) and no partial-file edits — both direct consequences of the same design that makes it scale so well.

**Worked examples**

**Keys that look like folders, but aren't**

Bucket: my-app-assets

Keys:
  photos/2026/vacation.jpg
  photos/2026/beach.jpg
  backups/weather-db/2026-10-01.sql

` Listing "photos/2026/" in the console LOOKS like browsing a folder,`
` but under the hood this is really:`
`   "give me every key that STARTS WITH the string 'photos/2026/'"`
` — a prefix search, not a real directory traversal.`

**A backup workflow — the exact shape Day 70's capstone could grow into**

`bash`
` on your VM, dump the weather.db and upload it as an objec`
sqlite3 weather.db ".backup weather_backup_$(date +%Y%m%d).db"

` conceptually (AWS CLI, once configured):`
aws s3 cp weather_backup_20261002.db s3://my-weather-backups/

` now the backup is durable across multiple data centers,`
` independent of whether the VM itself survives`

**Durability math, made concrete**

11 nines (99.999999999%) durability on 10,000,000 stored objects:
  → expected loss: roughly 1 object every 10,000 years

Compare: a single disk on your laptop has no such guarantee —
  a drive failure can lose everything on it at once, with no
  automatic replication happening behind the scenes.

**Why a linear scan is O(n) — walking through it mentally**

`python`
hostnames = ["web-01"]
` find "web-01": 1 check`

hostnames = ["web-01", "web-02", "web-03"]
` find "web-03": up to 3 checks`

hostnames = ["web-01", "web-02", ..., "web-100"]
` find "web-100": up to 100 checks`

hostnames = [... 1,000,000 items ...]
` find the last one: up to 1,000,000 checks`
`python`
def find_linear(hostnames, target):
    checks = 0
    for host in hostnames:
        checks += 1
        if host == target:
            return checks
    return checks

print(find_linear(["a","b","c","d","e"], "e"))
` 5 — had to check every single one, worst case`

`The list length and the worst-case check count grow in lockstep, one-to-one — that direct proportionality is exactly what O(n) means. Nothing about the code changes as the list grows; only the number of times the loop body runs does.`
