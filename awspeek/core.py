import conns
from attrs import ami, bucket, instance, attr_default, inet
import tabulate

def attribute(boto_results, headers, attr_func):
    results = []
    for result in boto_results:
        results.append([attr_func(result, field) or 'missing' for field in headers])
    return results

def pretty_print(results, headers):
    return tabulate.tabulate(results, headers, tablefmt='psql')

def route53_fetch(conn):
    for zone in conn.get_zones():
        for record in zone.get_records():
            yield record

targets = {
    'instance': {
        'headers': ('id', 'vpc_id', '_state', 'instance_type', 'private_ip_address', 'name'),
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_only_instances(),
        'attr_field': instance,
    },
    'sec_group': {
        'headers': ('id', 'vpc_id', 'name', 'description'),
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_all_security_groups()
    },
    'ami': {
        'headers': ('id', 'state', 'name', 'boot_vol', 'description'),
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_all_images(owners=['self']),
        'attr_field': ami,
    },
    'bucket': {
        'headers': ('creation_date', 'size', 'name'),
        'connection': conns.s3,
        'fetch': lambda conn: conn.get_all_buckets(),
        'attr_field': bucket,
    },
    'dns_record': {
        'headers': ('name', 'type', 'ttl', 'resource_records'),
        'connection': conns.route53,
        'fetch': route53_fetch,
    },
    'elb': {
        'headers': ('name', 'instances', 'listeners'),
        'connection': conns.elb,
        'fetch': lambda conn: conn.get_all_load_balancers(),
    },
    'keys': {
        'headers': ('name', 'region'),
        'connection': conns.vpc,
        'fetch': lambda conn: conn.get_all_key_pairs(),
    },
    'nets': {
        'connection': conns.vpc,
        'fetch': lambda conn: conn.get_all_network_interfaces(),
        'headers': ('id', 'private_ip_address', 'publicIp', 'vpc_id', 'status', 'attachment', 'device_index'),
        'attr_field': inet,
    }
}
def show(profile, show):
    headers = targets[show]['headers']
    conn = targets[show]['connection'](profile)
    boto_results = targets[show]['fetch'](conn)
    attributed = attribute(boto_results, headers, targets[show].get('attr_field', attr_default))
    return pretty_print(attributed, headers)
