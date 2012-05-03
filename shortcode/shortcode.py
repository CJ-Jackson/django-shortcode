_dict = {}
_string = None
_init = False

def __init__():
    global _init
    from importlib import import_module
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        try:
            module = import_module(app + '.shortcodes')
            for k, v in list(module.shortcodes.items()):
                __register__(k, v)
        except:
            lambda x: x
    _init = True

def __key__():
    global _string
    if not _string:
        keys = list(_dict.keys())
        _string = "|".join(keys)
    return _string

def __attr__(pair):
    import re
    attr = {}
    pair = pair.replace('&quot;', '"')
    pair = pair.replace('&#39;', '\'')
    for match in re.finditer('(?P<key>\w+)(\s*)=(\s*)"(?P<value>[^"]+)"',
    pair, flags=re.I | re.M | re.S):
        key = match.group('key')
        key = key.lower()
        value = match.group('value')
        value = value.replace('"', '&quot;')
        value = value.replace('\'', '&#39;')
        attr[key] = value
    for match in re.finditer("(?P<key>\w+)(\s*)=(\s*)'(?P<value>[^']+)'",
    pair, flags=re.I | re.M | re.S):
        key = match.group('key')
        key = key.lower()
        value = match.group('value')
        value = value.replace('"', '&quot;')
        value = value.replace('\'', '&#39;')
        attr[key] = value
    return attr

def __hash__(kwargs):
    import hashlib
    import json
    hash = hashlib.new('ripemd160')
    hash.update(json.dumps(kwargs))
    return 'shortcode_%s' % hash.hexdigest()

def __callback__(match):
    key = match.group('key')
    try:
        attr = match.group('pair')
        attr = __attr__(attr)
    except:
        attr = {}
    try:
        content = match.group('content')
    except:
        content = False
    kwargs = {'key': key, 'attr': attr, 'content': content}
    hash = __hash__(kwargs)
    from django.core.cache import cache
    if cache.get(hash):
        return cache.get(hash)
    try:
        function = _dict[key]
        kwargs['parse'] = parse
        content = function(kwargs)
        if content:
            cache.set(hash, str(content), 3600)
            return str(content)
        else:
            raise Exception('Content Returned False')
    except:
        return match.group(0)

def __register__(key, function):
    _dict[str(key).strip()] = function

def parse(value):
    global _init
    if not _init:
        __init__()

    import re
    value = re.sub(
        "\[(?P<key>[" + __key__() +
        "]{1,})(\s{0,1})(?P<pair>.*?)(?:(/))?\]" +
        "(?:(?P<content>.+?)\[/(?P=key)\])?",
        __callback__,
        value, flags=re.I | re.M | re.S | re.U)

    return value
