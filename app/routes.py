# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from .models import get_all_articles, get_article_by_slug, save_article, delete_article
from .auth import login_required, check_credentials

# --- Guest Blueprint ---
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    articles = get_all_articles()
    return render_template('home.html', articles=articles)

@main_bp.route('/article/<slug>')
def article(slug):
    article = get_article_by_slug(slug)
    if not article:
        abort(404)
    return render_template('article.html', article=article)

# --- Admin Blueprint ---
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_credentials(username, password):
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next') or url_for('admin.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@admin_bp.route('/')
@login_required
def dashboard():
    articles = get_all_articles()
    return render_template('admin/dashboard.html', articles=articles)

@admin_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date')
        
        if not title or not content or not date:
            flash('All fields are required.', 'danger')
        else:
            try:
                save_article(title, content, date)
                flash('Article published!', 'success')
                return redirect(url_for('admin.dashboard'))
            except ValueError as e:
                flash(str(e), 'danger')
    # Pass today's date as default for the form
    from datetime import date
    return render_template('admin/edit.html', article=None, today=date.today().isoformat())

@admin_bp.route('/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit_article(slug):
    article = get_article_by_slug(slug)
    if not article:
        abort(404)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date')
        
        if not title or not content or not date:
            flash('All fields are required.', 'danger')
        else:
            try:
                # Pass existing slug to keep URL same
                save_article(title, content, date, slug=slug)
                flash('Article updated!', 'success')
                return redirect(url_for('admin.dashboard'))
            except ValueError as e:
                flash(str(e), 'danger')
    
    return render_template('admin/edit.html', article=article, today=article['date'])

@admin_bp.route('/delete/<slug>', methods=['POST']) # POST only for safety
@login_required
def delete_article_route(slug):
    if delete_article(slug):
        flash('Article deleted.', 'success')
    else:
        flash('Article not found.', 'danger')
    return redirect(url_for('admin.dashboard'))
