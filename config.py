# config.py
import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL', "mysql://root:VUIbHwcSoPDoUXMqKOAsrZxFUblnHAgP@hopper.proxy.rlwy.net:55188/railway")

if DATABASE_URL:
    url = urlparse(DATABASE_URL)

    class Config:
        MYSQL_HOST = url.hostname
        MYSQL_USER = url.username
        MYSQL_PASSWORD = url.password
        MYSQL_DB = url.path[1:]
        MYSQL_PORT = url.port
        SECRET_KEY = "village_sattam_secret_key"
