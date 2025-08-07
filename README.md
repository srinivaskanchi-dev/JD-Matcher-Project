# Fusion AI - AI-Powered Career Assistant

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

Fusion AI is an intelligent career assistance platform that revolutionizes the job application process. Built with Django and powered by Google's Gemini AI, it helps job seekers optimize their resumes, match them with job descriptions, and prepare for interviews with personalized AI guidance.

##📁 Project Structure
```
JD-Matcher-Project/
│
├── .gitignore                  # Git ignore file (includes .env)
├── manage.py                   # Django management script
├── requirements.txt            # All Python dependencies
├── FusionAI/                   # Django project folder
│   ├── settings.py             # Main settings (uses .env vars)
│   ├── urls.py                 # Project-level routes
│   └── wsgi.py                 # WSGI config for deployment
│
├── matcher/                    # Core app
│   ├── models.py               # DB models for resumes, scores, etc.
│   ├── views.py                # Views for upload, match, chat, etc.
│   ├── urls.py                 # App-level URL config
│   ├── templates/
│   │   └── *.html              # All UI templates (Home, Upload, etc.)
│   ├── static/
│   │   └── css/, js/, images/  # Custom styling and scripts
│   └── forms.py                # Django forms for file input
│
├── templates/
│   └── base.html               # Base layout with navbar & chat panel
│
├── media/                      # Uploaded resumes (served temporarily)
└── .env                        # 🔐 Secret credentials (Not committed!)
```

### ✨ Features

## 🤖 AI-Powered Resume Optimization
- **ATS-Friendly Resume Generation**: Automatically creates Applicant Tracking System (ATS) optimized resumes
- **Keyword Matching**: Identifies and highlights relevant keywords from job descriptions
- **Smart Content Enhancement**: Improves resume content with AI-driven suggestions
- **PDF Export**: Download optimized resumes in professional PDF format

## 📊 Intelligent Job Matching
- **Match Score Analysis**: Provides percentage-based compatibility scores
- **Keyword Extraction**: Automatically extracts key skills and requirements from job descriptions
- **Gap Analysis**: Identifies missing skills and suggests improvements
- **Visual Feedback**: Clear indicators of match quality and areas for improvement

## 🎯 Interview Preparation
- **Personalized Questions**: AI-generated interview questions based on your resume and job description
- **Context-Aware Responses**: Questions tailored to your specific experience and role
- **Practice Scenarios**: Realistic interview situations to prepare for
- **Skill Assessment**: Questions that test both technical and soft skills

## 💬 Interactive AI Chatbot
- **Real-time Assistance**: Get instant help with career-related questions
- **Context-Aware Responses**: Chatbot understands your resume and job context
- **Interview Coaching**: Receive personalized interview tips and advice
- **Resume Feedback**: Get suggestions for improving your resume

## 🔐 User Management
- **Secure Authentication**: User registration and login system
- **Profile Management**: Personal dashboard for managing resumes and applications
- **History Tracking**: View past resume analyses and improvements
- **Privacy Protection**: Secure handling of personal data

### 🛠️ Technology Stack

## Backend
- **Django 4.2+**: Robust web framework for rapid development
- **Python 3.8+**: Modern Python for AI and web development
- **Google Gemini AI**: Advanced AI model for content generation and analysis
- **SQLite/MySQL**: Database management (configurable)
- **Django ORM**: Object-relational mapping for database operations

## Frontend
- **Tailwind CSS**: Utility-first CSS framework for modern design
- **JavaScript (ES6+)**: Interactive user interface and AJAX functionality
- **HTML5**: Semantic markup for accessibility
- **Font Awesome**: Icon library for enhanced UI

## AI & Analysis
- **Google Gemini 2.0 Flash**: Advanced language model for content generation
- **TF-IDF Vectorization**: Text similarity analysis for job matching
- **SpaCy NLP**: Natural language processing for keyword extraction
- **Cosine Similarity**: Algorithm for calculating match scores

