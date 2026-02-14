from django.core.management.base import BaseCommand
from apps.products.models import Category


class Command(BaseCommand):
    help = 'Populate default product categories'
    
    def handle(self, *args, **options):
        """Create default categories"""
        categories = [
            {'name': 'Electronics', 'slug': 'electronics', 'order': 1},
            {'name': 'Clothing', 'slug': 'clothing', 'order': 2},
            {'name': 'Books', 'slug': 'books', 'order': 3},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'order': 4},
            {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors', 'order': 5},
            {'name': 'Toys & Games', 'slug': 'toys-games', 'order': 6},
            {'name': 'Beauty & Health', 'slug': 'beauty-health', 'order': 7},
            {'name': 'Food & Beverages', 'slug': 'food-beverages', 'order': 8},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'order': cat_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )
