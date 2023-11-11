from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'), # стандартное представление
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # альтернативное представление
    # path('', views.PostListView.as_view(), name='post_list'),
    # path('<int:id>/', views.post_detail, name='post_detail'), # изменим для отображения года месяца и дня в Юрл адресе 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
        views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    
    
]
