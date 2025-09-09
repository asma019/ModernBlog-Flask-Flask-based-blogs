# ModernBlog 🚀

A modern, feature-rich blogging platform built with Flask, featuring AI-powered content generation, beautiful responsive design, and comprehensive admin panel.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![AI Powered](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-purple.svg)
![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)
![Mobile](https://img.shields.io/badge/mobile-responsive-blue.svg)

## ✨ Features

### 🎨 **Modern Design**
- Beautiful, responsive UI with Tailwind CSS
- **Light/Dark Theme Toggle**: Persistent theme switching with localStorage
- Mobile-first design approach with touch-friendly interface
- Professional admin interface with mobile responsiveness
- Enhanced code blocks with copy functionality and syntax highlighting

### 🤖 **AI-Powered Content Generation**
- **Gemini 1.5 Pro Integration**: Generate high-quality blog posts with AI
- **One-Click Generation**: Enter a topic and get title, excerpt, and full content
- **Markdown Output**: AI generates properly formatted markdown content
- **Customizable**: Edit and refine AI-generated content

### 📝 **Content Management**
- **Markdown Editor**: EasyMDE with live preview and image upload
- **Custom URL Slugs**: SEO-friendly URLs with auto-generation and manual override
- **Categories & Tags**: Full CRUD operations with edit/delete functionality
- **Image Upload**: Local server storage with UUID filenames for uniqueness
- **Draft/Publish System**: Control content visibility
- **Enhanced Editor**: Code syntax highlighting and copy-to-clipboard features

### 🔍 **SEO & Performance**
- **SEO Optimized**: Meta tags, Open Graph, Twitter Cards, JSON-LD structured data
- **Fast Loading**: Optimized assets and responsive images
- **Search Functionality**: Full-text search across posts, titles, and excerpts
- **Sitemap & Robots**: Auto-generated sitemap.xml and robots.txt
- **Custom 404 Page**: Branded error page with navigation

### 👨‍💼 **Admin Panel**
- **Dashboard**: Overview statistics and recent posts
- **User Management**: Role-based access control
- **Comment System**: Moderation with approval workflow
- **Contact Forms**: Built-in contact form management
- **Menu Management**: Custom navigation menus
- **Settings Panel**: Site branding, analytics, ads integration

### 📱 **Responsive & Accessible**
- Works perfectly on desktop, tablet, and mobile
- Touch-friendly interface
- Keyboard navigation support
- Screen reader compatible

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- **Optional**: PostgreSQL 12+ (for production use)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/asma019/ModernBlog-Flask-Flask-based-blogs.git
cd ModernBlog-Flask-Flask-based-blogs
```

2. **Create virtual environment and install dependencies**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Initialize the database**

**Automatic Setup (Recommended):**
```bash
# For SQLite (Default)
python setup_db.py

# For PostgreSQL - Set environment variables first:
export DB_HOST="localhost"
export DB_NAME="modernblog"
export DB_USER="mdernblog"
export DB_PASS="your-db-password"
export DB_PORT="5432"  # Optional

# Install PostgreSQL dependencies
pip install -r requirements_postgres.txt

# Run automatic setup
python setup_db.py
```

**Manual Setup (Alternative):**
```bash
# SQLite
python init_db.py

# PostgreSQL
python init_db_postgres.py
```

4. **Run the application**
```bash
# Make sure virtual environment is activated
python app.py
```

5. **Access your blog**
- **Blog**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
  - Username: `mehedims`
  - Password: `admin2244`

### 🎯 First Steps After Installation
1. **Change Admin Password**: Go to Admin → Profile to update default credentials
2. **Configure Site Settings**: Admin → Settings to set site name, logo, and API keys
3. **Set Up Analytics**: Add Google Analytics code in Admin → Settings
4. **Configure Ads**: Set up ad codes for monetization in Admin → Settings
5. **Create Content**: Start with Admin → Posts → New Post

## 🤖 AI Setup (Optional)

To enable AI blog generation:

1. **Get Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a free API key

2. **Configure in Admin**
   - Go to Admin → Settings
   - Enter your Gemini API key
   - Save settings

3. **Generate Content**
   - Go to Admin → Posts → New Post
   - Enter a topic in the AI generation field
   - Click "Generate" to create content with AI

## 📁 Project Structure

```
ModernBlog/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_db.py            # Database initialization
├── blog.db               # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── post_detail.html  # Blog post page
│   └── admin/            # Admin templates
├── static/               # Static files
│   ├── css/style.css     # Custom styles
│   ├── js/main.js        # JavaScript
│   └── uploads/          # Image uploads
└── README.md             # This file
```

## 🌐 Deployment

### Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-blog-name
```

2. **Set environment variables**
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set GEMINI_API_KEY="your-gemini-key"
```

3. **Deploy**
```bash
git push heroku main
```

### VPS/Server Deployment

1. **Install dependencies**
```bash
pip install gunicorn
```

2. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Set up reverse proxy** (Nginx recommended)

### Environment Variables

For production, set these environment variables:

```bash
SECRET_KEY="your-secret-key-here"
GEMINI_API_KEY="your-gemini-api-key"

# PostgreSQL Option 1: Individual variables
DB_HOST="localhost"
DB_NAME="modernblog"
DB_USER="mdernblog"
DB_PASS="your-db-password"
DB_PORT="5432"  # Optional

# PostgreSQL Option 2: Single URL
DATABASE_URL="postgresql://username:password@host:port/database"
```

## 🔒 Database Security

### Security Features
- **Connection Encryption**: SSL/TLS support for PostgreSQL connections
- **URL Encoding**: Automatic escaping of special characters in credentials
- **Connection Pooling**: Prevents connection exhaustion attacks
- **Timeout Protection**: 10-second connection timeout prevents hanging
- **Pool Pre-ping**: Validates connections before use
- **Connection Recycling**: Automatic connection refresh every 5 minutes

### Best Practices
- Use strong passwords for database users
- Enable SSL/TLS for production PostgreSQL connections
- Regularly rotate database credentials
- Use environment variables, never hardcode credentials
- Limit database user permissions to minimum required

## 🗄️ Database Support

### SQLite (Default)
- **Perfect for**: Development, small to medium blogs
- **Setup**: Zero configuration, file-based database
- **Pros**: Easy setup, no server required, portable
- **Cons**: Limited concurrent users, no advanced features

### PostgreSQL (Production)
- **Perfect for**: Production, high-traffic blogs, scalability
- **Setup**: Requires PostgreSQL server installation
- **Pros**: High performance, concurrent users, advanced features, ACID compliance
- **Cons**: Requires server setup and maintenance

### PostgreSQL Setup

1. **Install PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib

# macOS
brew install postgresql

# Windows: Download from https://www.postgresql.org/download/
```

2. **Create Database and User (Secure Setup)**
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE modernblog;

# Create user with strong password
CREATE USER bloguser WITH PASSWORD 'your_strong_password_here';

# Grant only necessary privileges
GRANT CONNECT ON DATABASE modernblog TO bloguser;
GRANT USAGE ON SCHEMA public TO bloguser;
GRANT CREATE ON SCHEMA public TO bloguser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bloguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bloguser;

# Enable SSL (recommended for production)
ALTER SYSTEM SET ssl = on;
SELECT pg_reload_conf();

\q
```

3. **Set Environment Variables**
```bash
# Option 1: Individual variables (Recommended)
export DB_HOST="localhost"
export DB_NAME="modernblog"
export DB_USER="bloguser"
export DB_PASS="your_password"
export DB_PORT="5432"

# Option 2: Single URL
export DATABASE_URL="postgresql://bloguser:your_password@localhost/modernblog"
```

### Database Migration
```bash
# Export from SQLite
sqlite3 blog.db .dump > backup.sql

# Import to PostgreSQL (after creating database)
psql -d modernblog -f backup.sql
```

### 🌐 Production Deployment with Custom Domain

#### **Option 1: VPS/Server Deployment (Recommended)**

1. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y
```

2. **Deploy Application**
```bash
# Clone repository
git clone https://github.com/asma019/ModernBlog-Flask-Flask-based-blogs.git
cd ModernBlog-Flask-Flask-based-blogs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Initialize database
python init_db.py
```

3. **Create Gunicorn Service**
```bash
sudo nano /etc/systemd/system/modernblog.service
```

Add this content:
```ini
[Unit]
Description=ModernBlog Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/ModernBlog
Environment="PATH=/path/to/ModernBlog/venv/bin"
Environment="SECRET_KEY=your-secret-key-here"
Environment="GEMINI_API_KEY=your-gemini-key"
ExecStart=/path/to/ModernBlog/venv/bin/gunicorn --workers 3 --bind unix:modernblog.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/yourdomain.com
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/ModernBlog/modernblog.sock;
    }
    
    location /static {
        alias /path/to/ModernBlog/static;
        expires 30d;
    }
}
```

5. **Enable Site and SSL**
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Start services
sudo systemctl start modernblog
sudo systemctl enable modernblog

# Install SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### **Option 2: Docker Deployment**

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=your-secret-key
      - GEMINI_API_KEY=your-gemini-key
    volumes:
      - ./static/uploads:/app/static/uploads
      - ./blog.db:/app/blog.db
```

Deploy:
```bash
docker-compose up -d
```

#### **Domain Configuration**

**Important**: The application automatically detects your domain:
- **Development**: `http://localhost:5000` 
- **Production**: `https://yourdomain.com`
- **Custom Domain**: Any domain you configure

No manual URL changes needed! The sitemap, robots.txt, and all SEO meta tags automatically adapt to your domain.

## 🛠️ Built With

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: Tailwind CSS, JavaScript, Font Awesome
- **AI**: Google Gemini 1.5 Pro
- **Editor**: EasyMDE Markdown Editor
- **Security**: Werkzeug password hashing

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 AI Content Generation | Gemini-powered blog writing | ✅ |
| 📝 Markdown Editor | Rich text editing with preview | ✅ |
| 🖼️ Image Upload | Local file storage | ✅ |
| 🏷️ Categories & Tags | Content organization | ✅ |
| 🔍 Search | Full-text search | ✅ |
| 💬 Comments | Moderated comment system | ✅ |
| 👥 User Management | Admin and user roles | ✅ |
| 📱 Responsive Design | Mobile-friendly | ✅ |
| 🔒 SEO Optimized | Meta tags, structured data | ✅ |
| 📊 Analytics Ready | Google Analytics integration | ✅ |

## 🎯 Use Cases

### 📝 **Personal Blog**
- Share your thoughts and experiences
- Build your personal brand
- Showcase your expertise

### 💼 **Business Blog**
- Content marketing
- SEO-driven traffic generation
- Customer engagement

### 🏢 **Company Website**
- Corporate communications
- Product updates and announcements
- Industry insights and thought leadership

### 🎓 **Educational Content**
- Tutorial and how-to guides
- Course materials and resources
- Knowledge sharing platform

### 📰 **News & Media**
- News publication
- Magazine-style content
- Community-driven content

## 🆕 Recent Updates

### Version 2.1.0 (Latest)
- ✅ **Mobile-Responsive Admin Panel**: Full admin functionality on mobile devices
- ✅ **Light/Dark Theme Toggle**: Persistent theme switching with localStorage
- ✅ **Enhanced Ad Integration**: Multi-zone responsive ads with Google AdSense support
- ✅ **Category Management**: Full CRUD operations with edit/delete functionality
- ✅ **Code Enhancement**: Syntax highlighting and copy-to-clipboard features
- ✅ **Mobile Admin Navigation**: Hamburger menu and touch-friendly interface
- ✅ **Improved SEO**: Complete meta tags, structured data, and sitemap generation
- ✅ **Custom 404 Page**: Branded error handling with navigation
- ✅ **Enhanced Security**: UUID-based file naming and improved validation

### Bug Fixes
- 🐛 Fixed mobile admin panel navigation issues
- 🐛 Resolved post management visibility on mobile devices
- 🐛 Improved responsive design across all admin pages
- 🐛 Fixed theme persistence and switching functionality
- 🐛 Enhanced mobile touch targets and interaction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 🐛 Reporting Issues
- Use GitHub Issues for bug reports
- Include steps to reproduce the issue
- Specify your environment (OS, Python version, browser)
- Screenshots are helpful for UI issues

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mehedi Hasan** - [GitHub](https://github.com/asma019)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Google for the powerful Gemini AI
- Tailwind CSS for the beautiful styling system
- All contributors and users of this project

## 📞 Support

If you have any questions or need help:

1. Check the [Issues](https://github.com/asma019/ModernBlog-Flask-Flask-based-blogs/issues) page
2. Create a new issue if your problem isn't already reported
3. Star ⭐ this repository if you find it helpful!
4. Join discussions for feature requests and improvements

### 🔧 Troubleshooting

**Common Issues:**
- **Admin panel not responsive on mobile**: Clear browser cache and refresh
- **Theme not switching**: Check if JavaScript is enabled in your browser
- **AI generation not working**: Verify Gemini API key in Admin → Settings
- **Images not uploading**: Check file permissions on `static/uploads/` directory
- **Database setup fails**: Run `python setup_db.py` for automatic setup
- **SQLite database errors**: Run `python setup_db.py` to reinitialize
- **PostgreSQL connection errors**: Check credentials and PostgreSQL service status
- **PostgreSQL permission errors**: Ensure user has proper database privileges
- **SSL connection errors**: Check PostgreSQL SSL configuration

### 📱 Mobile Admin Access
- Use the hamburger menu (☰) to access navigation on mobile
- All admin features are fully functional on mobile devices
- Touch-friendly interface with proper button sizing

---

**Happy Blogging!** 🎉

Made with ❤️ by [Mehedi Hasan](https://github.com/asma019)

**Latest Version**: 2.1.0 | **Last Updated**: September 10 2025
