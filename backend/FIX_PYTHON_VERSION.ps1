# ===================================================================
# FIX: Django Admin Error - Python 3.14 Incompatibility
# ===================================================================
#
# PROBLEM: Django 4.2.10 doesn't support Python 3.14.2
# SOLUTION: Install Python 3.12 and recreate virtual environment
#
# ===================================================================

Write-Host "Django Admin Fix - Python Version Downgrade" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Download Python 3.12
Write-Host "STEP 1: Install Python 3.12" -ForegroundColor Yellow
Write-Host "  Download from: https://www.python.org/downloads/release/python-3127/" -ForegroundColor White
Write-Host "  Choose: Windows installer (64-bit)" -ForegroundColor White
Write-Host "  IMPORTANT: Check 'Add Python to PATH' during installation" -ForegroundColor Red
Write-Host ""
Write-Host "Press Enter AFTER you've installed Python 3.12..." -ForegroundColor Green
Read-Host

# Verify Python 3.12 is installed
Write-Host ""
Write-Host "STEP 2: Verifying Python 3.12 installation..." -ForegroundColor Yellow
py -3.12 --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.12 not found! Please install it first." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python 3.12 found!" -ForegroundColor Green
Write-Host ""

# Step 2: Remove old virtual environment
Write-Host "STEP 3: Removing old virtual environment..." -ForegroundColor Yellow
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
Write-Host "✓ Old venv removed" -ForegroundColor Green
Write-Host ""

# Step 3: Create new virtual environment with Python 3.12
Write-Host "STEP 4: Creating new virtual environment with Python 3.12..." -ForegroundColor Yellow
py -3.12 -m venv venv
Write-Host "✓ New venv created" -ForegroundColor Green
Write-Host ""

# Step 4: Activate virtual environment
Write-Host "STEP 5: Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Step 5: Upgrade pip
Write-Host ""
Write-Host "STEP 6: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 6: Install dependencies
Write-Host ""
Write-Host "STEP 7: Installing Django and dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 7: Run migrations
Write-Host ""
Write-Host "STEP 8: Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 8: Recreate demo users
Write-Host ""
Write-Host "STEP 9: Creating demo users..." -ForegroundColor Yellow
python manage.py create_demo_users

# Step 9: Re-enable admin in urls.py
Write-Host ""
Write-Host "STEP 10: Re-enabling Django admin..." -ForegroundColor Yellow
$urlsPath = "config\urls.py"
$content = Get-Content $urlsPath -Raw
$content = $content -replace "# path\('admin/', admin\.site\.urls\),  # Disabled: Python 3\.14 incompatible with Django 4\.2", "path('admin/', admin.site.urls),"
Set-Content $urlsPath $content
Write-Host "✓ Admin re-enabled" -ForegroundColor Green

# Done
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Start the server with:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Test credentials:" -ForegroundColor Yellow
Write-Host "  Buyer:  buyer@example.com / test123" -ForegroundColor White
Write-Host "  Seller: seller@example.com / test123" -ForegroundColor White
Write-Host "  Admin:  admin@example.com / admin123" -ForegroundColor White
Write-Host ""
Write-Host "Access admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Yellow
