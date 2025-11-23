# Orv Hub - Premium Video Streaming Platform

A modern, responsive video streaming platform built with Django, featuring live streaming capabilities, premium content management, and a professional user interface.

## Overview

Orv Hub is a full-featured video streaming platform designed for delivering premium video content with support for live streaming, video categorization, user authentication, and subscription management. The platform features a responsive design optimized for both desktop and mobile devices.

## Features

### Core Functionality
- **Video Management**: Upload, organize, and stream video content
- **Live Streaming**: Real-time live streaming capabilities
- **User Authentication**: Secure user registration and login system
- **Premium Content**: Support for premium and free content tiers
- **Categories**: Organized content categorization system
- **Search & Filter**: Advanced search and filtering options
- **Responsive Design**: Fully optimized for mobile and desktop devices

### Technical Features
- RESTful API architecture
- Token-based authentication
- Media file management
- Database migrations
- Static file serving
- CSRF protection
- Session management

## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **API**: Django REST Framework
- **Task Queue**: Celery (configured)
- **Cache**: Redis (configured)

## Project Structure

```
Video-platform/
├── accounts/          # User authentication and profile management
├── videos/            # Video content management
├── payments/          # Payment processing
├── categories/        # Category management
├── tags/              # Tagging system
├── moderation/        # Content moderation
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

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Video-platform
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file in the project root for environment-specific settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration

The project is configured to use SQLite by default for development. For production, update the database settings in `video_platform/settings.py` to use PostgreSQL or your preferred database.

## API Endpoints

The platform includes REST API endpoints for:

- User authentication (`/api/auth/`)
- Video management (`/api/videos/`)
- Category listing (`/api/categories/`)
- Payment processing (`/api/payments/`)

API documentation is available when running the development server.

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow PEP 8 guidelines for Python code. Use Django's coding style for templates and views.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Set up media file storage (AWS S3 or similar)
- [ ] Configure email backend
- [ ] Set up SSL/HTTPS
- [ ] Configure Celery and Redis for background tasks
- [ ] Set up monitoring and logging

### Recommended Production Stack

- **Web Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL
- **Cache**: Redis
- **Media Storage**: AWS S3 or similar
- **Task Queue**: Celery with Redis broker

## Security

- CSRF protection enabled
- XSS protection
- SQL injection protection (Django ORM)
- Secure password hashing
- Session security
- Content Security Policy ready

## License

This project is proprietary software. All rights reserved.

## Support

For issues, questions, or contributions, please contact the development team.

## Changelog

### Version 1.0.0
- Initial release
- Core video streaming functionality
- User authentication system
- Responsive UI/UX design
- Mobile optimization
- Live streaming support
- Premium content management
