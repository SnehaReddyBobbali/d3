# KLH Lost & Found System - Quick Reference

## 🚀 Quick Start (5 Minutes)

### 1. Setup
```powershell
# Run the automated setup script
.\setup.ps1
```

OR manually:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 2. Run Server
```powershell
python manage.py runserver
```
Visit: http://localhost:8000/

### 3. Configure Google OAuth (Required!)

**Admin Panel:** http://localhost:8000/admin/

#### Step 1: Fix Site Domain
- Sites → Edit "example.com"
- Domain: `localhost:8000`
- Display name: `KLH Lost & Found`

#### Step 2: Add Google OAuth
- Social applications → Add
- Provider: **Google**
- Client ID: `<from Google Console>`
- Secret: `<from Google Console>`
- Sites: Choose `localhost:8000`

**Get Google Credentials:**
1. Go to: https://console.cloud.google.com/
2. Create project → Enable Google+ API
3. Credentials → Create OAuth 2.0 Client ID
4. Redirect URI: `http://localhost:8000/accounts/google/login/callback/`

---

## 📋 Features Checklist

### Authentication
- ✅ Google OAuth login
- ✅ Restricted to @klh.edu.in emails
- ✅ Automatic email verification

### Lost Items Management
- ✅ Post lost/found items
- ✅ Upload images
- ✅ Edit/Delete own items
- ✅ Categorize items
- ✅ Set status (Lost/Found/Claimed)

### Search & Browse
- ✅ Search by title/description
- ✅ Filter by category
- ✅ Filter by status
- ✅ View all items

### Claims System
- ✅ Claim items with message
- ✅ View own claims
- ✅ Manage claims (for item owners)
- ✅ Approve/Reject claims
- ✅ Auto-update item status

---

## 🗂️ File Structure

```
d3/
├── manage.py              # Django management
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── DEPLOYMENT.md         # Deployment guide
├── setup.ps1             # Setup script
│
├── lostandfound/         # Project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI config
│
├── items/               # Main app
│   ├── models.py        # LostItem, Claim models
│   ├── views.py         # View functions
│   ├── forms.py         # Django forms
│   ├── adapters.py      # KLH email restriction
│   ├── urls.py          # App URLs
│   └── admin.py         # Admin configuration
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   └── items/          # Item templates
│       ├── home.html
│       ├── item_detail.html
│       ├── post_item.html
│       ├── my_items.html
│       ├── claim_item.html
│       └── ...
│
├── static/             # Static files
│   └── css/
│       └── style.css   # Custom styles
│
└── media/              # Uploaded files
    └── lost_items/     # Item images
```

---

## 🎯 Key URLs

| URL | Purpose |
|-----|---------|
| `/` | Home - Browse items |
| `/post/` | Post new item |
| `/item/<id>/` | View item details |
| `/item/<id>/claim/` | Claim an item |
| `/my-items/` | Your posted items |
| `/my-claims/` | Your claims |
| `/admin/` | Admin panel |
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout |

---

## 💻 Development Commands

```powershell
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

---

## 🐛 Common Issues

### "Redirect URI mismatch"
**Fix:** Ensure Google Console has exact URI:
```
http://localhost:8000/accounts/google/login/callback/
```

### "Only KLH students allowed"
**Fix:** This is correct! Use @klh.edu.in email

### Images not displaying
**Fix:**
```powershell
# Check media folder exists
ls media\lost_items

# Ensure DEBUG=True for development
```

### Static files not loading
**Fix:**
```powershell
python manage.py collectstatic --noinput
```

---

## 📦 Database Models

### LostItem
```python
- title (CharField)
- description (TextField)
- category (CharField) - electronics, documents, etc.
- status (CharField) - lost, found, claimed
- location_lost (CharField)
- date_lost (DateField)
- image (ImageField)
- posted_by (ForeignKey → User)
- contact_info (CharField)
- created_at, updated_at
```

### Claim
```python
- item (ForeignKey → LostItem)
- claimed_by (ForeignKey → User)
- message (TextField)
- status (CharField) - pending, approved, rejected
- created_at, updated_at
```

---

## 🚢 Deployment Options

### Option 1: Heroku (Recommended)
```bash
heroku create klh-lostandfound
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
```

### Option 2: PythonAnywhere
1. Upload code
2. Create virtualenv
3. Configure WSGI
4. Set up static files

### Option 3: Railway
```bash
railway init
railway add postgresql
railway up
```

**See DEPLOYMENT.md for detailed instructions!**

---

## 🧪 Testing Flow

1. ✅ Open http://localhost:8000/
2. ✅ Click "Login" → Sign in with @klh.edu.in
3. ✅ Click "Post Item" → Fill form → Submit
4. ✅ View item on homepage
5. ✅ Click item → View details
6. ✅ Logout → Login with different @klh.edu.in
7. ✅ Claim the item
8. ✅ Logout → Login as item owner
9. ✅ Go to "My Items" → "Manage Claims"
10. ✅ Approve/Reject claim

---

## 👥 Team Collaboration

```bash
# Clone repository
git clone <repo-url>

# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "Add feature"

# Push to GitHub
git push origin feature/your-feature

# Create Pull Request on GitHub
```

---

## 📚 Resources

- **Django Docs:** https://docs.djangoproject.com/
- **django-allauth:** https://django-allauth.readthedocs.io/
- **Bootstrap 5:** https://getbootstrap.com/docs/5.3/
- **Google OAuth:** https://console.cloud.google.com/

---

## 📝 Project Submission Checklist

- [ ] GitHub repository created
- [ ] All team members have commits
- [ ] Google OAuth configured
- [ ] Application deployed (live link)
- [ ] README.md completed
- [ ] Test with @klh.edu.in emails
- [ ] Screenshots/video demo
- [ ] Submission document with:
  - Repository link
  - Live deployment link
  - Team member contributions
  - Testing credentials

---

## 🎓 Assignment Requirements Met

- ✅ Google Authentication (@klh.edu.in only)
- ✅ Post lost items with images
- ✅ View and claim items
- ✅ SQL Database (SQLite/PostgreSQL)
- ✅ Fully functional website
- ✅ GitHub repository with team commits
- ✅ Deployment ready

---

**Good luck! For detailed information, see README.md and DEPLOYMENT.md**
