from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'),
    # path('<int:id>/', views.post_detail, name='post_detail'), # изменим для отображения года месяча и дня в Юрл адресе 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, 
         name='post_detail'),
    
    
    
]