## Development Tools
- **Git**: Version control system
- **Virtual Environment**: Isolated Python environment
- **Django Debug Toolbar**: Development debugging
- **Pytest**: Testing framework

### 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **Google Gemini API Key** (for AI features)
- **MySQL** (optional, for production)

### 🚀 Installation

## 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fusion-ai.git
cd fusion-ai
```

## 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Environment Setup
Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Settings (for MySQL)
MYSQL_DATABASE=fusion_ai_db
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Google Gemini AI
GOOGLE_API_KEY=your-gemini-api-key-here
```

## 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## 6. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

### 📖 Usage Guide

## Getting Started

1. **Register/Login**: Create an account or log in to access all features
2. **Upload Resume**: Either upload a PDF file or paste your resume text
3. **Add Job Description**: Paste the job description you're applying for
4. **Get Analysis**: Receive instant feedback on your resume-job match
5. **Download Optimized Resume**: Get your ATS-optimized resume in PDF format

### Key Features Walkthrough

## Resume Upload
- **Supported Formats**: PDF files and plain text
- **File Size Limit**: Up to 10MB for PDF uploads
- **Text Processing**: Automatic extraction and cleaning of resume content

## Job Description Analysis
- **Keyword Extraction**: AI identifies key skills and requirements
- **Match Scoring**: Calculates compatibility percentage
- **Gap Analysis**: Highlights missing skills and experiences

## AI Chatbot
- **Context-Aware**: Understands your resume and job description
- **Real-time Responses**: Instant help with career questions
- **Interview Coaching**: Personalized interview preparation tips

## Resume Optimization
- **ATS Compliance**: Ensures resume passes through applicant tracking systems
- **Keyword Integration**: Naturally incorporates job-specific keywords
- **Professional Formatting**: Clean, professional layout
- **PDF Export**: Download ready-to-use resume

### 🔧 Configuration

## Django Settings
The main settings are in `jdmatcher/settings.py`:

```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('MYSQL_PORT'),
    }
}

# AI Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
```

### Environment Variables
Key environment variables to configure:

- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to False in production
- `GOOGLE_API_KEY`: Your Google Gemini AI API key
- Database credentials for MySQL

### 🗄️ Database Schema

### Core Models

#### UserInput
- `user`: Foreign key to Django User
- `resume_text`: Extracted resume content
- `jd_text`: Job description text
- `upload_time`: Timestamp of upload
- `match_score`: Calculated match percentage

#### ResumeResult
- `user_input`: One-to-one relationship with UserInput
- `ats_resume`: AI-generated optimized resume
- `interview_questions`: Generated interview questions
- `explanation`: Match score explanation

#### ChatLog
- `user`: Foreign key to Django User
- `user_message`: User's chat message
- `bot_response`: AI's response
- `created_at`: Timestamp of conversation

### 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **User Authentication**: Secure login/logout system
- **Session Management**: Secure session handling
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Template auto-escaping

### 🧪 Testing

Run tests to ensure everything works correctly:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
   ```bash
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Database Migration**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Web Server Setup**
   - Configure Nginx/Apache
   - Set up Gunicorn/uWSGI
   - Configure SSL certificates

### Recommended Production Stack

- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: MySQL/PostgreSQL
- **Cache**: Redis
- **File Storage**: AWS S3 (for media files)

### 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 Python style guide
- Write comprehensive tests
- Update documentation for new features
- Ensure all tests pass before submitting

### Acknowledgments

- **Google Gemini AI**: For providing the AI capabilities
- **Django Community**: For the excellent web framework
- **Tailwind CSS**: For the beautiful UI components
- **Font Awesome**: For the icon library

## 📞 Support

For support and questions:

- **Email**: srinivaskanchi25@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/fusion-ai/issues)
- **Documentation**: Check the project wiki

### 🔄 Version History

### v1.0.0 (Current)
- Initial release
- AI-powered resume optimization
- Job matching analysis
- Interactive chatbot
- User authentication system
- PDF export functionality

---

**Built with ❤️ by [Srinivas Kanchi](https://github.com/srinivaskanchi-dev)**
