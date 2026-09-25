# 📅 September 2026 — Relational Databases, Linux Networking & Cloud VMs

## 🚀 Weekly Breakdown & Key Highlights

### Week 1 (Days 41–47): Relational Databases & SQL
* **Core Concepts:** Database normalization, Primary Keys, Foreign Keys, and data integrity.
* **SQL Querying:** `SELECT`, `WHERE` filtering, `INNER`/`LEFT JOIN`, `GROUP BY`, aggregate functions (`COUNT`, `AVG`, `SUM`), and `HAVING`.
* **Milestone:** Built a 3-table SQLite database and executed multi-table JOINs and aggregations cold.

### Week 2 (Days 48–54): Linux Services, Port Management & Cloud Orientation
* **Systemd & Logging:** Controlled background services (`systemctl start/stop/enable`) and inspected system logs using `journalctl`.
* **Networking & Ports:** Mapped open/listening sockets using `ss -tulpn` and `netstat` (understanding `LISTEN` vs `ESTABLISHED`).
* **Cloud Foundations:** Set up cloud infrastructure (AWS/Azure/GCP), configured budget alerts, and mapped cloud Security Groups directly to local port management.

### Week 3 (Days 55–61): Provisioning & Securing Cloud VMs
* **Compute Provisioning:** Launched an Ubuntu VM instance on the cloud free-tier.
* **Remote Access:** Configured inbound Security Groups (Port 22) and SSH'd securely into the remote server.
* **Web Service Deployment:** Installed and managed `nginx` (`systemctl`), opened Port 80, and verified public HTTP accessibility via `curl`.

### Week 4 (Days 62–70): Capstone — Automated Cloud Data Pipeline
* **Environment Setup:** Configured Python `venv`, installed `requests`, and integrated stdlib `sqlite3`.
* **API & DB Integration:** Built a Python script to fetch third-party JSON API data and insert timestamped records into SQLite.
* **Resilience & Automation:** Wrapped pipeline in robust `try/except` error handling and scheduled automated execution via `cron`.
* **Data Verification:** Queried accumulated live server data using SQL (`GROUP BY`, `WHERE`) directly over SSH.

---

## 💡 In My Own Words

* **SQL is Just Asking Questions:** Tables are structured spreadsheets, Primary Keys give every row a unique SSN, Foreign Keys link those rows together, and `JOIN` lets you combine them in a single query.
* **Ports Are Doors, Security Groups Are Guards:** Running `ss -tulpn` shows which door an app is listening at inside the server; a cloud Security Group decides whether the outside internet is allowed through that door.
* **Cloud VMs Are Just Someone Else's Linux Box:** SSHing into an EC2/Compute instance feels no different than my local terminal—`apt update`, `systemctl`, and path navigation work identically.
* **Automated Data Pipelines:** Connecting Python `requests` + `sqlite3` + `cron` creates a self-running engine that collects real-world data while I sleep.

---

## 🛠️ How I Solved Problems (My Debugging Process)

* **Locked Out of Remote VM:** Couldn't SSH into the cloud instance initially. Realized the inbound Security Group blocked port 22. Fixed it by adding a rule allowing SSH traffic from my public IP.
* **Nginx Page Not Loading:** The web server was active, but browser requests timed out. Mapped local listening state (`ss -tulpn` on port 80) to cloud firewall rules and opened inbound HTTP (Port 80) in the cloud console.
* **Cron Silent Failures:** Python API script ran fine manually, but failed under `cron`. Solved it by specifying absolute environment paths (`/home/ubuntu/venv/bin/python3`) inside the `crontab` definition.

# 🤓 EVERYDAY PROGESS IN DEPTH AND DETAILED 

## September 1 (Day 41) Relational model basics — what a database/table/row/column actually is, why relational vs flat files. Set up SQLite in VS Code or CoCalc, create your first table.

`RELATIONAL MODEL:`

1. **Database** — a structured collection of data, organized into tables, that a database engine manages for you (handling storage, retrieval, and integrity).
2. **Table** — a single structured set of data, organized into rows and columns, representing one type of "thing" (e.g. `users`, `orders`, `servers`).
3. **Row** (a.k.a. record) — one single entry in a table — one specific user, one specific order.
4. **Column** (a.k.a. field) — one attribute shared by every row — `email`, `created_at`, `price`. Every row has a value (or NULL) for every column.
5. **Relational** — tables can reference each other (e.g. an `orders` table pointing at a `user_id` that exists in the `users` table), letting you model connected data without duplicating it everywhere.

`Why relational vs. a flat file (like a single CSV or JSON blob):`

1. A flat file mixes everything into one structure — if a user places 10 orders, a flat file duplicates that user's name/email 10 times, once per order row.
2. A relational database stores the user once, in `users`, and each order in `orders` just references that user's ID — no duplication, and updating the user's email updates it everywhere at once.
3. This also enforces consistency: the database itself can refuse to let an order reference a `user_id` that doesn't exist.

`WORKED EXAMPLES: SETTING UP SQLITE:`

sqlite3 shop.db
` opens (or creates, if it doesn't exist) shop.db and drops you into a SQL prompt`

`CREATING YOUR FIRST TABLE:`
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

.tables
`-- users`
`-- lists every table in the current database`

.schema users
`-- CREATE TABLE users (`
`--     id INTEGER PRIMARY KEY,`
`--     name TEXT NOT NULL,`
`--     email TEXT`
`-- );`
`-- shows you the exact structure you defined`

`Inserting your first rows (a small preview — full INSERT syntax comes later this week)`

INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');

SELECT * FROM users;
`-- 1|Alice|alice@example.com`
`-- 2|Bob|bob@example.com`

`REAL-WORLD USE: Almost every real application you'll ever build — a web app, an internal tool, a cloud service's backend — stores its data relationally, because the alternative (flat files, or one giant blob of JSON) breaks down fast once data has real relationships: users who have orders, orders that have items, items that belong to categories. The relational model is what SQL, the language you're about to spend a week learning, was built specifically to query.`

`From Python instead of the SQL prompt:`

import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
` [(1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com')]`

conn.close()

`SQLite specifically is what you'll find embedded inside countless real tools — it's the default database for a lot of mobile apps, small internal scripts, and even some production systems, precisely because it needs no separate server to run and just lives in one file.`

## September 2 (Day 42)  Keys — primary keys, foreign keys, why they enforce data integrity. Practice: build two related tables (e.g. users and orders) linked by a FK.

`DEFINITION:`
1. `Primary key (PK)` — a column (or set of columns) that uniquely identifies each row in a table. No two rows can share the same PK value, and it can't be NULL.
2. `id INTEGER PRIMARY KEY` — the standard pattern; SQLite auto-increments this for you on each insert if you don't specify a value.
3. `Foreign key (FK)` — a column in one table that references the primary key of another table, creating the actual "relational" link between them.
4. `FOREIGN KEY (user_id) REFERENCES users(id)` — declares that `orders.user_id `must match an existing `id` in `users`.
5. `Referential integrity` — the guarantee (enforced by the database, if you turn it on) that a foreign key value must actually exist in the referenced table — you can't have an order pointing at a user that doesn't exist.
6. SQLite has foreign key enforcement off by default — you have to explicitly turn it on with `PRAGMA foreign_keys = ON`; at the start of each connection, or it'll silently allow orphaned references.

`WORKED EXAMPLES:`

PRAGMA foreign_keys = ON;
`-- must run this every time you connect, or FK constraints are just decoration`

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    item TEXT,
    quantity INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');

INSERT INTO orders (user_id, item, quantity) VALUES (1, 'Widget', 3);
INSERT INTO orders (user_id, item, quantity) VALUES (2, 'Gadget', 1);
`-- both work fine — user_id 1 and 2 exist in users`

INSERT INTO orders (user_id, item, quantity) VALUES (99, 'Ghost Item', 1);
`-- Error: FOREIGN KEY constraint failed`
`-- (only if PRAGMA foreign_keys = ON was set — otherwise this silently succeeds, which is worse)`

`-- primary keys reject duplicates automatically, no PRAGMA needed`
INSERT INTO users (id, name, email) VALUES (1, 'Someone Else', 'x@example.com');
`-- Error: UNIQUE constraint failed: users.id`

`From Python:`

import sqlite3

conn = sqlite3.connect("shop.db")
conn.execute("PRAGMA foreign_keys = ON")  `# must set this per-connection`
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO orders (user_id, item, quantity) VALUES (99, 'Ghost Item', 1)")
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Integrity error: {e}")
    `# Integrity error: FOREIGN KEY constraint failed`

