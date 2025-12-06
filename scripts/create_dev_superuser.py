"""Small helper: create a development superuser if it doesn't already exist.

Run this from the repository root like:
python video_auth/scripts/create_dev_superuser.py
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_auth.settings')

import django

django.setup()

from django.contrib.auth import get_user_model


def ensure_superuser(username='admin', email='admin@example.com', password='adminpass'):
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        print('superuser already exists')
        return
    print('creating superuser:', username)
    User.objects.create_superuser(username=username, email=email, password=password)
    print('done')


if __name__ == '__main__':
    ensure_superuser()
