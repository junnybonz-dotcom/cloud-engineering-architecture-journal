
import datetime
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

REGION = "us-east-1"


def get_buckets(s3):
    response = s3.list_buckets()

    rows = [
        (
            bucket["Name"],
            bucket["CreationDate"].strftime("%Y-%m-%d"),
        )
        for bucket in response.get("Buckets", [])
    ]

    return sorted(rows)


def get_instances(ec2):
    rows = []

    # Get every page of EC2 results
    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in inst.get("Tags", [])
                }

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
        code = e.response["Error"]["Code"]
        print(f"  Could not list buckets: {code}")
        return
    except BotoCoreError as e:
        print(f"  S3 connection/configuration error: {e}")
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
        code = e.response["Error"]["Code"]
        print(f"  Could not list instances: {code}")
        return
    except BotoCoreError as e:
        print(f"  EC2 connection/configuration error: {e}")
        return

    if not rows:
        print(f"  (none in {ec2.meta.region_name})")
        return

    print(
        f"  {'NAME':<16} {'INSTANCE ID':<21} "
        f"{'STATE':<12} {'TYPE':<10} PUBLIC IP"
    )

    for name, iid, state, itype, ip in rows:
        print(
            f"  {name:<16} {iid:<21} "
            f"{state:<12} {itype:<10} {ip}"
        )

    print(f"  Total: {len(rows)}")


def main():
    sts = boto3.client("sts", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        identity = sts.get_caller_identity()["Arn"]
    except NoCredentialsError:
        print("No AWS credentials found.")
        return
    except ClientError as e:
        print(f"AWS identity check failed: {e.response['Error']['Code']}")
        return
    except BotoCoreError as e:
        print(f"AWS connection/configuration error: {e}")
        return

    now = datetime.datetime.now(
        datetime.timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")

    print("=" * 65)
    print(f"AWS REPORT | {now}")
    print(f"Identity: {identity}")
    print(f"Region:   {ec2.meta.region_name}")
    print("=" * 65)

    report_buckets(s3)
    report_instances(ec2)


if __name__ == "__main__":
    main()
