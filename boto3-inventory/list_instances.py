# list_instances.py
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

try:
    response = ec2.describe_instances(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)
except ClientError as e:
    print(f"Failed: {e.response['Error']['Code']}")
else:
    count = 0
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
            name = tags.get("Name", "(no name)")
            ip = inst.get("PublicIpAddress", "-")
            state = inst["State"]["Name"]
            print(f"{inst['InstanceId']}  {name:<14} {state:<10} {inst['InstanceType']:<9} {ip}")
            count += 1
    print(f"Total: {count} instances in {ec2.meta.region_name}")
