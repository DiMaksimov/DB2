from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import PostList, PostDetail, PostCreate


app_name = 'posts'

urlpatterns = [
    path('', login_required(PostList.as_view(), login_url='accounts/login'), name='list_view'),
    path('create/', login_required(PostCreate.as_view(), login_url='accounts/login'), name='create_view'),
    path('<int:pk>/', login_required(PostDetail.as_view(), login_url='accounts/login'), name='details_view'),

]
