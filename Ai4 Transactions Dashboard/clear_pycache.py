#!/usr/bin/python
#-*- coding:utf-8 -*-

try:
    import os 
    import sys 
    import json 
    import logging 
    import warnings 
    import contextlib 
    import pathlib
    import pandas as pd
    from pprint import pprint
    from functools import wraps
    from dotenv import load_dotenv, find_dotenv
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

class ClearVSCodeCache:
    @classmethod 
    def clear_vs_code_cache(cls):
        if hasattr(ClearVSCodeCache, "clear_vs_code_cache"):
            for _cache in pathlib.Path(".").rglob("*.py[co]"):
                _cache.unlink()
            for _cache in pathlib.Path(".").rglob("__pycache__"):
                _cache.rmdir()

if __name__ == "__main__":
    ClearVSCodeCache.clear_vs_code_cache()