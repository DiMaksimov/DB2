from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import PostList, PostDetail, PostCreate, add_comment_view, like_post_view


app_name = 'posts'

urlpatterns = [
    path('', login_required(PostList.as_view(), login_url='../account/login'), name='list_view'),
    path('create/', login_required(PostCreate.as_view(), login_url='../account/login'), name='create_view'),
    path('<int:pk>/', login_required(PostDetail.as_view(), login_url='../account/login'), name='details_view'),
    path('<int:id>/like/', login_required(like_post_view, login_url='../account/login'), name='likes_view'),
    path('<int:pk>/comment/', login_required(add_comment_view, login_url='../account/login'), name='comment_view'),
]
