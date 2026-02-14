from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Populate database with test users'

    def handle(self, *args, **options):
        # Test users data
        test_users = [
            {
                'email': 'buyer@example.com',
                'first_name': 'Test',
                'last_name': 'Buyer',
                'user_type': 'buyer',
                'is_verified': True,
                'balance': 1500.50,
            },
            {
                'email': 'seller@example.com',
                'first_name': 'Test',
                'last_name': 'Seller',
                'user_type': 'seller',
                'is_verified': True,
                'balance': 5000.00,
            },
            {
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
                'is_verified': True,
                'balance': 0.00,
            },
            {
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'buyer',
                'is_verified': False,
                'balance': 250.00,
            },
            {
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'user_type': 'seller',
                'is_verified': True,
                'balance': 10000.00,
            },
        ]

        created_count = 0
        for user_data in test_users:
            email = user_data.pop('email')
            password = 'test123'  # Default password for all test users
            
            # Check if user exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {email} already exists, skipping...')
                )
                continue
            
            # Create user
            user = User.objects.create_user(email=email, password=password, **user_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created user: {email} ({user_data["user_type"]})')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} test users!')
        )
        self.stdout.write(
            self.style.WARNING(
                '\nTest Account Credentials:\n'
                '- Email: buyer@example.com | Password: test123\n'
                '- Email: seller@example.com | Password: test123\n'
                '- Email: admin@example.com | Password: test123\n'
            )
        )
