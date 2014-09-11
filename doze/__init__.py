import urlparse
import posixpath
import urllib
from itertools import chain

__version__ = '0.5'


def querydict_to_querylist(querydict):
    """converts a querydict to a querylist"""
    for key, value in querydict.iteritems():
        if type(value) is list:
            for subitem in value:
                yield key, subitem
        else:
            yield key, value


def merge_querylist(querylist1, querylist2):
    return merge_querylist2(querylist1, querylist2)


def merge_querylist1(querylist1, querylist2):
    querydict = {}
    for i, (key, value) in enumerate(querylist1):
        querydict[key] = (1, i, key, value)
    for i, (key, value) in enumerate(querylist2):
        querydict[key] = (2, i, key, value)        
    
    querylist = sorted(querydict.values())
    return [(key, value) for (_,_,key,value) in querylist]


def merge_querylist2(querylist1, querylist2):
    querylist = []
    override_existing = set(key for (key, _) in querylist2)

    for key, value in querylist1:
        if key not in override_existing:
            querylist.append((key, value))
    
    for key, value in querylist2:
        override_existing.add(key)
        querylist.append((key, value))


    return querylist
    


def url_join(base, *args, **querydict):
    """
    Helper function to join an arbitrary number of url segments together.
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
    # parse the querylist
    querylist = urlparse.parse_qsl(query)

    path = path if len(path) else "/"
    for x in args:
        if not isinstance(x, basestring):
            x = unicode(x)

        bits = x.split("?")
        if len(bits) == 2:
            querylist = merge_querylist(querylist, urlparse.parse_qsl(bits[1]))
        path = posixpath.join(path, bits[0])

    # update the querylist
    querylist = merge_querylist(querylist, list(querydict_to_querylist(querydict)))

    # encode the querylist
    query = urllib.urlencode(querylist)
    
    return urlparse.urlunsplit([scheme, netloc, path, query, fragment])


class Url(object):
    def __init__(self, *args, **kwargs):
        self.base_url = url_join(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        base_url = url_join(self.base_url, *args, **kwargs)

        return Url(base_url)

    def __getattr__(self, name):
        return self(name)

    def __str__(self):
        return self.base_url

    def __repr__(self):
        return "<doze %s>" % (str(self))

url = Url

