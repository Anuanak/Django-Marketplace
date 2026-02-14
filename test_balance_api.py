#!/usr/bin/env python
"""Test script for balance update functionality."""

import requests
import json

BASE_URL = 'http://localhost:8000/api'

# Step 1: Login as admin
print("=" * 60)
print("Step 1: Login as Admin")
print("=" * 60)

login_data = {
    'email': 'admin@example.com',
    'password': 'admin123'
}

try:
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    response.raise_for_status()
    auth_data = response.json()
    access_token = auth_data.get('access')
    print(f"✅ Login successful")
    print(f"   Access Token: {access_token[:50]}...")
except Exception as e:
    print(f"❌ Login failed: {e}")
    access_token = None

if not access_token:
    print("Cannot continue without token")
    exit(1)

headers = {'Authorization': f'Bearer {access_token}'}

# Step 2: Get list of all users
print("\n" + "=" * 60)
print("Step 2: Get List of Users")
print("=" * 60)

try:
    response = requests.get(f'{BASE_URL}/auth/users/', headers=headers)
    response.raise_for_status()
    users_data = response.json()
    users = users_data.get('results', users_data) if isinstance(users_data, dict) else users_data
    print(f"✅ Retrieved {len(users)} users:")
    for user in users[:3]:
        print(f"   - {user['email']} (ID: {user['id']}, Balance: {user['balance']})")
except Exception as e:
    print(f"❌ Failed to get users: {e}")
    exit(1)

# Step 3: Find a test user (buyer) to update
print("\n" + "=" * 60)
print("Step 3: Update Balance for Buyer")
print("=" * 60)

buyer = next((u for u in users if u['user_type'] == 'buyer'), None)
if not buyer:
    print("❌ No buyer user found")
    exit(1)

print(f"Found buyer: {buyer['email']} (ID: {buyer['id']})")
print(f"Current balance: {buyer['balance']}")

# Update balance
new_balance = 2500.50
update_data = {
    'balance': new_balance,
    'is_verified': True
}

print(f"Attempting to update balance to: {new_balance}")

try:
    response = requests.patch(f'{BASE_URL}/auth/users/{buyer["id"]}/', 
                             json=update_data, 
                             headers=headers)
    response.raise_for_status()
    updated_user = response.json()
    print(f"✅ Balance updated successfully!")
    print(f"   New balance: {updated_user['balance']}")
    print(f"   Verification: {updated_user['is_verified']}")
except Exception as e:
    print(f"❌ Failed to update balance: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"   Response: {e.response.text}")

# Step 4: Verify the update
print("\n" + "=" * 60)
print("Step 4: Verify Update")
print("=" * 60)

try:
    response = requests.get(f'{BASE_URL}/auth/users/{buyer["id"]}/', headers=headers)
    response.raise_for_status()
    final_user = response.json()
    if final_user['balance'] == str(new_balance) or final_user['balance'] == new_balance:
        print(f"✅ Verification successful!")
        print(f"   Balance in database: {final_user['balance']}")
    else:
        print(f"⚠️ Balance mismatch:")
        print(f"   Expected: {new_balance}")
        print(f"   Got: {final_user['balance']}")
except Exception as e:
    print(f"❌ Failed to verify: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
