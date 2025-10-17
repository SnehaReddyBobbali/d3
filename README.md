# KLH Lost & Found System

A Django-based Lost and Found platform exclusive to KLH students, where users can sign in using their @klh.edu.in Gmail accounts, post lost items, and help others recover them.

## Features

- **Google Authentication**: Restricted to @klh.edu.in email addresses only
- **Post Items**: Users can post lost or found items with images
- **Search & Filter**: Search items by title, description, category, and status
- **Claim System**: Users can claim items with detailed messages
- **Claim Management**: Item owners can approve or reject claims
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Image Upload**: Support for uploading images of lost/found items
- **User Dashboard**: View posted items and claims

## Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: django-allauth with Google OAuth
- **Frontend**: Bootstrap 5, Font Awesome
- **Image Handling**: Pillow

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd d3
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `https://yourdomain.com/accounts/google/login/callback/` (for production)
6. Copy Client ID and Client Secret

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Configure Social App

1. Run the development server:
```bash
python manage.py runserver
```

2. Go to `http://localhost:8000/admin/`
3. Login with superuser credentials
4. Navigate to **Sites** → Edit the default site:
   - Domain name: `localhost:8000` (for development)
   - Display name: `KLH Lost & Found`
5. Navigate to **Social applications** → Add social application:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: `<your-client-id>`
   - Secret key: `<your-client-secret>`
   - Sites: Select your site

### 7. Run the Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000/`

## Project Structure

```
d3/
├── lostandfound/          # Main project directory
│   ├── settings.py        # Project settings
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI configuration
├── items/                # Items app
│   ├── models.py         # Database models (LostItem, Claim)
│   ├── views.py          # View functions
│   ├── forms.py          # Django forms
│   ├── adapters.py       # Custom allauth adapter
│   ├── urls.py           # App URLs
│   └── admin.py          # Admin configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── items/            # Item templates
├── static/               # Static files (CSS, JS)
│   └── css/
│       └── style.css     # Custom styles
├── media/                # User uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Project dependencies
```

## Usage

### For Students:

1. **Sign In**: Click "Login" and sign in with your @klh.edu.in Google account
2. **Post Item**: Click "Post Item" to report a lost or found item
3. **Browse Items**: View all posted items on the home page
4. **Search**: Use search and filters to find specific items
5. **Claim Item**: If you see your lost item, click "Claim This Item"
6. **Track Claims**: View your claims in "My Claims" section

### For Item Owners:

1. **Manage Items**: View and edit your posted items in "My Items"
2. **Review Claims**: Check claims on your items in "Manage Claims"
3. **Approve/Reject**: Approve genuine claims or reject false ones
4. **Update Status**: Mark items as "Claimed" when recovered

## Database Models

### LostItem
- title, description, category, status
- location_lost, date_lost
- image (optional)
- posted_by (User), contact_info
- timestamps

### Claim
- item (ForeignKey to LostItem)
- claimed_by (User)
- message, status (pending/approved/rejected)
- timestamps

## Security Features

- Email restriction to @klh.edu.in domain
- CSRF protection
- Login required decorators
- User ownership validation
- Secure file uploads

## Deployment (Production)

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

### Deployment Platforms

**Recommended platforms:**
- **Heroku**: Easy deployment with PostgreSQL
- **PythonAnywhere**: Free tier available
- **Railway**: Modern deployment
- **Render**: Free tier with PostgreSQL

### Heroku Deployment Steps:

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## GitHub Repository Setup

```bash
git init
git add .
git commit -m "Initial commit: KLH Lost & Found System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Team Collaboration

Each team member should:
1. Clone the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m "description"`
4. Push changes: `git push origin feature-name`
5. Create a Pull Request on GitHub

## Screenshots

(Add screenshots of your deployed application)

## License

This project is for educational purposes as part of KLH coursework.

## Support

For issues or questions, contact your team members or course instructor.

---

**Developed by**: [Your Team Name]  
**Course**: Dynamic Website Hosting  
**Institution**: KL University Hyderabad
