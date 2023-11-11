from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse

from taggit.managers import TaggableManager


class PublishedManager(models.Manager): # вместе с менеджером добавили два поля в модель Пост
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED) # objects and published


class Post(models.Model):
    
    class Status(models.TextChoices): # класс для хранения черновика
        DRAFT = 'DF', 'Draft'         # Post.Status.values вернет список ['DF', 'PB']
        PUBLISHED = 'PB', 'Published' # Post.Status.names ['DRAFT', 'PUBLISHED']
    
    title = models.CharField(max_length=250)  # Заголовок
    # Slug – это короткая метка, содержащая только буквы,цифры, знаки подчеркивания или дефисы.
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')   # с помощью этого параметра предотвратим хранение в модели Пост дублирующих записей. 
    author = models.ForeignKey(User, 
                            on_delete=models.CASCADE, 
                            related_name='blog_posts') # для обращения user.blog_posts.
    body = models.TextField()  # поле для хранения тела поста
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Определили перечисляемый класс Статус путем подклассирования 
    # класса models.TextChoices значениями выступают DF и PB, 
    # их метками или читаемыми именами являются Draft и Published.
    status = models.CharField(max_length=2,             
                            choices=Status.choices,   # Post.Status.choices вернет [('DF', 'Draft'), ('PB', 'Published')]
                            default=Status.DRAFT)     # Post.Status.labels вернет ['Draft', 'Published']
    
    objects = models.Manager() # менеджер применяемый по умолчанию добавили вместе с классом  
    published = PublishedManager() # конкретно прикладной менеджер                 (PublishedManager)
    # Менеджер tags позволит добавлять, извлекать и удалять теги из объектов Post.
    tags = TaggableManager() 
    
    class Meta:
        ordering = ['-publish'] # атрибут  ordering сортирует результаты по полю публикация
        indexes = [     # В Meta-класс модели была добавлена опция indexes
            models.Index(fields=['-publish']),   # 
        ]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): 
        return reverse('blog:post_detail', 
                        args=[self.publish.year, 
                              self.publish.month, 
                              self.publish.day, 
                              self.slug])
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    