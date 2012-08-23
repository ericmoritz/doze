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

    def test_hardcoded_queries(self):
        google = doze.url("http://google.com/?x=doze")

        self.assertEqual("http://google.com/?x=doze&q=Eric+Moritz",
                         str(google(q="Eric Moritz")))


    def test_dupe_queries(self):
        google = doze.url("http://google.com/?q=doze")

        self.assertEqual("http://google.com/?q=doze&q=Eric+Moritz",
                         str(google(q="Eric Moritz")))
        

    def test_query_merge(self):
        google = doze.url("http://google.com/?x=doze")
        google = google("search/?q=query")
        self.assertEqual("http://google.com/search/?x=doze&q=query",
                         str(google))
