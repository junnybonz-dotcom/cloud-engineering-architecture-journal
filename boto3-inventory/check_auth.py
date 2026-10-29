import boto3
from botocore.exceptions import ClientError, NoCredentialsError


try:
    sts = boto3.client("sts")

    identity = sts.get_caller_identity()

    print("Authenticated!")
    print("ARN:", identity["Arn"])

except NoCredentialsError:
    print("Boto3 could not find AWS credentials.")

except ClientError as e:
    print("AWS rejected the request:")
    print(e)
