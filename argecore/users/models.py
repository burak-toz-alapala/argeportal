from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
import os.path

class UserType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name

    class Meta:
        verbose_name = "User Type"
        verbose_name_plural = "User Types"
    
    class Meta:
        verbose_name_plural = "User Types"

def rename_image(instance, filename):
    path = "profil_foto"
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4())[:8], ext)

    return os.path.join(path, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.ForeignKey(UserType, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=rename_image, default="profil_foto/6b9f250c.png",)

    def save(self, *args, **kwargs):
        ### IMAGE RESIZE
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = "Profiller"