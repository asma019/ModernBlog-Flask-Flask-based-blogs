#!/usr/bin/env python3
"""
Database initialization script for ModernBlog
Creates tables and adds sample data
"""

from app import app, db, Category, Tag, Post
from slugify import slugify
from datetime import datetime

def init_database():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Check if data already exists
        if Category.query.first():
            print("✓ Database already has data")
            return
        
        # Create sample categories
        categories_data = [
            "Technology",
            "Web Development", 
            "Python",
            "Tutorial",
            "News"
        ]
        
        categories = []
        for cat_name in categories_data:
            category = Category(name=cat_name, slug=slugify(cat_name))
            db.session.add(category)
            categories.append(category)
        
        # Create sample tags
        tags_data = [
            "flask", "python", "web", "tutorial", "beginner",
            "advanced", "tips", "guide", "coding", "development"
        ]
        
        tags = []
        for tag_name in tags_data:
            tag = Tag(name=tag_name, slug=slugify(tag_name))
            db.session.add(tag)
            tags.append(tag)
        
        db.session.commit()
        print("✓ Sample categories and tags created")
        
        # Create sample posts
        sample_posts = [
            {
                "title": "Welcome to ModernBlog",
                "content": """# Welcome to ModernBlog!

This is your first blog post. ModernBlog is a modern, feature-rich blogging platform built with Flask.

## Features

- **Markdown Support**: Write your posts in Markdown for easy formatting
- **Image Uploads**: Upload and manage images for your posts
- **Categories & Tags**: Organize your content with categories and tags
- **SEO Friendly**: Built-in SEO optimization features
- **Responsive Design**: Looks great on all devices
- **Admin Panel**: Easy-to-use admin interface

## Getting Started

1. Log in to the admin panel using your credentials
2. Create categories to organize your content
3. Write your first blog post using the markdown editor
4. Upload images and set featured images for your posts
5. Publish and share your content!

Happy blogging! 🎉""",
                "excerpt": "Welcome to ModernBlog - a modern, feature-rich blogging platform built with Flask. Learn about all the amazing features and how to get started.",
                "published": True,
                "category": categories[0],  # Technology
                "tags": [tags[0], tags[1], tags[2]]  # flask, python, web
            },
            {
                "title": "Getting Started with Flask",
                "content": """# Getting Started with Flask

Flask is a lightweight and powerful web framework for Python. In this tutorial, we'll cover the basics of building web applications with Flask.

## What is Flask?

Flask is a micro web framework written in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications.

## Installation

```bash
pip install Flask
```

## Your First Flask App

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

## Key Concepts

- **Routes**: Define URL patterns and their handlers
- **Templates**: Use Jinja2 for dynamic HTML generation
- **Request Handling**: Process GET, POST, and other HTTP methods
- **Session Management**: Handle user sessions and authentication

Flask's simplicity makes it perfect for both beginners and experienced developers!""",
                "excerpt": "Learn the basics of Flask, a lightweight Python web framework. Perfect for beginners starting their web development journey.",
                "published": True,
                "category": categories[1],  # Web Development
                "tags": [tags[0], tags[1], tags[3], tags[4]]  # flask, python, tutorial, beginner
            },
            {
                "title": "Python Best Practices for 2024",
                "content": """# Python Best Practices for 2024

Writing clean, maintainable Python code is essential for any developer. Here are the top best practices to follow in 2024.

## Code Style and Formatting

### Use Black for Code Formatting
```bash
pip install black
black your_file.py
```

### Follow PEP 8 Guidelines
- Use 4 spaces for indentation
- Keep lines under 88 characters (Black's default)
- Use meaningful variable names

## Project Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── main.py
├── tests/
├── requirements.txt
├── README.md
└── setup.py
```

## Error Handling

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
```

## Type Hints

```python
def calculate_total(items: List[float]) -> float:
    return sum(items)
```

Following these practices will make your Python code more professional and maintainable!""",
                "excerpt": "Discover the essential Python best practices for 2024. Learn about code style, project structure, error handling, and more.",
                "published": True,
                "category": categories[2],  # Python
                "tags": [tags[1], tags[5], tags[6], tags[8]]  # python, advanced, tips, coding
            }
        ]
        
        for post_data in sample_posts:
            post = Post(
                title=post_data["title"],
                slug=slugify(post_data["title"]),
                content=post_data["content"],
                excerpt=post_data["excerpt"],
                published=post_data["published"],
                category=post_data["category"]
            )
            
            # Add tags
            for tag in post_data["tags"]:
                post.tags.append(tag)
            
            db.session.add(post)
        
        db.session.commit()
        print("✓ Sample blog posts created")
        print("\n🎉 Database initialization complete!")
        print("\nYou can now:")
        print("1. Run the application: python app.py")
        print("2. Visit http://localhost:5000 to see your blog")
        print("3. Login to admin panel at http://localhost:5000/admin/login")
        print("   Username: mehedims")
        print("   Password: admin2244")

if __name__ == "__main__":
    init_database()