# app.py - Village Sattam Main Application
# ============================================

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from functools import wraps
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)

# ============================================
# DATABASE CONNECTION
# ============================================

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
@app.route("/testdb")
def testdb():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    return "Database Connected Successfully!"
# ============================================
# AUTH DECORATORS
# ============================================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def index():
    """Homepage with scheme previews and announcements."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM schemes ORDER BY created_at DESC LIMIT 3")
            featured_schemes = cur.fetchall()
            cur.execute("SELECT * FROM announcements ORDER BY created_at DESC LIMIT 4")
            announcements = cur.fetchall()
        return render_template('index.html',
                               featured_schemes=featured_schemes,
                               announcements=announcements)
    finally:
        db.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        village = request.form.get('village', '').strip()

        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters.')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append('Please enter a valid email address.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('register.html', form_data=request.form)

        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE email=%s", (email,))
                if cur.fetchone():
                    flash('Email already registered. Please login.', 'warning')
                    return render_template('register.html', form_data=request.form)

                hashed_pw = generate_password_hash(password)
                cur.execute(
                    "INSERT INTO users (name, email, password, village) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_pw, village)
                )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        finally:
            db.close()

    return render_template('register.html', form_data={})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cur.fetchone()

            if user and check_password_hash(user['password'], password):
                session.clear()
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['is_admin'] = bool(user['is_admin'])
                session['village'] = user['village']
                flash(f"Welcome back, {user['name']}!", 'success')
                if user['is_admin']:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        finally:
            db.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# ============================================
# USER ROUTES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    db = get_db()
    try:
        with db.cursor() as cur:
            # Recent schemes
            cur.execute("SELECT * FROM schemes ORDER BY created_at DESC LIMIT 4")
            schemes = cur.fetchall()
            # User complaints
            cur.execute("SELECT * FROM complaints WHERE user_id=%s ORDER BY created_at DESC LIMIT 5",
                        (session['user_id'],))
            complaints = cur.fetchall()
            # Announcements
            cur.execute("SELECT * FROM announcements ORDER BY created_at DESC LIMIT 3")
            announcements = cur.fetchall()
            # Stats
            cur.execute("SELECT COUNT(*) as total FROM complaints WHERE user_id=%s", (session['user_id'],))
            total_complaints = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) as total FROM complaints WHERE user_id=%s AND status='Resolved'",
                        (session['user_id'],))
            resolved = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) as total FROM schemes")
            total_schemes = cur.fetchone()['total']

        stats = {
            'total_complaints': total_complaints,
            'resolved': resolved,
            'pending': total_complaints - resolved,
            'total_schemes': total_schemes
        }
        return render_template('dashboard.html', schemes=schemes, complaints=complaints,
                               announcements=announcements, stats=stats)
    finally:
        db.close()

@app.route('/schemes')
@login_required
def schemes():
    """View all schemes with search/filter."""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    db = get_db()
    try:
        with db.cursor() as cur:
            query = "SELECT * FROM schemes WHERE 1=1"
            params = []
            if search:
                query += " AND (title LIKE %s OR description LIKE %s)"
                params += [f'%{search}%', f'%{search}%']
            if category:
                query += " AND category=%s"
                params.append(category)
            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
            all_schemes = cur.fetchall()
            cur.execute("SELECT DISTINCT category FROM schemes")
            categories = [r['category'] for r in cur.fetchall()]
        return render_template('schemes.html', schemes=all_schemes,
                               categories=categories, search=search, selected_cat=category)
    finally:
        db.close()

@app.route('/schemes/<int:scheme_id>')
@login_required
def scheme_detail(scheme_id):
    """Scheme detail page."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM schemes WHERE id=%s", (scheme_id,))
            scheme = cur.fetchone()
        if not scheme:
            flash('Scheme not found.', 'warning')
            return redirect(url_for('schemes'))
        return render_template('scheme_detail.html', scheme=scheme)
    finally:
        db.close()

