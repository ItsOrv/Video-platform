# Orv Hub - Video Streaming Platform

A comprehensive video streaming platform built with Django, featuring content management, user subscriptions, payment processing, and analytics.

## Overview

Orv Hub is a full-featured video streaming platform designed for delivering premium and free video content. The platform includes live streaming capabilities, user authentication, subscription management, content moderation, and comprehensive analytics.

## Features

### Content Management
- Video upload and streaming with thumbnail support
- Live streaming capabilities
- Video categorization and tagging system
- Playlist creation and management
- Premium and free content tiers
- Video pricing and purchase system
- Featured content management
- Watch history tracking
- Video duration and metadata management

### User Management
- Custom user authentication system
- User profiles with avatar and bio
- User following system
- Watch history and favorites
- Comment system with nested replies
- Like and dislike functionality for videos and comments

### Subscription & Payments
- Subscription plans (monthly and yearly)
- Individual video purchases
- Payment processing integration
- Payment history tracking
- Subscription expiry management
- Transaction management

### Content Organization
- Category-based organization
- Tag system for content discovery
- Advanced search and filtering
- Trending content
- Browse by category

### Platform Features
- Content moderation and reporting system
- Analytics dashboard for users, videos, and platform
- RESTful API with token authentication
- Responsive design for mobile and desktop
- DRM support for secure video streaming

## Technology Stack

### Backend
- Django 4.x
- Django REST Framework
- Celery for background tasks
- Redis for caching and task queue

### Database
- SQLite (development)
- PostgreSQL ready (production)

### Frontend
- HTML5, CSS3, JavaScript
- Responsive design

### Infrastructure
- Docker and Docker Compose support
- Gunicorn for production deployment
- WhiteNoise for static file serving
- AWS S3 ready for media storage

## Project Structure

```
Video-platform/
├── accounts/          # User authentication and profile management
├── videos/            # Video content management and streaming
├── payments/          # Payment processing and subscriptions
├── categories/        # Category management
├── tags/              # Tagging system
├── moderation/        # Content moderation and reporting
├── analytics/         # Analytics and reporting
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded media files
├── video_platform/    # Main project configuration
└── manage.py          # Django management script
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)
- Redis (for Celery and caching)
- PostgreSQL (optional, for production)

### Setup Instructions

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd Video-platform
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   CELERY_BROKER_URL=redis://localhost:6379/0
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   PAYMENT_GATEWAY_KEY=your-payment-gateway-key
   ```

5. Run migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files
   ```bash
   python manage.py collectstatic
   ```

8. Run development server
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose

```bash
docker-compose up --build
```

This will:
- Build the Docker image
- Run database migrations
- Collect static files
- Start the Gunicorn server on port 8000

## Configuration

### Environment Variables

Required environment variables:

- `SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `CELERY_BROKER_URL`: Redis connection URL for Celery
- `EMAIL_BACKEND`: Email backend configuration
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_USE_TLS`: Use TLS for email (True/False)
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `DEFAULT_FROM_EMAIL`: Default sender email
- `PAYMENT_GATEWAY_KEY`: Payment gateway API key
- `VIDEO_STREAMING_SERVER`: Video streaming server URL for DRM

### Database Configuration

The project uses SQLite by default for development. For production, update the database settings in `video_platform/settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Documentation

The platform includes REST API endpoints for:

- User authentication (`/api/auth/`)
- Video management (`/api/videos/`)
- Category listing (`/api/categories/`)
- Payment processing (`/api/payments/`)
- User profiles (`/api/accounts/`)

API documentation is available at `/api/docs/` when running the development server.

### Authentication

The API uses token-based authentication. Obtain a token by logging in through the API:

```bash
POST /api/auth/login/
{
    "username": "your_username",
    "password": "your_password"
}
```

Include the token in subsequent requests:

```
Authorization: Token your_token_here
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow PEP 8 guidelines for Python code. Use Django's coding style for templates and views.

### Background Tasks

Start Celery worker for background tasks:

```bash
celery -A video_platform worker -l info
```

Start Celery beat for scheduled tasks:

```bash
celery -A video_platform beat -l info
```

## Production Deployment

### Production Checklist

- Set `DEBUG = False` in settings
- Configure proper `ALLOWED_HOSTS`
- Set up production database (PostgreSQL recommended)
- Configure static file serving (WhiteNoise or CDN)
- Set up media file storage (AWS S3 or similar)
- Configure email backend with real SMTP service
- Set up SSL/HTTPS
- Configure Celery and Redis for background tasks
- Set up monitoring and logging
- Configure backup strategy
- Set up error tracking (Sentry recommended)

### Recommended Production Stack

- Web Server: Gunicorn or uWSGI
- Reverse Proxy: Nginx
- Database: PostgreSQL
- Cache: Redis
- Media Storage: AWS S3 or similar
- Task Queue: Celery with Redis broker
- Process Manager: Supervisor or systemd

### Security Settings

The platform includes comprehensive security features:

- CSRF protection enabled
- XSS protection
- SQL injection protection (Django ORM)
- Secure password hashing
- Session security
- Content Security Policy ready
- Secure cookie settings in production
- HSTS headers configured

## Models Overview

### Core Models

- `CustomUser`: Extended user model with phone number support
- `UserProfile`: User profile with subscription and avatar
- `Video`: Video content with metadata, pricing, and categorization
- `Category`: Video categories
- `Tag`: Content tags
- `Playlist`: User-created playlists
- `Comment`: Video comments with nested replies
- `Payment`: Payment transactions
- `Subscription`: User subscriptions
- `VideoPurchase`: Individual video purchases
- `WatchHistory`: User watch history tracking

## License

This project is proprietary software. All rights reserved.

## Support

For issues, questions, or contributions, please contact the development team.
