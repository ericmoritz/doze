from unittest import TestCase as BaseTest
import doze

class TestCase(BaseTest):
    pass


class TestDoze(TestCase):

    
    def test(self):
        twitter = doze.url("http://api.twitter.com/1/")

        home_timeline = twitter.statuses("home_timeline.json")
        user_lookup = twitter.users("lookup.json")

        self.assertEqual("http://api.twitter.com/1/statuses/home_timeline.json",
                         str(home_timeline))

        self.assertEqual("http://api.twitter.com/1/users/lookup.json?screen_name=ericmoritz",
                         str(user_lookup(screen_name="ericmoritz")))

    def test_simple(self):
        user_lookup = doze.url("http://api.twitter.com/1/",
                               "users",
                               "lookup.json",
                               screen_name="ericmoritz")
                                 
        self.assertEqual("http://api.twitter.com/1/users/lookup.json?screen_name=ericmoritz",
                         str(user_lookup))

    def test_hardcoded_queries(self):
        google = doze.url("http://google.com/?x=doze")

        self.assertEqual("http://google.com/?x=doze&q=Eric+Moritz",
                         str(google(q="Eric Moritz")))


    def test_dupe_queries(self):
        google = doze.url("http://google.com/?q=doze")

        self.assertEqual("http://google.com/?q=Eric+Moritz",
                         str(google(q="Eric Moritz")))
        

    def test_query_merge(self):
        google = doze.url("http://google.com/?x=doze")
        google = google("search/?q=query")
        self.assertEqual("http://google.com/search/?x=doze&q=query",
                         str(google))

        google = doze.url("http://google.com/?q=doze")
        google = google("search/?q=query")
        self.assertEqual("http://google.com/search/?q=query",
                         str(google))

    def test_nonstring_bits(self):
        google = doze.url("http://google.com/")
        google = google("story", 10)
        self.assertEqual("http://google.com/story/10?page=1",
                         str(google(page=1)))

    def test_list_params(self):
        google = doze.url("http://example.com/")
        self.assertEqual("http://example.com/?x=1&x=2",
                         str(google(x=[1,2])))


class TestMergeQueryList(TestCase):
    def test(self):
        # second query list trumps the first
        self.assertEqual([("a", "2")],
                         doze.merge_querylist([("a", "1")],
                                              [("a", "2")]))
        # items in the second list always appear last
        self.assertEqual([("a", "1"), ("b", "2")],
                         doze.merge_querylist([("a", "1")],
                                              [("b", "2")]))

        # items in the second list always appear last even if they dupe
        self.assertEqual([("c", "c1"), ("a", "a2"), ("b", "b1")],
                         doze.merge_querylist([("a", "a1"), ("c", "c1")],
                                              [("a", "a2"), ("b", "b1")]))

