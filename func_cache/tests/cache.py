from func_cache.tests.base import CacheTestCase
from func_cache.tests.base import db
from func_cache.cache import Cache
import datetime

cache = Cache(database=db, name='test.cache')


@cache.cached()
def now(arg=None):
    return datetime.datetime.now()


class Date(object):
    @cache.cached_property()
    def now(self):
        return datetime.datetime.now()


class TestCache(CacheTestCase):

    def test_cache_decorator(self):
        n0 = now()
        n1 = now(1)
        n2 = now(2)

        self.assertTrue(n0 != n1 != n2)
        self.assertEqual(now(), n0)
        self.assertEqual(now(1), n1)
        self.assertEqual(now(2), n2)

        now.bust(1)
        self.assertNotEqual(now(1), n1)
        self.assertEqual(now(1), now(1))

    def test_cached_property(self):
        d = Date()
        n1 = d.now
        n2 = d.now
        self.assertEqual(n1, n2)

        del d.now
        n3 = d.now

        self.assertTrue(n1 != n3)
        self.assertTrue(d.now, n3)
