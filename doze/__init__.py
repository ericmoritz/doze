import urlparse
import posixpath
import urllib

__version__ = '0.1'


def querydict_to_querylist(querydict):
    """converts a querydict to a querylist"""
    for key, value in querydict.iteritems():
        if type(value) is list:
            for subitem in value:
                yield key, subitem
        else:
            yield key, value


def url_join(base, *args, **querydict):
    """
    Helper function to join an arbitrary number of url segments together.
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])

    # update the querydict
    querylist = urlparse.parse_qsl(query)
    querylist.extend(querydict_to_querylist(querydict))

    # encode the querydict
    query = urllib.urlencode(querylist)
    
    return urlparse.urlunsplit([scheme, netloc, path, query, fragment])


class Url(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def __call__(self, *args, **kwargs):
        base_url = url_join(self.base_url, *args, **kwargs)
        return Url(base_url)

    def __getattr__(self, name):
        return self(name)

    def __str__(self):
        return self.base_url

    def __repr__(self):
        return "<doze %s>" % (str(self))
    
def url(base):
    return Url(base)
