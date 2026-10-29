import sys
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def format_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024

    return f"{num_bytes:.1f} TB"


def list_objects(bucket, prefix=""):
    s3 = boto3.client("s3")
    total = 0

    try:
        paginator = s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(
            Bucket=bucket,
            Prefix=prefix
        ):
            objects = page.get("Contents", [])

            for obj in objects:
                modified = obj["LastModified"].strftime(
                    "%Y-%m-%d %H:%M UTC"
                )

                print(
                    f"{obj['Key']:<40} "
                    f"{format_size(obj['Size']):>9}   "
                    f"{modified}"
                )

                total += 1

    except NoCredentialsError:
        print("Boto3 could not find AWS credentials.")
        return

    except ClientError as e:
        code = e.response["Error"]["Code"]
        print(f"S3 request failed: {code}")
        return

    if total == 0:
        print("No objects found.")
    else:
        print(f"Total: {total} objects")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 list_objects.py "
            "<bucket-name> [prefix]"
        )
        sys.exit(1)

    bucket_name = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""

    list_objects(bucket_name, prefix)
