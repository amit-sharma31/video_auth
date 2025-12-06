from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Video
from .forms import UploadForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponse


def index(request):
    if request.user.is_authenticated:
        videos = Video.objects.filter(owner=request.user).order_by('-uploaded_at')
    else:
        videos = Video.objects.none()
    return render(request, 'videos/index.html', {'videos': videos})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = request.user
            video.save()
            return redirect('videos:index')
    else:
        form = UploadForm()

    return render(request, 'videos/upload.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos:index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
