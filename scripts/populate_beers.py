
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

def populate():
    # 1. Create Categories
    categories_data = {
        'Light Beer': 'light-beer',
        'Unfiltered Beer': 'unfiltered-beer',
        'Dark Beer': 'dark-beer'
    }
    
    cats = {}
    for name, slug in categories_data.items():
        cat, created = Category.objects.get_or_create(name=name, defaults={'slug': slug})
        cats[name] = cat
        print(f"Category '{name}' {'created' if created else 'already exists'}")

    # 2. Create Products
    # Sample names for each type
    light_beers = [
        "Summer Lager", "Golden Pilz", "Sunray Ale", "Crisp Morning", "Beachside Brew", 
        "Citrus Breeze", "Meadow Gold", "Crystal Clear", "Light Delight", "Helles Angel", "Session Lite"
    ]
    
    unfiltered_beers = [
        "Hazy IPA", "Cloudy Wheat", "Yeast Feast", "Raw Power", "Natur Trub",
        "Kellerbier Custom", "Zwickl Original", "Forest Haze", "Wheat Dream", "Bio Unfiltered"
    ]
    
    dark_beers = [
        "Midnight Stout", "Black Porter", "Ebony Ale", "Choco Malz", "Coffee Break",
        "Night Watch", "Imperial Shadow", "Velvet Underground", "Oatmeal Stout", "Baltic Porter"
    ]

    products_map = {
        'Light Beer': light_beers,
        'Unfiltered Beer': unfiltered_beers,
        'Dark Beer': dark_beers
    }

    for cat_name, beer_names in products_map.items():
        category = cats[cat_name]
        for i, name in enumerate(beer_names):
            # Create a unique slug just in case
            slug = name.lower().replace(' ', '-')
            
            # Random price between 3.00 and 12.00
            price = round(random.uniform(3.00, 12.00), 2)
            
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': category,
                    'description': f"A delicious {name} from our {cat_name} collection. Brewed with passion and the finest ingredients.",
                    'price': price,
                    'stock': random.randint(10, 100),
                    'is_active': True
                    # image will be null effectively, falling back to placeholder in template
                }
            )
            print(f"Product '{name}' {'created' if created else 'already exists'}")

if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