conn.close()

`REAL-WORLD USE: Primary keys are what every other system — your app code, an API, a join between tables — uses to reliably refer to "this exact row" without ambiguity; without one, you'd have no reliable way to update or delete a specific record if two rows happened to look identical. Foreign keys are what stop a real application from ending up with broken references — an order pointing at a deleted user, a comment pointing at a deleted post — bugs that are notoriously painful to track down once they've already corrupted a production database. Turning PRAGMA foreign_keys = ON is a genuinely common gotcha specifically with SQLite that trips people up in real projects, since the constraint you wrote in your CREATE TABLE does nothing at all until you enable enforcement.`

## September 3 (Day 43) SELECT basics — SELECT *, specific columns, LIMIT, ORDER BY, DISTINCT.

`Definition:`
1. `SELECT *` — retrieves every column from a table. Fast to write, but pulls more data than you often need.
2. `SELECT column1, column2` — retrieves only the specific columns you name, in the order you list them.
3. `LIMIT n` — caps the number of rows returned, regardless of how many actually match.
4. `ORDER BY column` — sorts the results by that column (default ascending; `DESC `for descending).
5. `DISTINCT` — removes duplicate rows from the result, keeping only unique values.

`WORKED EXAMPLES Using your users/orders tables from the last two days:`

SELECT * FROM orders;
`-- every column, every row`

SELECT item, user_id FROM orders;
`-- only these two columns, ignoring 'id'`

SELECT * FROM orders LIMIT 2;
`-- only the first 2 rows, even if there are 100`

SELECT * FROM orders ORDER BY item;
`-- alphabetical by item, A→Z`

SELECT * FROM orders ORDER BY item DESC;
`-- Z→A instead`

SELECT DISTINCT user_id FROM orders;
`-- each user_id listed once, even if they placed 5 orders`

`Combining them — this is where it gets useful:`

SELECT item, user_id
FROM orders
ORDER BY user_id
LIMIT 5;
`-- 5 rows, only 2 columns, sorted by user_id`

`REAL-WORLD USE: SELECT * is fine for poking around a small table, but real applications almost always name exact columns — pulling every column from a huge table wastes bandwidth and memory for data you'll never use. LIMIT is what makes "show the 10 most recent orders" possible without scanning a whole massive table into your app. DISTINCT is the standard way to answer "how many unique customers do we have" without writing extra code to dedupe results yourself.`

## September 4 (Day 44) WHERE — comparison operators, AND/OR/NOT, LIKE, IN, BETWEEN.

`DEFINITION:`
1. `WHERE condition` — filters rows before they're returned, keeping only rows where the condition is true.
2. Comparison operators: `=`, `!=` (or `<>`), `>`, `<`, `>=`, `<=`
3. `AND` / `OR` — combine multiple conditions; AND requires both true, OR requires at least one.
4. `NOT` — negates a condition.
5. `LIKE` — pattern match on text, using `%` (any number of characters) and `_` (exactly one character) as wildcards.
6. `IN (val1, val2, ...)` — shorthand for "equals any of these values."
7. `BETWEEN low AND high` — inclusive range check.

`WORKED EXAMPLES:`

SELECT * FROM orders WHERE user_id = 2;
`-- only rows belonging to user 2`

SELECT item, user_id FROM orders WHERE user_id != 2;
`-- everyone except user 2`

SELECT * FROM orders WHERE user_id = 2 AND item = 'Widget';
`-- both conditions must be true`

SELECT * FROM orders WHERE user_id = 1 OR user_id = 2;
`-- either condition true`

SELECT * FROM orders WHERE NOT user_id = 2;
`-- same result as != 2, written with NOT instead`

SELECT * FROM orders WHERE item LIKE 'W%';
`-- item starts with 'W' (Widget, etc.)`

SELECT * FROM orders WHERE user_id IN (1, 3, 5);
`-- user_id is 1, 3, or 5`

SELECT * FROM orders WHERE user_id BETWEEN 1 AND 3;
`-- user_id is 1, 2, or 3, inclusive`

`REAL-WORLD USE: WHERE is what turns a table into an answer to a question — "which orders are unpaid," "which users signed up this month." Filtering in the database with WHERE, instead of pulling every row into your app and filtering there, is the difference between a query that scales and one that falls over on a million-row table. LIKE with % is the basic tool behind most search boxes; IN is the standard way to avoid a long chain of ORs.`

## September 5 (Day 45) JOIN — INNER JOIN and LEFT JOIN, querying across your two linked tables from Day 2.

`Definition:`
1. `JOIN` — combines rows from two tables based on a related column between them (here, `orders.user_id` matching `users.id`).
2. `INNER JOIN` — returns only rows where the match exists in both tables. A user with no orders, or an order with a nonexistent user, is left out entirely.
3. `LEFT JOIN` — returns every row from the left (first-named) table, plus matching data from the right table where it exists. If there's no match, the right table's columns come back as `NULL` instead of dropping the row.
4. Syntax: `FROM tableA JOIN tableB ON tableA.column = tableB.column`
5. `table.column` notation (e.g. `users.id`, `orders.user_id`) — needed once two tables are involved, since both might have a column with the same name (like `id`).

`WORKED EXAMPLES Using your users and orders tables from Day 42:`   

SELECT users.name, orders.item, orders.quantity
FROM orders
INNER JOIN users ON orders.user_id = users.id;
`-- Alice | Widget | 3`
`-- Bob   | Gadget | 1`
`-- only users who actually have an order show up`

`-- add a user with NO orders, to see the difference`
INSERT INTO users (name, email) VALUES ('Carol', 'carol@example.com');

SELECT users.name, orders.item, orders.quantity
FROM orders
INNER JOIN users ON orders.user_id = users.id;
`-- Carol still doesn't appear — INNER JOIN only shows matched rows`

SELECT users.name, orders.item, orders.quantity
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
`-- Alice | Widget | 3`
`-- Bob   | Gadget | 1`
`-- Carol | NULL   | NULL`
`-- Carol now appears, since LEFT JOIN keeps every row from users (the left table)`

`-- combining JOIN with WHERE and ORDER BY`
SELECT users.name, orders.item
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.item IS NULL;
`-- Carol`
`-- this specifically finds users who have placed NO orders at all`

`REAL-WORLD USE: INNER JOIN is what you use when you only care about complete, matched data — "show me every order along with who placed it," where an order with no valid user wouldn't make sense to show anyway. LEFT JOIN is what you reach for the moment you need to include things with no match — "which customers have never placed an order" (exactly the query above) is one of the most common real business questions, and it's impossible to answer with INNER JOIN alone, since that would silently exclude the very rows you're looking for.`

## September 6 (Day 46) GROUP BY — aggregate functions (COUNT, SUM, AVG, MAX/MIN), then HAVING to filter grouped results.

`Definition:`
1. **Aggregate function** — a function that collapses many rows into a single summary value: `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()`.
2. `COUNT(*)` — counts rows. `COUNT(column)` counts non-NULL values in that column specifically.
3. `SUM(column)` — adds up a numeric column.
4. `AVG(column)` — averages a numeric column.
5. `MAX(column)` / `MIN(column)` — the largest/smallest value in that column.
6. `GROUP BY column` — splits rows into buckets based on shared values in `column`, then applies any aggregate function per bucket instead of across the whole table.
7. `HAVING condition` — filters groups after aggregation, the same way `WHERE` filters individual rows before aggregation. You can't use `WHERE` to filter on an aggregate result (like `COUNT(*) > 2`) — that's exactly what `HAVING` is for.

`WORKED EXAMPLES USING "ORDERS" TABLES":`

SELECT COUNT(*) FROM orders;
`-- 6`
`-- total number of orders, no grouping`

SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id;
`-- 1 | 3`
`-- 2 | 2`
`-- 3 | 1`
`-- how many orders EACH user placed`

SELECT user_id, SUM(quantity) AS total_items
FROM orders
GROUP BY user_id;
`-- 1 | 9`
`-- 2 | 4`
-`- 3 | 1`
`-- total quantity ordered, per user`

SELECT item, AVG(quantity) AS avg_quantity, MAX(quantity) AS max_quantity, MIN(quantity) AS min_quantity
FROM orders
GROUP BY item;
`-- Widget | 3.0 | 5 | 1`
`-- Gadget | 1.5 | 2 | 1`

`-- HAVING filters groups, not individual rows`
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 1;
`-- 1 | 3`
`-- 2 | 2`
`-- user 3, with only 1 order, is filtered OUT of the result`

