#!/usr/bin/env python3
""" exercise """

import redis
import uuid
from typing import Union


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
