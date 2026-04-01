from flask import Flask, render_template
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

try:
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT COUNT(*) as c FROM users WHERE is_admin=0')
        total_users = cur.fetchone()['c']
        cur.execute('SELECT COUNT(*) as c FROM schemes')
        total_schemes = cur.fetchone()['c']
        cur.execute('SELECT COUNT(*) as c FROM complaints')
        total_complaints = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) as c FROM complaints WHERE status='Pending'")
        pending = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) as c FROM complaints WHERE status='Resolved'")
        resolved = cur.fetchone()['c']

    stats = {
        'total_users': total_users,
        'total_schemes': total_schemes,
        'total_complaints': total_complaints,
        'pending': pending,
        'resolved': resolved,
        'in_progress': total_complaints - pending - resolved
    }

    # Test template rendering
    with app.app_context():
        rendered = render_template('admin_dashboard.html', stats=stats, recent_complaints=[], recent_users=[])
        print('Template rendered successfully!')
        print('Stats:', stats)

    db.close()

except Exception as e:
    print(f'Error: {e}')