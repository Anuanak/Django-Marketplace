# Balance Update Fix - Admin Panel

## ✅ Changes Made

### Frontend (Vue.js Admin Panel)

#### 1. **Users.vue - API Integration**
Fixed all API calls to properly connect to Django REST API:

**Changes:**
- `fetchUsers()` - Now makes real API calls to `/api/auth/users/`
- `saveUser()` - Implements proper POST (create) and PATCH (update) operations
- `deleteUser()` - Makes DELETE request to remove users
- `toggleVerification()` - Makes PATCH request to toggle verification status

**Key Features:**
- Balance field (`el-input-number`) is now properly sent to backend
- Password field is only shown when creating new users
- All CRUD operations use real API endpoints
- Error handling with user-friendly messages

---

### Backend (Django REST API)

#### 2. **Serializers - Permission-Based Field Restrictions**

**Modified: `UserSerializer` and `UserDetailSerializer`**

**Before:**
```python
read_only_fields = ['id', 'balance', 'is_verified', 'date_joined', 'last_login']
```
- Balance and is_verified were ALWAYS read-only
- Admin couldn't update them

**After:**
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    request = self.context.get('request')
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        if request.user.user_type != 'admin':
            # Regular users can't modify balance and verification status
            self.fields['balance'].read_only = True
            self.fields['is_verified'].read_only = True
```

**Result:**
- ✅ Admin users CAN update balance and is_verified
- ✅ Regular users CANNOT modify balance (for security)
- ✅ is_verified toggle only works for admins

---

#### 3. **UserViewSet - Admin-Only Access Control**

**Modified: Permission Checks and Filters**

**New Methods:**
- `get_queryset()` - Filters users based on role
- `list()` - Requires admin access
- `update()` - Admin can modify any user, regular users can only edit themselves
- `partial_update()` - Same as update with PATCH support
- `destroy()` - Admin-only user deletion

**Benefits:**
- ✅ Only admin can list/manage all users
- ✅ Regular users can't see other profiles
- ✅ Balance updates only via admin
- ✅ Secure permission model

---

## 🚀 How It Works Now

### Admin Adding/Updating User Balance

**Flow:**
1. Admin logs in with `admin@example.com` / `admin123`
2. Navigates to **Admin Panel** → **Users**
3. Clicks **Edit** on a user
4. Dialog opens with form including **Balance** field
5. Admin enters new balance amount
6. Clicks **Save**
7. **PATCH** request sent to `/api/auth/users/{id}/`
8. Backend verifies admin privilege
9. Serializer allows balance update (since request user is admin)
10. Balance is updated in database
11. Success message shown
12. User list refreshes with new balance

### API Request Structure

**Update User Balance:**
```
PATCH /api/auth/users/2/
Content-Type: application/json
Authorization: Bearer {admin_token}

