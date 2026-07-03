from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('welcome'))
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if session.get('user_id') is not None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        error = None
        
        if not fullname or not email or not username or not password:
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
            
        if error is None:
            db = get_db_connection()
            try:
                db.execute(
                    'INSERT INTO users (fullname, email, username, password_hash) VALUES (?, ?, ?, ?)',
                    (fullname, email, username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or {email} is already registered."
            else:
                db.close()
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('auth.login'))
            db.close()
            
        flash(error, 'error')
        
    return render_template('signup.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('user_id') is not None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        
        db = get_db_connection()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?', (identifier, identifier)
        ).fetchone()
        
        if user is None:
            error = 'Invalid username or email.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['fullname'] = user['fullname']
            if request.form.get('remember'):
                session.permanent = True
            return redirect(url_for('home'))
            
        flash(error, 'error')
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))

@auth_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')
