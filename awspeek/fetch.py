def route53(conn):
    for zone in conn.get_zones():
        for record in zone.get_records():
            yield record

def route(conn):
    for route_table in conn.get_all_route_tables():
        for r in route_table.routes:
            setattr(r, 'route_table_id', route_table.id)
            yield r
