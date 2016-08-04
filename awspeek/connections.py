import boto.ec2
from boto.s3.connection import S3Connection

profiles = {
    'prod': 'us-east-1',
    'prod-au': 'ap-southeast-2',
    'dev': 'eu-west-1',
    'talend': 'us-west-2',
}

def get_ec2_conn(profile, region=None):
    if not region:
        region = profiles[profile]
    return boto.ec2.connect_to_region(region, profile_name=profile)

def get_s3_conn(profile):
    return S3Connection(profile)
