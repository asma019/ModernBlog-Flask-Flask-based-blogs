#!/bin/bash

# ModernBlog Production Deployment Script
# Usage: ./deploy.sh yourdomain.com

if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh yourdomain.com"
    exit 1
fi

DOMAIN=$1
APP_DIR="/var/www/modernblog"

echo "🚀 Deploying ModernBlog to $DOMAIN..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🔧 Installing dependencies..."
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git -y

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
    echo "🔄 Updating existing repository..."
    cd $APP_DIR
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/asma019/ModernBlog.git $APP_DIR
    cd $APP_DIR
fi

# Setup virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Initialize database
echo "🗄️ Initializing database..."
python init_db.py

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/modernblog.service > /dev/null <<EOF
[Unit]
Description=ModernBlog Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="SECRET_KEY=$(openssl rand -hex 32)"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:$APP_DIR/modernblog.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/$DOMAIN > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/modernblog.sock;
    }
    
    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
echo "✅ Enabling site..."
sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo nginx -t

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start modernblog
sudo systemctl enable modernblog
sudo systemctl restart nginx

# Setup SSL
echo "🔒 Setting up SSL certificate..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo "✨ Deployment complete!"
echo "🌐 Your blog is now available at: https://$DOMAIN"
echo "🔧 Admin panel: https://$DOMAIN/admin/login"
echo "📊 Default credentials: mehedims / admin2244"
echo ""
echo "📝 Next steps:"
echo "1. Change admin password in Admin → Profile"
echo "2. Configure Gemini API key in Admin → Settings"
echo "3. Customize site name and logo in Admin → Settings"