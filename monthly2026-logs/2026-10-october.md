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

**REAL-WORLD USE: Almost every real backup strategy — database dumps, config snapshots, log archives — ends up in object storage specifically because of the durability/availability split: you want the data to survive catastrophically (11 nines), while tolerating the occasional brief unavailability, since backups aren't usually read under time pressure. Static assets for a website (images, CSS, downloadable files) live here for the same reason — read constantly, written rarely, no need for in-place edits, and the near-infinite scale means you never think about running out of space the way you would provisioning a block volume.                                                                                       Recognizing O(n) by eye — "this loop's work count depends directly on the input size" — is the single most common thing to spot in your own code before it becomes a real performance problem, especially the moment an O(n) scan ends up nested inside another loop, which is tomorrow's natural next question.**

## October 3 (Day 73) Block storage deep dive — how it attaches to a VM like a hard drive, why databases/OS volumes want it, IOPS and low-latency reads/writes. +15 min: hashmap intuition — why lookup by key skips the scan entirely, O(1) on average.

**Definition**

**How block storage attaches to a VM**

* A block volume (AWS EBS, Azure Managed Disk, GCP Persistent Disk) is provisioned separately from the VM, then **attached** to it over the provider's internal network — appearing to the OS as a raw device, like `/dev/xvdf` or `/dev/sdb`.
* The OS doesn't understand "files" at this layer — you format it with a filesystem (`mkfs.ext4`, from Day 72's mention) and `mount` it before it behaves like a normal disk with folders and files.
* It's **detachable and reattachable** — you can unmount a volume from one VM and attach it to another, carrying its data with it, something object storage doesn't need (since it's never "attached" to anything — it's accessed over HTTP, not mounted).
* A VM's **root volume** (where the OS itself lives) is almost always block storage — this is literally what your Day 55 Ubuntu instance has been running on since launch, even though you never had to think about it.

**Why databases and OS volumes specifically want this**

* A database constantly does small, random reads/writes — update one row, read one index entry, append one log line — scattered across the file, not sequentially. Block storage is built for exactly this: address block #48213 directly, read/write just that piece, done.
* An OS volume needs the same thing — modifying one config file, writing one log line, updating one package — all small, in-place, frequent operations.
* Contrast with object storage: there, "modifying one row" would mean re-uploading an entire multi-GB database file for a one-row change — completely impractical.

**IOPS and latency**

* **IOPS** (Input/Output Operations Per Second) — how many individual read/write operations a volume can handle per second. This is the number that matters for databases, not raw throughput (MB/s) — a database does *many small* operations, not a few huge ones.
* **Latency** — how long a single operation takes to complete. Block storage is attached over a low-latency internal connection (sometimes physically local to the VM), versus object storage's HTTP round-trip, which is inherently slower per-request even though it scales better in aggregate.
* Provider tiers let you provision IOPS directly (e.g. AWS `io2` volumes) when a workload — like a busy database — needs guaranteed, consistent low-latency performance rather than best-effort.

**Hashmap intuition — why lookup by key skips the scan**

* A dict doesn't search for your key — it **computes** where the value should be. `hash(key)` turns the key into a number, and that number maps (roughly) directly to a storage slot.
* Compare to yesterday's linear scan, which checks items one at a time until it finds a match — a hashmap instead jumps straight to roughly the right spot, checks it, and is usually done. No matter how many other keys are in the dict, that computation takes the same amount of work.
* **"On average"** matters: in rare cases two different keys hash to the same slot (a **collision**), requiring a little extra work to resolve — so O(1) here is an average/typical case, not an absolute guarantee like it would be for, say, accessing a fixed array index.

**Worked examples**

**Attaching a block volume (conceptual — AWS naming)**

`bash`
` after creating and attaching an EBS volume via the console to your VM:`
lsblk
` NAME    SIZE`
` xvda    8G    <- root volume, already mounted`
` xvdf    10G   <- new volume, attached but not yet usable`

sudo mkfs.ext4 /dev/xvdf
sudo mkdir /data
sudo mount /dev/xvdf /data

df -h /data
` Filesystem  Size  Used Avail Use% Mounted on`
` /dev/xvdf    10G   24K  9.5G   1% /data`
`bash`
` now it behaves exactly like any other disk — Day 1-8 commands, unchanged`
touch /data/test.txt
echo "hello" >> /data/test.txt
cat /data/test.txt
` hello`

**Why this matters for your Day 65 weather.db, concretely**

weather.db sits on the VM's root block volume right now.` `Every INSERT
is a small, random write to a specific part of that file — exactly
the access pattern block storage is built for.` `If weather.db were
somehow stored in S3 instead, every single row insert would require
re-uploading the entire database file — the pipeline from Week 4
simply wouldn't work that way.`

**Hashmap intuition, step by step**

`python`
hostnames = {"web-01": "10.0.0.1", "web-02": "10.0.0.2", "db-primary": "10.0.0.3"}

` what Python roughly does internally when you look something up:`
key = "db-primary"
slot = hash(key) % 8   ` conceptually — real dicts resize/rehash, this is simplified`
` jumps directly to that slot, checks it, done`

print(hostnames["db-primary"])
` 10.0.0.3`
` no scanning through "web-01" and "web-02" first — straight to the answer`
`python`
import time

big_dict = {i: str(i) for i in range(1_000_000)}

start = time.time()
999_999 in big_dict
print(f"1M entries: {time.time() - start:.8f}s")

small_dict = {i: str(i) for i in range(100)}
start = time.time()
99 in small_dict
print(f"100 entries: {time.time() - start:.8f}s")
` both roughly the same tiny number — size barely matters, unlike yesterday's list scan`

**Real-world use: Every cloud database service — a managed Postgres/MySQL instance, your own self-hosted database on a VM — ultimately sits on provisioned block storage, and IOPS is one of the first numbers a real production database gets sized against, because an underpowered volume (too few IOPS) becomes the bottleneck long before CPU or RAM does, especially under heavy write load. This is also exactly why "lift your database onto object storage to save money" is a design mistake you'll see proposed by people who haven't internalized this week's distinction — the access pattern, not just the price per GB, determines which one actually works.                                                                                     The hashmap/O(1) lookup is one of the most consequential small decisions in everyday code — anywhere you find yourself writing "is X in this list?" repeatedly inside a loop, switching that list to a set or dict is often the single highest-leverage performance fix available, turning an accidental O(n²) script into something that stays fast as data grows.**

## October 4 (Day 74) Decision framework — given an app's needs (random access + speed vs scale + HTTP access), which storage type fits and why. +15 min: side-by-side — searching a Python list vs a dict for the same value, why the dict wins as data grows.

**Definition**

**The decision framework**

Three questions, asked in order, settle most storage choices:

1. **Does this data need random, in-place edits to small pieces of it — or do you always read/write it as a whole unit?**
 → Small in-place edits: **block storage.** Always-whole: **object storage.**
2. **Does it need to be attached to one specific machine, or accessed from anywhere over HTTP?**
 → Attached to a machine: **block.** Accessed broadly, possibly by many services/users at once: **object.**
3. **Does raw speed/low-latency matter more than near-infinite scale — or the reverse?**
 → Speed-critical, bounded size (a database, an OS volume): **block.** Scale-critical, less latency-sensitive (backups, media, logs, archives): **object.**

`If the answers conflict (rare, but possible — e.g. "I need both speed AND huge scale"), that's usually a sign the real answer is "use both": block storage for the active working set, object storage for everything older/archived — exactly the backup pattern from Day 72.`

**A compact way to hold this**

          Random, small edits          Whole-object, HTTP access
Speed-    BLOCK STORAGE                 —
critical  (database, OS volume)

Scale-    —                             OBJECT STORAGE
critical                                (backups, media, logs, archives)

**List vs. dict — why the dict wins as data grows**

* A list search (`in`, or a manual loop) is `O(n)` — Day 72's linear scan, checking items one at a time.
* A dict lookup (`in`, `.get()`, `[key]`) is `O(1)` on average — Day 73's hash-based jump straight to the slot.
* The gap doesn't matter at small `n` (10 items: both are instant to a human). It becomes the entire story at large `n` — this is the actual lesson of Big-O: not "which is faster right now," but "which one's cost grows."

**Worked examples**

**Applying the framework to real scenarios**

Scenario 1: Your Day 70 weather.db itself
  Q1: small in-place edits (one INSERT per cron run)?  → yes → BLOCK
  Q2: attached to one VM?                               → yes → BLOCK
  Q3: speed-critical, bounded size?                     → yes → BLOCK
  → Confirms Day 73's conclusion: block storage, correctly.

