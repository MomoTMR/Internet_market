from products.models import Product
import os

# Mapping slug -> relative path in MEDIA_ROOT
products_map = {
    'ipa-classic': 'products/ipa-classic.png',
    'stout-dark': 'products/stout-dark.png',
    'lager-light': 'products/lager-light.png',
    'pale-ale': 'products/pale-ale.png',
    'porter': 'products/porter.png',
}

for slug, relative_path in products_map.items():
    try:
        product = Product.objects.get(slug=slug)
        # Verify file exists (relative to project root where script runs, assuming media is in root)
        full_path = os.path.join('media', relative_path)
        if os.path.exists(full_path):
            product.image.name = relative_path
            product.save()
            print(f"SUCCESS: Image linked for '{slug}' to '{relative_path}'")
        else:
            print(f"WARNING: File not found at '{full_path}'")
    except Product.DoesNotExist:
        print(f"WARNING: Product with slug '{slug}' not found")
    except Exception as e:
        print(f"ERROR: Failed to update '{slug}': {e}")
