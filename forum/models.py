from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='forum_posts'
        )
    updated_date = models.DateTimeField(auto_now=True)
    html_content = models.TextField()
    css_content = models.TextField()
    js_content = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, max_length=60, on_delete=models.CASCADE,
        related_name='catego')
    favorites = models.ManyToManyField(
        User, related_name="forum_favorutes", blank=True
        )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.slug})

    def avg_rating(self):
        ratings = Rating.objects.filter(post=self)
        if ratings.exists():
            return round(ratings.aggregate(Avg('value'))['value__avg'], 2)
        return None


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
