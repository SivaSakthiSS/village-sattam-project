import pymysql
from werkzeug.security import generate_password_hash
from config import Config

conn = pymysql.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    db=Config.MYSQL_DB,
    port=Config.MYSQL_PORT,
    autocommit=True
)

cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE email=%s", ('admin@villagesattam.gov.in',))

hashed_password = generate_password_hash('admin123')

cursor.execute("""
INSERT INTO users (name, email, password, village, is_admin)
VALUES (%s, %s, %s, %s, %s)
""", ('Admin', 'admin@villagesattam.gov.in', hashed_password, 'District HQ', 1))

print("Admin created successfully!")