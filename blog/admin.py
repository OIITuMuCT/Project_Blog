from django.contrib import admin
from .models import Post # импортируем из файла модель.пу модель Пост

# admin.site.register(Post)       # добавляем модельПост на сайт администратора джанго

# изменим внешний вид панели администратора

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status' ]
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}    # предварительно заполненные поля
    raw_id_fields = ['author']
    date_hierarchy = 'publish'  # иерархия дат
    ordering = ['status', 'publish'] 
    
    
    