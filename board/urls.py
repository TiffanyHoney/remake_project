from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('write/', views.post_create, name='post_create'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),

    # ✅ 추가된 수정/삭제 관련 URL
    path('edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
]
