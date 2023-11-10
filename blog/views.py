from django.shortcuts import render, get_object_or_404
from .models import Post

# from django.http import Http404
# Create your views here.

def post_list(request):
    posts = Post.published.all()  # создаем переменную и выполняем queryset-запрос в базу данных
    # В данном представлении (Функции)извлекаются все посты со статусом PUBLISHED, 
    # используя менеджер published, который мы создали ранее.
    return render(request,         
                  'blog/post/list.html',
                  {'posts': posts}) # прописываем путь для шаблона сайта и словарь Публикациями пост
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,  # удаляем параметр id=id и добавляем год, месяц, день 
                             slug=post, 
                             publish__year=year, 
                             publish__month=month,
                             publish__day=day,) 
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No Post found')
    
    return render(request, 
                  'blog/post/detail.html',
                  {'post': post})
    
    
    