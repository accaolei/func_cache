## func_cache

在python项目中基于redis-py对函数进行缓存
只支持python3.5以上的版本



**使用方法**

```python
import datetime
import time
from func_cache import Cache
from redis import Redis

db = Redis()
cache = Cache(database=db)

@cache.cached(timeout=10)
def now(arg=None):
  return datetime.datetime.now()

print(now(1))
print(now(1))
time.sleep(10)
print(now(1))

# 2020-02-13 18:27:26.159922
# 2020-02-13 18:27:26.159922
# 2020-02-13 18:27:26.164827
# 2020-02-13 18:27:36.173809

class DateCache(object):

    @cache.cached_property(timeout=10)
    def now(self):
        return datetime.datetime.now()

d = DateCache()
d.now
d.now
time.sleep(12)
print(c.now)
# 2020-02-13 18:32:39.342156
# 2020-02-13 18:32:39.342156
# 2020-02-13 18:32:51.355638

# 异步支持
@cache.async_cached(timeout=10)
async def async_func(arg=None):
    return datetime.datetime.now()
  

class DateCache(object):
    @cache.cached_property(timeout=10,_async=True)
    async def now(self):
        return datetime.datetime.now()



```

