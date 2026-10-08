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
   │     DATA TIER        │                 │   OBJECT STORAGE        │
   │  BLOCK STORAGE        │                 │  (recipe photos, user   │
   │  (recipes, users,     │                 │   avatars)              │
   │   ratings — relational │                 │  - whole-file, read-    │
   │   DB, small random     │                 │    heavy, no in-place   │
   │   writes)              │                 │    edits                │
   │  SG: inbound from App  │                 │  - accessed via HTTP    │
   │  tier SG only          │                 │    from App tier        │
   └─────────────────────┘                 └─────────────────────────┘

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