from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.conf import settings
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        ("email address"),
        unique=True,
        validators=[
            EmailValidator,
        ],
    )
    registration_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    groups = None
    user_permissions = None

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class File(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    file = models.FileField(upload_to='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0, blank=True, verbose_name='Количество скачиваний')
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Comment(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:20]}..."


class Review(models.Model):
    STATUS_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=STATUS_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
