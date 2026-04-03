import mysql.connector
from urllib.parse import urlparse
import os

DATABASE_URL = os.getenv('DATABASE_URL', "mysql://root:fpwyMeYfiWKNKaHxmmuCPNyvochKibYw@interchange.proxy.rlwy.net:19314/railway")

url = urlparse(DATABASE_URL)

print("HOST:", url.hostname)
print("PORT:", url.port)
print("USER:", url.username)
print("DB:", url.path)

db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],
    port=url.port or 3306
)

print("✅ Railway MySQL Connected!")


