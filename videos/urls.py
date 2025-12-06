from django.urls import include, path

from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_video, name='upload'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
