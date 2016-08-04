import boto.vpc
import boto.ec2
import boto.ec2.elb
import boto.route53
from boto.s3.connection import S3Connection

profiles = {
    'prod': 'us-east-1',
    'prod-au': 'ap-southeast-2',
    'dev': 'eu-west-1',
    'talend': 'us-west-2',
}

def s3(profile):
    print profile
    return S3Connection(profile)

def ec2(profile, region=None):
    if not region:
        region = profiles[profile]
    return boto.ec2.connect_to_region(region, profile_name=profile)

def route53(profile):
    region = profiles[profile]
    return boto.route53.connect_to_region(region, profile_name=profile)

def elb(profile):
    region = profiles[profile]
    return boto.ec2.elb.connect_to_region(region, profile_name=profile)

def vpc(profile):
    region = profiles[profile]
    return boto.vpc.connect_to_region(region, profile_name=profile)
