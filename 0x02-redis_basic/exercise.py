#!/usr/bin/env python3
""" exercise """

import redis
import uuid
from typing import Union, Callable, Optional


class Cache(object):
    """ Cache Class """
    def __init__(self) -> None:
        """ init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
