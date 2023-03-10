from django.db import models
from django.contrib.auth import get_user_model

MAX_LENGTH_TITLE = 200


class Group(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_TITLE)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
