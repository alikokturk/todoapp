from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Özel kullanıcı modeli."""
    
    email = models.EmailField(unique=True, verbose_name='E-posta Adresi')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='Profil Resmi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
    
    def __str__(self):
        return self.username 