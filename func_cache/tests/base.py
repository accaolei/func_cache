import unittest
import os
from redis import Redis
HOST = os.environ.get('WALRUS_REDIS_HOST') or '127.0.0.1'
PORT = os.environ.get('WALRUS_REDIS_PORT') or 6379

db = Redis(host=HOST, port=PORT, db=10)


class CacheTestCase(unittest.TestCase):
    def setUp(self):
        db.flushdb()

    def tearDown(self):
        db.flushdb()

    def assertList(self, values, exected):
        values = list(values)
        self.assertEqual(len(values), len(exected))
        for value, item in zip(values, exected):
            self.assertEqual(value, item)
