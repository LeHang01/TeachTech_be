from django.apps import AppConfig

from app.admin.admins import load_admin


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        load_admin()