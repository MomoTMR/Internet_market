from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, Category
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize database with superuser, users, and products'

    def handle(self, *args, **options):
        # 1. Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))

        # 2. Create Regular Users
        users_data = [
            ('user1', 'user1@example.com', 'pass1'),
            ('user2', 'user2@example.com', 'pass2'),
            ('user3', 'user3@example.com', 'pass3'),
        ]

        for username, email, password in users_data:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'User "{username}" created'))

        # 3. Create Categories
        category, created = Category.objects.get_or_create(
            name='Craft Beer',
            defaults={'slug': 'craft-beer'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Category "Craft Beer" created'))

        # 4. Create Products
        products_data = [
            {
                'name': 'IPA Classic',
                'slug': 'ipa-classic',
                'description': 'Classic Indian Pale Ale with strong hops.',
                'price': Decimal('5.50'),
                'quantity': 100,
                'category': category
            },
            {
                'name': 'Stout Dark',
                'slug': 'stout-dark',
                'description': 'Rich and creamy dark stout.',
                'price': Decimal('6.00'),
                'quantity': 50,
                'category': category
            },
            {
                'name': 'Lager Light',
                'slug': 'lager-light',
                'description': 'Crisp and refreshing lager.',
                'price': Decimal('4.50'),
                'quantity': 200,
                'category': category
            },
            {
                'name': 'Pale Ale',
                'slug': 'pale-ale',
                'description': 'Balanced pale ale with fruity notes.',
                'price': Decimal('5.00'),
                'quantity': 75,
                'category': category
            },
            {
                'name': 'Porter',
                'slug': 'porter',
                'description': 'Dark style of beer developed in London.',
                'price': Decimal('5.80'),
                'quantity': 60,
                'category': category
            }
        ]

        for p_data in products_data:
            if not Product.objects.filter(slug=p_data['slug']).exists():
                Product.objects.create(**p_data)
                self.stdout.write(self.style.SUCCESS(f'Product "{p_data["name"]}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Product "{p_data["name"]}" already exists'))

        self.stdout.write(self.style.SUCCESS('Data initialization complete'))