Scenario 2: A nightly backup of weather.db (Day 72's pattern)
  Q1: edited in place, or written once and left alone?  → write once → OBJECT
  Q2: needs to survive even if the VM is destroyed?     → yes → OBJECT
  Q3: scale/durability over raw speed?                  → durability matters more → OBJECT
  → Block storage for the live database, object storage for its backups —
    same data, two different storage types, at two different points in its life.

Scenario 3: A video-streaming app's actual video files
  Q1: edited in place?                                  → no, read-only once uploaded → OBJECT
  Q2: accessed by many users over HTTP, globally?        → yes → OBJECT
  Q3: scale (petabytes of video) over per-request speed? → scale wins → OBJECT

Scenario 4: That same app's user session/login database
  Q1: constant small reads/writes (login checks)?        → yes → BLOCK
  Q2: attached to the app server?                        → yes → BLOCK
  Q3: low-latency matters (users waiting on a response)?  → yes → BLOCK

**List vs. dict, side by side, same lookup, growing n**

`python`
import time

def time_list_search(n):
    data = list(range(n))
    target = -1  ` worst case: not present, scans everything`
    start = time.time()
    target in data
    return time.time() - start

def time_dict_search(n):
    data = {i: True for i in range(n)}
    target = -1
    start = time.time()
    target in data
    return time.time() - start

for n in [1_000, 10_000, 100_000, 1_000_000]:
    list_time = time_list_search(n)
    dict_time = time_dict_search(n)
    print(f"n={n:>9}: list={list_time:.6f}s  dict={dict_time:.8f}s")
n=     1000: list=0.000041s  dict=0.00000012s
n=    10000: list=0.000398s  dict=0.00000013s
n=   100000: list=0.004012s  dict=0.00000011s
n=  1000000: list=0.041233s  dict=0.00000013s

The list's time grows roughly 10x each time `n` grows 10x — straight-line proportional, the signature of `O(n)`. The dict's time barely moves at all — the signature of `O(1)`.

**The same pattern, applied to something from your own capstone**

`python`
` a membership check buried in a loop — the classic accidental O(n²)`
known_hosts = ["web-01", "web-02", "db-primary", ...]  ` grows over time`

for reading in weather_readings:          ` O(n)`
    if reading["source"] in known_hosts:  ` O(n) AGAIN, nested inside the first loop`
        process(reading)
` total: O(n * m) — slows down fast as BOTH lists grow`

known_hosts_set = set(known_hosts)        ` one-time O(n) conversion`
for reading in weather_readings:          ` O(n)`
    if reading["source"] in known_hosts_set:  ` O(1) — doesn't add a second dimension`
        process(reading)
` total: O(n) — the set conversion paid for itself immediately`

**Real-world use: This three-question framework is genuinely how real architecture decisions get made day to day — not from memorizing a list of which AWS service to use where, but from reasoning backward from the access pattern the data actually has. Interviewers and real system-design conversations care far more about why you'd pick one over the other for a given workload than whether you can recite service names, which is exactly what today practiced.                                                                                     The list-vs-dict gap is one of the most common real-world performance bugs in production code — a lookup that was fine in testing with 50 rows and becomes the entire bottleneck once a table has 500,000, purely because nobody swapped a list for a set when the data outgrew what a human would ever notice by eye.**

## October 5 (Day 75) 3-tier architecture basics — web/app/db tiers explained, why they're separated (scalability, security, independent scaling). +15 min: space complexity — what "extra memory" a hashmap costs you for that speed.

**Definition**

**3-tier architecture**

* **Web tier** — handles incoming HTTP requests, serves static content, often the first thing a user's request hits (a load balancer + web servers, or a reverse proxy like the nginx you set up Day 58).
* **App tier** — runs your actual application logic: processes requests, applies business rules, talks to the database, returns a response to the web tier.
* **Data tier** — the database itself: stores and retrieves persistent data, nothing else. No business logic lives here.
* Each tier only talks to the tier directly next to it — web talks to app, app talks to data. The web tier never touches the database directly, and the database never talks to the web tier.

**Why they're separated**

* **Scalability** — tiers often need to scale at different rates. A sudden traffic spike might need 10x more web servers, while the database stays exactly the same size — separating them means you scale *only* the tier under load, instead of duplicating everything together.
* **Security** — the data tier can sit on a private network, completely unreachable from the internet (recall Day 59's security group: SSH scoped to your IP, HTTP open to everyone — a database tier would get *no* public inbound rule at all, only "allow connections from the app tier"). A compromised web server then can't reach the database directly, even if an attacker gets in.
* **Independent scaling/deployment** — you can redeploy app-tier code without touching the database, patch the database without redeploying app code, and swap technologies within one tier (change web servers, change the app framework) without rewriting the others, as long as the interfaces between tiers stay the same.

**Space complexity — the other half of Big-O**

* Time complexity (`O(1)`, `O(n)`) measures *operations*. **Space complexity** measures *extra memory used*, as a function of input size `n`.
* A hashmap's `O(1)` lookup speed isn't free — it costs `O(n)` space: the dict has to actually store every key somewhere, plus some empty "slack" slots (dicts intentionally keep extra empty capacity to keep collisions rare and lookups fast).
* Contrast: a plain list also uses `O(n)` space (has to store every item too) — but a dict typically uses *more* memory per item than a list does, because of that extra slack plus the overhead of storing hash values alongside each key.
* This is the actual tradeoff: you're trading some memory overhead for a large, often decisive, speed advantage — rarely a bad trade, but not a free one.

**Worked examples**

**A concrete 3-tier layout, mapped onto what you've already built**

Web tier:   nginx (Day 58) — could later sit behind a load balancer
                ↓
App tier:   a Python app (imagine Flask/FastAPI) handling requests,
            running business logic
                ↓
Data tier:  weather.db / a real managed database — only reachable
            from the app tier, never directly from the internet
Security groups, applied per tier (extending Day 54/59):

Web tier SG:   inbound 80/443 from 0.0.0.0/0 (public)
App tier SG:   inbound from Web tier's SG ONLY (not the internet)
Data tier SG:  inbound from App tier's SG ONLY (not even the web tier)

A request's actual path:
Internet → Web tier → App tier → Data tier
Nothing can skip a layer, by design — not even you, without reconfiguring it.

**Independent scaling, concretely**

Black Friday traffic spike on the web tier:
  → launch 5 more web servers behind a load balancer
  → app tier: unchanged (still 2 servers)
  → data tier: unchanged (still 1 database)

A slow database query under load:
  → upgrade the data tier's instance size, or add a read replica
  → web tier: unchanged
  → app tier: unchanged

**Space complexity, made concrete**

`python`
import sys

small_list = list(range(1000))
small_dict = {i: i for i in range(1000)}

print(sys.getsizeof(small_list))
` ~8056 bytes`
print(sys.getsizeof(small_dict))
` ~36960 bytes`
` same 1000 items — the dict takes noticeably more raw memory`
python
` the O(n) space cost, scaling up`
import sys

for n in [1_000, 10_000, 100_000]:
    d = {i: i for i in range(n)}
    l = list(range(n))
    print(f"n={n:>7}: list={sys.getsizeof(l):>9} bytes   dict={sys.getsizeof(d):>9} bytes")
n=   1000: list=    8056 bytes   dict=   36960 bytes
n=  10000: list=   85176 bytes   dict=  294984 bytes
n= 100000: list=  824456 bytes   dict= 3145944 bytes

`Both grow roughly linearly with n (both are O(n) space) — but the dict's constant factor is noticeably bigger. That extra memory is the literal price of the O(1) lookup speed from Days 73–74.`

**Real-world use: The 3-tier model is the default shape of essentially every real web application you'll ever work on — even "serverless" architectures are usually this same pattern with managed services standing in for each tier. The security argument specifically is what real breach postmortems come back to again and again: a database that's only reachable from the app tier's security group, never from the internet, survives far more attack scenarios than one that's technically "password protected" but still publicly reachable.                                                                                   Space complexity matters most when memory is genuinely constrained — an embedded device, a process handling millions of records at once, a serverless function with a hard memory limit — where O(n) space with a large constant factor (like a dict) can be the thing that actually breaks, even when the time complexity is perfect. In most everyday backend work the speed win dominates and the memory cost is a non-issue, but knowing the tradeoff exists is what lets you reason about it the one time it actually matters.**

## October 6 (Day 76)  Sketch your own 3-tier architecture for a simple app idea — pick something concrete (to-do app, blog), map web tier → app tier → db tier, and decide where object storage (uploads) vs block storage (the database itself) fits in the diagram.

**Definition**

Today has no new concept — it's applying Days 71–75 as one synthesis exercise. The checklist to work through while sketching:

1. **Draw the three tiers** — web, app, data — as boxes, with arrows showing the one-directional flow: `Internet → Web → App → Data`. No arrow should skip a tier.
2. **For each tier, name what actually runs there** — a web server, your app's backend code, a database engine.
3. **For every distinct piece of data your app produces, run Day 74's three-question framework** — small in-place edits vs. whole-object, attached-to-a-machine vs. HTTP-accessed, speed-critical vs. scale-critical — and place it as either block or object storage *on the diagram itself*, not as an afterthought.
4. **Scope security per tier** (Day 75) — note in one line per tier what's allowed to talk to it, and from where.

**Worked example (a different app, so yours stays your own — a recipe-sharing app)**
                     ┌─────────────────────────┐
  Internet  ──────▶ |       WEB TIER          │
  (users)            │  nginx / load balancer  │
                     │  SG: 80/443 from 0.0.0.0/0
                     └───────────┬─────────────┘
                                 │
                                 ▼
                     ┌─────────────────────────┐
                     │       APP TIER          │
                     │  backend (e.g. Flask)   │
                     │  - handles recipe CRUD  │
                     │  - handles photo upload │
                     │  SG: inbound from Web tier SG only
                     └──────┬──────────┬───────┘
                            │          │
              ┌─────────────┘          └─────────────┐
              ▼                                       ▼
   ┌─────────────────────┐                 ┌─────────────────────────┐
   │     DATA TIER          │                 │   OBJECT STORAGE        │
   │  BLOCK STORAGE         │                 │  (recipe photos, user   │
   │  (recipes, users,      │                 │   avatars)              │
   │   ratings — relational │                 │  - whole-file, read-    │
   │   DB, small random     │                 │    heavy, no in-place   │
   │   writes)              │                 │    edits                │
   │  SG: inbound from App  │                 │  - accessed via HTTP    │
   │  tier SG only          │                 │    from App tier        │
   └──────────────────────                    └─────────────────────────┘

**Why each storage decision, walked through the Day 74 framework:**

Recipes/users/ratings table:
  Q1: small in-place edits (editing one recipe, adding one rating)? → yes → BLOCK
  Q2: attached to one machine (the DB server)?                       → yes → BLOCK
  Q3: speed-critical, bounded size?                                  → yes → BLOCK

Recipe photos / avatars:
  Q1: edited in place, or uploaded once and read many times?         → whole-file → OBJECT
  Q2: accessed broadly over HTTP, not tied to one machine?            → yes → OBJECT
  Q3: scale (thousands of users' photos) over per-request speed?      → scale wins → OBJECT

**One subtlety worth drawing explicitly:** the app tier talks to both storage types — it queries the database (block, low-latency) AND makes HTTP calls to object storage (uploading/fetching photos) — these aren't alternatives to each other, they coexist, each handling the piece of data it's actually suited for.

**Real-world use: This is genuinely the exercise real architecture diagrams are for — not decoration, but a forcing function that makes you commit to where every piece of data lives and why, before writing code, the same discipline as Day 62's schema-before-code habit, just one layer up. Drawing security scope per tier on the same diagram (rather than as a separate afterthought) is what real infrastructure-as-code setups do too — the network topology and the security rules are designed together, not bolted on after the app works.**

## October 7 (Day 77) Review + refine — layer in security groups/ports from Sep Week 3 onto your sketch, label everything, then explain your own diagram out loud as if to someone who's never seen it. Close the week by re-deriving O(1) vs O(n) from scratch without notes.

**Today's structure**

No new concept — this is Week 1's close, built entirely around two things you already have: yesterday's sketch, and everything from September Week 3. Three steps, in order.

**Step 1 — layer security groups/ports onto yesterday's diagram**

Go back to Day 76's sketch and add, next to each tier, the actual port-level detail Week 3 (Days 54, 59) covered — not just "App tier SG: inbound from Web tier," but the real specifics:

WEB TIER
  Inbound:  TCP 80 (HTTP) from 0.0.0.0/0
            TCP 443 (HTTPS) from 0.0.0.0/0
            TCP 22 (SSH) from YOUR_IP/32 only   ← Day 56's habit, still applies
  Outbound: to App tier only, on whatever port your app listens on (e.g. 5000)

APP TIER
  Inbound:  TCP 5000 (or your app's port) from WEB TIER'S SG only — not 0.0.0.0/0
  Outbound: to Data tier (e.g. TCP 5432 for Postgres) + to Object storage over HTTPS (443)

DATA TIER
  Inbound:  TCP 5432 (or your DB's port) from APP TIER'S SG only
  Outbound: none needed, typically

OBJECT STORAGE
  Not a "tier" with a security group in the same sense — it's reached over
  HTTPS from the App tier, authenticated via IAM permissions (Day 53's
  roles/policies), not a port rule at all.

The one thing worth double-checking as you do this: confirm your diagram never shows the Web tier with a direct arrow to the Data tier, and never shows the Data tier's security group allowing `0.0.0.0/0` anywhere. If either shows up, that's the mistake Day 75's whole argument was built to prevent.

**Step 2 — explain it out loud, as if to someone who's never seen it**

This is today's actual test. Out loud (or written, if that's easier to do honestly with yourself), walk through your diagram start to finish:

* What happens, step by step, from the moment a user's request leaves their browser to the moment data comes back?
* At each tier boundary, say *why* that boundary exists — not just "there's a security group here," but what it protects against.
* For each storage type on the diagram, say why that piece of data landed there and not the other type — reuse Day 74's three questions as the actual words you say, not just as a checklist you silently ran.

If you stumble on a step — can't explain *why*, only *what* — that's the exact spot worth rereading from Days 71–76 before moving on. Narrating out loud surfaces gaps that silently nodding along to your own diagram won't.

**Step 3 — re-derive O(1) vs O(n) from scratch, no notes**

Before checking anything below, write out, cold:

1. What does `O(1)` mean, in your own words — not the formal definition, just what it means for the work involved.
2. What does `O(n)` mean, same way.
3. Why does a `for` loop checking `if target in my_list` get slower as the list grows, concretely — what is the loop actually doing differently?
4. Why does `target in my_dict` not get meaningfully slower — what is a dict doing instead of what a list does?
5. One real example (yours, not a textbook one) from the last week where this distinction would actually change which data structure you'd reach for.

**Check yourself only after attempting all five:**

1. O(1): the amount of work stays the same no matter how big the input is.
2. O(n): the amount of work grows in direct proportion to the input size —
   double the input, roughly double the work.
3. A list has no way to know where a value is except checking items one
   by one, in order, until it finds a match or reaches the end — more
   items means more possible checks before that happens.
4. A dict computes a hash of the key and jumps near-directly to where
   that key's value would be stored, rather than checking other entries
   at all — the computation itself doesn't depend on how many other
   keys exist.
5. (yours will vary — e.g. "checking if a hostname is already in a
   growing list of known hosts before processing each new reading,
   from Day 74's nested-loop example")

**Real-world use: Explaining your own design out loud, to an imagined listener who knows nothing, is one of the most reliable ways to find the parts you think you understand but actually only recognize — this is essentially a rubber-duck session applied to architecture instead of code, and it's a genuinely standard practice before a real design review or interview. Re-deriving Big-O cold, rather than re-reading it, is the same principle applied to the 15-minutes-a-day thread — if you can rebuild the idea from nothing, it's actually yours; if you can only recognize it when you see it again, it isn't yet.**   

## October 8 (Day 78) Set up boto3 — install it, configure AWS credentials (~/.aws/credentials or env vars), confirm you can authenticate. +15 min: IAM basics — what IAM actually is, users vs roles vs policies.

**Definition**

**boto3**

* **boto3** is AWS's official Python SDK. Each AWS API call (list buckets, describe instances) becomes a Python method call, so you manage infrastructure with code instead of console clicks.
* `boto3.client("service")` gives you a low-level client for a service (`"s3"`, `"ec2"`, `"sts"`), where each method maps to one API call and returns plain dicts (Day 6/35).
* **Credentials** are an access key ID plus a secret access key. boto3 finds them automatically, checking in order: environment variables (Day 31), then `~/.aws/credentials`, then an attached IAM role if running on EC2.
* `~/.aws/credentials` holds the keys. `~/.aws/config` holds defaults like the region (Day 53: resources are region-scoped).
* **STS** `get_caller_identity()` is the standard "who am I?" call. It needs no special permissions and returns the ARN of whoever boto3 authenticated as, which makes it the cleanest way to confirm setup worked.

**IAM, in 15 minutes**

* **IAM** answers two questions: *who is this?* (authentication) and *what are they allowed to do?* (authorization).
* **User:** a long-term identity, with a password for the console and/or access keys for code. Today's boto3 setup uses one.
* **Role:** an identity with no permanent credentials. A user or service *assumes* it and receives temporary credentials. Services like EC2 use roles, which is why a VM shouldn't hold access keys.
* **Policy:** a JSON document listing which **actions** are allowed or denied on which **resources.** Policies attach to users, roles, or groups.
* **Default deny:** everything is denied unless a policy explicitly allows it, and an explicit deny always wins.
* **How this relates to security groups (Day 54):** a security group controls whether *network traffic* reaches a resource. IAM controls whether an *API call* is permitted. This is also why Day 77's diagram showed object storage reached via IAM rather than a port rule.

**Worked examples**

**Step 1: create a limited IAM user (never use root keys)**

Console → IAM → Users → Create user → name: study-boto3
→ Attach policies directly:
    AmazonS3ReadOnlyAccess
    AmazonEC2ReadOnlyAccess
→ Create user → open it → Security credentials tab
→ Create access key → use case: "Command Line Interface / local code"
→ copy BOTH values now. The secret is shown once and can't be retrieved later.

`Those two read-only policies match what the week's script needs (listing buckets and VMs). That's least privilege in practice: grant what the job needs, nothing more.`

**Step 2: install boto3 in your venv (Day 33/63)**

`bash`
cd ~/capstone
source env/bin/activate
pip install boto3
pip list | grep -i boto
` boto3  1.35.x`
` botocore ...`

**Step 3: store the credentials**

`bash`
mkdir -p ~/.aws
nano ~/.aws/credentials
`ini`
[default]
aws_access_key_id = AKIA...YOUR_KEY_ID
aws_secret_access_key = YOUR_SECRET_KEY
`bash`
nano ~/.aws/config
`ini`
[default]
region = us-east-1

Use the region you chose on Day 53. Then lock the file down (Day 8's octal math):

`bash`
chmod 600 ~/.aws/credentials
ls -l ~/.aws/credentials
` -rw------- 1 yourname yourname ...`

**Alternative: environment variables (Day 31)**

`bash`
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1

These last only for the current shell session unless you put them in `.bashrc`, and you shouldn't put secrets there casually.

**Step 4: confirm you can authenticate**

`python`
` check_auth.py`
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

try:
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    print("Authenticated as:", identity["Arn"])
except NoCredentialsError:
    print("boto3 couldn't find any credentials.")
except ClientError as e:
    print(f"AWS rejected the request: {e}")
`bash`
python3 check_auth.py
` Authenticated as: arn:aws:iam::123456789012:user/study-boto3`

That ARN ending in `user/study-boto3` proves boto3 is acting as your limited user, not root.

**What a policy looks like**

`json`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListAllMyBuckets"],
      "Resource": "*"
    }
  ]
}

Read it as: allow the action `s3:ListAllMyBuckets` on any resource. Every policy is Effect + Action + Resource.

**Common failures and what they mean**

NoCredentialsError: Unable to locate credentials
→ boto3 found nothing: wrong file path, wrong profile name, or env vars not exported.

ClientError: InvalidClientTokenId / SignatureDoesNotMatch
→ credentials were found but are wrong: a typo, a stray space, or a deactivated key.

ClientError: AccessDenied (on a later call, not this one)
→ authentication worked, but the policy doesn't allow that action.

This is the same split as Day 56's SSH failures: "can't find or verify who you are" versus "you're verified, but not permitted."

**Real-world use: Hardcoding keys in a script is how real credentials leak. People push them to GitHub and get compromised within minutes, because bots scan public repos for AWS key patterns. Keeping keys in ~/.aws/credentials (outside your repo, mode 600) and using a limited IAM user instead of root is the baseline habit. The same reasoning is why on an EC2 instance the real-world answer is an IAM role rather than keys on disk: there is nothing stored to steal, because the credentials are temporary and issued automatically. That's coming later this week.                                                                                     get_caller_identity() is also worth keeping in your toolkit. When something is denied and you can't tell why, the first question is "which identity is this code actually running as?", and that call answers it directly.**

## October 9 (Day 79) First script — boto3.client('s3').list_buckets(), print bucket names. +15 min: least privilege — why you scope permissions down instead of granting admin by default; look at one overly broad policy vs one scoped policy side by side

**Definition**

`list_buckets()`

* `s3 = boto3.client("s3")` creates the S3 client using the credentials you set up yesterday. You never pass keys in code, because boto3 finds them itself.
* `s3.list_buckets()` makes one API call (it needs the `s3:ListAllMyBuckets `permission, which `AmazonS3ReadOnlyAccess` includes) and returns a plain dict (Day 6/35).
* The response has a `"Buckets"` key holding a **list of dicts,** one per bucket, each with `"Name"` and `"CreationDate"` (a Python `datetime`, from Day 17). It also has `"Owner"` and `"ResponseMetadata"`, which you’ll mostly ignore.
* Bucket listing is account-wide. You see every bucket regardless of which region it lives in, even though each bucket itself belongs to one region (Day 53).
* A brand-new account probably has **zero buckets,** so an empty list is a correct result. Your `study-boto3` user is read-only and can’t create one, so you’ll make one in the console to have something to list.

**Least privilege**

* **Least privilege** means giving an identity only the permissions its job requires, scoped to the specific resources it touches, and nothing more.
* **Admin by default** is the opposite habit: `"Action": "*"` on `"Resource": "*"` means every API call on every resource in the account, including creating users, deleting data, and disabling logging.
* The reason is **blast radius:** the damage possible if credentials leak (Day 78’s GitHub scenario) or code has a bug. A leaked read-only key lets someone look. A leaked admin key lets them *own* the account.
* Scoping happens on both parts of a policy: **Action** (which API calls) and **Resource** (which things, identified by ARN).

**Worked examples**

**Step 1: create a bucket to list (console, not boto3)**

Console → S3 → Create bucket
Name: must be globally unique across all AWS accounts (Day 72),
      e.g. junnybonz-study-bucket-20261009
Region: the one you chose on Day 53
Leave "Block all public access" ON (default)
→ Create bucket

An empty bucket costs nothing, and it sits well inside free-tier limits.

**Step 2: the script**

`python`
` list_buckets.py`
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

try:
    response = s3.list_buckets()
except ClientError as e:
    print(f"AWS rejected the request: {e.response['Error']['Code']}")
else:
    buckets = response["Buckets"]
    if not buckets:
        print("No buckets found in this account.")
    for bucket in buckets:
        created = bucket["CreationDate"].strftime("%Y-%m-%d")
        print(f"{bucket['Name']}  (created {created})")
    print(f"Total: {len(buckets)}")
`bash`
source env/bin/activate
python3 list_buckets.py
` junnybonz-study-bucket-20261009  (created 2026-10-09)`
` Total: 1`

**What the raw response looks like (trimmed)**

`python`
print(response)
` {`
`   'ResponseMetadata': {'HTTPStatusCode': 200, ...},`
`   'Buckets': [`
`       {'Name': 'junny-study-bucket-20261009',`
`        'CreationDate': datetime.datetime(2026, 10, 9, 8, 14, 3, tzinfo=tzutc())}`
`   ],`
`   'Owner': {'ID': '...'}`
` }`

The `try`/`except`/`else` shape comes from Day 22 and Day 67. `else` runs only when the call succeeded.

**Seeing least privilege work: call something outside your policy**

`python`
import boto3
from botocore.exceptions import ClientError

iam = boto3.client("iam")

try:
    iam.list_users()
except ClientError as e:
    print(e.response["Error"]["Code"])
    ` AccessDenied`

Your user authenticated fine yesterday (`get_caller_identity` worked). This call fails because no attached policy allows `iam:ListUsers`. That’s the default-deny rule from Day 78, and it’s the safety net doing its job.

**Overly broad vs. scoped, side by side**

Overly broad (this is what the managed `AdministratorAccess` policy amounts to):

`json`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}

Scoped to a real job: “read objects from one bucket, and list buckets”:

json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::junnybon-study-bucket-20261009",
        "arn:aws:s3:::junnybon-study-bucket-20261009/*"
      ]
    }
  ]
}
	
