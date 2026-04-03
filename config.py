import os
from urllib.parse import urlparse

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY", "village_secret")

    # 🔥 Railway provides DATABASE_URL
    DATABASE_URL = os.environ.get("mysql://root:fpwyMeYfiWKNKaHxmmuCPNyvochKibYw@interchange.proxy.rlwy.net:19314/railway")

    if DATABASE_URL:

        url = urlparse(DATABASE_URL)

        MYSQL_HOST = url.hostname
        MYSQL_USER = url.username
        MYSQL_PASSWORD = url.password
        MYSQL_DB = url.path[1:]
        MYSQL_PORT = url.port

    else:
        # Local fallback
        MYSQL_HOST = "localhost"
        MYSQL_USER = "root"
        MYSQL_PASSWORD = ""
        MYSQL_DB = "village_sattam"
        MYSQL_PORT = 3306