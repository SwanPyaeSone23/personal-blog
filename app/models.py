# app/models.py
import os
import json
import uuid
from datetime import datetime
from flask import current_app

def get_articles_dir():
    return current_app.config['ARTICLES_DIR']

def _get_filepath(slug):
    return os.path.join(get_articles_dir(), f"{slug}.json")

def generate_slug(title):
    """Simple slug generator: lowercase, spaces to hyphens, remove special chars."""
    import re
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = slug.strip('-')
    # Ensure uniqueness
    base_slug = slug
    counter = 1
    while os.path.exists(_get_filepath(slug)):
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

def get_all_articles(sort_desc=True):
    """Read all JSON files, return list of dicts."""
    articles = []
    for filename in os.listdir(get_articles_dir()):
        if filename.endswith('.json'):
            with open(os.path.join(get_articles_dir(), filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    articles.append(data)
                except json.JSONDecodeError:
                    continue
    # Sort by date
    articles.sort(key=lambda x: x.get('date', ''), reverse=sort_desc)
    return articles

def get_article_by_slug(slug):
    filepath = _get_filepath(slug)
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_article(title, content, date_str, slug=None):
    """Create or Update article."""
    if slug is None: # New article
        slug = generate_slug(title)
    
    # Validate date format (YYYY-MM-DD)
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Date must be YYYY-MM-DD format")

    article = {
        'slug': slug,
        'title': title,
        'content': content,
        'date': date_str,
        'created_at': datetime.now().isoformat() # Internal timestamp
    }
    
    filepath = _get_filepath(slug)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(article, f, indent=4, ensure_ascii=False)
    return slug

def delete_article(slug):
    filepath = _get_filepath(slug)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
