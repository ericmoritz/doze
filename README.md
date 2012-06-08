# Doze

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

    response = requests.get(str(user_lookup(screen_name="ericmoritz")))

    if response.status_code == 200:
        data = response.json
    else:
        data = None
    
While this code is a bit more verbose it give us much more flexibility
and control over the fetching and serialization of the data.

For instance if we wanted to add a object_hook to the json.loads:

    import requests
    from doze import url
    import json
    
    def custom_object_hook(obj):
        # do something with obj
        return obj
    
    twitter = url("http://api.twitter.com/1/")
    user_lookup = twitter.users("lookup.json")
    
    response = requests.get(str(user_lookup(screen_name="ericmoritz")))
    
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
        url = str(user_lookup(screen_name="ericmoritz"))
        response = requests.get(url)
        if response.status_code == 200:
            users.append(json.loads(response.content))