Two details are worth noticing. `ListAllMyBuckets` has to use `"Resource": "*"`, because it operates on the account rather than a single bucket. And the bucket ARN appears twice: once for the bucket itself (needed for `s3:ListBucket`) and once with `/*` for the objects inside it (needed for `s3:GetObject`). That’s the same flat-key-space idea from Day 72, showing up in permissions

**Real-world use: Granting *:* “just to get it working” is probably the single most common IAM mistake in real accounts. It works instantly, so it never gets revisited, and it sits there until the day a key leaks or a script misfires. The professional habit runs the opposite way: start from zero permissions, run the code, read the AccessDenied message (which names the exact action that was blocked), and add only that. Slightly slower at first, it’s far safer than shrinking an admin policy later when you can no longer remember what depends on what.                                                                                       This also connects to Day 75’s tier security. A database tier that accepts connections only from the app tier’s security group is least privilege at the network layer. A policy scoped to one bucket is the same principle at the API layer, so a compromise of one component stays contained to what that component actually needed.**

## October 10 (Day 80) Extend it — list objects inside a bucket (name, size, last modified). +15 min: shared responsibility model — what AWS secures (physical infra, hypervisor) vs what you secure (data, access, config).

**Definition**

`list_objects_v2`

* `s3.list_objects_v2(Bucket="name")` lists the objects inside one bucket. It needs the `s3:ListBucket` permission, which `AmazonS3ReadOnlyAccess` already includes.
* The response has a `"Contents"` key holding a `list of dicts,` one per object. Each has `"Key"` (the full name, Day 72’s flat-key idea), `"Size"` (in bytes), and `"LastModified`" (a `datetime`, like `CreationDate` yesterday).
* **An empty bucket has no** `"Contents"` **key at all**. Writing `response["Contents"]` raises a `KeyError`, so use `response.get("Contents", [])`.
* **Pagination:** one call returns at most 1,000 objects. Beyond that, you use a **paginator** (`s3.get_paginator("list_objects_v2")`), which fetches page after page for you. A script that ignores this silently reports a wrong total on large buckets.
* `Prefix="backups/"` filters to keys starting with that string. This is the “folders aren’t real” point from Day 72, now doing actual work.

**Shared responsibility model**

* The cloud provider and you each secure different layers. The standard phrasing is **security** *of* **the cloud** (AWS) versus **security** *in* **the cloud** (you).
* **AWS secures:** physical data centers, hardware, the global network, the hypervisor (the software that splits one physical machine into many VMs), and the underlying software of managed services.
* **You secure:** your data, who can access it (IAM), how resources are configured (security groups, public access settings), and encryption choices.
* **The split shifts by service.** With EC2, you get a raw VM, so you also patch the guest OS and secure what runs on it. With S3, AWS runs the storage system entirely, so your job shrinks to access policies, public-access settings, and encryption.

**Worked examples**

**Step 1: put a few objects in your bucket (console)**

Console → S3 → your bucket → Upload
Upload 2-3 small files, e.g. a text file or a copy of your README.
Then create a folder named "backups" and upload one file inside it.

Your `study-boto3` user is read-only, so uploading happens in the console.

**Step 2: the script**

`python`
` list_objects.py`
import sys
import boto3
from botocore.exceptions import ClientError


