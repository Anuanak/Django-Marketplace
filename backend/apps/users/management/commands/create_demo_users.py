"""
Management command to create demo users for testing.
"""
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Creates demo users for testing the marketplace'

    def handle(self, *args, **options):
        # Create test buyer
        buyer, created = User.objects.get_or_create(
            email='buyer@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'Buyer',
                'user_type': 'buyer',
                'is_verified': True
            }
        )
        if created:
            buyer.set_password('test123')
            buyer.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created buyer: {buyer.email} / password: test123'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Buyer already exists: {buyer.email}'))

        # Create test seller
        seller, created = User.objects.get_or_create(
            email='seller@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'Seller',
                'user_type': 'seller',
                'is_verified': True
            }
        )
        if created:
            seller.set_password('test123')
            seller.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created seller: {seller.email} / password: test123'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Seller already exists: {seller.email}'))

        # Create admin
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin: {admin.email} / password: admin123'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Admin already exists: {admin.email}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Demo users are ready!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Buyer:  buyer@example.com / test123')
        self.stdout.write('  Seller: seller@example.com / test123')
        self.stdout.write('  Admin:  admin@example.com / admin123')
