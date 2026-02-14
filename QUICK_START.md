# 🚀 Quick Start - Testing Balance Update

## In 30 Seconds

1. **Both servers are running:**
   - Backend: http://localhost:8000 ✅
   - Frontend: http://localhost:5176 ✅

2. **Login as Admin:**
   - Email: `admin@example.com`
   - Password: `admin123`

3. **Go to Admin Panel:**
   - Click your avatar (top right)
   - Select "Admin Panel" (purple option)

4. **Test Balance Update:**
   - Click "Users" in sidebar
   - Click "Edit" on any user
   - Change the **Balance** field
   - Click "Save"
   - ✅ Success! Balance updated in database

---

## What Was Fixed?

### ❌ Before
- Balance field was READ-ONLY  
- Admin panel had mock data only
- No API integration
- Couldn't save balance changes

### ✅ After
- Admin can update balance
- All CRUD operations work
- Real API calls to Django backend
- Balance persists in database
- Security: Only admins can access

---

## Test Scenarios

### Scenario 1: Add Money to Buyer
1. Login as admin
2. Admin Panel → Users
3. Click Edit on `buyer@example.com`
4. Change Balance to `5000.00`
5. Click Save → ✅ Success

### Scenario 2: Toggle Verification
1. Same as above
2. Toggle the "Verified" switch
3. ✅ Updates in real-time

### Scenario 3: Create User with Balance
1. Admin Panel → Users
2. Click "Create User" button
3. Fill form with Balance: `1000.00`
4. Click Save → ✅ New user created

### Scenario 4: Regular User Blocked
1. Login as `buyer@example.com` / `test123`
2. Try URL: `http://localhost:5176/admin/dashboard`
3. ✅ Redirected to home page
4. Admin menu doesn't appear

---

## Key Code Changes

### Frontend (Vue.js)
```javascript
// Users.vue - Real API calls
const saveUser = async () => {
  await api.patch(`/auth/users/${id}/`, {
    balance: 2500.50,  // Now works!
    is_verified: true
  })
}
```

### Backend (Django)
```python
# Serializers - Admin-only permissions
if request.user.user_type != 'admin':
    self.fields['balance'].read_only = True  # Locked for non-admins
    
# Views - Admin-only access
def list(self, request):
    if request.user.user_type != 'admin':
        return 403 Forbidden  # Only admins see user list
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Balance won't save** | Verify you're logged in as admin |
| **Admin panel not visible** | Make sure user_type='admin' in database |
| **API returns 403** | You need admin permissions |
| **Changes don't persist** | Check browser DevTools → Network tab |

---

## Database Check

Want to verify the balance was saved?

```bash
python manage.py shell
>>> from apps.users.models import User
>>> u = User.objects.get(email='buyer@example.com')
>>> print(f"Balance: {u.balance}")  # Should show new value
```

---

## Files Modified

- ✅ `frontend/src/views/admin/Users.vue` - API integration
- ✅ `backend/apps/users/serializers.py` - Permission control
- ✅ `backend/apps/users/views.py` - Admin-only access

All changes are production-ready. Ready to test! 🎉