def format_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def list_objects(bucket, prefix=""):
    s3 = boto3.client("s3")
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    except ClientError as e:
        print(f"Failed: {e.response['Error']['Code']}")
        return

    objects = response.get("Contents", [])
    if not objects:
        print("No objects found.")
        return

    for obj in objects:
        modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M")
        print(f"{obj['Key']:<40} {format_size(obj['Size']):>9}   {modified}")
    print(f"Total: {len(objects)} objects")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 list_objects.py <bucket> [prefix]")
        sys.exit(1)
    list_objects(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")`       
`bash`    
python3 list_objects.py your-bucket-name
` README.md                                   2 KB   2026-10-10 02:41`
` backups/weather_backup_20261001.db         24 KB   2026-10-10 02:44`
` notes.txt                                 312 B   2026-10-10 02:40`
` Total: 3 objects`

python3 list_objects.py your-bucket-name backups/
` backups/weather_backup_20261001.db         24 KB   2026-10-10 02:44`
` Total: 1 objects`

The `sys.argv` check is Day 25’s CLI habit, and `format_size` is plain Day 15 function work.

**Seeing the empty-bucket trap**

`python`
response = s3.list_objects_v2(Bucket="an-empty-bucket")
print(response.keys())
` dict_keys(['ResponseMetadata', 'IsTruncated', 'Name', 'Prefix', 'MaxKeys', ...])`
` no 'Contents' key, so response['Contents'] would crash`

**Pagination, for when a bucket has more than 1,000 objects**

`python`
paginator = s3.get_paginator("list_objects_v2")
total = 0
for page in paginator.paginate(Bucket=bucket):
    for obj in page.get("Contents", []):
        total += 1
print(total)

It’s the same loop as before with an outer loop over pages. The paginator handles the “fetch the next 1,000” bookkeeping.

**Error codes you can now tell apart (Day 79’s habit)**

NoSuchBucket  → the name is wrong, or it's in a different account
AccessDenied  → you authenticated, but no policy allows s3:ListBucket here

**Shared responsibility, mapped onto things you’ve already done**

Layer                               Who secures it     Where you touched it
----------------------------------  -----------------  ---------------------------
Data center walls, power, hardware  AWS                nothing to do
Hypervisor / host isolation         AWS                nothing to do
Your VM's OS patches                YOU                Day 57: apt update && upgrade
Open ports on the VM                YOU                Day 54/59: security groups
SSH key handling                    YOU                Day 33/56: key pair, chmod 600
Who can call which AWS APIs         YOU                Day 78/79: IAM users, policies
Bucket public-access settings       YOU                Day 79: "Block all public access"
Is data encrypted, and with what    YOU (configure)    covered in tomorrow's 15 minutes
S3's underlying storage system      AWS                nothing to do

Notice that nearly everything you’ve actually done in this course falls in the “you” column. AWS’s side is the part you never see.

**Real-world use: Listing objects with a prefix is the building block of real backup tooling: “find yesterday’s backup,” “delete anything older than 30 days,” “count what’s under logs/2026/.” The empty-bucket KeyError and the 1,000-object cap are both classic production bugs, because the code works perfectly on a test bucket with five files and misbehaves once it meets real data. Day 74’s lesson that small-N testing hides scaling problems applies here too.                                                                                         The shared responsibility model matters because most cloud breaches aren’t AWS being hacked. They are customer-side configuration mistakes: a publicly readable S3 bucket, an admin key committed to GitHub, a security group open to 0.0.0.0/0 on a database port. AWS’s side is rarely the weak link, which is why “the cloud is secure” and “my deployment is secure” are different claims. Knowing which column a layer sits in tells you whether a problem is yours to fix.** 

## October 11 (Day 81) List your VMs — boto3.client('ec2').describe_instances(), print instance IDs and states. +15 min: encryption at rest — what it protects against, where you’d toggle it (S3 SSE, EBS encryption).

**Definition**

`describe_instances()`

* `ec2 = boto3.client("ec2")` uses the same credentials as the last three days. It needs `ec2:DescribeInstances`, which `AmazonEC2ReadOnlyAccess` already includes.
* The response nests two levels deep: `"Reservations"` is a list, and each reservation holds an "Instances" list. A reservation is just the group of instances created by one launch request, so you loop over reservations, then over the instances inside each (a Day 3 nested loop).
* Each instance dict has `"InstanceId"`, `"State"` (a dict like `{"Name": "running", "Code": 16}`), `"InstanceType"`, `"LaunchTime"`, and more.
* **Optional fields can be missing.** A stopped instance has no `"PublicIpAddress"` key, so use `.get()` instead of `[]` (the same trap as the empty-bucket `Contents` on Day 80).
* **Names live in tags.** There’s no `"Name"` field. It’s a `"Tags"` list of `{"Key": ..., "Value": ...}` dicts, and the one with `Key == "Name"` is what the console shows.
* **It’s region-scoped** (Day 53). The call only sees instances in the region boto3 is configured for. An empty result often means “wrong region”, not “no instances.”
* **State values:** `pending`, `running`, `stopping`, `stopped`, `shutting-down`, `terminated`. Terminated instances stay visible for roughly an hour.

**Encryption at rest**

* **At rest** means data sitting on storage, as opposed to **in transit** (moving over a network, which is a separate topic). Encryption at rest scrambles the stored bytes so they’re unreadable without the key.
* **What it protects against:** someone getting at the raw storage without going through AWS’s access controls. That includes lost or improperly retired drives, and a snapshot or backup copied out of your account. An encrypted snapshot is useless to whoever holds it unless they can also use the encryption key.
* **What it does not protect against:** anyone who is legitimately allowed to read the data. When your code, or someone with stolen valid credentials, asks for an encrypted object, the service decrypts it transparently and hands it over. It also doesn’t make a public bucket private. This is why encryption complements IAM (Days 78–79) rather than replacing it.
* **Where you toggle it:**
1. * **S3 (SSE, server-side encryption):** since January 2023, every new object is encrypted by default with SSE-S3 (AES-256, keys fully managed by AWS). You can switch a bucket to SSE-KMS if you want your own key and an audit trail of key use. The setting lives under the bucket’s Properties → Default encryption.
2. * **EBS:** encryption is chosen when a volume is created, or turned on account-wide per region with “EBS encryption by default” in the EC2 console’s settings. An existing unencrypted volume can’t be flipped in place. You snapshot it, copy the snapshot with encryption on, and create a new volume from that copy.
* **Shared responsibility (Day 80):** AWS does the cryptography. *You* decide whether it’s on and which key protects it.

**Worked examples**

**The script**

`python`
` list_instances.py`
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

try:
    response = ec2.describe_instances()
except ClientError as e:
    print(f"Failed: {e.response['Error']['Code']}")
else:
    count = 0
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
            name = tags.get("Name", "(no name)")
            ip = inst.get("PublicIpAddress", "-")
            state = inst["State"]["Name"]
            print(f"{inst['InstanceId']}  {name:<14} {state:<10} {inst['InstanceType']:<9} {ip}")
            count += 1
    print(f"Total: {count} instances in {ec2.meta.region_name}")
`bash`
source env/bin/activate
python3 list_instances.py
` i-0a1b2c3d4e5f67890  study-vm-01    running    t3.micro  54.221.XX.XX`
` Total: 1 instances in us-east-1`

The IP and ID should match what you wrote down on Day 55. ec2.meta.region_name prints the region boto3 actually used, which makes the wrong-region problem easy to spot.

**The raw shape (trimmed)**

`python`
` {'Reservations': [`
`     {'Instances': [`
`         {'InstanceId': 'i-0a1b2c3d4e5f67890',`
`          'InstanceType': 't3.micro',`
`          'State': {'Code': 16, 'Name': 'running'},`
`          'PublicIpAddress': '54.221.XX.XX',`
`          'Tags': [{'Key': 'Name', 'Value': 'study-vm-01'}], ...}`
`     ]}`
` ]}`

**Filtering to one state**

`python`
response = ec2.describe_instances(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)

AWS does the filtering server-side, so you don’t loop through and discard instances in Python (the Day 44 `WHERE` idea, applied to an API).

**The wrong-region trap**

`python`
ec2_other = boto3.client("ec2", region_name="eu-west-1")
print(ec2_other.describe_instances()["Reservations"])
` []`
` not an error, just nothing in that region`

**Checking encryption on what you already own**

`python`
` S3: what encryption does my bucket use by default?`
s3 = boto3.client("s3")
rules = s3.get_bucket_encryption(Bucket="your-bucket-name")[
    "ServerSideEncryptionConfiguration"]["Rules"]
print(rules[0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"])
` AES256   <- SSE-S3`
`python`
` EBS: is my VM's disk encrypted?`
for vol in ec2.describe_volumes()["Volumes"]:
    attached_to = [a["InstanceId"] for a in vol["Attachments"]]
    print(vol["VolumeId"], f"{vol['Size']} GiB", "encrypted:", vol["Encrypted"], attached_to)
` vol-0f1e2d3c4b5a69788 8 GiB encrypted: False ['i-0a1b2c3d4e5f67890']`

That second output is the interesting one. Your Day 55 root volume is the block storage from Day 73, and it was probably created unencrypted, because the account-level default is off unless you turned it on. That’s a real example of the “you configure it” half of shared responsibility.

**Where each toggle lives**

S3:   Console → bucket → Properties → Default encryption → Edit
EBS:  Console → EC2 → Settings (or "Account attributes") → EBS encryption
      → "Always encrypt new EBS volumes" (applies per region, to new volumes only)

**Real-world use: describe_instances is the starting point of nearly every real infrastructure script: finding every running instance that’s missing a tag, listing everything still running so it doesn’t quietly bill you (the Day 61 concern), or locating the instance to patch. The nested Reservations → Instances structure and the missing-key behavior trip up almost everyone once. Writing it defensively with .get() now saves a crash the first time a stopped instance appears in the results.                                                                                    Encryption at rest is a standard compliance checkbox, and it’s cheap to enable because there’s no meaningful performance cost. Knowing its limits matters more than knowing the toggle. “It’s encrypted” gets said as though it settles the security question, but it only defends against the storage layer being exposed, not against the credential or permission mistakes that cause most real incidents. That’s why today’s 15 minutes sits next to Days 78–79 rather than replacing them.**

## October 12 (Day 82) Combine both — one script that reports buckets and instances together, formatted cleanly. +15 min: encryption in transit — TLS/HTTPS, why the connection between your script and AWS’s API needs it too, not just the stored data.

**Definition**

**Combining the two scripts**

* Days 79 and 81 each answer one question. Today’s script answers “what do I own in this account?” in one run: buckets and instances together, under one header.
* **Each section handles its own failure.** If the bucket call is denied, the instance section should still print. This is Day 67’s lesson (separate failure layers, don’t let one crash hide the other), applied to two AWS services.
* **Pagination applies here too** (Day 80). `describe_instances` can return results in pages, so the script uses a paginator.
* `get_caller_identity()` (Day 78) goes in the header so every report says which identity produced it.

**Encryption in transit**

* **In transit** means data moving across a network, as opposed to at rest (Day 81). **TLS** is the protocol that protects it. **HTTPS is HTTP running over TLS,** on port 443 instead of 80 (Day 25).
* TLS provides three things:
    * **Confidentiality:** anyone on the path (Wi-Fi, ISP, a router in between) sees scrambled bytes.
    * **Integrity:** tampering in flight is detected.
    * **Authentication:** the server presents a **certificate** signed by a trusted authority, proving you reached the real endpoint and not an impostor.
* **Simplified handshake:** client says hello and lists what it supports, the server replies with its certificate, the client verifies it, both sides agree on a shared key, and everything after that is encrypted with it. This is Day 21’s Presentation layer (“TLS encrypts it”) in action.
* **Why your script’s connection to AWS needs it:** your API calls cross networks you don’t control. AWS’s request signing (SigV4) means your **secret key is never transmitted,** only a signature computed from it. But the *contents* still travel: bucket names, instance IDs, public IPs, S3 object bytes, and the session token if you’re ever using role credentials. Without TLS, all of that is readable on the wire, and without certificate verification an impostor could feed your script fake responses.
* **boto3 does this for you:** it uses HTTPS and verifies certificates by default. The two ways to switch that off are `use_ssl=False` and `verify=False`. Don’t. Disabling verification is the classic “fix” for a certificate error, and it removes the authentication property entirely.

**Worked examples**

**The combined script**

`python`
` aws_report.py`
import datetime
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def get_buckets(s3):
    buckets = s3.list_buckets().get("Buckets", [])
    rows = [(b["Name"], b["CreationDate"].strftime("%Y-%m-%d")) for b in buckets]
    return sorted(rows)


def get_instances(ec2):
    rows = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
                rows.append((
                    tags.get("Name", "(no name)"),
                    inst["InstanceId"],
                    inst["State"]["Name"],
                    inst["InstanceType"],
                    inst.get("PublicIpAddress", "-"),
                ))
    return sorted(rows)


def report_buckets(s3):
    print("\nS3 BUCKETS")
    try:
        rows = get_buckets(s3)
    except ClientError as e:
        print(f"  could not list buckets: {e.response['Error']['Code']}")
        return
    if not rows:
        print("  (none)")
        return
    print(f"  {'NAME':<40} {'CREATED':<12}")
    for name, created in rows:
        print(f"  {name:<40} {created:<12}")
    print(f"  Total: {len(rows)}")


def report_instances(ec2):
    print("\nEC2 INSTANCES")
    try:
        rows = get_instances(ec2)
    except ClientError as e:
        print(f"  could not list instances: {e.response['Error']['Code']}")
        return
    if not rows:
        print(f"  (none in {ec2.meta.region_name})")
        return
    print(f"  {'NAME':<16} {'INSTANCE ID':<21} {'STATE':<10} {'TYPE':<10} PUBLIC IP")
    for name, iid, state, itype, ip in rows:
        print(f"  {name:<16} {iid:<21} {state:<10} {itype:<10} {ip}")
    print(f"  Total: {len(rows)}")


def main():
    try:
        identity = boto3.client("sts").get_caller_identity()["Arn"]
    except NoCredentialsError:
        print("No credentials found. Check ~/.aws/credentials.")
        return
    except ClientError as e:
        print(f"Authentication failed: {e.response['Error']['Code']}")
        return

    s3 = boto3.client("s3")
    ec2 = boto3.client("ec2")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 62)
    print(f"AWS REPORT   {now}")
    print(f"Identity: {identity}")
    print(f"Region:   {ec2.meta.region_name}")
    print("=" * 62)

    report_buckets(s3)
    report_instances(ec2)


if __name__ == "__main__":
    main()
`bash`
source env/bin/activate
python3 aws_report.py
` ==============================================================`
` AWS REPORT   2026-10-12 09:30`
` Identity: arn:aws:iam::123456789012:user/study-boto3`
` Region:   us-east-1`
` ==============================================================`
`
` S3 BUCKETS`
`   NAME                                     CREATED`
`   junny-study-buckeXxxxXX                 2026-10-09`
`   Total: 1`
`
` EC2 INSTANCES`
`   NAME             INSTANCE ID           STATE      TYPE       PUBLIC IP`
`   study-vm-01      i-0a1bXXXXXXXX   running    t3.micro   54.221.XX.XX`
`   Total: 1`

If you screenshot this for your portfolio (Day 70’s idea), mask the account ID inside the ARN first.

**Proving the sections fail independently**

`python`
` temporarily, inside get_buckets(): replace the s3 call with one your user isn't allowed to make`
buckets = boto3.client("iam").list_users().get("Users", [])
S3 BUCKETS
  could not list buckets: AccessDenied

EC2 INSTANCES
  study-vm-01 ...   <- still prints

Revert it afterward. This is the same default-deny from Days 78–79, now showing that one denial doesn’t take down the whole report.

**Seeing that boto3 is already using HTTPS**

`python`
print(ec2.meta.endpoint_url)
` https://ec2.us-east-1.amazonaws.com`
print(s3.meta.endpoint_url)
` https://s3.amazonaws.com        (region-dependent)`

**Watching a TLS handshake with** `curl` (Day 34 flags, Day 13/14 grep and pipes, Day 68’s `2>81`)

`bash`
curl -vI https://api.github.com 2>&1 | grep -iE "tls|ssl|verify"
` * TLSv1.3 (OUT), TLS handshake, Client hello (1):`
` * TLSv1.3 (IN), TLS handshake, Server hello (2):`
` * SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256`
` *  SSL certificate verify ok.`
` (trimmed; exact lines vary with your curl version)`

The last line is the authentication property: curl checked the certificate and it was valid.

**Now the same check against your own nginx from Day 58**

`bash`
curl -vI http://54.221.XX.XX 2>&1 | grep -iE "tls|ssl|verify"
` (no output)`

Empty output means no TLS was involved at all. Your nginx serves plain HTTP on port 80, so anything sent to it crosses the network readable. Real sites also open 443 in the security group (Day 59) and install a certificate. You don’t need to do that today, but it’s the concrete gap between your VM and a production web tier.

**Checking the TLS version from Python**

`python`
import socket
import ssl

host = "ec2.us-east-1.amazonaws.com"
ctx = ssl.create_default_context()   ` verification ON by default`

with socket.create_connection((host, 443)) as sock:
    with ctx.wrap_socket(sock, server_hostname=host) as tls:
        print(tls.version())
        print(tls.cipher()[0])
` TLSv1.3`
` TLS_AES_256_GCM_SHA384    (yours may differ)`

`server_hostname=host` is what ties the certificate to the name you meant to reach.

**Enforcing in transit on S3: a bucket policy**

`json`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::junny-study-bucket-20261009",
        "arn:aws:s3:::junny-study-bucket-20261009/*"
      ],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}

