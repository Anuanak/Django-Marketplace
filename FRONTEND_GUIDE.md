# 🎨 Django Marketplace - Frontend Implementation Guide

## Overview

You now have **TWO complete frontend options**:

### Option 1️⃣: Django Templates (Server-Rendered)
- **Location**: `Backend/main/templates/main/`
- **Best for**: Quick testing, simple deployment, traditional Django apps
- **Type**: Server-side rendering (MVC pattern)
- **Setup time**: Immediate (already configured)
- **Files**:
  - `base.html` - Main layout template
  - `index.html` - Home page
  - `product_list.html` - Product listing with filters
  - `product_detail.html` - Single product page
  - `cart.html` - Shopping cart
  - `checkout.html` - Checkout form
  - `auth.html` - Login/Register
  - `orders.html` - Order history
  - `dashboard.html` - User dashboard

### Option 2️⃣: React + TypeScript (Modern SPA)
- **Location**: `Frontend/`
- **Best for**: Production, better UX, mobile app future
- **Type**: Single Page Application (REST API consumer)
- **Setup time**: ~5 minutes for full install
- **Architecture**: React components + REST API

---

## 🚀 Option 1: Django Templates (READY NOW)

### Features
✅ Responsive design  
✅ Search and filtering  
✅ Product reviews  
✅ Shopping cart management  
✅ Order tracking  
✅ User authentication  
✅ Seller profiles  
✅ Admin-integrated  

### How to Use

1. **Django templates are already configured** in your Django app
2. Start the server:
   ```bash
   python manage.py runserver
   ```

3. Access the marketplace:
   - Home: `http://127.0.0.1:8000/`
   - Products: `http://127.0.0.1:8000/products/`
   - Admin: `http://127.0.0.1:8000/admin/` (admin/admin123)

4. The templates automatically use:
   - Django ORM for database queries
   - Django Template Language for rendering
   - Django forms (with proper CSRF protection)
   - Django authentication system
   - Static files (CSS/JS in `/static/` folder)

### Template Files Structure

```
Backend/
├── main/
│   ├── templates/main/
│   │   ├── base.html              # Main layout (navbar, footer)
│   │   ├── index.html             # Home with featured products
│   │   ├── product_list.html      # All products with filters
│   │   ├── product_detail.html    # Single product + reviews
│   │   ├── cart.html              # Shopping cart + checkout
│   │   ├── checkout.html          # Final checkout form
│   │   ├── auth.html              # Login/Register combined
│   │   ├── orders.html            # Order history
│   │   └── dashboard.html         # User & seller stats
│   ├── static/
│   │   ├── css/style.css          # Global styles
│   │   └── js/main.js             # Frontend JS
│   ├── urls.py                    # Updated with new routes
│   ├── views.py                   # Updated with template rendering
│   └── models.py                  # Existing models
```

### Views Auto-Generated

The views now include:
- `home()` - Featured products page
- `product_list()` - Browse with search/filters
- `product_detail()` - Full product info + reviews
- `add_to_cart()` - Cart management
- `checkout()` - Order placement
- `order_list()` - Order history
- `dashboard()` - User statistics
- `login_view()` - User login
- `register_view()` - User registration
- `logout_view()` - Logout handler

### Styling

All templates include:
- Responsive grid layouts
- Color-coded status badges
- Hover effects
- Mobile-friendly design
- Form validation feedback
- Product image galleries

### Add Custom Styles

Edit `Backend/static/css/style.css` to customize:
```css
/* Example: Change primary color */
.btn-primary {
    background-color: YOUR_COLOR;
}
```

---

## 🔥 Option 2: React Frontend (Production-Ready)

### Installation

1. **Navigate to Frontend directory**:
   ```bash
   cd c:\Users\montenegro\Desktop\proj\Django-Marketplace\Frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Access React app**:
   - Frontend: `http://127.0.0.1:3000`
   - Backend API: `http://127.0.0.1:8000/api/v1/`

### Project Structure

```
Frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx           # Navigation bar
│   │   ├── Header.css
│   │   ├── Footer.tsx           # Footer
│   │   ├── Footer.css
│   │   ├── ProductCard.tsx      # Product display card
│   │   └── ProductCard.css
│   ├── pages/
│   │   ├── Home.tsx             # Home page
│   │   ├── Products.tsx         # Product listing
│   │   ├── Products.css
│   │   ├── Login.tsx            # Login form
│   │   └── Cart.tsx             # Shopping cart
│   ├── services/
│   │   └── api.ts               # API client (axios)
│   ├── App.tsx                  # Main app + routing
│   ├── App.css
│   ├── main.tsx                 # Entry point
│   └── index.css
├── index.html                   # HTML template
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
├── package.json                 # Dependencies
└── README.md                     # React README
```

