#!/usr/bin/env python3
""" web """

import redis
import requests
from typing import Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count calls """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ wrapper fxn """
        client = redis.Redis()

        count_key = "count:{url}".format(url=url)
        result_key = "result:{url}".format(url=url)
        client.incr(count_key)

        result = client.get(result_key)
        if result:
            return result.decode("utf-8")

        return_value = method(url)
        client.setex(result_key, 10, return_value)

        return return_value
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ gets page """
    try:
        return requests.get(url).text
    except requests.RequestException:
        return str(None)