{
  "balance": 5000.00,
  "email": "seller@example.com",
  "first_name": "Test",
  "last_name": "Seller",
  "user_type": "seller",
  "is_verified": true
}
```

**Response:**
```json
{
  "id": 2,
  "email": "seller@example.com",
  "username": "seller@example.com",
  "first_name": "Test",
  "last_name": "Seller",
  "phone_number": null,
  "user_type": "seller",
  "is_verified": true,
  "balance": "5000.00",
  "date_joined": "2024-02-14T10:00:00Z",
  "last_login": "2024-02-14T12:30:00Z"
}
```

---

## 🧪 Testing Steps

### Test 1: Admin Adding Money to Buyer Account

1. **Login as Admin**
   - URL: http://localhost:5176 (or 5175, 5174, 5173)
   - Email: `admin@example.com`
   - Password: `admin123`

2. **Navigate to Admin Panel**
   - Click user avatar (top right)
   - Select "Admin Panel" (purple option)

3. **Open Users Management**
   - Click "Users" in sidebar
   - Should see list of users with their balances

4. **Edit Buyer User**
   - Click **Edit** button on buyer@example.com row
   - Dialog opens with user form

5. **Add/Update Balance**
   - Find "Balance" field in form
   - Clear existing value
   - Enter new amount (e.g., `2500.50`)
   - Click **Save**

6. **Verify Update**
   - Should see "User updated successfully" message
   - User list refreshes
   - Balance column shows new value

### Test 2: Verify Verification Toggle

1. **In Users Management**
   - Find a user in table
   - Toggle the Verified switch on/off
   
2. **Expected Result**
   - Success message appears
   - User's verification status updates in table

### Test 3: Create New User with Initial Balance

1. **Click "Create User" button** (top right)
2. **Fill form:**
   - Email: `newuser@example.com`
   - First Name: `New`
   - Last Name: `User`
   - User Type: `buyer`
   - Password: `test123`
   - Balance: `1000.00`
   - Verified: ✓ (checked)

3. **Click Save**
4. **Verify:**
   - Success message
   - New user appears in list with correct balance

### Test 4: Security - Regular User Can't Update Balance

1. **Login as Regular User**
   - Email: `buyer@example.com`
   - Password: `test123`

2. **Try to Access Admin Panel**
   - URL: http://localhost:5176/admin/dashboard
   - Should be **redirected to home page**
   - Admin menu item should NOT appear in header

3. **Update Own Profile**
   - Click "Profile" in user menu
   - Edit personal information
   - Try to send balance update (advanced testing)
   - **Should be rejected** with 403 error

---

## 🔧 Troubleshooting

### Issue: "Balance field still read-only"

**Solution:**
1. Verify backend is running: `python manage.py runserver`
2. Check admin user type: `/api/auth/users/me/` should show `"user_type": "admin"`
3. Restart backend server to pick up code changes
4. Clear browser cache (DevTools → Application → Clear Storage)

### Issue: "Permission denied" error when saving

**Possible Causes:**
- User is not admin (check `user_type` in response)
- JWT token is expired
- User account doesn't exist

**Solution:**
- Logout and login again with admin account
- Check browser console for token issues

### Issue: Balance shows old value after update

**Solution:**
1. Refresh page manually (F5)
2. Clear browser cache (Cmd+Shift+Delete)
3. Check Network tab to verify API returned new value
4. Check database directly:
   ```python
   python manage.py shell
   >>> from apps.users.models import User
   >>> u = User.objects.get(email='buyer@example.com')
   >>> print(u.balance)
   ```

---

## 📊 Database Schema

**User Model - Balance Field:**
```python
balance = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0.00,
    help_text="User's account balance in currency"
)
```

**Why Decimal?**
- ✅ Precise currency calculations
- ✅ No floating point errors
- ✅ Can store up to 99,999,999.99

---

## 🔒 Security Features

### Permission Model

| User Type | Can List Users | Can Edit Balance | Can Edit Verification | Can Delete Users |
|-----------|-----------------|------------------|----------------------|------------------|
| **Admin** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Seller** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Buyer** | ❌ No | ❌ No | ❌ No | ❌ No |

### API Endpoint Protection

All user management endpoints require:
1. **Authentication** - Valid JWT token
2. **Authorization** - Admin user type for list/update/delete
3. **Ownership** - Regular users can only access themselves

---

## 🚨 Important Notes

1. **Balance Updates Are Permanent**
   - Changes are written to database immediately
   - No undo functionality (yet)
   - Consider implementing transaction history

2. **No Validation on Balance**
   - Can set negative balances (intentional for testing)
   - Add validation in future if needed

3. **Currency Handling**
   - Balance stored in RUB (Russian Rubles)
   - Frontend formats as RUB currency
   - Backend uses Decimal for precision

4. **Testing Database**
   - Using SQLite (c:\\Users\\montenegro\\Desktop\\proj\\Django-Marketplace\\backend\\db.sqlite3)
   - All changes persist between runs
   - Reset with: `python manage.py migrate --fake zero && python manage.py migrate`

---

## ✨ Next Steps

After testing balance updates:

1. **Add Transaction History**
   - Track all balance changes
   - Show who made the change and when
   - Create TransactionLog model

2. **Add Top-Up Methods**
   - Manual admin transfer
   - Auto top-up system
   - Payment integration (Stripe, etc.)

3. **Add Withdrawal System**
   - Sellers can withdraw earnings
   - Require verification
   - Bank account linking

4. **Add Audit Log**
   - Track all admin actions
   - For compliance and debugging

---

## 📝 Files Modified

1. **Frontend:**
   - `frontend/src/views/admin/Users.vue` - API integration

2. **Backend:**
   - `backend/apps/users/serializers.py` - Permission-based field access
   - `backend/apps/users/views.py` - Admin-only access control

---

**Status:** ✅ Ready for Testing  
**Date:** February 14, 2026  
**Backend Port:** 8000  
**Frontend Port:** 5176 (or 5175, 5174, 5173)  
