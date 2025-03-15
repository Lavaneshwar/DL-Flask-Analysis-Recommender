import os
import requests
import webbrowser
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
FLIC_TOKEN = os.getenv("FLIC_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")

# Initialize Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    thumbnail_url = db.Column(db.String(255))

# Function to fetch data from API with proper error handling
def fetch_data(endpoint):
    try:
        if not API_BASE_URL or not FLIC_TOKEN:
            raise ValueError("Missing API_BASE_URL or FLIC_TOKEN in environment variables")
        
        url = f"{API_BASE_URL}{endpoint}"
        headers = {"Flic-Token": FLIC_TOKEN}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("posts", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return []
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching data: {e}")
        return []

# Function to generate recommended posts based on user interactions
def recommend_posts():
    try:
        viewed_posts = fetch_data("/posts/view?page=1&page_size=1000")
        liked_posts = fetch_data("/posts/like?page=1&page_size=1000")
        inspired_posts = fetch_data("/posts/inspire?page=1&page_size=1000")
        rated_posts = fetch_data("/posts/rating?page=1&page_size=1000")

        all_posts = viewed_posts + liked_posts + inspired_posts + rated_posts
        return all_posts if all_posts else fetch_data("/posts/summary/get?page=1&page_size=1000")
    except Exception as e:
        print(f"Unexpected error in recommendation system: {e}")
        return []

# Fetch recommended posts on application start
posts = recommend_posts()

# HTML Template for displaying posts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recommended Posts</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: url("https://images.pexels.com/photos/326333/pexels-photo-326333.jpeg") no-repeat center center fixed; background-size: cover; color: white; }
        h1 { background: rgba(0, 0, 0, 0.6); padding: 20px; border-radius: 10px; display: inline-block; }
        .post-container { display: flex; flex-wrap: wrap; justify-content: center; margin: 20px; }
        .post { width: 250px; margin: 15px; padding: 15px; border: 1px solid #ccc; background: rgba(0, 0, 0, 0.6); border-radius: 10px; }
        img { width: 100%; height: auto; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Recommended Posts</h1>
    <div class="post-container">
        {% for post in posts %}
            <div class="post">
                <p><strong>{{ post.get('first_name', 'N/A') }} {{ post.get('last_name', 'N/A') }}</strong> (@{{ post.get('username', 'N/A') }})</p>
                {% if post.get('thumbnail_url') %}
                    <img src="{{ post.get('thumbnail_url') }}" alt="Post Image">
                {% else %}
                    <p>No Image Available</p>
                {% endif %}
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# Flask Route to render the home page with recommended posts
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, posts=posts)

# Run Flask server and open in browser
if __name__ == "__main__":
    try:
        url = "http://127.0.0.1:5000"
        print(f"Opening browser at {url}...")
        webbrowser.open(url)
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask server: {e}")