Read it as: *deny* every S3 action on this bucket and its objects whenever the request did **not** use TLS. Day 78’s rule that an explicit deny always wins is why this works as a guardrail, since no other policy can override it. Your read-only user can’t attach it, so just read it.

**Real-world use: A single inventory script is a real tool. Audit and cost-control scripts start exactly here: list everything, flag what’s running that shouldn’t be, and notice what’s missing a tag. With free-tier limits in mind (Days 52 and 61), “show me everything I own and what state it’s in” is how you catch a forgotten instance before it bills you. The per-section error handling matters more than it looks: a report that dies entirely because one service was denied hides the information you still could have have had.                  Encryption in transit is usually on by default, and that’s the risk. People rarely turn it on, but they do turn it off, and verify=False is the usual way. A script that works around a certificate error that way will keep working while quietly accepting any server that claims to be AWS. Together with Day 81, you now have both halves: at rest protects stored bytes from someone reaching the storage layer, in transit protects them while moving. Neither helps if the credentials or permissions are wrong, which is why Days 78–79 come first.**

## October 13 (Day 83) Add error handling — try/except for missing credentials, wrong region, expired tokens. +15 min: write an actual least-privilege IAM policy by hand (JSON) that only allows read-only S3 access — direct application of Day 9’s concept.

**Definition**

**Two families of boto3 exceptions**

* `ClientError:` the request reached AWS and AWS replied with an error. The reason is in `e.response["Error"]["Code"]` (the habit from Days 79-80). `AccessDenied` and `NoSuchBucket` are examples.
* `BotoCoreError` (and its subclasses): the request never got a proper answer, because boto3 failed **before or around** the call. This family covers the three failures in today’s assignment:
   * `NoCredentialsError`: no credentials found anywhere in the lookup chain from Day 78.
   * `PartialCredentialsError:` half a credential, such as an access key with no secret.
   * `ProfileNotFound`: `AWS_PROFILE` names a profile that doesn’t exist.
   * `NoRegionError`: no region configured (clients like EC2 need one, but S3 typically still works without it).
   * `EndpointConnectionError`: can’t reach the endpoint, often because the region name is wrong.
   * `SSLError`: the TLS certificate check failed (Day 82). Never “fix” this with `verify=False`.
* **Catch order matters.** Put specific exceptions first and the broad ones last, the same rule as Day 22. Also, a client can fail at **creation** (`boto3.client("ec2")` raises `NoRegionError` immediately), so create clients *inside* the try.

**“Expired token”, and what it means for you**

* Your `study-boto3` key is a **long-term** key. It doesn’t expire. It can be deactivated or deleted, and then the error is `InvalidClientTokenId`, not “expired”.
* Expiry happens with **temporary credentials** (roles, SSO, STS). Those carry a lifetime, and the error codes are `ExpiredToken`, `ExpiredTokenException`, or `RequestExpired`, depending on the service.
* **Clock skew** is a lookalike: AWS rejects signed requests when your machine’s clock is too far off (`RequestTimeTooSkewed`). That’s a real risk on a VM.
* **Codes differ by service.** S3 says `AccessDenied`, but EC2 says `UnauthorizedOperation`. A handler has to know both.

**A hand-written least-privilege policy**

* **Bucket-level actions** (like `s3:ListBucket`) attach to the bucket ARN. **Object-level actions** (like `s3:GetObject`) attach to the `/*` ARN. Separate statements keep each action on only the resource it applies to.
* `s3:ListAllMyBuckets` can only use `"Resource": "*"`. It’s an account-level action and can’t be scoped to one bucket.

**Worked examples**

**The script**

`python`
` aws_errors.py`
import sys
import boto3
from botocore.exceptions import (
    BotoCoreError, ClientError, ConnectTimeoutError, EndpointConnectionError,
    NoCredentialsError, NoRegionError, PartialCredentialsError,
    ProfileNotFound, SSLError,
)

EXPIRED = {"ExpiredToken", "ExpiredTokenException", "RequestExpired"}
BAD_CREDS = {"InvalidClientTokenId", "SignatureDoesNotMatch",
             "UnrecognizedClientException", "AuthFailure", "InvalidAccessKeyId"}
DENIED = {"AccessDenied", "AccessDeniedException", "UnauthorizedOperation"}


def describe_error(e):
    """Turn an AWS/boto3 exception into (what happened, what to try)."""
    if isinstance(e, NoCredentialsError):
        return ("No credentials found.",
                "Check ~/.aws/credentials, or the AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars.")
    if isinstance(e, PartialCredentialsError):
        return ("Credentials are incomplete.",
                "Both the access key ID and the secret key must be set.")
    if isinstance(e, ProfileNotFound):
        return ("That AWS profile doesn't exist.",
                "Check AWS_PROFILE against the [section] names in ~/.aws/credentials.")
    if isinstance(e, NoRegionError):
        return ("No region configured.",
                "Add region = ... to ~/.aws/config or set AWS_DEFAULT_REGION.")
    if isinstance(e, (EndpointConnectionError, ConnectTimeoutError)):
        return ("Can't reach the AWS endpoint.",
                "Check the region name for typos and your network. This can pause several seconds while boto3 retries.")
    if isinstance(e, SSLError):
        return ("TLS certificate check failed.",
                "Don't disable verification. Check the system clock and CA certificates.")
    if isinstance(e, ClientError):
        code = e.response["Error"]["Code"]
        if code in EXPIRED:
            return (f"Credentials expired ({code}).",
                    "Temporary credentials (role/SSO/STS) have a lifetime. Refresh them and rerun.")
        if code in BAD_CREDS:
            return (f"AWS doesn't recognize these credentials ({code}).",
                    "Typo in a key, a deactivated or deleted key, or a stale session token.")
        if code == "RequestTimeTooSkewed":
            return ("This machine's clock is too far off.",
                    "Check `date` and `timedatectl`.")
        if code in DENIED:
            return (f"Not permitted ({code}).",
                    "Authentication worked, but no policy allows this action. print(e) names it.")
        return (f"AWS returned an error: {code}.", "print(e) shows the full message.")
    return (f"Unexpected boto3 error: {type(e).__name__}", "print(e) shows details.")


def authenticate():
    try:
        return boto3.client("sts").get_caller_identity()["Arn"]
    except (BotoCoreError, ClientError) as e:
        what, hint = describe_error(e)
        print(f"Cannot continue: {what}\n    -> {hint}")
        sys.exit(1)


def run_checked(label, func, *args):
    """Run one section. Print a friendly message instead of crashing."""
    try:
        return func(*args)
    except (BotoCoreError, ClientError) as e:
        what, hint = describe_error(e)
        print(f"[{label}] {what}\n    -> {hint}")
        return None


def list_bucket_names():
    s3 = boto3.client("s3")
    return sorted(b["Name"] for b in s3.list_buckets().get("Buckets", []))


def list_instance_summaries(region=None):
    ec2 = boto3.client("ec2", region_name=region)   # can raise NoRegionError right here
    rows = []
    for page in ec2.get_paginator("describe_instances").paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                rows.append((inst["InstanceId"], inst["State"]["Name"]))
    return rows


def main():
    print(f"Authenticated as: {authenticate()}")

    buckets = run_checked("S3", list_bucket_names)
    if buckets is not None:
        print(f"Buckets ({len(buckets)}): {', '.join(buckets) or '(none)'}")

    instances = run_checked("EC2", list_instance_summaries)
    if instances is not None:
        print(f"Instances ({len(instances)}):")
        for iid, state in instances:
            print(f"  {iid}  {state}")


if __name__ == "__main__":
    main()

`run_checked` takes `*args` (Days 16 and 20), so it can wrap any function. A normal run prints your identity, buckets, and instances, the same data as Day 82.

**Breaking it safely.** Every test below uses environment variables or a throwaway edit, so your real credentials file is never touched.

`bash`
` 1. no credentials anywhere (unset any exported AWS_* vars first: env | grep AWS)`
AWS_SHARED_CREDENTIALS_FILE=/nonexistent python3 aws_errors.py
` Cannot continue: No credentials found.`
`     -> Check ~/.aws/credentials, or the AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars.`

` 2. half a credential`
AWS_ACCESS_KEY_ID=AKIAFAKEFAKEFAKE1234 python3 aws_errors.py
` Cannot continue: Credentials are incomplete.`

` 3. credentials that look right but aren't (fake values only, never real keys on a command line)`
AWS_ACCESS_KEY_ID=AKIAFAKEFAKEFAKE1234 AWS_SECRET_ACCESS_KEY=notarealsecret python3 aws_errors.py
` Cannot continue: AWS doesn't recognize these credentials (InvalidClientTokenId).`

` 4. a profile that doesn't exist`
AWS_PROFILE=nope python3 aws_errors.py
` Cannot continue: That AWS profile doesn't exist.`

` 5. no region: S3 should still work, EC2 should not`
env -u AWS_DEFAULT_REGION AWS_CONFIG_FILE=/nonexistent python3 aws_errors.py
` Authenticated as: arn:aws:iam::...:user/study-boto3`
` Buckets (2): ...`
` [EC2] No region configured.`
`     -> Add region = ... to ~/.aws/config or set AWS_DEFAULT_REGION.`

Test 5 shows the section isolation from Day 82 working. The buckets still print even though EC2 failed.

A region that doesn’t exist. Temporarily change one line, run, then revert:

`python`
instances = run_checked("EC2", list_instance_summaries, "us-east-99")
` [EC2] Can't reach the AWS endpoint.`
`     -> Check the region name for typos and your network. This can pause several seconds ...`

Some mistakes never raise anything. A region that exists but is the *wrong* one returns an empty list (Day 81), so no `try`/`except` can catch it. The defense is printing the region in your output, as the Day 82 report did

**Testing the expired-token handler without waiting for a real expiry**

`python`
from botocore.exceptions import ClientError
from aws_errors import describe_error

fake = ClientError(
    {"Error": {"Code": "ExpiredToken", "Message": "The provided token has expired."}},
    "ListBuckets",
)
what, hint = describe_error(fake)
print(what)
print(hint)
` Credentials expired (ExpiredToken).`
` Temporary credentials (role/SSO/STS) have a lifetime. Refresh them and rerun.`

You can build a `ClientError` by hand to unit-test an error path you can’t trigger on demand. Try `RequestTimeTooSkewed` and `UnauthorizedOperation` the same way.

**The least-privilege S3 policy, by hand**

This covers exactly what Days 79-81 used (`list_buckets`, `list_objects_v2`, `get_bucket_encryption`), and nothing else:

