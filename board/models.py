from django.db import models
from django.contrib.auth.models import User  # ✅ 추가

class BlogPost(models.Model):  # 그대로 유지
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


