
import pickle
import time
from functools import wraps
import hashlib


class Cache(object):

    def __init__(self, database, name='cache', default_timeout=None, debug=False):
        """
        :param database: :py:class:`Database` instance.
        :param name: Namespace for this cache.
        :param int default_timeout: Default cache timeout.
        :param debug: Disable cache for debugging purposes. Cache will no-op.
        """
        self.database = database
        self.name = name
        self.prefix_len = len(self.name) + 1
        self.default_timeout = default_timeout
        self.metrics = {'hits': 0, 'misses': 0, 'writes': 0}
        self.debug = debug

    def make_key(self, s):
        return ':'.join((self.name, s))

    def unmake_key(self, k):
        return k[self.prefix_len:]

    def delete(self, key):
        if self.debug:
            return 0
        return self.database.delete(self.make_key(key))

    def get(self, key, default=None):
        key = self.make_key(key)

        if self.debug:
            return default

        value = self.database.get(key)
        if not value:
            self.metrics['misses'] += 1
            return default
        else:
            self.metrics['hits'] += 1
            return pickle.loads(value)

    def set(self, key, value, timeout=None):

        key = self.make_key(key)

        if self.debug:
            return True

        pickled_value = pickle.dumps(value)
        self.metrics['writes'] += 1
        if timeout:
            return self.database.setex(key, int(timeout), pickled_value)
        else:
            return self.database.set(key, pickled_value)

    def _key_fn(a, k):
        return hashlib.md5(pickle.dumps((a, k))).hexdigest()

    def cached(self, key_fn=_key_fn, timeout=None, metrics=False):
        def decorator(fn):
            def make_key(args, kwargs):
                return '%s:%s' % (fn.__name__, key_fn(args, kwargs))

            def bust(*args, **kwargs):
                key = make_key(args, kwargs)
                return self.delete(key)

            _metrics = {
                'hits': 0,
                'misses': 0,
                'avg_hit_time': 0,
                'avg_miss_time': 0}

            @wraps(fn)
            def inner(*args, **kwargs):
                start = time.time()
                is_cache_hit = True
                key = make_key(args, kwargs)
                res = self.get(key)
                if res is None:
                    res = fn(*args, **kwargs)
                    self.set(key, res, timeout)
                    is_cache_hit = False

                if metrics:
                    dur = time.time() - start
                    if is_cache_hit:
                        _metrics['hits'] += 1
                        _metrics['avg_hit_time'] += (dur / _metrics['hits'])
                    else:
                        _metrics['misses'] += 1
                        _metrics['avg_miss_time'] += (dur / _metrics['misses'])

                return res

            inner.bust = bust
            inner.make_key = make_key
            if metrics:
                inner.metrics = _metrics
            return inner
        return decorator

    def async_cached(self, key_fn=_key_fn, timeout=None, metrics=False):
        def decorator(fn):
            def make_key(args, kwargs):
                return '%s:%s' % (fn.__name__, key_fn(args, kwargs))

            def bust(*args, **kwargs):
                return self.delete(make_key(args, kwargs))

            _metrics = {
                'hits': 0,
                'misses': 0,
                'avg_hit_time': 0,
                'avg_miss_time': 0}

            @wraps(fn)
            async def inner(*args, **kwargs):
                start = time.time()
                is_cache_hit = True
                key = make_key(args, kwargs)
                res = self.get(key)
                if res is None:
                    res = await fn(*args, **kwargs)
                    self.set(key, res, timeout)
                    is_cache_hit = False

                if metrics:
                    dur = time.time() - start
                    if is_cache_hit:
                        _metrics['hits'] += 1
                        _metrics['avg_hit_time'] += (dur / _metrics['hits'])
                    else:
                        _metrics['misses'] += 1
                        _metrics['avg_miss_time'] += (dur / _metrics['misses'])

                return res

            inner.bust = bust
            inner.make_key = make_key
            if metrics:
                inner.metrics = _metrics
            return inner
        return decorator

    def cached_property(self, key_fn=_key_fn, timeout=None, _async=False):
        this = self

        class _cached_property(object):
            def __init__(self, fn):
                if _async:
                    self._fn = this.async_cached(key_fn, timeout)(fn)
                else:
                    self._fn = this.cached(key_fn, timeout)(fn)

            def __get__(self, instance, instance_type=None):
                if instance is None:
                    return self
                return self._fn(instance)

            def __delete__(self, obj):
                self._fn.bust(obj)

            def __set__(self, instance, value):
                raise ValueError('Cannot set value of a cached property.')

        def decorator(fn):
            return _cached_property(fn)

        return decorator
