from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# from django.http import Http404
# Create your views here.


def post_list(request, tag_slug=None):
    # В данном представлении (Функции)извлекаются все посты со статусом PUBLISHED, 
    # используя менеджер published, который мы создали ранее.
    # Добавили
    # В представление опциональный параметр tag_slug, значение
    # которого по умолчанию равно None. Этот параметр будет передан в URL-адресе.
    post_list = Post.published.all()  # создаем переменную и выполняем queryset-запрос в базу данных ## заменили posts на post_list
    
    tag = None
    
    
    if tag_slug:
        # Внутри указанного представления формируется изначальный набор
        # запросов, извлекающий все опубликованные посты, и если имеется
        # слаг данного тега, то берется объект Tag с данным слагом, 
        # используя функцию сокращенного доступа get_object_or_404().
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Здесь используется операция __in поиска по полю
        post_list = post_list.filter(tags__in=[tag])
    # постраничная разбивка с 3 постами на страницу 
    paginator = Paginator(post_list, 3)      #  Создаем экземпляр класса Paginator с числом объектов возвращаемых в  расчете на страницу. 
    page_number = request.GET.get('page', 1) #  Мы извлекаем HTTP GET-параметр page и сохраняем его в переменной page_number.
    
    try:
        posts = paginator.page(page_number)      #  Мы получаем объекты для желаемой страницы, вызывая метод page()
    
    except PageNotAnInteger:
        # if page_number is not an integer
        # return first page
        posts = paginator.page(1)
        
    except EmptyPage: #  класса Paginator. Этот метод возвращает объект Page, который хранится в переменной posts.
        # Если page_number находится вне диапазона, 
        # то выдать последнюю страницу
        posts =paginator.page(paginator.num_pages) 
    
    return render(request,         
                'blog/post/list.html',
                {'posts': posts,
                'tag': tag}) # прописываем путь для шаблона сайта и словарь Публикациями пост add tag


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,  # удаляем параметр id=id и добавляем год, месяц, день 
                            slug=post, 
                            publish__year=year, 
                            publish__month=month,
                            publish__day=day)
    # мы добавили набор запросов QuerySet, чтобы извлекать все активные
    # комментарии к посту, как показано ниже:
    
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    
    # Форма для комментирования пользователя
    form = CommentForm()
    
    # Список схожих комментариев пользователей
    
    
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No Post found')
    return render(request, 
                'blog/post/detail.html',
                {'post': post,
                'comments': comments,
                'form': form})

class PostListView(ListView):
    """ 
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3 
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # извлечь пост по идентификатору id 
    post = get_object_or_404(Post, 
                            id=post_id, 
                            status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        # Форма была подана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # отправить электронное письмо
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'vatamancorp@gmail.com',
                    [cd['to']])
            sent = True
    else:
        form =EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,
                                                    'form': form, 
                                                    'sent': sent})
    
    
@require_POST
def post_comment(request, post_id):
    # По ид поста извлекается опубликованный пост используя 
    # функцию сокращенного доступа get_object_or_404(). 
    post = get_object_or_404(Post, 
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    # Определяется переменная comment с изначальным значением None.
    # Указанная переменная будет использоваться для хранения комментарного 
    # объекта при его создании. 
    comment = None
    # Комментарий был отправлен
    # Создается экземпляр формы, используя переданные на обработку 
    # POST-данные, и проводиться их валидация методом is_valid()
    form = CommentForm(data=request.POST)
    # если форма валидна, то создается новый объект Comment
    # Вызывая метод save() формы, и назначается переменной new_comment, 
    # как показано ниже:
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию 
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post': post,
                            'form': form,
                            'comment': comment})
    
    