# ModernBlog 🚀

A modern, feature-rich blogging platform built with Flask, featuring AI-powered content generation, beautiful responsive design, and comprehensive admin panel.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![AI Powered](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-purple.svg)

## ✨ Features

### 🎨 **Modern Design**
- Beautiful, responsive UI with Tailwind CSS
- Mobile-first design approach
- Dark gradient footer with social links
- Professional admin interface

### 🤖 **AI-Powered Content Generation**
- **Gemini 1.5 Pro Integration**: Generate high-quality blog posts with AI
- **One-Click Generation**: Enter a topic and get title, excerpt, and full content
- **Markdown Output**: AI generates properly formatted markdown content
- **Customizable**: Edit and refine AI-generated content

### 📝 **Content Management**
- **Markdown Editor**: EasyMDE with live preview and image upload
- **Custom URL Slugs**: SEO-friendly URLs with auto-generation
- **Categories & Tags**: Organize content efficiently
- **Image Upload**: Local server storage for cover photos and in-post images
- **Draft/Publish System**: Control content visibility

### 🔍 **SEO & Performance**
- **SEO Optimized**: Meta tags, Open Graph, Twitter Cards
- **Fast Loading**: Optimized assets and responsive images
- **Search Functionality**: Full-text search across posts
- **Structured Data**: JSON-LD for better search engine understanding

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

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/asma019/ModernBlog.git
cd ModernBlog
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize the database**
```bash
python init_db.py
```

4. **Run the application**
```bash
python app.py
```

5. **Access your blog**
- **Blog**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
  - Username: `mehedims`
  - Password: `admin2244`

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
DATABASE_URL="your-database-url"  # Optional: for PostgreSQL
```

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Asma** - [GitHub](https://github.com/asma019)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Google for the powerful Gemini AI
- Tailwind CSS for the beautiful styling system
- All contributors and users of this project

## 📞 Support

If you have any questions or need help:

1. Check the [Issues](https://github.com/asma019/ModernBlog/issues) page
2. Create a new issue if your problem isn't already reported
3. Star ⭐ this repository if you find it helpful!

---

**Happy Blogging!** 🎉

Made with ❤️ by [Asma](https://github.com/asma019)