
---

## November 1-21 - TOO BUSY SLEEPING 

## November 22 — Portfolio Engineering Milestone

### Project Improvements

- Separated the Boto3 AWS Inventory Report into its own repository.
- Improved shared AWS region configuration and pagination.
- Added mocked unit tests for AWS inventory operations.
- Improved the Weather Logger API validation and SQLite handling.
- Added automated tests to the Weather Logger.
- Upgraded the Log Scanner with argparse, regex search, and file-size formatting.
- Upgraded the API Logger with configurable repositories, UTC timestamps, response validation, and JSONL output.

### Engineering Practices

- Added automated unit tests using mocks and temporary files or databases.
- Added GitHub Actions workflows to the four standalone repositories.
- Configured CI to test Python 3.12, 3.13, and 3.14.
- Practiced using feature branches, commits, pull requests, and merges.
- Improved project documentation and repository organization.

### What I Learned

- Why automated tests should not depend on live APIs or cloud resources.
- How mocking helps isolate application behavior.
- How CI can validate code across multiple Python versions.
- Why generated files, caches, and local runtime data should stay out of Git.
- Why project documentation must reflect the actual implementation.

### Next Improvements

- Continue strengthening Linux, Python, SQL, and networking fundamentals.
- Practice reproducing project logic independently.
- Keep project documentation and weekly learning records current.
