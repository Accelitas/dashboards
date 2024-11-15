#!/usr/bin/python
#-*- coding:utf-8 -*-

try:
    import os
    from dotenv import load_dotenv, find_dotenv
except ImportError as error:
    raise Exception(f"{error}") from None 

load_dotenv(find_dotenv("database/.env"))

connection_string_1 = (
                        'DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER={os.environ.get("server_1")};'
                        f'DATABASE={os.environ.get("database_1")};'
                        'Authentication=ActiveDirectoryServicePrincipal;'
                        f'UID={os.environ.get("client_id_1")};'
                        f'PWD={os.environ.get("client_secret_1")};'
                    )