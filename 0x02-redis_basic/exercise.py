#!/usr/bin/env python3
""" exercise """

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def replay(method: Callable) -> None:
    """ replay method """
    name = method.__qualname__
    client = redis.Redis()
    inputs = client.lrange("{}:inputs".format(name), 0, -1)
    outputs = client.lrange("{}:outputs".format(name), 0, -1)
    print('{} was called {} times:'.format(name, len(inputs)))
    for input, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, input.decode("utf-8"),
                                     output.decode("utf-8")))


def count_calls(method: Callable) -> Callable:
    """ counts the number of times Cache methods are called """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ wrapper fxn """
        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ stores history """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ wrapper fxn """
        inputs = f"{method.__qualname__}:inputs"
        outputs = f"{method.__qualname__}:outputs"
        ret_val = method(self, *args, **kwargs)

        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
            self._redis.rpush(outputs, ret_val)
        return ret_val
    return wrapper


class Cache(object):
    """ Cache Class """
    def __init__(self) -> None:
        """ init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store method """
        rand_key: str = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, float, int]:
        """ Gets Data """
        retrived_data: bytes = self._redis.get(key)
        if fn:
            return fn(retrived_data)
        return retrived_data

    def get_str(self, key: str) -> str:
        """ Returns a string """
        ret_val = self.get(key)
        if ret_val is not None:
            return ret_val.decode("utf-8")
        return None

    def get_int(self, key: int) -> int:
        """ Returns an int """
        ret_val = self.get(key)
        if ret_val is not None:
            return int(ret_val)
        return None
