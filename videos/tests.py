import hashlib

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from .models import Video


class VideosSmokeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='u', password='p')
        self.client = Client()

    def test_index_shows_no_videos_when_not_logged_in(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_upload_creates_video_and_computes_sha256(self):
        self.client.login(username='u', password='p')
        data = SimpleUploadedFile('video.mp4', b'my-video-bytes', content_type='video/mp4')
        resp = self.client.post('/upload/', {'file': data}, follow=True)
        self.assertEqual(resp.status_code, 200)
        v = Video.objects.filter(owner=self.user).first()
        self.assertIsNotNone(v)
        expected = hashlib.sha256(b'my-video-bytes').hexdigest()
        self.assertEqual(v.sha256, expected)
        self.assertEqual(v.status, 'verified')

    def test_duplicate_upload_marked_duplicate(self):
        self.client.login(username='u', password='p')
        data1 = SimpleUploadedFile('a.mp4', b'samecontent', content_type='video/mp4')
        self.client.post('/upload/', {'file': data1}, follow=True)

        data2 = SimpleUploadedFile('b.mp4', b'samecontent', content_type='video/mp4')
        self.client.post('/upload/', {'file': data2}, follow=True)

        videos = Video.objects.filter(owner=self.user).order_by('uploaded_at')
        self.assertEqual(videos.count(), 2)
        self.assertEqual(videos[0].status, 'verified')
        self.assertEqual(videos[1].status, 'duplicate')

    def test_index_shows_status_badges(self):
        # create a verified and a duplicate upload
        self.client.login(username='u', password='p')
        a = SimpleUploadedFile('a.mp4', b'one', content_type='video/mp4')
        b = SimpleUploadedFile('b.mp4', b'one', content_type='video/mp4')
        self.client.post('/upload/', {'file': a}, follow=True)
        self.client.post('/upload/', {'file': b}, follow=True)

        resp = self.client.get('/')
        self.assertContains(resp, 'status-badge status-verified')
        self.assertContains(resp, 'status-badge status-duplicate')
