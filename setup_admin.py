import pymysql
from werkzeug.security import generate_password_hash
from config import Config

try:
    # Connect to MySQL database
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        port=Config.MYSQL_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    cursor = conn.cursor()
    
    # Delete existing admin if present
    cursor.execute("DELETE FROM users WHERE email=%s", ('admin@villagesattam.gov.in',))
    
    # Insert new admin user
    hashed_password = generate_password_hash('admin123')
    cursor.execute("""
        INSERT INTO users (name, email, password, village, is_admin)
        VALUES (%s, %s, %s, %s, %s)
    """, ('Admin', 'admin@villagesattam.gov.in', hashed_password, 'District HQ', 1))
    
    conn.commit()
    conn.close()
    print('✓ Admin user created/updated successfully!')
    print('  Email: admin@villagesattam.gov.in')
    print('  Password: admin123')
    
except pymysql.err.ProgrammingError as e:
    print(f'✗ Error: {e}')
    print('\nPlease ensure:')
    print('1. MySQL server is running')
    print('2. Database "village_sattam" exists')
    print('3. Tables have been created from database.sql')
except Exception as e:
    print(f'✗ Connection error: {e}')
