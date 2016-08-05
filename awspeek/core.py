import conns
import tabulate
import attrs

def attribute(boto_results, headers, attr_func):
    results = []
    for result in boto_results:
        # results.append([attr_func(result, field) or 'missing' for field in headers])
        attributed = []
        for field in headers:
            attr = attr_func(result, field)
            if attr is None:
                attr = 'missing'
            attributed.append(attr)
        results.append(attributed)
    return results

def pretty_print(results, headers):
    return tabulate.tabulate(results, headers, tablefmt='psql')

def route53_fetch(conn):
    for zone in conn.get_zones():
        for record in zone.get_records():
            yield record

def routes_fetch(conn):
    for route_table in conn.get_all_route_tables():
        for r in route_table.routes:
            setattr(r, 'route_table_id', route_table.id)
            yield r

targets = {
    'instance': {
        'headers': ('id', 'vpc_id', '_state', 'instance_type', 'private_ip_address', 'name'),
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_only_instances(),
        'attr_field': attrs.instance,
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
        'attr_field': attrs.ami,
    },
    'bucket': {
        'headers': ('creation_date', 'size', 'name'),
        'connection': conns.s3,
        'fetch': lambda conn: conn.get_all_buckets(),
        'attr_field': attrs.bucket,
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
        'attr_field': attrs.inet,
    },
    'routes': {
        'connection': conns.vpc,
        'headers': ('route_table_id', 'destination_cidr_block', 'target', 'state'),
        'fetch': routes_fetch,
        'attr_field': attrs.route,
    },
    'route_tables': {
        'connection': conns.vpc,
        'fetch': lambda conn: conn.get_all_route_tables(),
        'headers': ('id', 'vpc_id', 'name', 'ismain', 'subnets', 'routes'),
        'attr_field': attrs.route_table,

    },
    'sec_group_rules': {
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_all_security_groups(),
        'headers': ('id', 'vpc_id', 'name', 'description'),
    },

    # no instance infos yet ( attachment )
    'snapshot': {
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_all_snapshots(owner='self'),
        'headers': ('id', 'volume_size', 'status', 'progress', 'description', 'start_time', 'tags'),
    },
    # route tables stuff
    'subnet': {
        'connection': conns.vpc,
        'fetch': lambda conn: conn.get_all_subnets(),
        'headers': ('id', 'vpc_id', 'cidr_block', 'availability_zone'),
        'attr_field': attrs.subnet
    },
    'volume': {
        'connection': conns.ec2,
        'fetch': lambda conn: conn.get_all_volumes(),
        'headers': ('id', 'snapshot_id', 'size', 'status', 'zone', 'create_time', 'status', 'instance', 'device', 'iops', 'type', 'encrypted'),
        'attr_field': attrs.volume
    }
}
def show(profile, show):
    headers = targets[show]['headers']
    conn = targets[show]['connection'](profile)
    boto_results = targets[show]['fetch'](conn)
    attributed = attribute(boto_results, headers, targets[show].get('attr_field', attrs.attr_default))
    return pretty_print(attributed, headers)
