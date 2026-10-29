import boto3
from botocore.exceptions import ClientError, NoCredentialsError

s3 = boto3.client("s3")

try:
    response = s3.list_buckets()

except NoCredentialsError:
    print("Boto3 could not find AWS credentials.")

except ClientError as e:
    print("AWS rejected the request:")
    print(e.response["Error"]["Code"])

else:
    buckets = response["Buckets"]

    if not buckets:
        print("No buckets found in this account.")

    for bucket in buckets:
        created = bucket["CreationDate"].strftime("%Y-%m-%d")
        print(f"{bucket['Name']} (created {created})")

    print(f"Total: {len(buckets)}")
