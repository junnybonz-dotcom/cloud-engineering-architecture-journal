# Capstone Redo: Gap Report
Date: October 24-25, 2026

## Context
Finals, exams, projects, and clearance delayed my original
Day 90-91 schedule. This was a guided recovery and rebuild,
not a completely independent cold attempt.

## What I Could Recall
- mkdir creates a directory.
- cd changes the current directory.
- python3 -m venv env creates a virtual environment.
- source env/bin/activate activates the environment.
- pip install requests installs the requests library.
- nano creates or edits a file in the terminal.
- curl can inspect the raw API response.
- I understood that fetch.py requests API data and returns
  only selected fields.

## Where I Needed Help
- Writing the SQLite table and insertion functions in db2.py.
- Understanding SQL placeholders and why conn.commit() matters.
- Connecting fetch_weather() and insert_weather() in main2.py.
- Understanding try/except and testing API, field, and database errors.
- Configuring cron with absolute paths and log redirection.
- Organizing both project versions safely in Git.

Assistance note:
I used direct examples and guided troubleshooting. I did not
complete every step independently or follow the original
no-AI rule throughout this recovery.

## What I Successfully Practiced
- Created fetch.py, db2.py, and main2.py.
- Ran the API-to-SQLite pipeline successfully.
- Tested failure scenarios and restored the working code.
- Configured cron to run the new project automatically.
- Changed the test schedule from every minute to every 15 minutes.
- Ran a GROUP BY query on the collected weather data.
- Preserved the original files and copied the redo separately.

## Remaining Gaps
- Rebuild db2.py without looking at the reference.
- Explain SQL placeholders, commits, and database connections.
- Recreate the main2.py error-handling flow independently.
- Configure cron from memory and explain each field.
- Compare the original files against the redo and check important details.

## Practice Plan
1. Rebuild db2.py from memory during the next practice session.
2. Rebuild main2.py and explain every exception handler.
3. Recreate the cron entry without copying the previous command.
4. Review the original-versus-redo differences and correct any gaps.