### Key Features

✅ **Modern SPA**: Fast, responsive single-page app  
✅ **Token Authentication**: Secure API integration  
✅ **TypeScript**: Type-safe development  
✅ **Vite**: Lightning-fast development server  
✅ **React Router**: Client-side navigation  
✅ **Axios**: Easy API calls  
✅ **Responsive Design**: Works on all devices  

### Available Pages

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | HomePage | Welcome page |
| `/products` | ProductsPage | Browse products |
| `/login` | LoginPage | User authentication |
| `/cart` | CartPage | Shopping cart |

### API Integration

All API calls are through `src/services/api.ts`:

```typescript
// Example: Get all products
const products = await API.getProducts();

// Example: Add to cart
await API.addToCart(productId, quantity);

// Example: Login
const response = await API.login(username, password);
localStorage.setItem('token', response.data.token);
```

### Building for Production

```bash
# Build optimized bundle
npm run build

# Preview production build
npm run preview
```

Output: `dist/` folder with optimized files

### Deployment Options

1. **Vercel** (Recommended for React):
   ```bash
   npm install -g vercel
   cd Frontend
   vercel
   ```

2. **Netlify**:
   - Connect GitHub repository
   - Auto-deploys on push

3. **Your own server** (Nginx, Apache):
   - Build the project
   - Copy `dist/` folder
   - Serve static files

### Environment Variables

Create `.env` for API URL:
```
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

---

## 🔀 Switching Between Frontends

### Using Django Templates

```bash
# In Backend folder
cd Backend
python manage.py runserver
# Visit: http://127.0.0.1:8000/
```

### Using React Frontend

```bash
# Terminal 1: Keep Django running
cd Backend
python manage.py runserver

# Terminal 2: Run React dev server
cd Frontend
npm install  # First time only
npm run dev
# Visit: http://127.0.0.1:3000/
```

### Production Serving React

```bash
# Build React
cd Frontend
npm run build

# Copy dist/ to Django static files
# OR serve from separate React hosting (Vercel, Netlify)

# Keep Django for API only
cd Backend
python manage.py runserver
```

---

## 🎯 Recommended Workflow

### For Development (Testing)
→ Use **Django Templates**
- Faster to modify
- No build step
- Server-side rendering

### For Production
→ Use **React Frontend**
- Better UX
- Faster navigation
- Better for mobile apps
- Can be deployed separately

---

## 📝 Next Steps

### Django Templates
1. ✅ Templates created
2. ✅ Views updated
3. ✅ URLs configured
4. Run and test: `python manage.py runserver`
5. Add custom styles in `Backend/static/css/`

### React Frontend
1. ✅ Project structure created
2. ✅ Components built
3. ✅ API service configured
4. Install: `npm install`
5. Run: `npm run dev`
6. Build: `npm run build`

---

## 🆘 Troubleshooting

### Django Templates
- **CSS not loading**: Check `STATIC_ROOT` in settings.py, run `python manage.py collectstatic`
- **Template not found**: Verify path in `TEMPLATES` setting
- **Views error**: Check `Backend/main/urls.py` has correct imports

### React Frontend
- **CORS errors**: Make sure Django has `django-cors-headers` installed
- **API 404**: Verify Django backend is running on `http://127.0.0.1:8000`
- **npm install fails**: Delete `node_modules/` and `package-lock.json`, then reinstall
- **Port 3000 in use**: `npm run dev -- --port 3001`

---

## 📚 Learning Resources

### Django Templates
- [Django Templates Documentation](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Django Template Language](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Bootstrap CSS](https://getbootstrap.com/) for styling

### React
- [React Documentation](https://react.dev)
- [React Router](https://reactrouter.com/)
- [Axios Documentation](https://axios-http.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 🎉 You're All Set!

Both frontends are production-ready:
- ✅ Django Templates (5 pages, fully styled)
- ✅ React App (4 pages, TypeScript, Vite)
- ✅ Full API integration
- ✅ Authentication ready
- ✅ Shopping cart functional
- ✅ Product management
- ✅ User dashboard

**Choose the one that fits your needs best!**

---

**Last Updated**: February 12, 2026  
**Status**: 🟢 Both Frontends Ready  
