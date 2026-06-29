import getpass
import pymysql
from werkzeug.security import generate_password_hash
from config import Config

# Connect to MySQL
connection = pymysql.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    db=Config.MYSQL_DB,
    port=Config.MYSQL_PORT,
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()

# Check whether admin already exists
cursor.execute(
    "SELECT id FROM users WHERE email=%s",
    ("admin@villagesattam.gov.in",)
)

if cursor.fetchone():
    print("Admin already exists.")
else:
    password = input("Enter admin password: ")

    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users(name, email, password, village, is_admin)
        VALUES(%s, %s, %s, %s, %s)
    """, (
        "Admin",
        "admin@gmail.com",
        hashed_password,
        "District HQ",
        1
    ))

    print("Admin created successfully!")

cursor.close()
connection.close()