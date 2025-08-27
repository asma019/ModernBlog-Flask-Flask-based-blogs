from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import markdown
import os
from datetime import datetime
import uuid
from slugify import slugify
import google.generativeai as genai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=['codehilite', 'fenced_code'])
    
    @property
    def approved_comments(self):
        return Comment.query.filter_by(post_id=self.id, approved=True).order_by(Comment.created_at.desc()).all()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text)
    
    @staticmethod
    def get(key, default=''):
        setting = Setting.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set(key, value):
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Setting(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=['codehilite', 'fenced_code'])

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    tracking_code = Setting.get('tracking_code')
    ads_header = Setting.get('ads_header')
    ads_footer = Setting.get('ads_footer')
    return render_template('index.html', posts=posts, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo, tracking_code=tracking_code, ads_header=ads_header, ads_footer=ads_footer)

@app.route('/post/<slug>', methods=['GET', 'POST'])
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    categories = Category.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        
        comment = Comment(name=name, email=email, content=content, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment submitted! It will appear after admin approval.')
        return redirect(url_for('post_detail', slug=slug))
    
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    tracking_code = Setting.get('tracking_code')
    ads_header = Setting.get('ads_header')
    ads_footer = Setting.get('ads_footer')
    return render_template('post_detail.html', post=post, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo, tracking_code=tracking_code, ads_header=ads_header, ads_footer=ads_footer)

@app.route('/category/<slug>')
def category_posts(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category=category, published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('category.html', posts=posts, category=category, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        posts = Post.query.filter(
            Post.published == True,
            db.or_(
                Post.title.contains(query),
                Post.content.contains(query),
                Post.excerpt.contains(query)
            )
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=6, error_out=False)
    else:
        posts = Post.query.filter_by(published=False).paginate(page=1, per_page=1, error_out=False)
    
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('search.html', posts=posts, query=query, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo)

@app.route('/page/<slug>', methods=['GET', 'POST'])
def page_detail(slug):
    page = Page.query.filter_by(slug=slug, published=True).first_or_404()
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    
    # Handle contact form submission
    if request.method == 'POST' and slug == 'contact':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        flash('Message sent successfully! We will get back to you soon.')
        return redirect(url_for('page_detail', slug=slug))
    
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('page_detail.html', page=page, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('categories.html', categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo)

@app.route('/tag/<slug>')
def tag_posts(slug):
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = tag.posts.filter_by(published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('tag.html', posts=posts, tag=tag, categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check database users first
        user = User.query.filter_by(username=username, is_admin=True).first()
        if user and user.check_password(password):
            session['admin'] = True
            session['admin_user'] = user.username
            return redirect(url_for('admin_dashboard'))
        # Fallback to default admin
        elif username == 'mehedims' and password == 'admin2244':
            session['admin'] = True
            session['admin_user'] = 'mehedims'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    posts_count = Post.query.count()
    published_count = Post.query.filter_by(published=True).count()
    categories_count = Category.query.count()
    tags_count = Tag.query.count()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         posts_count=posts_count,
                         published_count=published_count,
                         categories_count=categories_count,
                         tags_count=tags_count,
                         pending_comments=pending_comments,
                         unread_contacts=unread_contacts,
                         recent_posts=recent_posts)

@app.route('/admin/posts')
@admin_required
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/posts.html', posts=posts, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/posts/new', methods=['GET', 'POST'])
@admin_required
def admin_new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        excerpt = request.form['excerpt']
        category_id = request.form.get('category_id') or None
        published = 'published' in request.form
        
        # Handle cover image upload
        cover_image = None
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_image = filename
        
        # Create slug with custom option
        custom_slug = request.form.get('slug', '').strip()
        base_slug = slugify(custom_slug) if custom_slug else slugify(title)
        
        # Ensure slug uniqueness
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        post = Post(title=title, slug=slug, content=content, excerpt=excerpt,
                   cover_image=cover_image, category_id=category_id, published=published)
        
        # Handle tags
        tag_names = [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('admin_posts'))
    
    categories = Category.query.all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/post_form.html', categories=categories, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/posts/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.excerpt = request.form['excerpt']
        post.category_id = request.form.get('category_id') or None
        post.published = 'published' in request.form
        
        # Handle custom slug
        custom_slug = request.form.get('slug', '').strip()
        base_slug = slugify(custom_slug) if custom_slug else slugify(post.title)
        
        # Ensure slug uniqueness (excluding current post)
        slug = base_slug
        counter = 1
        while Post.query.filter(Post.slug == slug, Post.id != post.id).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        post.slug = slug
        
        # Handle cover image upload
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.cover_image = filename
        
        # Handle tags
        post.tags.clear()
        tag_names = [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)
        
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('admin_posts'))
    
    categories = Category.query.all()
    tag_names = ', '.join([tag.name for tag in post.tags])
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/post_form.html', post=post, categories=categories, tag_names=tag_names, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/posts/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('admin_posts'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/categories.html', categories=categories, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/categories/new', methods=['POST'])
@admin_required
def admin_new_category():
    name = request.form['name']
    slug = slugify(name)
    category = Category(name=name, slug=slug)
    db.session.add(category)
    db.session.commit()
    flash('Category created successfully!')
    return redirect(url_for('admin_categories'))

@app.route('/admin/comments')
@admin_required
def admin_comments():
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/comments.html', comments=comments, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/comments/<int:id>/approve', methods=['POST'])
@admin_required
def admin_approve_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.approved = True
    db.session.commit()
    flash('Comment approved!')
    return redirect(url_for('admin_comments'))

@app.route('/admin/comments/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!')
    return redirect(url_for('admin_comments'))

@app.route('/admin/pages')
@admin_required
def admin_pages():
    pages = Page.query.order_by(Page.created_at.desc()).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/pages.html', pages=pages, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/pages/new', methods=['GET', 'POST'])
@admin_required
def admin_new_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        published = 'published' in request.form
        custom_slug = request.form.get('slug', '').strip()
        slug = slugify(custom_slug) if custom_slug else slugify(title)
        
        page = Page(title=title, slug=slug, content=content, published=published)
        db.session.add(page)
        db.session.commit()
        flash('Page created successfully!')
        return redirect(url_for('admin_pages'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/page_form.html', pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/pages/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_page(id):
    page = Page.query.get_or_404(id)
    
    if request.method == 'POST':
        page.title = request.form['title']
        page.content = request.form['content']
        page.published = 'published' in request.form
        custom_slug = request.form.get('slug', '').strip()
        page.slug = slugify(custom_slug) if custom_slug else slugify(page.title)
        db.session.commit()
        flash('Page updated successfully!')
        return redirect(url_for('admin_pages'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/page_form.html', page=page, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/pages/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_page(id):
    page = Page.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted successfully!')
    return redirect(url_for('admin_pages'))

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/contacts.html', contacts=contacts, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/contacts/<int:id>/read', methods=['POST'])
@admin_required
def admin_mark_contact_read(id):
    contact = Contact.query.get_or_404(id)
    contact.read = True
    db.session.commit()
    flash('Message marked as read!')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Message deleted!')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/users.html', users=users, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/users/new', methods=['GET', 'POST'])
@admin_required
def admin_new_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        
        user = User(username=username, email=email, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('admin_users'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/user_form.html', pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/users/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form.get('password'):
            user.set_password(request.form['password'])
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('admin_users'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/user_form.html', user=user, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/users/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('admin_users'))

@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        # Check if using default admin
        if session.get('admin_user') == 'mehedims':
            if current_password == 'admin2244':
                # Create new admin user
                user = User(username='mehedims', email='admin@example.com', is_admin=True)
                user.set_password(new_password)
                db.session.add(user)
                db.session.commit()
                flash('Password changed successfully!')
            else:
                flash('Current password is incorrect')
        else:
            # Update existing user
            user = User.query.filter_by(username=session.get('admin_user')).first()
            if user and user.check_password(current_password):
                user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully!')
            else:
                flash('Current password is incorrect')
        
        return redirect(url_for('admin_profile'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/profile.html', pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/menu')
@admin_required
def admin_menu():
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/menu.html', menu_items=menu_items, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/menu/new', methods=['GET', 'POST'])
@admin_required
def admin_new_menu_item():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        order = int(request.form.get('order', 0))
        
        menu_item = MenuItem(title=title, url=url, order=order)
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item created successfully!')
        return redirect(url_for('admin_menu'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/menu_form.html', pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/menu/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    if request.method == 'POST':
        menu_item.title = request.form['title']
        menu_item.url = request.form['url']
        menu_item.order = int(request.form.get('order', 0))
        db.session.commit()
        flash('Menu item updated successfully!')
        return redirect(url_for('admin_menu'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/menu_form.html', menu_item=menu_item, pending_comments=pending_comments, unread_contacts=unread_contacts)

@app.route('/admin/menu/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    db.session.delete(menu_item)
    db.session.commit()
    flash('Menu item deleted successfully!')
    return redirect(url_for('admin_menu'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        Setting.set('site_name', request.form.get('site_name', 'ModernBlog'))
        Setting.set('gemini_api_key', request.form.get('gemini_api_key', ''))
        Setting.set('tracking_code', request.form.get('tracking_code', ''))
        Setting.set('ads_header', request.form.get('ads_header', ''))
        Setting.set('ads_sidebar', request.form.get('ads_sidebar', ''))
        Setting.set('ads_footer', request.form.get('ads_footer', ''))
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename:
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    filename = 'logo.' + file.filename.rsplit('.', 1)[1].lower()
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    Setting.set('logo', filename)
        
        flash('Settings saved successfully!')
        return redirect(url_for('admin_settings'))
    
    pending_comments = Comment.query.filter_by(approved=False).count()
    unread_contacts = Contact.query.filter_by(read=False).count()
    return render_template('admin/settings.html', 
                         site_name=Setting.get('site_name', 'ModernBlog'),
                         logo=Setting.get('logo'),
                         gemini_api_key=Setting.get('gemini_api_key'),
                         tracking_code=Setting.get('tracking_code'),
                         ads_header=Setting.get('ads_header'),
                         ads_sidebar=Setting.get('ads_sidebar'),
                         ads_footer=Setting.get('ads_footer'),
                         pending_comments=pending_comments,
                         unread_contacts=unread_contacts)

@app.route('/admin/upload', methods=['POST'])
@admin_required
def admin_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type'}), 400
    
    if file:
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'url': url_for('static', filename=f'uploads/{filename}')})

@app.route('/admin/generate-blog', methods=['POST'])
@admin_required
def admin_generate_blog():
    try:
        api_key = Setting.get('gemini_api_key')
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 400
        
        topic = request.json.get('topic', '').strip()
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate title
        title_prompt = f"Create an engaging, SEO-friendly blog post title about: {topic}. Return only the title, nothing else."
        title_response = model.generate_content(title_prompt)
        title = title_response.text.strip().replace('"', '')
        
        # Generate excerpt
        excerpt_prompt = f"Write a compelling 2-3 sentence excerpt/summary for a blog post about: {topic}. Make it engaging and informative. Return only the excerpt, nothing else."
        excerpt_response = model.generate_content(excerpt_prompt)
        excerpt = excerpt_response.text.strip().replace('"', '')
        
        # Generate content
        content_prompt = f"""
Write a comprehensive, well-structured blog post about: {topic}

Requirements:
- Use proper markdown formatting with headings (##, ###)
- Include practical examples and actionable tips
- Make it informative and engaging
- Aim for 800-1500 words
- Use bullet points and numbered lists where appropriate
- Include a conclusion section
- Write in a professional but accessible tone

Return only the markdown content, no additional text or formatting.
"""
        
        content_response = model.generate_content(content_prompt)
        content = content_response.text.strip()
        
        return jsonify({
            'title': title,
            'excerpt': excerpt,
            'content': content
        })
            
    except Exception as e:
        return jsonify({'error': f'Failed to generate blog: {str(e)}'}), 500

@app.route('/robots.txt')
def robots_txt():
    base_url = request.url_root.rstrip('/')
    return '''User-agent: *
Allow: /
Disallow: /admin/
Sitemap: {}/sitemap.xml'''.format(base_url), 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap_xml():
    base_url = request.url_root.rstrip('/')
    
    posts = Post.query.filter_by(published=True).all()
    pages = Page.query.filter_by(published=True).all()
    categories = Category.query.all()
    
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # Homepage
    sitemap += f'''  <url>
    <loc>{base_url}</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
'''
    
    # Posts
    for post in posts:
        sitemap += f'''  <url>
    <loc>{base_url}/post/{post.slug}</loc>
    <lastmod>{post.updated_at.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
    
    # Pages
    for page in pages:
        sitemap += f'''  <url>
    <loc>{base_url}/page/{page.slug}</loc>
    <lastmod>{page.updated_at.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
'''
    
    # Categories
    for category in categories:
        sitemap += f'''  <url>
    <loc>{base_url}/category/{category.slug}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    
    # Categories page
    sitemap += f'''  <url>
    <loc>{base_url}/categories</loc>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
'''
    
    sitemap += '</urlset>'
    
    response = app.response_class(sitemap, mimetype='application/xml')
    return response

@app.errorhandler(404)
def not_found_error(error):
    categories = Category.query.all()
    pages = Page.query.filter_by(published=True).all()
    menu_items = MenuItem.query.filter_by(active=True).order_by(MenuItem.order).all()
    site_name = Setting.get('site_name', 'ModernBlog')
    logo = Setting.get('logo')
    return render_template('404.html', categories=categories, pages=pages, menu_items=menu_items, site_name=site_name, logo=logo), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)