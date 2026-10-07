# app/auth.py
from functools import wraps
from flask import session, redirect, url_for, request, flash
import os

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access the admin area.', 'warning')
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_credentials(username, password):
    # In a real app, use hashed passwords & database. 
    # For this project: hardcoded from .env as per requirements.
    return (username == os.getenv('ADMIN_USERNAME') and 
            password == os.getenv('ADMIN_PASSWORD'))
