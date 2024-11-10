# app/urls/__init__.py
import importlib
import os
import glob
from django.urls import include, path

urlpatterns = []

# Dynamically find all the URL configuration files in the urls directory
current_dir = os.path.dirname(__file__)
url_files = glob.glob(os.path.join(current_dir, '*.py'))

for url_file in url_files:
    module_name = os.path.splitext(os.path.basename(url_file))[0]
    if module_name == '__init__':
        continue
    module = f'app.urls.{module_name}'
    try:
        # Import the module
        imported_module = importlib.import_module(module)
        # Ensure the module has a urlpatterns attribute
        if hasattr(imported_module, 'urlpatterns'):
            urlpatterns.append(path('', include((imported_module, module_name), namespace=module_name)))
        else:
            print(f"{module} does not have urlpatterns attribute")
    except Exception as e:
        print(f"Error importing {module}: {e}")
