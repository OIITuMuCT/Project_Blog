from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm
# from django.http import Http404
# Create your views here.


def post_list(request):
    post_list = Post.published.all()  # создаем переменную и выполняем queryset-запрос в базу данных ## заменили posts на post_list
    # В данном представлении (Функции)извлекаются все посты со статусом PUBLISHED, 
    # используя менеджер published, который мы создали ранее.
    
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
                  {'posts': posts}) # прописываем путь для шаблона сайта и словарь Публикациями пост
 
   
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,  # удаляем параметр id=id и добавляем год, месяц, день 
                             slug=post, 
                             publish__year=year, 
                             publish__month=month,
                             publish__day=day) 
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No Post found')
    
    return render(request, 
                  'blog/post/detail.html',
                  {'post': post})

       
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
    if request.method == 'POST':
        # Форма была подана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.changed_data
            # отправить электронное письмо
    else:
        form =EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,
                                                    'form': form})