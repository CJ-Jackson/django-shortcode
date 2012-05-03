shortcodes = {}

def tag(kwargs):
    content = kwargs['content']
    element = kwargs['key']
    element = element.split('_')[0]
    attr = kwargs['attr']
    if not content:
        return False

    if 'id' in attr:
        del attr['id']

    param = ''
    for k,v in list(attr.items()):
        param += " %s='%s'" % (k, v)

    content = kwargs['parse'](content)

    return "<%s%s>%s</%s>" % (element, param, content, element)

shortcodes['h1'] = tag
shortcodes['h2'] = tag
shortcodes['h3'] = tag
shortcodes['h4'] = tag
shortcodes['h5'] = tag
shortcodes['h6'] = tag
shortcodes['div'] = tag
shortcodes['div_1'] = tag
shortcodes['div_2'] = tag
shortcodes['div_3'] = tag
shortcodes['div_5'] = tag
shortcodes['div_6'] = tag
shortcodes['div_6'] = tag
shortcodes['div_7'] = tag
shortcodes['div_8'] = tag
shortcodes['div_9'] = tag
shortcodes['div_10'] = tag
shortcodes['p'] = tag
shortcodes['span'] = tag
shortcodes['aside'] = tag
shortcodes['code'] = tag
shortcodes['strong'] = tag
shortcodes['em'] = tag

def link(kwargs):
    attr = kwargs['attr']

    if 'id' in attr:
        del attr['id']

    try:
        href = attr['href']
        del attr['href']
    except:
        if kwargs['content']:
            href = kwargs['content']
        else:
            return False

    if not kwargs['content']:
        kwargs['content'] = href
    else:
        kwargs['content'] = kwargs['parse'](kwargs['content'])

    param = " href='%s' " % href

    for k,v in list(attr.items()):
        param += "%s='%s' " % (k, v)

    return "<a%s>%s</a>" % (param, kwargs['content'])

shortcodes['a'] = link

def img(kwargs):
    attr = kwargs['attr']

    if 'id' in attr:
        del attr['id']

    try:
        src = attr['src']
        del attr['src']
    except:
        if kwargs['content']:
            src = kwargs['content']
        else:
            return False

    if 'alt' not in attr:
        attr['alt'] = 'Image'

    if 'title' not in attr:
        attr['title'] = 'Image'

    param = " src='%s' " % src

    for k,v in list(attr.items()):
        param += "%s='%s' " % (k, v)

    return "<img%s />" % param

shortcodes['img'] = img

def linebreak(kwargs):
    del kwargs
    return "<br />"

shortcodes['br'] = linebreak

def clear(kwargs):
    del kwargs
    return '<p class="clear">'

shortcodes['clear'] = clear

def url_reverse(kwargs):
    attr = kwargs['attr']
    if not kwargs['content']:
        return False

    if 'name' in attr:
        name = attr['name']
        del attr['name']
    else:
        return False

    try:
        from django.core.urlresolvers import reverse
        if attr:
            url = reverse(name, kwargs=attr)
        else:
            url = reverse(name)
        from django.utils.html import escape
        return '<a href="%s" >%s</a>' % (escape(url), kwargs['content'])
    except:
        return False

shortcodes['url'] = url_reverse

def tab(kwargs):
    del kwargs
    return "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

shortcodes['tab'] = tab