@app.route('/complaints', methods=['GET', 'POST'])
@login_required
def complaints():
    """View and submit complaints."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not description:
            flash('Please fill in all fields.', 'danger')
        elif len(description) < 20:
            flash('Description must be at least 20 characters.', 'danger')
        else:
            db = get_db()
            try:
                with db.cursor() as cur:
                    cur.execute(
                        "INSERT INTO complaints (user_id, title, description) VALUES (%s, %s, %s)",
                        (session['user_id'], title, description)
                    )
                flash('Complaint submitted successfully!', 'success')
                return redirect(url_for('complaints'))
            finally:
                db.close()

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM complaints WHERE user_id=%s ORDER BY created_at DESC",
                        (session['user_id'],))
            user_complaints = cur.fetchall()
        return render_template('complaint.html', complaints=user_complaints)
    finally:
        db.close()

# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT COUNT(*) as c FROM users WHERE is_admin=0")
            total_users = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM schemes")
            total_schemes = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM complaints")
            total_complaints = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM complaints WHERE status='Pending'")
            pending = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM complaints WHERE status='Resolved'")
            resolved = cur.fetchone()['c']
            cur.execute("""
                SELECT c.*, u.name as user_name, u.village
                FROM complaints c JOIN users u ON c.user_id=u.id
                ORDER BY c.created_at DESC LIMIT 10
            """)
            recent_complaints = cur.fetchall()
            cur.execute("SELECT * FROM users WHERE is_admin=0 ORDER BY created_at DESC LIMIT 8")
            recent_users = cur.fetchall()

        stats = {
            'total_users': total_users,
            'total_schemes': total_schemes,
            'total_complaints': total_complaints,
            'pending': pending,
            'resolved': resolved,
            'in_progress': total_complaints - pending - resolved
        }
        return render_template('admin_dashboard.html', stats=stats,
                               recent_complaints=recent_complaints, recent_users=recent_users)
    finally:
        db.close()

@app.route('/admin/schemes', methods=['GET', 'POST'])
@admin_required
def admin_schemes():
    """Admin scheme management."""
    if request.method == 'POST':
        action = request.form.get('action')
        db = get_db()
        try:
            with db.cursor() as cur:
                if action == 'add':
                    cur.execute(
                        "INSERT INTO schemes (title, description, eligibility, benefits, category) VALUES (%s,%s,%s,%s,%s)",
                        (request.form['title'], request.form['description'],
                         request.form['eligibility'], request.form['benefits'],
                         request.form['category'])
                    )
                    flash('Scheme added successfully!', 'success')
                elif action == 'update':
                    cur.execute(
                        "UPDATE schemes SET title=%s, description=%s, eligibility=%s, benefits=%s, category=%s WHERE id=%s",
                        (request.form['title'], request.form['description'],
                         request.form['eligibility'], request.form['benefits'],
                         request.form['category'], request.form['scheme_id'])
                    )
                    flash('Scheme updated successfully!', 'success')
                elif action == 'delete':
                    cur.execute("DELETE FROM schemes WHERE id=%s", (request.form['scheme_id'],))
                    flash('Scheme deleted.', 'info')
        finally:
            db.close()
        return redirect(url_for('admin_schemes'))

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM schemes ORDER BY created_at DESC")
            all_schemes = cur.fetchall()
        return render_template('admin_schemes.html', schemes=all_schemes)
    finally:
        db.close()

@app.route('/admin/complaints')
@admin_required
def admin_complaints():
    """Admin complaint management."""
    status_filter = request.args.get('status', '')
    db = get_db()
    try:
        with db.cursor() as cur:
            if status_filter:
                cur.execute("""
                    SELECT c.*, u.name as user_name, u.village, u.email as user_email
                    FROM complaints c JOIN users u ON c.user_id=u.id
                    WHERE c.status=%s ORDER BY c.created_at DESC
                """, (status_filter,))
            else:
                cur.execute("""
                    SELECT c.*, u.name as user_name, u.village, u.email as user_email
                    FROM complaints c JOIN users u ON c.user_id=u.id
                    ORDER BY c.created_at DESC
                """)
            all_complaints = cur.fetchall()
        return render_template('admin_complaints.html', complaints=all_complaints,
                               status_filter=status_filter)
    finally:
        db.close()

@app.route('/admin/complaints/update', methods=['POST'])
@admin_required
def update_complaint():
    """Update complaint status."""
    complaint_id = request.form.get('complaint_id')
    status = request.form.get('status')
    valid_statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected']
    if status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin_complaints'))
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE complaints SET status=%s WHERE id=%s", (status, complaint_id))
        flash(f'Complaint #{complaint_id} status updated to {status}.', 'success')
    finally:
        db.close()
    return redirect(url_for('admin_complaints'))

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin user management."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT u.*, COUNT(c.id) as complaint_count
                FROM users u LEFT JOIN complaints c ON u.id=c.user_id
                WHERE u.is_admin=0
                GROUP BY u.id ORDER BY u.created_at DESC
            """)
            users = cur.fetchall()
        return render_template('admin_users.html', users=users)
    finally:
        db.close()

@app.route('/admin/announcements', methods=['GET', 'POST'])
@admin_required
def admin_announcements():
    """Admin announcement management."""
    if request.method == 'POST':
        action = request.form.get('action')
        db = get_db()
        try:
            with db.cursor() as cur:
                if action == 'add':
                    cur.execute("INSERT INTO announcements (title, content) VALUES (%s, %s)",
                                (request.form['title'], request.form['content']))
                    flash('Announcement added!', 'success')
                elif action == 'delete':
                    cur.execute("DELETE FROM announcements WHERE id=%s", (request.form['ann_id'],))
                    flash('Announcement deleted.', 'info')
        finally:
            db.close()
        return redirect(url_for('admin_announcements'))

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
            announcements = cur.fetchall()
        return render_template('admin_announcements.html', announcements=announcements)
    finally:
        db.close()

# ============================================
# API ENDPOINT
# ============================================

@app.route('/api/complaints/<int:complaint_id>/status')
@login_required
def get_complaint_status(complaint_id):
    """API: Get complaint status."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT status FROM complaints WHERE id=%s AND user_id=%s",
                        (complaint_id, session['user_id']))
            result = cur.fetchone()
        if result:
            return jsonify({'status': result['status']})
        return jsonify({'error': 'Not found'}), 404
    finally:
        db.close()

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', error=str(e)), 500

# ============================================
# RUN
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)