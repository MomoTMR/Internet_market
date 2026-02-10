#!/bin/bash

# Загрузка переменных из .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
fi

# Проверка, запущен ли контейнер
CONTAINER_NAME="${WEB_CONTAINER_NAME:-hopbarley_web}"
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Ошибка: Контейнер $CONTAINER_NAME не запущен."
    echo "Запустите проект с помощью 'docker compose up' перед запуском этого скрипта."
    exit 1
fi

echo "Инициализация данных..."

docker exec -i $CONTAINER_NAME python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from products.models import Product, Category
from decimal import Decimal
import random
import os

User = get_user_model()

# 1. Создание суперпользователя из .env
SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(SUPERUSER_USERNAME, f'{SUPERUSER_USERNAME}@example.com', SUPERUSER_PASSWORD)
    print(f'SUCCESS: Суперпользователь "{SUPERUSER_USERNAME}" создан')
else:
    print(f'WARNING: Суперпользователь "{SUPERUSER_USERNAME}" уже существует')

# 2. Создание обычных пользователей
users_data = [
    ('user1', 'user1@example.com', 'pass1'),
    ('user2', 'user2@example.com', 'pass2'),
    ('user3', 'user3@example.com', 'pass3'),
]

for username, email, password in users_data:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, email, password)
        print(f'SUCCESS: Пользователь "{username}" создан')

# 3. Создание категории
category, created = Category.objects.get_or_create(
    name='Craft Beer',
    defaults={'slug': 'craft-beer'}
)
if created:
    print('SUCCESS: Категория "Craft Beer" создана')

# 4. Создание товаров
products_data = [
    {
        'name': 'IPA Classic',
        'slug': 'ipa-classic',
        'description': 'Classic Indian Pale Ale with strong hops.',
        'price': Decimal('5.50'),
        'stock': 100
    },
    {
        'name': 'Stout Dark',
        'slug': 'stout-dark',
        'description': 'Rich and creamy dark stout.',
        'price': Decimal('6.00'),
        'stock': 50
    },
    {
        'name': 'Lager Light',
        'slug': 'lager-light',
        'description': 'Crisp and refreshing lager.',
        'price': Decimal('4.50'),
        'stock': 200
    },
    {
        'name': 'Pale Ale',
        'slug': 'pale-ale',
        'description': 'Balanced pale ale with fruity notes.',
        'price': Decimal('5.00'),
        'stock': 75
    },
    {
        'name': 'Porter',
        'slug': 'porter',
        'description': 'Dark style of beer developed in London.',
        'price': Decimal('5.80'),
        'stock': 60
    }
]

for p_data in products_data:
    if not Product.objects.filter(slug=p_data['slug']).exists():
        Product.objects.create(category=category, **p_data)
        print(f'SUCCESS: Товар "{p_data["name"]}" создан')
    else:
        print(f'WARNING: Товар "{p_data["name"]}" уже существует')

EOF

echo "Готово! Данные успешно инициализированы."
