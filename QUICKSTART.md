# Quick Start Guide for Django Marketplace

This guide will help you get the marketplace up and running quickly.

## Prerequisites

Make sure you have the following installed:
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Redis (for caching and Celery)

## Option 1: Manual Setup (Development)

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements\development.txt
   ```

4. **Create .env file:**
   ```powershell
   copy .env.example .env
   ```

5. **Update .env with your database credentials:**
   ```
   DB_NAME=marketplace_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Create database (in PostgreSQL):**
   ```sql
   CREATE DATABASE marketplace_db;
   ```

7. **Run migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create superuser:**
   ```powershell
   python manage.py createsuperuser
   ```

9. **Run development server:**
   ```powershell
   python manage.py runserver
   ```

Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory (new terminal):**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Run development server:**
   ```powershell
   npm run dev
   ```

Frontend will be available at: http://localhost:5173

### Optional: Run Celery Worker

For background tasks (digital key delivery, emails):

```powershell
cd backend
.\venv\Scripts\activate
celery -A config worker -l info --pool=solo
```

## Option 2: Docker Setup (Production-like)

**Note:** Make sure Docker Desktop is installed and running.

1. **Build and start all services:**
   ```powershell
   docker-compose up -d
   ```

2. **Wait for services to start (check logs):**
   ```powershell
   docker-compose logs -f
   ```

3. **Run migrations:**
   ```powershell
   docker-compose exec backend python manage.py migrate
   ```

4. **Create superuser:**
   ```powershell
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin

## First Steps After Setup

1. **Access Django Admin:**
   - Go to http://localhost:8000/admin
   - Login with your superuser credentials
   - Create some categories
   - Create products (both physical and digital)

2. **For Digital Products:**
   - Go to Digital Keys section in admin
   - Add digital keys for your digital products

3. **Test the marketplace:**
   - Register as a buyer at http://localhost:5173/auth/register
   - Browse products
   - Add items to cart
   - Test checkout

4. **Register as a seller:**
   - Register with user_type='seller'
   - Access seller dashboard at /seller/dashboard
   - Add your products

## Common Issues & Solutions

### Database Connection Error
- Make sure PostgreSQL is running
- Check database credentials in .env file
- Verify database exists: `psql -l`

### Redis Connection Error
- Make sure Redis is running
- On Windows, use Redis for Windows or Docker

### Port Already in Use
- Backend (8000): Change in manage.py runserver command
- Frontend (5173): Change in vite.config.js

### Module Not Found Errors
- Backend: Make sure virtual environment is activated
- Frontend: Run `npm install` again

## Development Workflow

1. **Backend Changes:**
   - Modify models → run `python manage.py makemigrations` → run `python manage.py migrate`
   - Changes auto-reload with runserver

2. **Frontend Changes:**
   - Changes auto-reload with Vite HMR
   - For new dependencies: `npm install package-name`

3. **Adding Translations:**
   - Edit `frontend/src/locales/ru.json`, `en.json`, `uk.json`
   - Use `$t('key')` in Vue components

## Testing API Endpoints

Use the built-in API documentation:
- Swagger UI: http://localhost:8000/api/docs/
- You can test all endpoints directly from the browser

## Need Help?

- Check the main README.md for detailed documentation
- Review Django admin for data management
- Check browser console for frontend errors
- Check terminal/PowerShell for backend errors

## Next Steps

1. Customize the design and colors
2. Add more product categories
3. Configure email settings for notifications
4. Set up payment gateway integration (Stripe/YooKassa)
5. Configure Elasticsearch for better search (optional)
6. Add more features based on your needs

Happy coding! 🚀
