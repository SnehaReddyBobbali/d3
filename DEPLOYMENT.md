# Deployment Guide - KLH Lost & Found System

## Quick Start Commands

### 1. Initial Setup

```powershell
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 2. Running the Server

```powershell
python manage.py runserver
```

Access at: http://localhost:8000/

## Google OAuth Setup (IMPORTANT!)

### Step-by-Step Google Cloud Console Configuration:

1. **Create/Select Project**
   - Go to: https://console.cloud.google.com/
   - Create new project or select existing
   - Project name: "KLH Lost and Found"

2. **Enable APIs**
   - Search for "Google+ API" and enable it
   - Or enable "Google Identity Services"

3. **Configure OAuth Consent Screen**
   - Go to: APIs & Services → OAuth consent screen
   - User Type: External
   - App name: KLH Lost & Found
   - User support email: your@klh.edu.in
   - Developer contact: your@klh.edu.in
   - Scopes: email, profile
   - Test users: Add your @klh.edu.in emails

4. **Create OAuth Credentials**
   - Go to: APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Application type: Web application
   - Name: KLH Lost & Found Web Client
   
   **Authorized JavaScript origins:**
   ```
   http://localhost:8000
   http://127.0.0.1:8000
   https://yourdomain.com
   ```
   
   **Authorized redirect URIs:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   https://yourdomain.com/accounts/google/login/callback/
   ```

5. **Copy Credentials**
   - Client ID: `xxxxxxxxxxxx.apps.googleusercontent.com`
   - Client Secret: `GOCSPX-xxxxxxxxxxxxx`

### Configure in Django Admin:

1. Start server: `python manage.py runserver`
2. Go to: http://localhost:8000/admin/
3. Login with superuser

**Configure Site:**
- Navigate to: **Sites** → Click on "example.com"
- Domain name: `localhost:8000` (for development)
- Display name: `KLH Lost & Found`
- Save

**Add Social Application:**
- Navigate to: **Social applications** → Add social application
- Provider: **Google**
- Name: **Google OAuth**
- Client id: *paste your Client ID*
- Secret key: *paste your Client Secret*
- Sites: Select "localhost:8000" (move to "Chosen sites")
- Save

## Testing Authentication

1. Logout from admin
2. Go to homepage: http://localhost:8000/
3. Click "Login"
4. Click "Sign in with Google"
5. Use @klh.edu.in email

**Important:** Only @klh.edu.in emails are allowed!

## Database Models

The system has 2 main models:

### LostItem
- Stores information about lost/found items
- Fields: title, description, category, status, location, date, image, contact
- Relationships: belongs to User (posted_by)

### Claim
- Stores claims made on items
- Fields: item, claimed_by, message, status
- Relationships: belongs to LostItem and User

## Common Issues & Solutions

### Issue 1: Google Login Shows "Redirect URI Mismatch"
**Solution:**
- Check authorized redirect URIs in Google Console
- Ensure exact match: `http://localhost:8000/accounts/google/login/callback/`
- No trailing slash issues

### Issue 2: "Only KLH students" error appears
**Solution:**
- This is correct behavior!
- Only @klh.edu.in emails are allowed
- Use proper KLH email for testing

### Issue 3: Images not displaying
**Solution:**
```powershell
# Check MEDIA_ROOT in settings.py
# Ensure media folder exists
mkdir media\lost_items

# Check URLs configuration includes media URLs
```

### Issue 4: Static files not loading
**Solution:**
```powershell
python manage.py collectstatic --noinput
```

## Production Deployment

### Option 1: Heroku

```bash
# Install Heroku CLI
heroku login
heroku create klh-lostandfound

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configure environment
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="klh-lostandfound.herokuapp.com"

# Create Procfile
echo "web: gunicorn lostandfound.wsgi" > Procfile

# Install gunicorn
pip install gunicorn
pip freeze > requirements.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# Configure Google OAuth for production URL
```

### Option 2: PythonAnywhere

1. Sign up at pythonanywhere.com
2. Upload code or clone from GitHub
3. Create virtual environment
4. Configure WSGI file
5. Set up static files
6. Add domain to allowed hosts
7. Configure Google OAuth with production URL

### Option 3: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Add PostgreSQL
railway add

# Deploy
railway up
```

## Environment Variables (Production)

Create `.env` file:

```env
SECRET_KEY=your-very-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Update `settings.py`:

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

## Database Migration to PostgreSQL

```powershell
# Install psycopg2
pip install psycopg2-binary

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lostandfound',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Run migrations
python manage.py migrate
```

## Testing Checklist

- [ ] User can sign in with @klh.edu.in email
- [ ] Non-KLH emails are rejected
- [ ] User can post lost items
- [ ] User can post found items
- [ ] Images upload successfully
- [ ] Search functionality works
- [ ] Filters work (category, status)
- [ ] User can claim items
- [ ] Item owner can see claims
- [ ] Item owner can approve/reject claims
- [ ] Approved items show as "Claimed"
- [ ] Users can view their posted items
- [ ] Users can view their claims
- [ ] Edit/Delete works only for item owners
- [ ] Mobile responsive design works

## Performance Optimization

```python
# In settings.py - for production

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Media files on CDN (optional)
# Use AWS S3 or Cloudinary for image storage

# Database optimization
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,
    }
}
```

## Security Checklist (Production)

- [ ] DEBUG = False
- [ ] SECRET_KEY is strong and secret
- [ ] ALLOWED_HOSTS is properly configured
- [ ] HTTPS is enabled
- [ ] CSRF protection enabled
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection enabled
- [ ] Secure cookies configured
- [ ] HSTS headers configured
- [ ] Regular security updates

## Maintenance

```powershell
# Backup database
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json

# Clear old sessions
python manage.py clearsessions

# Check for issues
python manage.py check

# Run tests (if created)
python manage.py test
```

## Team Collaboration with Git

```bash
# Clone repository
git clone https://github.com/username/klh-lostandfound.git

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
# After review, merge to main branch
```

## Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- django-allauth: https://django-allauth.readthedocs.io/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- Google OAuth: https://developers.google.com/identity

## Project Submission

Include in your submission:
1. GitHub repository link (with all team commits)
2. Live deployment link
3. Google OAuth credentials (for testing)
4. Demo video (optional)
5. Team member contributions document

---

Good luck with your project! 🚀
