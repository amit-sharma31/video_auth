from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='admin').exists():
    print('admin already exists')
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print('created admin (username=admin, password=adminpass)')
