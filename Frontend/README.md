# Django Marketplace - React Frontend

Modern React frontend for the Django Marketplace project.

## Features

- ⚡ Built with Vite for lightning-fast development
- 🎨 Beautiful UI with responsive design
- 🔐 Token-based authentication
- 🛒 Full shopping cart functionality
- 📦 Product browsing and filtering
- ⭐ Product reviews and ratings
- 👤 User dashboard
- 📱 Mobile-responsive design

## Project Structure

```
Frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API service layer
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── vite-env.d.ts   # Vite types
├── index.html          # HTML entry point
├── vite.config.ts      # Vite configuration
├── tsconfig.json       # TypeScript configuration
└── package.json        # Dependencies
```

## Installation

```bash
cd Frontend
npm install
```

## Running Development Server

```bash
npm run dev
```

The app will start at http://127.0.0.1:3000

## API Integration

The frontend connects to the Django backend API at `http://127.0.0.1:8000/api/v1/`

API calls are handled through `src/services/api.ts` with axios.

Authentication tokens are stored in localStorage.

## Building for Production

```bash
npm run build
```

## Available Pages

- `/` - Home page
- `/products` - Product listing and search
- `/products/<id>` - Product details
- `/login` - User login
- `/register` - User registration
- `/cart` - Shopping cart
- `/checkout` - Checkout
- `/orders` - Order history
- `/dashboard` - User dashboard

## Key Components

- **Header** - Navigation and user menu
- **Footer** - Footer information
- **ProductCard** - Product display card
- **LoginPage** - User authentication
- **CartPage** - Shopping cart management
- **ProductsPage** - Product listing with filters

## API Endpoints Used

- `GET /api/v1/products/` - Get all products
- `GET /api/v1/products/<id>/` - Get single product
- `GET /api/v1/categories/` - Get product categories
- `POST /api/v1/cart/add_item/` - Add item to cart
- `POST /api/v1/cart/remove_item/` - Remove item from cart
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/` - Get user orders

## Tips

1. Make sure the Django backend is running on http://127.0.0.1:8000
2. Create product data in the Django admin panel first
3. Use the provided API service for all backend calls
4. Token is automatically added to all requests once logged in

## Next Steps

- Add product detail page with full information
- Implement checkout flow
- Add order tracking
- Create user profile page
- Add wishlist functionality
- Implement product reviews display
- Add search and advanced filters
- Mobile app development

---

Built with React, TypeScript, and Vite ⚡
