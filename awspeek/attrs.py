def instance(instance, attr):
    if attr == 'name':
        return getattr(instance, 'tags', {}).get('Name')
    else:
        return attr_default(instance, attr)

def ami(ami, attr):
    if attr == 'boot_vol':
        return '/dev/sda1=' + str(ami.block_device_mapping['/dev/sda1'].snapshot_id)
    else:
        return attr_default(ami, attr)

def bucket(bucket, attr):
    if attr == 'size':
        return sum([i.size() for i in bucket.list()])
    else:
        return attr_default(bucket, attr)

def inet(inet, attr):
    if not inet or not getattr(inet, 'attachment'):
        return
    if attr == 'attachment':
        return inet.attachment.instance_id
    if attr == 'device_index':
        return inet.attachment.device_index
    else:
        return attr_default(inet, attr)

def attr_default(field, attr):
    return getattr(field, attr, None)
