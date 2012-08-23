# Doze

[![Build Status](https://secure.travis-ci.org/ericmoritz/doze.png)](http://travis-ci.org/ericmoritz/doze)

Doze is a URL building package inspired by
[slumber](http://slumber.in/)

This project attempts to take what is awesome about slumber while
enabling more flexibility.

## Usage

We will demonstrate how to fetch data from the twitter API:

    import requests
    from doze import url
    
    twitter = url("http://api.twitter.com/1/")
    user_lookup = twitter.users("lookup.json")

    # generates "http://api.twitter.com/1/lookup.json?screen_name=ericmoritz"
    response = requests.get(str(user_lookup(screen_name="ericmoritz")))

    if response.status_code == 200:
        data = response.json
    else:
        data = None
    
While this code is a bit more verbose it give us much more flexibility
and control over the fetching and serialization of the data.

For instance if we wanted to add a object_hook to the json.loads:

    if response.status_code == 200:
        data = json.loads(response.content,
                           object_hook=custom_object_hook)
    else:
        data = None

You can also reuse `user_lookup` to compose multiple requests:

    import requests
    from doze import url
    
    twitter = url("http://api.twitter.com/1/")
    user_lookup = twitter.users("lookup.json")

    # Fetch the user_lookup data for each screen name
    users = []
    for screen_name in ["ericmoritz", "montylounge"]:
        url = str(user_lookup(screen_name=screen_name))
        response = requests.get(url)
        if response.status_code == 200:
            users.append(json.loads(response.content))

If you find the dotted notation awkward you can pass the path items as
arguments and the url params as kwargs:

    from doze import url

    endpoint = url("http://example.com/v1")

    # dotted way
    def sections(section_id):
        # http://example.com/v1/sections/{section_id}?page=2
        url = str(endpoint.sections(section_id, page=2))
        return requests.get(url).json
    
    # "functional way"
    def sections(section_id):
        # http://example.com/v1/sections/{section_id}?page=2
        url = str(endpoint("sections", section_id, page=2))
        return requests.get(url).json


    
## Changelog

### v0.3

Backwards compatible change: duplicate query parameters overwrite
previous values with later values.

    # old behavior
    url = endpoint(page=3)
    url = endpoint(page=4)
    assert "http://example.com/v1?page=3&page=4" == str(url)

    # new behavior
    assert "http://example.com/v1?page=4" == str(url)
