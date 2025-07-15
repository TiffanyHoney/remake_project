from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost  # 수정됨
from .forms import BlogPostForm

# 게시글 목록
def post_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

# 글 작성
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # 글 목록으로 이동
    else:
        form = BlogPostForm()
    return render(request, 'board/post_form.html', {'form': form})

# 게시글 좋아요 기능
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    session_key = f'liked_post_{post_id}'

    if request.session.get(session_key, False):
        # 이미 좋아요를 누른 경우 → 취소
        post.likes -= 1
        del request.session[session_key]
    else:
        # 처음 누른 경우
        post.likes += 1
        request.session[session_key] = True

    post.save()
    return redirect('post_list')