`json`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListAllBucketNames",
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    },
    {
      "Sid": "ReadOneBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetEncryptionConfiguration"
      ],
      "Resource": "arn:aws:s3:::junny12-study-bucXXXXXXXXX9"
    },
    {
      "Sid": "ReadObjectsInOneBucket",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::junny12-study-bucXXXXXXXXX9/*"
    }
  ]
}

Compare it with `AmazonS3ReadOnlyAccess`, which you opened on Day 79:

	Managed `AmazonS3ReadOnlyAccess`	              Your hand-written policy
Actions	s3:Get*, s3:List*, s3:Describe* (plus S3 Object Lambda)	4 named actions
Buckets -	every bucket in the account	one
Can read bucket policies and ACLs =	yes (they match Get*)	no

Two details to notice:

* **The action name differs from the API call.** `get_bucket_encryption` is authorized by `s3:GetEncryptionConfiguration`. Leave it out and Day 81’s encryption check fails with `AccessDenied`. Tightening a policy tends to surface exactly these hidden dependencies.
* `ListAllMyBuckets` **still shows every bucket name in the account**. It can’t be scoped. The policy limits what you can read *inside* buckets, not which names you can see.

**Creating it and testing it**

Console → IAM → Policies → Create policy → JSON tab → paste → Next
Name: study-s3-read-one-bucket → Create policy
(The editor's validator flags syntax errors and warnings. Read them.)

IAM → Users → study-boto3 → Permissions:
  remove AmazonS3ReadOnlyAccess
  add study-s3-read-one-bucket
  (keep AmazonEC2ReadOnlyAccess. Changes can take a few seconds to apply.)
`bash`
python3 aws_errors.py                              ` buckets and instances still work`
python3 list_objects.py junny12-stuxxxxxxx9   ` works`
python3 list_objects.py your-second-bucket         ` Failed: AccessDenied`

The last line is the point of the exercise. The same user and the same script now succeed on one bucket and fail on the other, and the only thing that changed is the policy. If you want the broad policy back, re-attach it.

**The three classic mistakes when writing this by hand:**

- Putting s3:GetObject on the bare bucket ARN (it needs the /* ARN). Fails silently with AccessDenied.
- Using "Action": "s3:*" "just to test", then forgetting to narrow it.
- A trailing comma in the JSON. The validator catches it, so read what it says.

**Real-world use: Most scripts that run unattended die from one of today’s errors: a rotated key, an expired session, the wrong region, or a missing permission. A handler that says “credentials expired, refresh them” instead of dumping a traceback is the difference between a ten-second fix and a ten-minute search. It also connects to Day 67. Error messages are for the person reading the log days later, so they should say what happened and what to try.    Writing the policy by hand teaches the habit that managed policies hide. Start from nothing, run the code, read the AccessDenied, add the one action it names, and repeat. The GetEncryptionConfiguration surprise is typical: the code runs, the policy looks complete, and one missing action shows up only when that code path runs. That’s why you test a tightened policy against the real scripts instead of trusting it by eye.**

## October 14 (Day 84) Apply it for real — attach that read-only policy to a dedicated IAM user/role in the console instead of using your root/admin credentials, swap your script to use those credentials, confirm it still works. Review the week: your script now runs under the same least-privilege principle you spent all week learning about.

**Definition**
* **Dedicated identity:** one IAM identity per job, holding only what that job needs. A shared “do everything” user means every script inherits the permissions of the most demanding one.
* **User vs. role (Day 78):** a user has long-term keys. A role hands out temporary credentials. For code on your laptop, a user with keys is the usual choice. For code on your EC2 instance, a role is better because no keys sit on disk.
* **Named profile:** a `[section]` in `~/.aws/credentials`. `AWS_PROFILE=name `makes boto3 use it, so **the script’s code doesn’t change at all**. Only the identity running it does.
* **The credential chain (Day 78)** has an order, and `[default]` is what boto3 uses when you don’t ask for a profile. If `[default]` still holds your old key, you can believe you’ve swapped while you’re still on the old identity. `get_caller_identity` is how you check.
* **Retire, don’t just add:** a new key next to an old one that’s still active is not progress. You deactivate the old one, confirm nothing broke, then delete it.
* **Policy scope:** `ec2:DescribeInstances` and `s3:ListAllMyBuckets` can’t be limited to specific resources (they need `"Resource": "*"`). The scoping *you* can do is the specific action list and the one-bucket ARN.

**Worked examples**

**Step 1: confirm root has no access keys**

Console → account name (top right) → Security credentials
→ "Access keys" section should be empty.
If it lists any, delete them. Root should never have keys.

**Step 2: a policy for what the script actually does**

`aws_report.py` and `list_objects.py` call `sts:GetCallerIdentity` (needs no permission), `s3:ListAllMyBuckets`, `s3:ListBucket`, and `ec2:DescribeInstances`. They never download anything, so Day 83’s `s3:GetObject` statement can go. Least privilege means trimming even what looked reasonable yesterday.

`json`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucketNames",
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    },
    {
      "Sid": "ListOneBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::junny-study-bucket-20261009"
    },
    {
      "Sid": "DescribeInstances",
      "Effect": "Allow",
      "Action": "ec2:DescribeInstances",
      "Resource": "*"
    }
  ]
}
Console → IAM → Policies → Create policy → JSON → paste
Name: report-script-readonly`

**Step 3: create the dedicated user**

IAM → Users → Create user → name: report-script
  (leave "console access" OFF: this identity exists only for code)
→ Attach policies directly → report-script-readonly ONLY
→ Create → Security credentials → Create access key → "Local code"
→ copy both values now (the secret appears once)

**Step 4: add it as a named profile, leaving the old keys alone for now**

`ini`
` ~/.aws/credentials`
[default]
aws_access_key_id = (old study-boto3 key, unchanged for now)
aws_secret_access_key = (old secret)

[report-script]
aws_access_key_id = AKIA...NEW_KEY_ID
aws_secret_access_key = NEW_SECRET
ini
` ~/.aws/config`
[default]
region = us-east-1

[profile report-script]
region = us-east-1

Note the `profile` prefix in the **config file**. It’s required there but not in `credentials`, and forgetting it is a common cause of `ProfileNotFound`. The credentials file should still be `chmod 600`.

**Step 5: run the same script, unchanged, under the new identity**

`bash`
python3 check_auth.py
` Authenticated as: arn:aws:iam::123456789012:user/study-boto3      <- old identity`

AWS_PROFILE=report-script python3 check_auth.py
` Authenticated as: arn:aws:iam::123456789012:user/report-script    <- new identity`

AWS_PROFILE=report-script python3 aws_report.py
` (the same report as Day 82. Buckets and instances still appear.)`

The two ARNs differing is the proof the swap happened. If you’d rather select the profile in code:

`python`
session = boto3.Session(profile_name="report-script")
s3 = session.client("s3")
ec2 = session.client("ec2")

The environment-variable route is usually better, because the same file runs under whichever identity it’s launched with, and no profile name is hardcoded.

**Step 6: prove the new identity is actually narrower**

`bash`
AWS_PROFILE=report-script python3 list_objects.py junny-study-bucket-20261009
` works (s3:ListBucket on this bucket)`

AWS_PROFILE=report-script python3 list_objects.py your-second-bucket
` Failed: AccessDenied`
`python`
import boto3
from botocore.exceptions import ClientError

session = boto3.Session(profile_name="report-script")

for label, call in [
    ("get_bucket_encryption", lambda: session.client("s3").get_bucket_encryption(Bucket="junny-study-bucket-20261009")),
    ("describe_volumes",      lambda: session.client("ec2").describe_volumes()),
    ("iam list_users",        lambda: session.client("iam").list_users()),
]:
    try:
        call()
        print(label, "-> allowed")
    except ClientError as e:
        print(label, "->", e.response["Error"]["Code"])
` get_bucket_encryption -> AccessDenied`
` describe_volumes      -> UnauthorizedOperation`
` iam list_users        -> AccessDenied`

Day 81’s encryption-check snippets now fail, and that’s the trade you made when you trimmed the policy. If you want them back, add `s3:GetEncryptionConfiguration` and `ec2:DescribeVolumes`, and nothing more. The two different error codes for S3 and EC2 are the Day 83 point about service-specific codes.

**Step 7: retire the old key, in this order**

IAM → Users → study-boto3 → Security credentials
  → check "Last used": it shows when and which service touched this key
  → Actions → Make inactive   (not delete yet)
`bash`
python3 check_auth.py
` now fails: [default] still points at the inactive key`
` (the failure is the point: it shows [default] was still using the old identity)`

Then edit `~/.aws/credentials` so nothing relies on the old key. Either move the new key under `[default]`, or delete the old `[default]` block and always use `AWS_PROFILE`. Re-run, confirm it works, and after a day or two with nothing broken, **delete** the inactive key. Inactive is recoverable and deleted isn’t, which is why that order is the safe one.

**The role version, for the VM (this is the real-world form of the week)**

IAM → Roles → Create role → AWS service → EC2
→ attach report-script-readonly → name: report-script-role

EC2 → Instances → your VM → Actions → Security → Modify IAM role
→ choose report-script-role → Update
`bash`
` SSH into the VM (Day 56). Don't copy ANY credentials file onto it.`
ls ~/.aws/credentials
` ls: cannot access '~/.aws/credentials': No such file or directory`

python3 check_auth.py
` Authenticated as: arn:aws:sts::123456789012:assumed-role/report-script-role/i-0a1b2c3d4e5f67890`

`assumed-role/...` instead of `user/...` is Day 78’s role concept working. boto3 fetched temporary credentials from the instance on its own, and refreshes them before they expire. There is nothing stored on disk to steal. The VM may need a region, which is config rather than a secret: set `AWS_DEFAULT_REGION` or add a `~/.aws/config`.

Anyone with a shell on that VM now has the role’s permissions, including any process an attacker runs there. That’s the strongest argument for keeping the role this small. Its permissions are its blast radius.

**Real-world use: The script is the same file before and after. What changed is what it can do when something goes wrong: a leaked report-script key lets someone list bucket names and describe instances, where a leaked admin key would have let them do almost anything. That is what least privilege buys. It also gives you a way to audit. When each job has its own identity, “Last used” and the logs tell you exactly which script did what, and you can revoke one without breaking the others. Shared credentials make both impossible.                                          Rotating by swapping in a new key, checking the ARN, deactivating the old one, and only then deleting it is the standard careful sequence. Skipping the verify step is how people lock themselves out, or leave an old key alive for years.**

**Week 2 review (Days 78-84)**
* **78:** boto3 installed, credentials configured, `get_caller_identity()` as the “who am I” check. IAM basics: users, roles, policies, default deny.
* **79:** `list_buckets()`, and least privilege with a broad vs. scoped policy side by side.
* **80:** `list_objects_v2` with prefixes and pagination. Shared responsibility model.
* **81:** `describe_instances()` and its nested response. Encryption at rest.
* **82:** one combined report with per-section error isolation. Encryption in transit, TLS, and why `verify=False` is never the fix.
* **83:** error handling for credential, region, and token failures. A hand-written read-only policy.
* **84:** the policy attached to a dedicated identity, the script re-run under it, the old key retired. The role version for the VM.

## October 15 (Day 85) Self-audit — list every topic since August (permissions, regex, loops, joins, SSH, boto3, everything), rate your confidence 1–5 on each, cold. No notes. Whatever gets a 2 or lower is your real target for the week.

**Definition**

Today is a measurement day, so there’s nothing new to learn. The risk is rating yourself by how a topic *feels*. Recognizing an answer when you see it feels the same as knowing it, which is why “I’ve seen this a hundred times” turns into a blank page. So each topic below has a **cold probe**, a one-line task. Attempt it on paper or in a scratch file, with no notes and no earlier lessons open, then rate what you actually produced.

**The scale**

**5:** wrote it correctly, from scratch, and could explain why it works.
**4:** correct, with a minor slip (syntax, flag order) you’d catch on your own.
**3:** needed a hint, or got the idea but not the exact form.
**2:** recognized the answer once you saw it, but couldn’t produce it.
**1:** don’t remember it.

**Worked example (a filled-in row, so the scale is concrete)**
Permissions — probe: write rwxr-x--- as octal; add execute with chmod; chown owner+group
Attempt: wrote 750 instantly, wrote chmod +x correctly, wrote "chown group:user file"
Rating: 4. Right idea, swapped the order (it's user:group).

The rating comes from the attempt, not from the feeling that you know permissions.

**The audit (copy this into your journal, then fill in the ratings)**

**Linux**

1. Permissions: `rwxr-x---` as octal, `chmod +x`, `chown user:group`
2. grep, pipes, redirection: case-insensitive recursive search, `>` vs `>>`, a 3-command pipe that counts error lines excluding timeouts
3. Processes: `ps`/`top`, `kill` vs `kill -9`, `&`/`jobs`/`fg`
4. `find`/`df`/`du`: find every `.log` file, then find what’s eating the disk
5. cron: a 6:30 PM Friday schedule, plus why a script that works over SSH can fail under cron
6. Env vars: `export` vs plain assignment, `.env` and `.gitignore`
7. Bash scripting: `$1`, an `if` with correct bracket spacing, a `for` loop
8. SSH: the `ssh-keygen` edss25519 command with a comment, private vs public key, “timed out” vs “permission denied”
9. `systemctl`/`journalctl`: restart, `enable --now`, follow a service’s logs

Python
10. Functions: default args, `*args`, `return` vs print
11. File I/O: `with open`, `"w"` vs `"a"`, reading line by line
12. `try`/`except`/`finally`: specific exceptions, and why a bare `except: pass `is worse than a crash
13. `re`: `findall` with groups, named groups, `search` vs `match`
14. `os`/`sys`/`datetime`: `sys.argv`, `os.path`, `strftime`
15. Classes: `__init__`, `self`, inheritance with `super()`
16. `json`: `dumps` vs `dump` vs `loads` vs `load`
17. `venv` + `requests`: create, activate, `raise_for_status()`, parse nested JSON
18. `sqlite3` from Python: parameterized insert, `commit()`, why `?` instead of f-strings
19. boto3: the credentials chain, `ClientError` vs `BotoCoreError`, paginators

SQL
20. `SELECT`/`WHERE`: `LIKE`, `IN`, `BETWEEN`, clause order
21. Keys and `JOIN`: PK/FK, `PRAGMA foreign_keys`, `INNER` vs `LEFT`, find users with no orders
22. `GROUP BY`/`HAVING`: why `WHERE COUNT(*) > 2` fails

Networking
23. OSI’s 7 layers in one line each, and the TCP/IP mapping
24. Ports, IPs, DNS: `10.0.0.1` in binary, `ss -tulpn`, `LISTEN` vs `ESTABLISHED`
25. Security group vs `ss`: why a port can be `LISTEN` and still unreachable

Cloud
26. IAM: user vs role vs policy, default deny, write a one-action policy by hand
27. Shared responsibility, plus encryption at rest vs in transit
28. Regions/AZs, stop vs terminate, the billing alert, free-tier checks
29. Object vs block storage, the three-question framework, durability vs availability
30. 3-tier architecture, and how security scoping differs per tier

CS
31. Big-O: `O(1)` vs `O(n)`, list vs dict, what the hashmap costs in memory

**Turning ratings into a plan**
1. **List your 2-or-lowers.** If there are more than four, rank them rather than trying to fix everything.
2. **Rank by foundation.** Some topics are load-bearing. Permissions underlies SSH keys and IAM, and keys underlie joins. Fix the one other things rest on first.
3. **Rank by capstone need.** The cold redo covers fetch, insert, error handling, cron, and querying. Items 5, 10-12, 16-18, and 20-22 matter most for it.
4. **If nothing is 2 or lower, don’t trust that yet.** Re-test your 3s with a why question instead of a what question (“why does LEFT JOIN produce NULLs?”). Honest self-audits almost always turn up a couple of real gaps.
5. **Pick two or three targets** and carry the rest forward. Fixing a couple of gaps properly beats skimming ten.

**Real-world use: Knowing precisely where your gaps are is a working skill. In interviews and on the job, “I haven’t used that yet, here’s how I’d find out” lands better than bluffing, and you can only say it if you know which topics those are. The recall-versus-recognition split is also the reason review days beat re-reading: reading feels productive, but retrieval is what builds the memory.**

**Practice**
1. Copy the list into your journal.
2. Attempt each probe on paper, cold, with a rough time limit of 60-90 seconds each.
3. Rate each by what you produced, then mark everything at 2 or lower.
4. Pick your two or three targets using the ranking above.
5. Don’t start fixing anything today. Measuring comes first, and the fixing starts tomorrow.

## October 16 (Day 86) Weakest topic #1 — re-study it from scratch as if you’d never seen it, then rebuild the smallest possible example yourself (not copy-pasted from old work).  The scale confidence of 1 is Linux, Python, SQL and Networking except  Cloud and CS

Rating almost everything a 1 on a cold probe is normal after a single pass through this much material. Recall is hard to build, and it doesn’t mean the last three months didn’t land. It does mean you can’t fix four domains in one week, so you need an order.

I’d start with **Python core** (conditionals, loops, lists, dicts, functions), for two reasons. The capstone is a Python program, and `requests`, `sqlite3`, `json`, and `boto3` are all this same toolkit applied to something else. If you can’t write a loop over a list of dicts cold, none of them will feel solid. Here is the order I’d suggest for the rest of the week; tell me if you’d rather swap anything:

* **Oct 17:** Python file I/O, `try`/`except`, `json`
* **Oct 18:** SQL (`SELECT`, `WHERE`, `JOIN`, `GROUP BY`) via `sqlite3`
* **Oct 19:** Linux (permissions, grep and pipes, cron, SSH)
* **Oct 20-21:** networking basics, then the capstone cold

**Definition (from scratch, no assumed knowledge)**
* **Variable:** a name pointing at a value. `count = 3`. Types you’ll use: `int`, `float`, `str`, `bool`.
* `if` / `elif` / `else`: runs the first block whose condition is true and skips the rest. Indentation (4 spaces) defines what’s inside the block.
* **List:** an ordered collection, `[a, b, c]`, accessed by position starting at **0**. `len(x)` counts items.
* **Dict:** key-value pairs, `{"name": "web-01"}`, accessed by key. A missing key raises `KeyError`; `.get(key, default)` doesn’t.
* `for item in collection`: runs the block once per item. `while condition:` repeats until the condition is false, so something inside must change it.
* **Function:** `def name(params)`: bundles reusable code. `return` sends a value back to the caller. Without it, the function returns `None`, and `print` is not the same thing as `return`.

**Worked examples**

I’m using a shopping-cart theme so the practice problem below isn’t a copy of anything here.

1. **Variables and a condition**

`python`
price = 20.0
quantity = 3
total = price * quantity

if total > 100:
    print("free shipping")
elif total > 50:
    print("discount applies")
else:
    print("standard")
` discount applies (total is 60.0)`

2. **A list and a loop**

`python`
items = ["pen", "book", "lamp"]
print(items[0])        ` pen  (first item is position 0)`
print(len(items))      ` 3`

for item in items:
    print(item.upper())

3. **A dict, and its trap**

`python`
product = {"name": "pen", "price": 1.5, "stock": 40}
print(product["price"])               ` 1.5`
print(product.get("color", "none"))   ` none  (safe)`
` product["color"]  -> KeyError, so use .get() when a key might be missing`
product["stock"] -= 1                 ` modify in place: 39`

4. **A function with return**

`python`
def line_total(price, quantity=1):
    return price * quantity

print(line_total(1.5, 4))   ` 6.0`
print(line_total(1.5))      ` 1.5`

5. **All of it together: a list of dicts, a loop, a condition, a function**

`python`
cart = [
    {"name": "pen", "price": 1.5, "qty": 4},
    {"name": "book", "price": 12.0, "qty": 1},
    {"name": "lamp", "price": 30.0, "qty": 2},
]

def expensive_lines(cart, limit):
    result = []
    for line in cart:
        if line["price"] * line["qty"] > limit:
            result.append(line["name"])
    return result

print(expensive_lines(cart, 20))
` ['lamp']`

That last shape (build an empty result, loop, test, append, return) is what most of your capstone code is. Read example 5 slowly until you can say what each line does.

**Real-world use: Most real scripts are “get a list of records, loop over them, decide something about each, return or store the result.” The capstone’s fetch_weather produced a dict, insert_weather consumed one, and describe_instances returned a list of dicts you looped over. If you can write that skeleton from a blank file, API and database work becomes a matter of filling in details.**

## October 17 (Day 87) Weakest topic #1, applied cold — use it in a slightly different context than you originally learned it (e.g. if it’s JOINs, query a different table pair; if it’s regex, match a pattern you haven’t tried before).

Yesterday’s practice used server and cart dicts that were already structured. Today the data arrives as **raw text**, the way logs and CSV files really come, and you turn it into structure yourself. The skills are the same, so a shaky one will show up as a bug today. This follows your roadmap’s version of today, so file I/O and `json` can wait until later this week.

**Definition**

Three small additions to yesterday’s toolkit:

* `text.split(sep)` breaks a string into a list at each separator. `"a,b,c".split(",")` gives `["a", "b", "c"]`. A second argument caps the splits, so `"a b c d".split(" ", 2)` gives `["a", "b", "c d"]`.
* `text.strip()` removes whitespace and newlines from both ends.
* `int("4")` / `float("1.50")` convert a string to a number. Text from a file or log is always a string until you convert it, so `"4" * 2` is `"44"`, not `8`.

You also use patterns you already have: `continue` to skip a bad item, `return None` when a function has nothing valid to return, and a dict as an **accumulator** for counting (yesterday’s `count_by_status`).

**Worked examples**

1. **Split one line into fields**

`python`
line = "2026-10-17 09:15:02 ERROR disk full on web-02"
parts = line.strip().split(" ", 3)
print(parts)
` ['2026-10-17', '09:15:02', 'ERROR', 'disk full on web-02']`

date, clock, level, message = parts   ` unpack four values into four names`

The `3` stops the splitting after three spaces, so the message keeps its own spaces.

2. **Turn it into a dict, and refuse bad input**

`python`
def parse_line(line):
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return None
    date, clock, level, message = parts
    return {"date": date, "clock": clock, "level": level, "message": message}

print(parse_line("2026-10-17 09:15:02 ERROR disk full"))
` {'date': '2026-10-17', 'clock': '09:15:02', 'level': 'ERROR', 'message': 'disk full'}`
print(parse_line("garbage"))
` None`

3. **Parse a whole list, skipping the junk**

`python`
raw_lines = [
    "2026-10-17 09:01:10 INFO service started",
    "2026-10-17 09:15:02 ERROR disk full on web-02",
    "",
    "2026-10-17 09:20:45 WARNING cpu high on db-01",
    "garbage",
    "2026-10-17 09:31:09 ERROR timeout calling api",
]

def parse_all(lines):
    records = []
    for line in lines:
        record = parse_line(line)
        if record is None:
            continue
        records.append(record)
    return records

records = parse_all(raw_lines)
print(f"{len(records)} valid, {len(raw_lines) - len(records)} skipped")
` 4 valid, 2 skipped`

4. **Count by level (yesterday’s accumulator pattern, new data)**

`python`
def count_levels(records):
    counts = {}
    for r in records:
        level = r["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts

print(count_levels(records))
` {'INFO': 1, 'ERROR': 2, 'WARNING': 1}`

`counts.get(level, 0)` returns 0 the first time a level appears, so `+ 1` works without a `KeyError`.\

5. **Pull out one slice of the data**

`python`
errors = []
for r in records:
    if r["level"] == "ERROR":
        errors.append(r)

print(errors[-1]["message"])
` timeout calling api      (-1 is the last item, from Day 3)`

**Real-world use: Real data is text first and structure second. The step from “a string in a file” to “a dict I can query” is the same one your capstone did when it trimmed the API response down to three fields before inserting them into SQLite. Parsers also meet bad input all the time (blank lines, truncated lines, a header row), so “skip it, count it, keep going” is the right default. A crash on line 40,000 of a log file is much worse.**

## October 18 (Day 88) Weakest topic #2 — same re-study-from-scratch approach.

**Definition (from scratch)**
* **Table, row, column:** a table holds one kind of thing, each row is one record, and each column is one attribute of every record.
* **Primary key (PK):** a column whose value is unique per row (`id`). A **foreign key (FK)** is a column holding another table’s PK, which is how rows in different tables point at each other.
* `SELECT` picks columns, `FROM` names the table, `WHERE` filters rows, `ORDER `BY sorts, and `LIMIT` cuts the result off at n rows.
* `JOIN ... ON` combines two tables by matching rows. `INNER JOIN` keeps only matched rows. `LEFT JOIN` keeps every left-table row and fills NULL where there’s no match.
* `GROUP BY` collapses rows that share a value into one row per group, so you can use aggregates (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`). `HAVING` filters those groups.
* `NULL` means “no value.” Test for it with `IS NULL`, never `= NULL`.

**The mental model that unlocks most of it.** SQL runs in a different order than you write it:

1. FROM / JOIN   build the combined rows
2. WHERE         throw away rows
3. GROUP BY      collapse rows into groups
4. HAVING        throw away groups
5. SELECT        pick the columns (and compute aggregates)
6. ORDER BY      sort
7. LIMIT         cut

That order explains why `WHERE COUNT(*) > 1` fails. At step 2, nothing has been counted yet, so counts can only be filtered at step 4.

**Worked examples**

One runnable file, using an in-memory database so nothing is left on disk. Library theme, which differs from your shop data:

`python`
` library.py`
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript("""
CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE books   (id INTEGER PRIMARY KEY, title TEXT NOT NULL, genre TEXT);
CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    member_id INTEGER, book_id INTEGER, days INTEGER,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (book_id)   REFERENCES books(id)
);
INSERT INTO members (name) VALUES ('Ana'), ('Ben'), ('Cara'), ('Dev');
INSERT INTO books (title, genre) VALUES
    ('Dune','scifi'), ('Emma','classic'), ('Neuromancer','scifi'), ('Ulysses','classic');
INSERT INTO loans (member_id, book_id, days) VALUES
    (1,1,14), (1,3,7), (2,1,21), (3,2,10), (1,2,5);
""")

def run(label, sql, params=()):
    print(f"\n{label}")
    for row in conn.execute(sql, params):
        print("  ", row)

**Add each query below after the setup and run `python3 library.py`.**

`python`
run("1. SELECT + ORDER BY", "SELECT title, genre FROM books ORDER BY title")
` ('Dune', 'scifi')  ('Emma', 'classic')  ('Neuromancer', 'scifi')  ('Ulysses', 'classic')`

run("2. WHERE (parameterized)", "SELECT * FROM loans WHERE days > ?", (10,))
` (1, 1, 1, 14)  (3, 2, 1, 21)`

run("3. INNER JOIN across three tables", """
    SELECT members.name, books.title, loans.days
    FROM loans
    JOIN members ON loans.member_id = members.id
    JOIN books   ON loans.book_id   = books.id
    ORDER BY loans.id""")
` ('Ana','Dune',14) ('Ana','Neuromancer',7) ('Ben','Dune',21) ('Cara','Emma',10) ('Ana','Emma',5)`

run("4. LEFT JOIN: members who never borrowed", """
    SELECT members.name
    FROM members
    LEFT JOIN loans ON loans.member_id = members.id
    WHERE loans.id IS NULL""")
` ('Dev',)`

run("5. GROUP BY: loans per member", """
    SELECT members.name, COUNT(*) AS loan_count
    FROM loans JOIN members ON loans.member_id = members.id
    GROUP BY members.name
    ORDER BY members.name""")
` ('Ana', 3)  ('Ben', 1)  ('Cara', 1)`

run("6. HAVING: only members with 2+ loans", """
    SELECT members.name, COUNT(*) AS loan_count
    FROM loans JOIN members ON loans.member_id = members.id
    GROUP BY members.name
    HAVING COUNT(*) > 1""")
` ('Ana', 3)`

run("7. LEFT JOIN: books nobody borrowed", """
    SELECT books.title
    FROM books
    LEFT JOIN loans ON loans.book_id = books.id
    WHERE loans.id IS NULL""")
` ('Ulysses',)`

**Why query 4 works.** The `LEFT JOIN` keeps Dev even though Dev has no loans, and fills Dev’s `loans` columns with `NULL`. `WHERE loans.id IS NULL` then keeps exactly those rows. An `INNER JOIN` would have dropped Dev before you could find them.

**Traps to hit on purpose, once, so you recognize them:**

`python`
` a JOIN with no ON multiplies rows (4 members x 5 loans)`
print(conn.execute("SELECT COUNT(*) FROM members JOIN loans").fetchone())   # (20,)

` an aggregate in WHERE is an error about misuse of an aggregate`
` conn.execute("SELECT member_id FROM loans WHERE COUNT(*) > 1")`

` = NULL is never true, so this returns nothing`
print(conn.execute("SELECT * FROM loans WHERE book_id = NULL").fetchall())  # []

**Real-world use: Most “report” requests are one of these shapes: rows matching a condition (WHERE), the same thing across two tables (JOIN), a count or total per category (GROUP BY), or the things that have no match (LEFT JOIN ... IS NULL). That last one, finding customers with no orders or files with no owner, is the question inner joins can’t answer, and it comes up constantly. Your capstone used only a single table, so this is the part that real databases need on top of it.**

## October 19 (Day 89) Weakest topic #2, applied cold — same "different context" test.

**Definition**

Three ideas that matter more once the data is messy:

* **A foreign key can be** `NULL`s. It means “no parent.” A ticket with `agent_id = NULL` is valid, and the foreign key doesn’t reject it. An `INNER JOIN` silently drops that ticket, so a join can make rows vanish without any error.
* `COUNT(*)` **counts rows.** `COUNT(column)` **counts non-**`NULL` **values in that column.** After a `LEFT JOIN`, an agent with no tickets still has one row, with `NULL` in every ticket column. So `COUNT(*)` says 1 and `COUNT(tickets.id)` says 0. When you want “how many, including zero,” count a column from the *right* table.
* **Where a filter goes changes a** `LEFT JOIN`. A condition in `ON` limits which right-side rows match, and left rows are kept regardless. A condition in `WHERE` runs afterward and deletes rows, including the `NULL`-padded ones you wanted to keep. It silently turns your `LEFT JOIN` back into an `INNER JOIN`.

**Worked examples**
`python`
` support.py`
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript("""
CREATE TABLE agents (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    status TEXT, priority INTEGER, opened TEXT,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);
INSERT INTO agents (name) VALUES ('Lina'), ('Omar'), ('Pia'), ('Quin');
INSERT INTO tickets (agent_id, status, priority, opened) VALUES
    (1,'open',3,'2026-10-01'), (1,'closed',1,'2026-10-02'),
    (2,'open',2,'2026-10-02'), (2,'open',3,'2026-10-05'),
    (1,'closed',2,'2026-10-06'), (3,'closed',1,'2026-10-06'),
    (NULL,'open',3,'2026-10-07');
""")

def run(label, sql, params=()):
    print(f"\n{label}")
    for row in conn.execute(sql, params):
        print("  ", row)

**Add the queries below after the setup.**

`python`
run("1. Open tickets, highest priority first", """
    SELECT id, priority FROM tickets
    WHERE status = 'open'
    ORDER BY priority DESC, id""")
` (1, 3)  (4, 3)  (7, 3)  (3, 2)`
`python`
run("2. INNER JOIN: ticket with its agent", """
    SELECT agents.name, tickets.id, tickets.status
    FROM tickets JOIN agents ON tickets.agent_id = agents.id
    ORDER BY tickets.id""")
` ('Lina',1,'open') ('Lina',2,'closed') ('Omar',3,'open')`
` ('Omar',4,'open') ('Lina',5,'closed') ('Pia',6,'closed')`
` 6 rows. There are 7 tickets. Ticket 7 vanished with no error.`
`python`
run("3. Agents with no tickets", """
    SELECT agents.name
    FROM agents LEFT JOIN tickets ON tickets.agent_id = agents.id
    WHERE tickets.id IS NULL""")
` ('Quin',)`

run("4. Tickets with no agent (the NULL foreign key)", """
    SELECT id, status FROM tickets WHERE agent_id IS NULL""")
` (7, 'open')`
`python`
run("5a. The COUNT(*) trap", """
    SELECT agents.name, COUNT(*) AS n
    FROM agents LEFT JOIN tickets ON tickets.agent_id = agents.id
    GROUP BY agents.name ORDER BY agents.name""")
` ('Lina',3) ('Omar',2) ('Pia',1) ('Quin',1)    <- Quin has 0 tickets, not 1`

run("5b. Fixed: count a right-side column", """
    SELECT agents.name, COUNT(tickets.id) AS n
    FROM agents LEFT JOIN tickets ON tickets.agent_id = agents.id
    GROUP BY agents.name ORDER BY agents.name""")
` ('Lina',3) ('Omar',2) ('Pia',1) ('Quin',0)`
`python`
run("6a. Filter in WHERE: agents with no open tickets disappear", """
    SELECT agents.name, COUNT(tickets.id) AS open_n
    FROM agents LEFT JOIN tickets ON tickets.agent_id = agents.id
    WHERE tickets.status = 'open'
    GROUP BY agents.name ORDER BY agents.name""")
` ('Lina',1) ('Omar',2)         <- Pia and Quin are gone`

run("6b. Filter in ON: everyone stays, zeros included", """
    SELECT agents.name, COUNT(tickets.id) AS open_n
    FROM agents
    LEFT JOIN tickets ON tickets.agent_id = agents.id AND tickets.status = 'open'
    GROUP BY agents.name ORDER BY agents.name""")
` ('Lina',1) ('Omar',2) ('Pia',0) ('Quin',0)`
`python`
run("7. HAVING: days with more than one ticket", """
    SELECT opened, COUNT(*) FROM tickets
    GROUP BY opened HAVING COUNT(*) > 1 ORDER BY opened""")
` ('2026-10-02', 2)  ('2026-10-06', 2)`

**Two checks that catch silent wrongness:**

`python`
print(conn.execute("SELECT COUNT(*) FROM tickets").fetchone())                        # (7,)
print(conn.execute("SELECT COUNT(*) FROM tickets JOIN agents ON agent_id = agents.id").fetchone())  # (6,)
` sanity habit: compare row counts before and after a join. A gap means rows were dro`

**Real-world use: The queries that cause real trouble in reports aren’t the ones that crash. They run fine and return a plausible-looking wrong number: a dashboard that shows 6 tickets when there are 7, or an “agents by open tickets” table that quietly omits everyone at zero. Those errors are INNER JOIN dropping NULLs, COUNT(*) counting padding rows, and a filter in WHERE undoing a LEFT JOIN. Checking a join’s row count against the source table is a cheap habit that catches most of them.**

## October 20 (Day 90) Redo Capstone #2 cold, part 1 — VM + API script, entirely from memory. No looking at your original repo. Get as far as you can; note exactly where you get stuck.

Definition: scope and finish line

Part 1 covers (the Day 62-64 territory): reach your VM, set up an isolated Python environment, call a public API, and produce a trimmed dict of the fields you care about.

Part 1 does not cover: SQLite, error handling around the whole run, cron, or querying. Those are Oct 21.

You’re done when all of these are true, in order:

You can reach the VM and prove you’re on the remote machine, not your laptop.
A fresh project folder (capstone2) exists with a venv you activated, and you can prove python3 is the venv’s.
requests is installed in that venv and imports cleanly.
You picked a no-key API, hit it once from the terminal, and chose 3 fields worth keeping.
A function returns a dict containing only those fields plus a timestamp, using a timeout and a status check.
Running the file prints that dict.
You broke the URL on purpose, saw the failure, and reverted it.

The rules
No old repo, no old lessons, no AI. Allowed: error messages, --help, man, and official docs (docs.python.org, the requests docs, your chosen API’s docs).
Time-box about 2.5 hours. Stop the clock when you’ve been stuck on one thing for 15 minutes.
Use the hint ladder (below) instead of opening the old files, and log which rung you needed.
Don’t fix silently. Write the stall down first, then fix it.

**Commands, in order**

bash
ssh -i ~/.ssh/id_ed25519 ubuntu@<public-ip>
whoami; hostname; pwd            # prove you're remote

mkdir capstone2 && cd capstone2
python3 -m venv env
source env/bin/activate
which python3                    # should point inside capstone2/env
pip install requests
python3 -c "import requests; print(requests.__version__)"

curl -s "https://api.open-meteo.com/v1/forecast?latitude=14.6&longitude=121.0&current=temperature_2m,wind_speed_10m"

fetch2.py

python
import datetime
import requests

API_URL = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=14.6&longitude=121.0&current=temperature_2m,wind_speed_10m")


def fetch_weather():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    raw = response.json()
    return {
        "fetched_at": datetime.datetime.now().isoformat(),
        "temperature_c": raw["current"]["temperature_2m"],
        "wind_speed_kmh": raw["current"]["wind_speed_10m"],
    }


if __name__ == "__main__":
    print(fetch_weather())

**Real-world use: Rebuilding something from a blank folder is the closest thing to a real interview or on-call situation, where the old repo isn’t open and the machine is in front of you. Your stuck log doubles as a practical study plan. A pattern like “all three stalls were environment problems” tells you far more than “I feel shaky on Python.”**

## October 21 (Day 91) Redo Capstone #2 cold, part 2 — finish it, then diff your redo against the original. Whatever you had to guess at or couldn’t remember is your actual weak spot, more honest than Day 15’s self-rating. Document the gap, push both versions.

**Definition: scope and finish line**

**Part 2 covers** the Day 65-69 territory: SQLite, error handling, cron, and one real query. Then the comparison.

**You’re done when, in order:**

1. A `db2.py` creates the table with `CREATE TABLE IF NOT EXISTS` and inserts one row using `?` placeholders and a commit.
2. A `main2.py` wires fetch and insert together, and you’ve run it 3 times manually.
3. You confirmed the rows from the `sqlite3` CLI: the count matches the runs, and the timestamps are distinct.
4. The fetch and insert are wrapped in `try`/`except` with **specific** exceptions, and you broke each failure layer once (timeout or bad URL, bad field name, bad DB path) and reverted.
5. A cron job runs it **every minute for a test**, using absolute paths and a log file. You saw rows climb, then changed it to `*/15` or removed it.
6. You ran one `GROUP BY` query on your own data.
7. You diffed against the original, wrote the gap document, and pushed both versions.

**The rules**
1. Same as yesterday: no old repo, no AI. Error messages, --help, and official docs are fine.
2. Build for about 3 hours, then diff for about 1. Don’t open the original until your own version runs or the build time is up.
3. Use the hint ladder and the stuck log from yesterday.
4. Housekeeping:
    * Use the `capstone2` folder and new file and DB names (weather2.db). Your *  original cron job probably still runs against the original folder, so the  two keep separate databases.
    * Don’t launch a second VM while the first runs (free-tier hours).
    * `datetime.now()` on the VM is UTC.

**Real-world use: Rebuilding from memory and then diffing is how people find out what they know versus what they’ve seen. It also gives you something concrete for a portfolio or interview: “here’s my first build, my second build from memory, and a written analysis of what I got wrong.” That shows how you learn, which is rarer than a clean repo.**    

## October 22-25 (Day 92-95) Finals get first priority.