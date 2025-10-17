# Quick Setup Script for KLH Lost & Found System
# Run this script to set up the project quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "KLH Lost & Found System - Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Blue
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host "`nRunning database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "✓ Database migrations completed" -ForegroundColor Green

# Create media directories
Write-Host "`nCreating media directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "media\lost_items" | Out-Null
New-Item -ItemType Directory -Force -Path "static" | Out-Null
Write-Host "✓ Media directories created" -ForegroundColor Green

# Collect static files
Write-Host "`nCollecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "✓ Static files collected" -ForegroundColor Green

# Prompt for superuser creation
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Create Superuser Account" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$createSuperuser = Read-Host "`nDo you want to create a superuser account? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
}

# Display next steps
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Run the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Cyan

Write-Host "`n2. Access the application:" -ForegroundColor White
Write-Host "   http://localhost:8000/" -ForegroundColor Cyan

Write-Host "`n3. Configure Google OAuth:" -ForegroundColor White
Write-Host "   a. Go to: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "   b. Configure Sites (change domain to 'localhost:8000')" -ForegroundColor Cyan
Write-Host "   c. Add Social Application (Google OAuth credentials)" -ForegroundColor Cyan
Write-Host "   d. See DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan

Write-Host "`n4. Read the documentation:" -ForegroundColor White
Write-Host "   - README.md - Project overview and features" -ForegroundColor Cyan
Write-Host "   - DEPLOYMENT.md - Detailed setup and deployment guide" -ForegroundColor Cyan

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Happy Coding! 💻" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