`-- WHERE (filters rows before grouping) + HAVING (filters groups after) together`
SELECT user_id, COUNT(*) AS order_count
FROM orders
WHERE item != 'Gadget'
GROUP BY user_id
HAVING COUNT(*) >= 2;

`PRACTICE!:`

import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT user_id, COUNT(*) AS order_count, SUM(quantity) AS total_items
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 1
""")
for row in cursor.fetchall():
    print(row)

conn.close()

`REAL-WORLD USE: GROUP BY with aggregates is how almost every real business report gets built — "orders per customer," "total revenue per day," "average order size per product category." HAVING is specifically what lets you ask "which of these groups actually meets some threshold" — like "which customers placed more than 5 orders this month" — a question you literally cannot answer with WHERE alone, since WHERE runs before the grouping/counting even happens.`

## September 7 (Day 47) Review/mini-drill — build a small 3-table SQLite DB from scratch and write 5 queries cold (one SELECT, one WHERE, one JOIN, one GROUP BY, one combining all four) without looking anything up.

**IT WENT ALL WRONG...**

**HERE IS THE FINAL:**

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL
);

CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO customers (name) VALUES ('Alice'), ('Bob'), ('Carol');
INSERT INTO products (name, price) VALUES ('Widget', 9.99), ('Gadget', 19.99);
INSERT INTO purchases (customer_id, product_id, quantity) VALUES
    (1, 1, 3), (1, 2, 1), (2, 1, 2), (3, 2, 5);

`-- 1. plain SELECT`
SELECT name, price FROM products ORDER BY price DESC;

`-- 2. WHERE`
SELECT * FROM purchases WHERE quantity > 2;

`-- 3. JOIN`
SELECT customers.name, products.name, purchases.quantity
FROM purchases
JOIN customers ON purchases.customer_id = customers.id
JOIN products ON purchases.product_id = products.id;

`-- 4. GROUP BY`
SELECT customer_id, SUM(quantity) AS total_bought
FROM purchases
GROUP BY customer_id;

`-- 5. all four combined`
SELECT customers.name, SUM(purchases.quantity) AS total_bought
FROM purchases
JOIN customers ON purchases.customer_id = customers.id
WHERE purchases.quantity > 1
GROUP BY customers.name
ORDER BY total_bought DESC;    

`REAL-WORLD USE: This is the exact skill real SQL work demands day to day — not recalling one clause in isolation, but building a schema and immediately querying it without needing a reference open. Being able to go from "here's the data I need to model" to "here's the query that answers a real question" cold is the actual bar for basic SQL fluency, and it's what this whole week has been building toward.`

## September 8 (Day 48) systemctl basics — status, start, stop, restart a service, list active services with systemctl list-units.

`Definition:`
1. **systemd** — the modern init system most Linux distributions use to manage background services (daemons) — things like web servers, databases, SSH, cron.
2. `systemctl status service_name` — shows whether a service is running, its recent log output, and its process ID.
3. `systemctl start service_name` — starts a service that isn't currently running.
4. `systemctl stop service_name` — stops a running service.
5. `systemctl restart service_name` — stops and immediately starts a service again (useful after a config change).
6. `systemctl list-units --type=service` — lists every currently loaded service unit and its state (active, inactive, failed).
7. Most `systemctl` actions that change state (`start`/`stop`/`restart`) require `sudo`, since services often run as other users or affect the whole system.

**WORKED EXAMPKES:**
systemctl status ssh
` ● ssh.service - OpenBSD Secure Shell server`
`      Loaded: loaded (/lib/systemd/system/ssh.service; enabled)`
`      Active: active (running) since Mon 2026-09-08 09:00:12 UTC`               `    Main PID: 812 (sshd)`

sudo systemctl stop ssh
systemctl status ssh
`      Active: inactive (dead)`

sudo systemctl start ssh
systemctl status ssh
`      Active: active (running)`

sudo systemctl restart ssh
` stops then starts in one command — common after editing /etc/ssh/sshd_config`

systemctl list-units --type=service
` UNIT                LOAD   ACTIVE SUB     DESCRIPTION`
` cron.service        loaded active running Regular background program processing daemon`
` ssh.service         loaded active running OpenBSD Secure Shell server`
` nginx.service       loaded active running A high performance web server`

systemctl list-units --type=service --state=failed
` quickly spot anything that crashed or failed to start`

**REAL-WORLD USE: systemctl status is the very first command to run when something isn't responding — is the service even running? did it crash? what's the last thing it logged? restart is the standard move after changing a service's config file, since most services don't pick up config changes until they're restarted. list-units --state=failed is a quick way to scan a whole server for anything broken without checking each service individually — genuinely useful during an incident when you don't know yet what's wrong.**

## September 9 (Day 49) systemctl enable/disable (persistence across reboot), intro to journalctl for reading service logs.

**DEFINETION:**
1. `systemctl start`/`stop` (from yesterday) only affects the **current** boot session — if the server reboots, the service goes back to whatever its default was.
2. `systemctl enable service_name` — configures a service to start **automatically** on every future boot. Doesn't start it right now, just sets it up for next time.
3. `systemctl enable --now service_name` — enables it for future boots **and** starts it immediately, in one command.
4. `systemctl disable service_name` — removes a service from auto-start on boot. Doesn't stop it if it's currently running — just stops it from coming back after a reboot.
5. `systemctl is-enabled service_name` — quickly checks whether a service is set to auto-start, without needing the full `status` output.
6. `journalctl` — reads the systemd journal, the centralized log system that captures output from every systemd-managed service.
7. `journalctl -u service_name` — shows logs for one specific service/unit.
8. `journalctl -u service_name -f` — "follow" mode, same idea as tail -f, streams new log lines live.
9. `journalctl -u service_name --since "1 hour ago"` — filters logs by time.

**WORKED EXAMPLES:**
systemctl is-enabled nginx
` disabled`
` won't come back automatically on reboot right now`

sudo systemctl enable nginx
` Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service...`

systemctl is-enabled nginx
` enabled`

sudo systemctl enable --now nginx
` enabled AND started in one command`
systemctl status nginx
`      Active: active (running)`

sudo systemctl disable nginx
systemctl status nginx
`      Active: active (running)`
`      (still running right now — disable only affects future boots)`

journalctl -u nginx
` Sep 09 09:15:01 myserver nginx[812]: Starting nginx...`
` Sep 09 09:15:02 myserver nginx[812]: nginx started successfully`
` Sep 09 10:02:14 myserver nginx[812]: 502 Bad Gateway on /api/status`

journalctl -u nginx --since "1 hour ago"
` only recent entries — useful when a service has years of accumulated logs`

**REAL-WORLD USE: enable/disable is exactly what separates "works until the next reboot" from "actually production-ready" — a critical service that isn't enabled will silently fail to come back after a server restart or crash, which is a genuinely common real incident cause. enable --now is the one-liner you'll use constantly when setting up a new service for the first time. journalctl -u service_name is usually the very next step after systemctl status shows something's wrong — status gives you the summary, journalctl gives you the actual history to figure out why it failed or what it was doing right before it crashed. -f paired with -u is the direct systemd equivalent of tail -f on a plain log file, which you already know from Day 12.**

## September 10 (Day 50) netstat/ss basics — list open/listening ports, difference between LISTEN and ESTABLISHED states.

**DEFINITION:**
1. **Port** — as covered back on Day 25, a number identifying a specific service on a machine. A "listening" port means something is actively waiting for incoming connections on it.
2. `netstat` — older, traditional tool for viewing network connections and listening ports. Still widely known, though increasingly considered legacy.
3. `ss` — "socket statistics," the modern replacement for netstat; faster and the recommended tool on current systems, though netstat still shows up constantly in older docs/scripts.
4. `ss -tuln` — a common combo:
     -t TCP, -u UDP, -l listening sockets only, -n show numeric ports instead resolving service names (faster, and avoids DNS lookups).
5. Connection states:
   `LISTEN` — nothing connected yet; the service is just waiting for a connection to come in.
   `ESTABLISHED` — an active, currently-open connection between two endpoints, with data actively able to flow both ways.

**WORKED EXAMPLES:**
netstat -tuln
` Proto Recv-Q Send-Q Local Address     Foreign Address   State`
` tcp   0      0      0.0.0.0:22        0.0.0.0:*         LISTEN`
` tcp   0      0      0.0.0.0:80        0.0.0.0:*         LISTEN`
` tcp   0      0      127.0.0.1:5432    0.0.0.0:*         LISTEN`

ss -tuln
` State    Recv-Q Send-Q Local Address:Port  Peer Address:Port`
` LISTEN   0      128    0.0.0.0:22          0.0.0.0:*`
` LISTEN   0      511    0.0.0.0:80          0.0.0.0:*`
` LISTEN   0      128    127.0.0.1:5432      0.0.0.0:*`
` same information, different tool, modern default`

ss -tun
` (no -l) — shows active connections too, not just listening ones`
` State       Local Address:Port     Peer Address:Port`
` ESTABLISHED 192.168.1.10:22        203.0.113.5:51422`
` LISTEN      0.0.0.0:80             0.0.0.0:*`

ss -tulnp
` adds -p to show which PROCESS owns each listening port`
` LISTEN   0.0.0.0:80    users:(("nginx",pid=812,fd=6))`
` (often needs sudo to see process names for ports you don't own)`

ss -tuln | grep :22
` filter the output down to one port you care about — same grep habit from Week 1`

**REAL-WORLD USE: Checking listening ports is one of the first things to do when diagnosing "why can't I connect to this service" — if the port isn't in LISTEN state, the service either isn't running or isn't configured to listen where you expect (e.g. bound to 127.0.0.1 only, not 0.0.0.0). ESTABLISHED connections tell you who's actually talking to a server right now — useful for spotting unexpected connections during a security check, or confirming a client is actually connected during debugging. ss largely replaced netstat on modern systems because it's faster and pulls from the kernel more directly, but you'll still see netstat in plenty of older tutorials, scripts, and job environments, so recognizing both matters.**

## September 11 (Day 51) Combine both — pick a running service, confirm it's active with systemctl status, then find its listening port with ss -tulpn. This is the actual skill: connecting a service to its port.

**DEFINITION:** 
This is an integration day — no brand-new syntax, but one new flag combo worth calling out:

1. `ss -tulpn` — everything from Day 50's `-tuln`, plus `-p` (show the owning process/PID). Combined, this is the single command that answers "what's listening on this port, and what process is it?"
2. The actual skill today: going from "I know a service exists" (`systemctl status`) to "I know exactly which port it's bound to and can prove it" (`ss -tulpn`), and tying the two together by matching the PID.

**WORKED EXAMPLES:**

`Step 1 — confirm the service is active`
systemctl status nginx
` ● nginx.service - A high performance web server`
`      Active: active (running) since Fri 2026-09-11 09:00:00 UTC`
`    Main PID: 812 (nginx)`

`Step 2 — find its listening port`
sudo ss -tulpn
` Netid State  Local Address:Port   Process`
` tcp   LISTEN 0.0.0.0:80           users:(("nginx",pid=812,fd=6))`
` tcp   LISTEN 0.0.0.0:22           users:(("sshd",pid=634,fd=3))`

`Step 3 — connect the dots`
sudo ss -tulpn | grep 812
` tcp   LISTEN 0.0.0.0:80   users:(("nginx",pid=812,fd=6))`
` same PID from systemctl status shows up here — confirmed:`
` nginx (PID 812) is the process listening on port 80`

`A second example, working the other direction (port → service)`
sudo ss -tulpn | grep :5432
` tcp   LISTEN   127.0.0.1:5432   users:(("postgres",pid=1204,fd=7))`

systemctl status postgresql
`    Main PID: 1204 (postgres)`
` same PID — confirms this IS the service bound to 5432`

**REAL-WORLD USE: This is the actual troubleshooting workflow you'll use constantly: "the app can't reach the database" starts with checking whether the database service is even active (systemctl status), then confirming it's actually listening on the port the app expects (ss -tulpn) — and if the port's wrong, bound to the wrong address (127.0.0.1 instead of 0.0.0.0), or owned by a different process than you assumed, you've found the bug without guessing. Matching PIDs between the two commands is the concrete proof step — anyone can assume a service owns a port; confirming it by PID is what separates a guess from a diagnosis.**

## September 12 (Day 52) Sign up for your free-tier AWS/Azure/GCP account, verify it, and set a billing alert immediately (before anything else) so nothing surprises you later.

`I HAVE DONE IT!`

**WHAT SHOULD I REMEMBER: This is a genuinely important habit, not a formality — "I forgot to set a billing alert and got a surprise charge" is one of the most common early mistakes people make with cloud accounts, and it's completely avoidable with five minutes of setup before you launch anything. Every cloud engineer sets budget alerts as one of the first things on any new account, for exactly this reason — it's cheap insurance against a config mistake (like accidentally leaving an expensive instance running) turning into a real bill.**

## September 13 (Day 53) Explore the console — no building. Look at IAM (users/roles), regions/availability zones, and the main service dashboard. Just get oriented to where things live.

**DEFINITON:**
1. **IAM (Identity and Access Management)** — where users, roles, and permissions live. Controls *who* can do what in your account.
2. **Root user** — the account you signed up with; has unrestricted access to everything, including billing. Best practice (worth knowing now, acting on later): avoid using the root user for day-to-day work — create a separate IAM user with limited permissions instead.
3. **User** — an identity (a person, or a script) with its own credentials and permissions.
4. **Role** — a set of permissions that can be *assumed* temporarily by a user or a service — not tied to one specific person's long-term credentials. Used heavily for letting one service talk to another securely.
5. **Region** — a geographic area where a cloud provider has data centers (e.g. `us-east-1`, `u-west-1`). Resources you launch are tied to a specific region.
6. **Availability Zone (AZ)** — an isolated data center *within* a region. Regions typically have 2–6 AZs, so a failure in one AZ doesn't take down the whole region.
7. **Service dashboard** — the main console screen listing every available service (compute, storage, databases, networking, etc.) — often organized by category, with a search bar since providers offer hundreds of services.

**WORKED EXAMPLES:**
`IAM — just look, don't create anything yet`
Console → IAM (or "Identity and Access Management")

You should see:
- Users: likely empty, or just showing your root account context
- Roles: probably several pre-existing service-linked roles already present
- Policies: the actual permission documents attached to users/roles
  (e.g. "AmazonS3ReadOnlyAccess" — a policy granting read-only access to S3)

`Regions — check what's selected, and what's available`
Console → top-right region selector (AWS) or equivalent

Currently selected region: e.g. us-east-1 (N. Virginia)

Click the dropdown — you'll see a list like:
us-east-1 (N. Virginia)
us-west-2 (Oregon)
eu-west-1 (Ireland)
ap-southeast-1 (Singapore)
... often 20-30+ regions total

Note: resources in one region are generally invisible from another —
if you launch something in us-east-1, switching to us-west-2 won't show it.

`Availability Zones — within your selected region`
Console → EC2 (or equivalent compute service) → note the AZ options
when launching (even without launching anything)

us-east-1a
us-east-1b
us-east-1c
— each is a physically separate data center within the same region

`Service dashboard`
Console → main dashboard / "All services"

Broad categories you'll typically see:
- Compute (virtual machines)
- Storage (object storage, block storage)
- Databases
- Networking (VPC, load balancers)
- IAM/Security
- Monitoring (CloudWatch or equivalent)

Use the search bar rather than browsing — with hundreds of services,
searching "EC2" or "compute" is faster than scanning categories.

**REAL-WORLD USE: Understanding IAM's users/roles/policies structure now, even without creating anything, sets up next week's actual VM launch — you'll need at least a basic grasp of permissions before you can reason about why something is or isn't accessible. Knowing that resources are region-scoped is one of those things that trips up almost everyone once: launching a VM, switching tabs, and panicking because "it disappeared" — when really you just switched regions in the console. AZs matter the moment you care about reliability — production systems are typically spread across multiple AZs specifically so one data center's outage doesn't take the whole service down.**

## September 14 (Day 54) Tie it together — in the console, find where "security groups" or firewall rules live and connect that mentally to what ss/netstat showed you locally (cloud firewall = port control at the network level, same concept you just practiced). Review the week.

**DENITION:** 
1. **Security group (AWS term) / firewall rule / NSG (Azure: Network Security Group)** — a virtual firewall controlling what traffic is allowed to reach a cloud resource (like a VM), at the *network* level — before traffic even reaches the machine's own OS.
2. **Inbound rule** — controls traffic *coming* into the resource (e.g. "allow port 22 from my IP only").
3. **Outbound rule** — controls traffic *leaving* the resource (often left wide-open by default, since outbound is usually less risky than inbound).
4. A rule typically specifies: protocol (TCP/UDP), port range, and source (a specific IP, a range, or "anywhere" — `0.0.0.0/0`).
5. **The key mental connection today:** `ss -tulpn` (Day 50/51) shows you what's listening *on the machine itself*. A security group controls whether traffic is even allowed to *reach* that listening port from outside in the first place. A port can show `LISTEN` locally and still be completely unreachable from the internet if the security group blocks it — these are two separate layers, and both have to allow the traffic.

**WORKED EXAMPLES:**
`Finding security groups in the console (conceptual — AWS naming, other providers use equivalent terms)`
Console → EC2 → Security Groups (left sidebar)
  or: Console → VPC → Security Groups

You'll see a list (likely just a "default" one right now, since you haven't
launched anything yet). Click into it:

Inbound rules:
  Type    Protocol  Port   Source
  SSH     TCP       22     0.0.0.0/0   (default — allows SSH from anywhere)

Outbound rules:
  Type       Protocol  Port    Destination
  All traffic  All       All     0.0.0.0/0   (default — allows all outbound)

`Connecting the two layers conceptually`
Scenario: you launch a VM, SSH into it, and run:

ss -tulpn
` tcp   LISTEN   0.0.0.0:80   users:(("nginx",pid=812))`

This tells you: nginx IS listening on port 80, ON THE MACHINE.

But if you visit http://your-vm-ip in a browser and it times out,
the next place to check isn't the machine at all — it's the
security group. If there's no inbound rule allowing port 80,
the request never reaches the VM to begin with — ss would never
even show it, because the OS never saw the connection attempt.

Two separate gates, both must be open:
  Internet → [Security Group: is port 80 allowed in?] → [VM's own listening port: is nginx actually bound to 80?]

**Week Review (Days 48–54)**
`You went from managing individual services to understanding the full path from "is my service even reachable":`
1. **Day 48** — `systemctl status`/`start`/`stop`/`restart`, listing services.
2. **Day 49** — `enable`/`disable` for boot persistence, `journalctl` for service logs.
3. **Day 50** — `netstat`/`ss`, `LISTEN` vs `ESTABLISHED`.
4. **Day 51** — connecting a service to its port by matching PIDs.
5. **Day 52** — cloud account + billing alert (safety first).
6. **Day 53** — console orientation: IAM, regions/AZs, service dashboard.
7. **Day 54** — security groups, and how they relate to what you already know about local ports.

**REAL-WORLD USE: This exact two-layer distinction — "is the security group letting traffic in?" vs. "is the service actually listening?" — is one of the single most common troubleshooting sequences in real cloud work: "I can't reach my server" almost always comes down to one of these two, and knowing to check both (rather than assuming it's a code bug) saves enormous amounts of debugging time. Restricting SSH's source to your own IP instead of 0.0.0.0/0 is also a genuinely important real habit — leaving SSH open to the entire internet on a real VM is one of the most common ways servers get automated attack attempts within minutes of being launched.**

## September 15 (Day 55)  Launch the VM — pick a region, free-tier instance size, and OS (Ubuntu is the easy match for everything you've practiced). Note the public IP once it's running.
**IM FINALLY CAUGHT UP!**

**DEFINITION:**
1. **Instance** — the cloud term for a virtual machine — a provisioned slice of compute you can SSH into and use like a real server.
2. **AMI (Amazon Machine Image)** / equivalent — the base OS image an instance boots from. Ubuntu is the natural pick here since every command you've practiced (`ls`, `grep`, `systemctl`, `ss`) is native to it.
3. **Instance type/size** — determines CPU/RAM allocated. Free-tier eligible types are explicitly labeled as such in the console (AWS: `t2.micro` or `t3.micro`; Azure: B1s; GCP: e2-micro) — stick to exactly what's marked free-tier eligible.
4. **Key pair** — this is where Day 33's SSH key pair becomes real: when launching, you'll either upload your existing public key or generate a new pair — use the one you already made if the provider allows importing an existing public key, so you're connecting with a key you understand.
5. **Public IP** — the address the internet uses to reach your instance. Typically assigned automatically on launch for free-tier instances, shown in the instance's details once it's running.

**WORKED EXAMPLES:**
**Launch sequence (conceptual — AWS naming, equivalent steps on Azure/GCP):**

Console → EC2 → Launch Instance

1. Name: something identifiable, e.g. "study-vm-01"
2. AMI: Ubuntu Server 24.04 LTS (or latest LTS available) — free-tier eligible
3. Instance type: t2.micro or t3.micro — confirm "Free tier eligible" label is shown
4. Key pair:
     - "Create new key pair" (if you didn't set one up), OR
     - Import the PUBLIC key from Day 33 (~/.ssh/id_ed25519.pub) if the console allows it
5. Network settings: use the default VPC/security group for now — but EDIT
   the inbound rule so SSH (port 22) source is "My IP" instead of 0.0.0.0/0
   (this is Day 54's lesson, applied for real)
6. Storage: default (usually 8GB free-tier eligible) is fine
7. Review → Launch Instance

**Confirming it's running and finding the IP**

Console → EC2 → Instances

Instance State: running
Public IPv4 address: 54.221.XX.XX   <- write this down, you'll use it Day 56+

**A quick sanity check — is it actually up before you try SSH**

systemctl status  →  (this is a local command; you'll run it ON the instance
                       once you SSH in, tomorrow — today is just launch + confirm)

For today, confirming "running" state + public IP in the console is enough.

**REAL-WORLD USE: This is the moment everything from the last two months stops being local practice and becomes a real, internet-reachable machine — the same one you'll SSH into with your Day 33 key, check services on with systemctl, and verify ports on with ss, exactly as you've been practicing, except now for real. Restricting the SSH inbound rule to "My IP" instead of leaving it open to 0.0.0.0/0 at launch time — rather than fixing it later — is a genuinely good habit; plenty of real breaches trace back to a default-open SSH rule that nobody circled back to lock down.**

## September 16 (Day 56) SSH in using your Day 27 keys — you'll need to open port 22 in the security group first (this is where Week 2's console orientation pays off). Confirm you're actually on the remote box, not local.

**DEFINITION:**
1. `ssh -i /path/to/private_key user@public_ip` — connects to a remote host using a specific private key file. `-i` ("identity file") points at the private key; without it, SSH only checks its default key names.
2. **Default usernames by image** — you don't log in as `root`. Ubuntu images use `ubuntu`; Amazon Linux uses `ec2-user`; Debian uses `admin`. Using the wrong one is the single most common first-attempt failure.
3. **Key permissions** — SSH refuses to use a private key that's readable by others. If you get `WARNING: UNPROTECTED PRIVATE KEY FILE`, fix it with chmod 600 (Day 8's octal math, applied for real).
4. **Host key fingerprint prompt** — on first connection you'll see "The authenticity of host ... can't be established. Are you sure you want to continue connecting?" Typing `yes` adds it to `~/.ssh/known_hosts` so future connections skip the prompt.
5. **Security group port 22** — as covered Day 54, the inbound rule must allow TCP/22 from your IP, or the connection times out before SSH even gets a chance to authenticate.

**WORKED EXAMPLES:**
**Confirming the security group first (before you try connecting)**

Console → EC2 → Instances → select your instance → Security tab → Security groups

Inbound rules should include:
  Type   Protocol   Port   Source
  SSH    TCP        22     YOUR_IP/32

`If your home IP changed since Day 55 (it can, on most residential connections), this is exactly where the "My IP" rule silently stops matching — update it before debugging anything else.`

**Connecting**

bash
chmod 600 ~/.ssh/id_ed25519
` SSH will refuse the key if it's group- or world-readable`

ssh -i ~/.ssh/id_ed25519 ubuntu@54.221.XX.XX
` The authenticity of host '54.221.XX.XX' can't be established.`
` ED25519 key fingerprint is SHA256:abc123...`
` Are you sure you want to continue connecting (yes/no)? yes`
` Warning: Permanently added '54.221.XX.XX' to the list of known hosts.`
`
` Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-1012-aws x86_64)`
` ubuntu@ip-172-31-XX-XX:~$`

**Confirming you're actually on the remote box, not local**

bash
whoami
` ubuntu        <- Day 1, finally doing real work`

hostname
` ip-172-31-XX-XX    <- an internal AWS-style hostname, not your laptop's name`

pwd
` /home/ubuntu       <- not /home/yourname or /Users/yourname`
bash
ip addr | grep inet
` inet 172.31.XX.XX/20 ... <- the PRIVATE IP, not the public one you connected to`
` the VM doesn't know its own public IP — that mapping happens at the network layer`

**Common failures and what they actually mean**

bash
ssh -i ~/.ssh/id_ed25519 ubuntu@54.221.XX.XX
` ssh: connect to host 54.221.XX.XX port 22: Connection timed out`
` → security group is blocking you (or your IP changed). Not a key problem.`

` Permission denied (publickey)`
` → you reached the machine fine, but the key or username is wrong.`
`   Timed out = network layer. Permission denied = auth layer. Different fixes.`

**REAL-WORLD USE: That distinction between "connection timed out" and "permission denied" is worth internalizing now, because it's the fastest diagnostic split in all of SSH work: a timeout means your packets never arrived (firewall, security group, wrong IP, instance not running), while permission denied means you reached the server and it rejected your credentials (wrong key, wrong username, key not in authorized_keys). Checking whoami/hostname immediately after connecting is also a habit worth building early — running a destructive command on your laptop while believing you're on the remote box is a mistake that's embarrassingly easy to make once you have several terminal tabs open.**

## September 17 (Day 57) Basic VM hygiene — apt update && apt upgrade, poke around the filesystem, confirm your Linux commands from earlier weeks work identically here (they should — that's the point).

**DEFINITION:**
1. **APT (Advanced Package Tool)** — Ubuntu/Debian's package manager: installs, updates, and removes software.
2. `sudo apt update` — refreshes the local list of available packages and versions from the repositories. It does **not** install or upgrade anything — it just updates what APT *knows* about.
3. `sudo apt upgrade` — actually installs newer versions of packages you already have, based on the list `update` just refreshed.
4. `sudo apt update && apt upgrade` — the `&&` runs the second command only if the first succeeds, which is the whole point: upgrading against a stale package list is pointless.
5. `-y` flag — auto-confirms the "do you want to continue?" prompt: `sudo apt upgrade -y`.
6. **Key filesystem locations on a real server:**
   1. `/etc` — system-wide configuration files.
   2. `/var/log` — log files.
   3. `/home` — user home directories.
   4. `/usr/bin` — most installed executables.
   5. `/tmp` — temporary files, often cleared on reboot.

**Worked examples:**

**Updating**

bash
sudo apt update
` Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease`
` Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]`
` ...`
` 23 packages can be upgraded. Run 'apt list --upgradable' to see them.`
bash
apt list --upgradable
` lists exactly what would change, before you commit to it`
bash
sudo apt upgrade -y
` unpacks and installs the newer versions`

**Poking around the filesystem — all Day 1–8 commands, unchanged**

bash
pwd
` /home/ubuntu`

ls -la /etc | head -n 10
` every config file the system uses`

ls -la /var/log
` syslog, auth.log, cloud-init.log, dpkg.log ...`

du -sh /var/log
` 4.2M    /var/log      <- Day 22, on a real server`

df -h
` Filesystem      Size  Used Avail Use% Mounted on`
` /dev/root       7.6G  2.1G  5.5G  28% /`

Confirming earlier weeks' commands behave identically

bash
grep -i "ssh" /var/log/auth.log | tail -n 5
` your own login attempts from yesterday show up here — Day 13 + Day 12, real data`

systemctl status ssh
`      Active: active (running)      <- Day 48`

ss -tuln
` LISTEN 0.0.0.0:22     <- Day 50, and now you can see exactly why it's the only one`

ps aux | head -n 10
` Day 17, on a machine where the processes actually mean something`

**One thing genuinely worth checking on a fresh server**

bash
grep "Failed password" /var/log/auth.log | wc -l
` on a server with SSH open to 0.0.0.0/0, this number climbs within hours.`
` with your security group scoped to your IP, it should be ~0 — direct`
` evidence that Day 54's rule is doing something real.   `

**REAL-WORLD USE: apt update && apt upgrade is the first command run on essentially every freshly provisioned server, because a base image is a snapshot from whenever the provider built it — often weeks or months of security patches behind. The reason this day exists at all, though, is the second half: every command you drilled on CoCalc or WSL behaves identically here, on a real machine reachable from the internet. That's not a coincidence, it's the entire value of having learned the terminal rather than a GUI — the skills transfer to any Linux box, anywhere, with no translation.**

## September 18 (Day 58) Install something basic — nginx is the natural pick since it gives you something visible to test later. Start it with `systemctl start`/`enable`, same commands as Week 2.

**DEFINITION:**
1. `sudo apt install package_name` — downloads and installs a package plus its dependencies. Run `apt update` first (Day 57) so APT is working from a fresh package list.
2. **nginx** — a web server. Installing it gives you a real service that binds to a real port and serves a real page, which makes every check you've learned (`systemctl`, `ss`, `journalctl`, security groups) suddenly visible instead of abstract.
3. On Ubuntu, APT typically **starts and enables** a service automatically right after installing it — so you may find nginx already running before you touch `systemctl`. Confirming that, rather than assuming, is part of today.
4. `systemctl start` vs `enable` — Day 49's distinction, now on a machine that can actually reboot: `start` affects right now, `enable` affects every future boot.
`curl localhost` — tests the service **from the machine itself**, bypassing the security group entirely. This separates "is the service working?" from "is the network letting anyone in?"

**WORKED EXAMPLES:**
**Installing**

bash
sudo apt update
sudo apt install nginx -y
` Setting up nginx (1.24.0-...) ...`
` Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service ...`

`That symlink line is APT enabling the service for you — the same thing systemctl enable does.`

**Confirming state rather than assuming it**

bash
systemctl status nginx
` ● nginx.service - A high performance web server and a reverse proxy server`
`      Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; ...)`
`      Active: active (running) since Fri 2026-09-18 03:12:44 UTC`
`    Main PID: 1487 (nginx)`
bash
systemctl is-enabled nginx
` enabled`
bash
sudo systemctl start nginx
sudo systemctl enable nginx
` both likely say it's already done — running them anyway is harmless and confirms it`

**Proving it's actually serving, from the machine itself**

bash
curl localhost
` <!DOCTYPE html>`
` <html>`
` <head>`
` <title>Welcome to nginx!</title>`
` ...`
bash
sudo ss -tulpn | grep nginx
` tcp  LISTEN  0.0.0.0:80   users:(("nginx",pid=1488,fd=6))`
` tcp  LISTEN  [::]:80      users:(("nginx",pid=1488,fd=7))`

`Match that PID against systemctl status nginx — Day 51's exercise, now on your own server.`

**The part that won't work yet, deliberately**

bash
` from your laptop's browser: http://<your-public-ip>`
` → times out`

`Nothing is broken. curl localhost proved nginx is fine; port 80 just isn't open in the security group. That gap is tomorrow's work, and it's worth seeing the failure today so the fix means something.`

**REAL-WORLD USE: Testing with curl localhost before touching firewall rules is the standard order of operations for a reason: it splits one vague problem ("the site doesn't load") into two separate, individually answerable questions. If curl localhost works and the public IP doesn't, the service is fine and it's a network problem — you stop reading application logs entirely and go look at the security group. Reversing that order wastes time on the wrong layer, which is exactly the failure mode Day 54 was setting you up to avoid.**

## September 19 (Day 59) Security groups/firewall rules +15 min — open port 80 in the console for nginx. This is the direct console-mapping of the ss/netstat concept from Week 2: a security group rule is just a cloud-level version of "what port is listening."

**DEFINITION:**
1. Yesterday ended with `curl localhost` working but the public IP timing out — that gap is a missing **inbound rule**. Today closes it.
2. Adding an inbound rule doesn't touch the VM at all — it's a network-level permission slip, evaluated *before* traffic ever reaches nginx's listening socket.
3. The rule needs: protocol (TCP), port (80), and source (`0.0.0.0/0` — unlike SSH, a public web server is *meant* to be reachable from anywhere, so this is one of the rare cases where wide-open is correct instead of a mistake).
4. **The direct mapping to Week 2, stated plainly**: `ss -tulpn` on the machine tells you what's listening. A security group rule tells you what's *allowed* to *reach* what's listening. Yesterday you confirmed the first half (nginx: `LISTEN` on `0.0.0.0:80`). Today you add the second half.

**Worked examples:**
**Adding the rule (conceptual — AWS naming; Azure NSG / GCP firewall rules follow the same shape)**

Console → EC2 → Instances → select your instance → Security tab
→ click the security group name → Inbound rules → Edit inbound rules
→ Add rule:

    Type: HTTP
    Protocol: TCP
    Port range: 80
    Source: Anywhere-IPv4 (0.0.0.0/0)

→ Save rules

**Confirming the rule exists:**

Inbound rules now show:
  Type   Protocol  Port   Source
  SSH    TCP       22     YOUR_IP/32       <- Day 55/56, unchanged
  HTTP   TCP       80     0.0.0.0/0        <- new

**Testing — from your laptop, not the VM:**

bash
curl http://54.221.XX.XX
` <!DOCTYPE html>`
` <html>`
` <head>`
` <title>Welcome to nginx!</title>`
` ...`
` same HTML you saw with curl localhost yesterday — now reachable from outside`
Or just open http://<your-public-ip> in a browser — the nginx welcome page loads.

**If it still doesn't work — the two-layer check, applied:**

bash
` On the VM, confirm nginx is still listening (should be unchanged from yesterday):`
sudo ss -tulpn | grep :80

` If that's fine but the browser still times out:`
` - double check the rule actually saved (sometimes it's easy to click away before saving)`
` - confirm you're hitting the PUBLIC ip, not the private one from Day 56's ip addr`

**Real-world use: This is the exact moment the two halves of the last two weeks click into one working system: a service running and listening (systemctl + ss) is necessary but not sufficient — the network has to allow the traffic too. Every real "why can't users reach my site" incident that isn't a code bug traces back to exactly this checklist, in exactly this order: is the process running, is it listening on the right port/interface, and is the firewall letting the request through. You've now built and diagnosed all three layers yourself, on a real machine, rather than just reading about them.**

## September 20 (Day 60) Verify from outside — curl your VM's public IP from your own machine (or browser) and confirm you get nginx's response back. Ties together SSH, systemctl, and the curl/HTTP work from Day 28.

**DEFINITION:**
No new command today — this is the day everything from Days 28–59 gets proven end-to-end, from both directions at once:

1. From your **laptop**: `curl` (Day 34) hits the public IP over the internet.
2. On the **VM**: `journalctl`/log files (Day 12, 13, 49) show that exact request arriving in real time.
3. Seeing both sides of the same request — sent from outside, received and logged inside — is the actual proof that SSH access, `systemctl`-managed nginx, the security group rule, and HTTP itself are all correctly wired together, not just individually working in isolation.

**WORKED EXAMPLES:**
**Step 1 — open a live view on the VM, before you request anything**

bash
` SSH session, on the VM:`
sudo tail -f /var/log/nginx/access.log
` leave this running — nothing will print yet`

**Step 2 — from your laptop, in a separate terminal, make the request**

bash
curl -i http://54.221.XX.XX
` HTTP/1.1 200 OK`
` Server: nginx/1.24.0`
` Content-Type: text/html`
` Content-Length: 615`
` ...`
` <!DOCTYPE html>`
` <html>`
` ...`

`-i` (Day 34) shows the status line and headers above the body — confirming `200 OK` explicitly, not just assuming success because HTML came back.`

**Step 3 — watch it land, on the VM**

bash
` back in the SSH session, the tail -f window now shows:`
54.123.45.67 - - [20/Sep/2026:14:32:07 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.4.0"

`That's your laptop's IP, your exact request, logged the instant it arrived — the request genuinely traveled internet → security group → nginx → its own log file, and you can see every link in that chain from the VM's side.`

**Step 4 — do it once more from a browser, for a different signature**

Open http://54.221.XX.XX in a normal browser tab.

New line appears in the tail -f window:
54.123.45.67 - - [20/Sep/2026:14:33:41 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 ..."

Same IP, different User-Agent string — curl identifies itself as curl/x.x.x, a browser identifies itself very differently. Worth noticing once, since access logs are read this way constantly in real troubleshooting.

**Step 5 — Ctrl+C to stop watching, exit to disconnect**

bash
exit
` back to your laptop's own prompt`

**Real-world use: Watching a log file live while triggering the request yourself is one of the most reliable debugging habits in real ops work — instead of guessing whether a request even reached the server, you watch it arrive in real time and read exactly what the server saw and how it responded. This is precisely how you'd diagnose a flaky endpoint in a real job: reproduce the request, watch the log, read the actual status code and response size the server logged, rather than trusting only what the client reports back.**

## September 21 (Day 61) Review + cleanup — document what you did (README or short post), check free-tier usage/limits so nothing bills you unexpectedly, and decide whether to stop or keep the instance running into Week 4's capstone.

**Definition:**

No new syntax today — three concrete tasks close out Week 3 properly:

1. **Document** what you built — a README or short post, the same habit from Day 32/40, now covering SSH, nginx, security groups, and the full request-path verification from Day 60.
2. **Check free-tier usage** — confirm you're still within the limits set on Day 52, so nothing bills you unexpectedly heading into Week 4.
3. **Decide: stop or keep running** — a genuine tradeoff, not a formality, since Week 4's capstone needs a live VM.

**WORKED EXAMPLES**
**Checking free-tier usage (conceptual — AWS naming)**

Console → Billing → Free Tier (or Cost Management → Free Tier usage)

Look for:
- EC2 instance hours used this month vs. the free-tier allowance
  (typically 750 hours/month for a single t2.micro/t3.micro — comfortably
  covers one instance running continuously all month)
- Data transfer out (usually a separate, smaller free allowance)
- Estimated month-to-date charges — should still read $0.00
Console → Billing → Billing Dashboard

Confirm your Day 52 alarm is still Active, not accidentally disabled.
If you're at 0 of 750 hours used and it's not — that's worth investigating
before Week 4, not after.

**The README (mirrors Day 40's shape, scoped to this week)**

markdown
` Free-Tier VM Setu`

Launched an Ubuntu 24.04 t2.micro instance on [provider], SSH-secured
with an ed25519 key pair, running nginx as a proof-of-concept web service.

` What's running`
- nginx (installed Day 58, enabled at boot)
- SSH restricted to my own IP; HTTP open to 0.0.0.0/0

` Verified`
- Service confirmed active via `systemctl status`
- Listening port confirmed via `ss -tulpn`, matched by PID
- Public reachability confirmed via `curl -i <public-ip>` and live
  `tail -f access.log` while making the request

` What tripped me up`
- [your actual Day 55-60 error log entries — pull the real ones,
  don't invent generic ones]

**The stop-or-keep decision — reasoning through it, not just picking**

Keep running if:
  - Week 4's capstone script needs to run ON this VM (per the roadmap, it does)
  - You're comfortably within free-tier hours (750/month covers this easily)

Stop (not terminate) if:
  - You want a clean break and don't mind re-launching
  - Note: "stop" ≠ "terminate" — stopping preserves the instance/disk and
    you restart it later with the same setup; terminating deletes it
    permanently, and you'd redo Days 55-59 from scratch

Given the roadmap has Week 4 building directly on this VM, keep it running is the straightforward call here — you're well inside the free-tier hour allowance for a single small instance running continuously.

**Real-world use: Checking free-tier usage against the alarm you set weeks ago — rather than just trusting the alarm will fire — is a real habit worth keeping permanently: alarms can misfire, get accidentally disabled, or have thresholds set too high to catch a slow leak. The stop-vs-terminate distinction is one of the more consequential small facts in cloud work — "terminate" being irreversible (the disk is gone, not just paused) has cost people real rebuild time when they meant to just pause something.**

## September 22 (Day 62) Plan it out — pick the public API, decide what data matters, sketch the SQLite schema (table name, columns, types) before writing any code.

**DEFINITION:**
Today's the day before the code — the actual engineering habit being practiced is designing the schema *before* writing a single line of Python, instead of discovering the right columns mid-script the way most first attempts do.

1. **Picking the API** — for a capstone that'll run unattended (via cron eventually), the criteria matter more than the novelty of the data: no auth key required (one less thing to secure/rotate), a stable free endpoint, and a response shape that's actually worth storing over time (numbers that change — price, weather, stats — not static text).
2. **Deciding what data matters** — a real API response is often 20+ fields; storing all of them is rarely useful. The discipline is picking the handful that answer a specific question you actually care about tracking.
3. **Sketching the schema** — table name, column names, and SQLite types (`INTEGER`, `TEXT`, `REAL`), decided on paper/in a comment block *before* opening the API docs to write code. This mirrors Day 41–42: a table models one type of thing, with a primary key, before any `INSERT` happens.
4. `AUTOINCREMENT` — new detail worth knowing now: `id INTEGER PRIMARY KEY AUTOINCREMENT` guarantees IDs never get reused even if rows are deleted, which matters for anything logging a history over time (unlike plain `INTEGER PRIMARY KEY`, which can reuse a deleted row's ID).

**Worked examples:**

**Step 1 — pick the API (an example choice, yours can differ)**

Candidate: Open-Meteo (https://open-meteo.com) — free weather API, no key required.
Endpoint: https://api.open-meteo.com/v1/forecast?latitude=X&longitude=Y&current=temperature_2m,wind_speed_10m

Why this one: no auth, stable, and the data genuinely changes run to run —
worth tracking over time, unlike a static "about" endpoint.

**Step 2 — decide what data matters, before looking at the full response**

Full response includes: latitude, longitude, elevation, timezone,
generationtime_ms, utc_offset_seconds, current_units, current: {temperature_2m,
wind_speed_10m, time}, ...

What actually matters for THIS capstone:
- when the reading was taken
- temperature
- wind speed
Everything else (elevation, generationtime_ms, timezone metadata) — noise
for this purpose. Skip it.

**Step 3 — sketch the schema on paper first**

table: weather_log

column          type      notes
--------------  --------  -----------------------------
id              INTEGER   primary key, autoincrement
fetched_at      TEXT      timestamp of OUR script run (not the API's own time field)
temperature_c   REAL      matches current.temperature_2m
wind_speed_kmh  REAL      matches current.wind_speed_10m

Step 4 — only now, translate the sketch into SQL

`sql`
CREATE TABLE weather_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    temperature_c REAL,
    wind_speed_kmh REAL
);

**A second worked example, different domain, same process**

API: CoinGecko simple price endpoint (no key needed)
Data that matters: coin name, price in USD, when checked
Noise to skip: 24h volume, market cap, other currencies you don't need

table: price_log
column       type      notes
-----------  --------  --------------------------
id           INTEGER   primary key, autoincrement
coin         TEXT      e.g. "bitcoin"
price_usd    REAL
checked_at   TEXT      timestamp of the fetch
sql
CREATE TABLE price_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin TEXT NOT NULL,
    price_usd REAL,
    checked_at TEXT NOT NULL
);

**REAL-WORLD USE: Sketching a schema before touching code is what separates a script that grows painfully (adding columns after the fact, migrating existing rows, breaking old data) from one that's stable from the first run — exactly the same discipline behind Day 41–42's relational modeling, just applied to your own project instead of a given example. Deliberately narrowing "what data matters" down from a large API response to 3–4 meaningful columns is also a real skill: logging everything an API returns feels safer but produces bloated, hard-to-query tables — the useful data usually gets buried, not protected, by the noise.**

## September 23 (Day 63) On the VM, set up your Python environment — `venv` (Day 27 skill), `pip install requests` inside it, confirm `sqlite3` works (it's stdlib, no install needed).

**DEFINITION:**
1. Everything here is Day 33's `venv` skill, applied to a real remote machine instead of your laptop — same commands, new context.
2. `python3 -m venv env_name` — creates an isolated environment. On Ubuntu, `python3` (not `python`) is the standard binary name.
3. `source env_name/bin/activate` — activates it; your prompt prefixes with (`env_name`) once it's on.
4. `pip install requests` — installs into the active environment only, not system-wide. Worth checking `pip --version` first to confirm you're using the venv's pip, not a system one.
5. `import sqlite3` — part of Python's standard library, so it needs no pip install at all, in or out of a venv. Confirming this today (rather than assuming) is the actual point — it's a common early mixup to `pip install sqlite3` and get a confusing error, since the real package name on PyPI is unrelated to the stdlib module.
6. Why a venv matters *specifically* here: this VM may end up running other Python tools later (as the roadmap progresses), and keeping this capstone's dependencies isolated from whatever comes next avoids version conflicts down the line — the exact problem Day 33 described in the abstract, now genuinely relevant.

**Worked examples:**

**On the VM, via SSH**

bash
python3 --version
` Python 3.12.3   <- Ubuntu 24.04's default, confirm it's there before anything else`
bash
cd ~
mkdir capstone && cd capstone
python3 -m venv env
source env/bin/activate
` (env) ubuntu@ip-172-31-XX-XX:~/capstone$`
bash
which python3
` /home/ubuntu/capstone/env/bin/python3`
` confirms you're using the VENV's python, not the system one`

which pip
` /home/ubuntu/capstone/env/bin/pip`
bash
pip install requests
` Collecting requests`
` ...`
` Successfully installed requests-2.32.x certifi-... charset-normalizer-... idna-... urllib3-...`
bash
pip list
` certifi     ...`
` charset-normalizer ...`
` idna        ...`
` requests    2.32.x`
` urllib3     ...`

**Confirming sqlite3 — no install step**

bash
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
` 3.45.1`
` works immediately — stdlib, nothing to install`
bash
pip install sqlite3
` ERROR: Could not find a version that satisfies the requirement sqlite3`
` ERROR: No matching distribution found for sqlite3`
` expected failure — this is the mixup worth seeing once, so you recognize it later`

**A quick end-to-end sanity check before Day 64's real code**

bash
python3 -c "
import requests
import sqlite3
print('requests:', requests.__version__)
print('sqlite3:', sqlite3.sqlite_version)
"
` requests: 2.32.x`
` sqlite3: 3.45.1`
` both imports succeed — environment is ready for tomorrow`
bash
deactivate
` back to the system Python — confirm the venv really did isolate things:`
python3 -c "import requests"
` ModuleNotFoundError: No module named 'requests'`
` expected — requests only exists inside env/, not system-wide`

**REAL-WORLD USE: Confirming sqlite3 needs no install — rather than reflexively pip install-ing everything a script imports — is a small but genuinely common early trip-up, and knowing Python's standard library well enough to recognize what's already there (vs. third-party) saves real time once you're moving faster and not double-checking every import. The deactivate → confirm requests is gone check at the end is worth doing deliberately at least once: it's the actual proof that isolation is real, not just a claim from Day 33's lesson.**

## September 24 (Day 64) Write the API-calling function — request, parse JSON into a dict (Day 29 skill), print it to confirm it works before touching the database.

**Definition:**
1. Today is deliberately scoped to *one* function, tested in isolation, before the database touches it at all — the same discipline as Day 62's "plan before code," now applied to "verify the fetch before you build storage on top of an assumption."
2. `requests.get(url, timeout=10)` — Day 34/35's call, with `timeout` added: a script meant to run unattended (cron, eventually) should never hang forever on a dead connection.
3. `response.raise_for_status()` — Day 38's habit: raises an exception on 4xx/5xx instead of silently handing you a JSON-shaped error page.
4. The function's job today is narrow on purpose: take a URL, return a dict of *only* the fields your Day 62 schema actually needs — not the whole raw response. Trimming down to the schema's shape here means Day 65's insert code doesn't have to do any filtering itself.

**Worked examples:**

**Using the weather example from Day 62's schema (fetched_at, temperature_c, wind_speed_kmh) — substitute your own API/fields if you picked something different:**

python
` fetch.py`
import requests
import datetime

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=14.6&longitude=121.0&current=temperature_2m,wind_speed_10m"


def fetch_weather():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    raw = response.json()

    ` trim down to exactly what the Day 62 schema needs`
    data = {
        "fetched_at": datetime.datetime.now().isoformat(),
        "temperature_c": raw["current"]["temperature_2m"],
        "wind_speed_kmh": raw["current"]["wind_speed_10m"],
    }
    return data


if __name__ == "__main__":
    result = fetch_weather()
    print(result)
bash
source env/bin/activate
python3 fetch.py
` {'fetched_at': '2026-09-24T09:12:03.481200', 'temperature_c': 29.4, 'wind_speed_kmh': 11.2}`

**Confirming it fails sensibly, not silently, before moving on**

python
` quick manual check — temporarily break the URL to see the failure mode`
API_URL = "https://api.open-meteo.com/v1/forecastXXX"
bash
python3 fetch.py
` requests.exceptions.HTTPError: 404 Client Error: Not Found for url: ...`
` raise_for_status() caught it — good, this is the expected shape of failure,`
` not a silent empty dict or a KeyError buried three lines down`

**Revert the URL once you've seen that.**

**REAL-WORLD USE: Printing the trimmed dict and eyeballing it before any INSERT touches the database is a genuinely important habit — it's far easier to spot "wait, that's not the field I meant" in a printed dict than after it's already written into a table you then have to query to notice the mistake. Separating "does the fetch work" from "does the storage work" into two distinct, independently-testable steps is also just good practice generally: when something breaks later, you'll immediately know which half to look at instead of debugging both at once.**

## September 25 (Day 65) Create the SQLite DB and table via Python's sqlite3 module — CREATE TABLE, then write an INSERT function for a single row.

**DEFINITION:**

**WORKED EXAMPLES:**

**REAL-WORLD USE: 