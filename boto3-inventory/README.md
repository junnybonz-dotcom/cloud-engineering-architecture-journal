# AWS Inventory Report — Python and Boto3

A read-only Python reporting tool that uses the AWS SDK for Python (`boto3`) to inventory Amazon S3 buckets and EC2 instances in the `us-east-1` region. It identifies the AWS caller, displays bucket creation dates, and reports EC2 instance names, IDs, states, types, and public IP addresses.

## Skills Demonstrated

- Python functions, dictionaries, lists, and formatted output
- AWS SDK for Python (`boto3`)
- AWS Identity and Access Management (IAM)
- AWS STS identity verification
- Amazon S3 and Amazon EC2 API calls
- Pagination of EC2 instance results
- Exception handling for missing credentials, service errors, and connection/configuration problems

## Features

- Lists S3 bucket names and creation dates.
- Lists EC2 instance names, IDs, states, instance types, and public IP addresses.
- Uses an EC2 paginator to retrieve instance results across pages.
- Identifies the AWS caller and displays the configured region.
- Reports errors separately for S3 and EC2 so a problem in one section does not prevent the other section from attempting its report.
- Sorts inventory results for more consistent output.

The report uses `us-east-1`, configured by `REGION` in `aws_report.py`.

## Requirements

- Python 3
- `pip`
- An AWS account with appropriate read permissions
- AWS credentials supplied through a supported AWS credential provider, such as an attached IAM role on EC2 or a configured local AWS profile

## Setup

Create and activate a virtual environment, then install Boto3:

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install boto3
```

## Run

From the directory containing `aws_report.py`:

```bash
python3 aws_report.py
```

On an EC2 instance, an attached IAM role is preferable to storing long-term access keys in the project. For local development, use a configured AWS profile instead of hardcoding credentials.

The script needs permission to list S3 buckets and describe EC2 instances. The AWS identity check uses STS. The effective permissions depend on the identity and policies configured in your AWS account.

## Example Output

Sanitized example from a real run on October 28, 2026. The account ID, session identifier, bucket name, instance ID, and public IP have been masked.

```text
=================================================================
AWS REPORT | 2026-10-28 01:47 UTC
Identity: arn:aws:sts::<ACCOUNT-ID>:assumed-role/report-script-role/<SESSION>
Region:   us-east-1
=================================================================

S3 BUCKETS
  NAME                                     CREATED
  <BUCKET-NAME>                            2026-10-09
  Total: 1

EC2 INSTANCES
  NAME             INSTANCE ID           STATE        TYPE       PUBLIC IP
  study-vm-01      i-<INSTANCE-ID>        running      t3.micro   <PUBLIC-IP>
  Total: 1
```

The inventory varies with the resources visible to the configured AWS identity at runtime.

## Error Handling

The script handles several failure categories:

| Situation | Report behavior |
|---|---|
| No AWS credentials available | Prints a message explaining that credentials were not found. |
| Identity check fails | Reports the relevant AWS error code or connection/configuration issue. |
| S3 API operation fails | Reports the S3 error and continues to the EC2 report. |
| EC2 API operation fails | Reports the EC2 error without hiding the failure. |

## Security Notes

- The script is designed for inventory and does not create, modify, or delete AWS resources.
- Use a dedicated IAM identity with only the permissions needed for the inventory task.
- Prefer an attached IAM role on EC2 or a configured AWS profile for credentials.
- Never commit access keys, secret keys, private keys, credential files, or unredacted sensitive runtime output.
- Review IAM policies before running the script in an account containing production resources.

## Current Repository Status

The reporting scripts currently reside in the AWS VM workspace. Their inclusion in this journal repository is a separate repository-organization task, so this README alone does not constitute a complete fresh-clone runnable package yet.

## What I Learned

This project helped me connect Python with AWS services and practice identity verification, pagination, read-only inventory, and error handling. It also reinforced the importance of using IAM permissions carefully and avoiding hardcoded credentials.
