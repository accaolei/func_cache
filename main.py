from func_cache import Cache
from redis import Redis
import datetime
import time


db = Redis(port=6378)
cache = Cache(database=db)


class CaseCache(object):

    @cache.cached_property(timeout=10, _async=True)
    def now(self):
        return datetime.datetime.now()


c = CaseCache()
print(c.now)
print(c.now)
time.sleep(12)
print(c.now)


@cache.cached(timeout=10)
def now(arg=None):
    return datetime.datetime.now()


# h1 = hello(1)
# print(h1)
# print(hello(1) == h1)
# time.sleep(10)
# h2 = hello(1)
# print(hello(1) == h2)
print(now(1))
print(now(1))
print(now(2))
time.sleep(10)
print(now(1))


@cache.async_cached(timeout=10)
async def async_func(arg=None):
    return datetime.datetime.now()
