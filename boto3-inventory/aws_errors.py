
import sys
import boto3

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,
    NoRegionError,
    ProfileNotFound,
    EndpointConnectionError,
    ConnectTimeoutError,
    SSLError,
)

EXPIRED = {
    "ExpiredToken",
    "ExpiredTokenException",
    "RequestExpired",
}

DENIED = {
    "AccessDenied",
    "AccessDeniedException",
    "UnauthorizedOperation",
}


def describe_error(e):
    if isinstance(e, NoCredentialsError):
        return "No credentials found. Check your AWS credential setup."

    if isinstance(e, PartialCredentialsError):
        return "Credentials are incomplete. Check your AWS credential setup."

    if isinstance(e, ProfileNotFound):
        return "AWS profile not found. Check AWS_PROFILE and your profile names."

    if isinstance(e, NoRegionError):
        return "No region configured. Set the correct AWS region."

    if isinstance(e, SSLError):
        return "TLS/SSL error. Check the system clock and CA certificates; don't disable verification."

    if isinstance(e, (EndpointConnectionError, ConnectTimeoutError)):
        return "Can't reach the AWS endpoint. Check the region and network."

    if isinstance(e, ClientError):
        code = e.response["Error"]["Code"]

        if code in EXPIRED:
            return f"Temporary credentials expired: {code}."

        if code in DENIED:
            return f"Permission denied: {code}."

        return f"AWS returned an error: {code}."

    return f"Unexpected Boto3 error: {type(e).__name__}."


def authenticate():
    try:
        sts = boto3.client("sts")
        return sts.get_caller_identity()["Arn"]

    except (BotoCoreError, ClientError) as e:
        print(f"Cannot continue: {describe_error(e)}")
        sys.exit(1)


def run_checked(label, func, *args):
    try:
        return func(*args)

    except (BotoCoreError, ClientError) as e:
        print(f"[{label}] {describe_error(e)}")
        return None


def list_bucket_names():
    s3 = boto3.client("s3")
    return sorted(
        bucket["Name"]
        for bucket in s3.list_buckets().get("Buckets", [])
    )


def list_instance_summaries(region=None):
    # Client creation is inside run_checked's try block.
    ec2 = boto3.client("ec2", region_name=region)
    rows = []

    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                rows.append((
                    inst["InstanceId"],
                    inst["State"]["Name"],
                ))

    return rows


def main():
    print(f"Authenticated as: {authenticate()}")

    buckets = run_checked("S3", list_bucket_names)

    if buckets is not None:
        print(f"Buckets ({len(buckets)}): {', '.join(buckets) or '(none)'}")

    instances = run_checked("EC2", list_instance_summaries)

    if instances is not None:
        print(f"Instances ({len(instances)}):")

        for instance_id, state in instances:
            print(f"  {instance_id}  {state}")


if __name__ == "__main__":
    main()
