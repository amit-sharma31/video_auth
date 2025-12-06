import hashlib

from django.conf import settings
from django.db import models


class Video(models.Model):
    STATUS_CHOICES = (
        ("verified", "Verified"),
        ("duplicate", "Duplicate"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    file = models.FileField(upload_to='uploads/')
    sha256 = models.CharField(max_length=64, db_index=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='verified')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def compute_sha256(self) -> str:
        """Compute sha256 of the uploaded file content.

        This reads the file in chunks and safely rewinds the file pointer.
        """
        hasher = hashlib.sha256()
        fileobj = self.file
        # ensure file pointer is at start
        try:
            fileobj.open()
        except Exception:
            pass

        try:
            for chunk in fileobj.chunks():
                hasher.update(chunk)
        except AttributeError:
            # plain file-like
            fileobj.seek(0)
            while True:
                chunk = fileobj.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)

        # reset pointer when possible
        try:
            fileobj.seek(0)
        except Exception:
            pass

        return hasher.hexdigest()

    def save(self, *args, **kwargs):
        # compute sha256 on first save (when file is present)
        if self.file and not self.sha256:
            sha = self.compute_sha256()
            self.sha256 = sha
            # mark duplicate if any other video has same hash
            qs = Video.objects.filter(sha256=sha)
            # exclude self if updating
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                self.status = 'duplicate'
            else:
                self.status = 'verified'

        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.owner} - {self.file.name} [{self.status}]"
