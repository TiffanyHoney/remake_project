from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import BlogPost
from .forms import BlogPostForm

# 게시글 목록
def post_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

# 글 작성
@login_required
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 작성자 지정
            post.save()
            return redirect('post_list')  # 글 목록으로 이동
    else:
        form = BlogPostForm()
    return render(request, 'board/post_form.html', {'form': form})

# 글 수정
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    # 작성자가 아닌 경우 접근 금지
    if post.author != request.user:
        return HttpResponseForbidden("본인만 수정할 수 있습니다.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'board/post_form.html', {'form': form, 'edit': True})

# 글 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    # 작성자가 아닌 경우 접근 금지
    if post.author != request.user:
        return HttpResponseForbidden("본인만 삭제할 수 있습니다.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    # 삭제 확인 페이지(선택사항) 필요하면 만들기
    return render(request, 'board/post_confirm_delete.html', {'post': post})

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
