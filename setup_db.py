#!/usr/bin/env python3
"""
Automatic Database Setup Script for ModernBlog
Detects database type and initializes automatically
"""

import os
import sys
from app import app, db

def setup_database():
    """Automatically detect and setup database"""
    
    print("🔍 Detecting database configuration...")
    
    # Check database configuration
    database_url = os.environ.get('DATABASE_URL')
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    
    with app.app_context():
        try:
            # Test database connection
            print("🔗 Testing database connection...")
            db.engine.execute('SELECT 1')
            
            # Check if database is PostgreSQL or SQLite
            if 'postgresql' in str(db.engine.url):
                print("✅ PostgreSQL detected")
                db_type = "PostgreSQL"
            else:
                print("✅ SQLite detected")
                db_type = "SQLite"
            
            print(f"🏗️  Setting up {db_type} database...")
            
            # Create all tables
            db.create_all()
            
            # Import models for data creation
            from app import Category, Tag, Post, Comment, Setting, Page, Contact, User, MenuItem
            from slugify import slugify
            from datetime import datetime
            
            # Check if database is already initialized
            if Setting.query.first():
                print("ℹ️  Database already initialized")
                return
            
            print("📋 Creating initial data...")
            
            # Create default categories
            categories_data = [
                'Programming', 'Web Development', 'Python', 'JavaScript', 
                'Technology', 'Tutorial', 'News', 'Tips & Tricks'
            ]
            
            for cat_name in categories_data:
                if not Category.query.filter_by(name=cat_name).first():
                    category = Category(name=cat_name, slug=slugify(cat_name))
                    db.session.add(category)
            
            # Create default tags
            tags_data = [
                'flask', 'python', 'web-dev', 'tutorial', 'beginner',
                'advanced', 'tips', 'coding', 'programming', 'tech'
            ]
            
            for tag_name in tags_data:
                if not Tag.query.filter_by(name=tag_name).first():
                    tag = Tag(name=tag_name, slug=slugify(tag_name))
                    db.session.add(tag)
            
            # Create default admin user
            if not User.query.filter_by(username='mehedims').first():
                admin_user = User(
                    username='mehedims',
                    email='admin@modernblog.com',
                    is_admin=True
                )
                admin_user.set_password('admin2244')
                db.session.add(admin_user)
            
            # Create default settings
            default_settings = [
                ('site_name', 'ModernBlog'),
                ('gemini_api_key', ''),
                ('tracking_code', ''),
                ('ads_header', ''),
                ('ads_content', ''),
                ('ads_sidebar', ''),
                ('ads_footer', ''),
                ('logo', '')
            ]
            
            for key, value in default_settings:
                if not Setting.query.filter_by(key=key).first():
                    setting = Setting(key=key, value=value)
                    db.session.add(setting)
            
            # Create sample pages
            if not Page.query.filter_by(slug='about').first():
                about_page = Page(
                    title='About Us',
                    slug='about',
                    content='''# About ModernBlog

Welcome to ModernBlog - a modern, feature-rich blogging platform built with Flask!

## Features

- AI-powered content generation with Google Gemini
- Responsive design with light/dark themes
- SEO optimized with complete meta tags
- Mobile-friendly admin panel
- Advertisement integration
- PostgreSQL and SQLite support

## Contact

Feel free to reach out to us for any questions or suggestions.
''',
                    published=True
                )
                db.session.add(about_page)
            
            if not Page.query.filter_by(slug='contact').first():
                contact_page = Page(
                    title='Contact',
                    slug='contact',
                    content='''# Contact Us

Get in touch with us using the form below:

<form method="POST" class="space-y-4 max-w-md">
    <div>
        <label for="name" class="block text-sm font-medium mb-1">Name *</label>
        <input type="text" id="name" name="name" required class="w-full px-3 py-2 border rounded-lg">
    </div>
    <div>
        <label for="email" class="block text-sm font-medium mb-1">Email *</label>
        <input type="email" id="email" name="email" required class="w-full px-3 py-2 border rounded-lg">
    </div>
    <div>
        <label for="subject" class="block text-sm font-medium mb-1">Subject *</label>
        <input type="text" id="subject" name="subject" required class="w-full px-3 py-2 border rounded-lg">
    </div>
    <div>
        <label for="message" class="block text-sm font-medium mb-1">Message *</label>
        <textarea id="message" name="message" rows="4" required class="w-full px-3 py-2 border rounded-lg"></textarea>
    </div>
    <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">Send Message</button>
</form>
''',
                    published=True
                )
                db.session.add(contact_page)
            
            # Create sample menu items
            menu_items = [
                ('About', '/page/about', 1),
                ('Contact', '/page/contact', 2)
            ]
            
            for title, url, order in menu_items:
                if not MenuItem.query.filter_by(title=title).first():
                    menu_item = MenuItem(title=title, url=url, order=order, active=True)
                    db.session.add(menu_item)
            
            # Commit all changes
            db.session.commit()
            
            # Create sample blog post
            if not Post.query.first():
                programming_cat = Category.query.filter_by(name='Programming').first()
                flask_tag = Tag.query.filter_by(name='flask').first()
                python_tag = Tag.query.filter_by(name='python').first()
                
                sample_post = Post(
                    title='Welcome to ModernBlog - Your AI-Powered Blogging Platform',
                    slug='welcome-to-modernblog',
                    content='''# Welcome to ModernBlog! 🚀

Welcome to **ModernBlog**, a cutting-edge blogging platform built with Flask that combines modern web technologies with AI-powered content generation.

## What Makes ModernBlog Special?

### 🤖 AI-Powered Content Generation
- Generate high-quality blog posts using Google Gemini 1.5 Pro
- One-click content creation from simple topic prompts
- Markdown-formatted output ready for publishing

### 🎨 Modern Design
- Beautiful responsive UI with Tailwind CSS
- Light/Dark theme toggle with persistent storage
- Mobile-first design approach
- Professional admin interface

### 📱 Mobile-Responsive Admin Panel
- Full admin functionality on mobile devices
- Touch-friendly interface with hamburger navigation
- Responsive dashboard and management tools

### 💰 Advertisement Integration
- Multiple ad zones (header, content, sidebar, footer)
- Google AdSense ready with responsive containers
- Strategic ad placement for optimal revenue

## Database Support

ModernBlog supports both **SQLite** (default) and **PostgreSQL** for production deployments with automatic setup and security features.

Happy blogging! 🎉
''',
                    excerpt='Welcome to ModernBlog - a modern, AI-powered blogging platform built with Flask. Discover features like AI content generation, responsive design, and mobile admin panel.',
                    published=True,
                    category_id=programming_cat.id if programming_cat else None
                )
                
                if flask_tag:
                    sample_post.tags.append(flask_tag)
                if python_tag:
                    sample_post.tags.append(python_tag)
                
                db.session.add(sample_post)
                db.session.commit()
            
            print(f"✅ {db_type} database setup completed successfully!")
            print("\n🎯 Next Steps:")
            print("1. Start the application: python app.py")
            print("2. Visit: http://localhost:5000")
            print("3. Admin login: http://localhost:5000/admin/login")
            print("   Username: mehedims")
            print("   Password: admin2244")
            print("\n🔧 Important:")
            print("- Change the default admin password immediately")
            print("- Configure your Gemini API key for AI features")
            print("- Set up your site branding and settings")
            
        except Exception as e:
            print(f"❌ Database setup failed: {str(e)}")
            print("\n🔍 Troubleshooting:")
            if 'postgresql' in str(e).lower():
                print("- Check PostgreSQL server is running")
                print("- Verify database credentials")
                print("- Ensure database exists")
            else:
                print("- Check file permissions")
                print("- Ensure SQLite is available")
            sys.exit(1)

if __name__ == '__main__':
    setup_database()