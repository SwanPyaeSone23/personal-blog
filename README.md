# Personal Blog 📝

A simple Flask blog with file-based storage (JSON), Jinja2 templating, and session authentication.

## Features
- Guest: View articles list & read articles
- Admin: Dashboard, Create, Edit, Delete articles
- Markdown/JSON file storage (No database required)
- Bootstrap 5 UI

## Local Setup
```bash
git clone https://github.com/YOUR_USERNAME/personal-blog.git
cd personal-blog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your secrets
python run.py
