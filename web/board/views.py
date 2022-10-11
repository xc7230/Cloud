from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post, PostImage
from reply.forms import ReplyForm


@login_required(login_url='/accounts/login')
def like(request, bid):
    post = Post.objects.get(id=bid)
    user = request.user
    if post.like.filter(id=user.id).exists():
        post.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt': post.like.count()})
    else:
        post.like.add(user)
        return JsonResponse({'message': 'added', 'like_cnt': post.like.count()})


@login_required(login_url='/accounts/login')
def create(request):
    if request.method == "GET":
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, "board/create.html", context)
    elif request.method == "POST":
        postForm = PostForm(request.POST)

        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.writer = request.user
            post.save()
            for image in request.FILES.getlist('image', None):
                postImage = PostImage()
                postImage.image = image
                postImage.post = post
                postImage.save()


        return redirect('/board/read/' + str(post.id))


def list(request):
    posts = Post.objects.prefetch_related('postimage_set').all().order_by('-id')
    context = {'posts': posts}
    return render(request, 'board/list.html', context)


def read(request, bid):
    post = Post.objects.prefetch_related('reply_set').prefetch_related('postimage_set').get(id=bid)
    replyForm = ReplyForm()
    context = {'post': post, 'replyForm': replyForm}
    return render(request, 'board/read.html', context)


@login_required(login_url='/accounts/login')
def delete(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/read/' + str(bid))
    post.delete()
    return redirect('/')


@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/read/' + str(bid))

    if request.method == "GET":
        context = {'post': post}
        return render(request, "board/update.html", context)

    elif request.method == "POST":
        postForm = PostForm(request.POST, instance=post)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/' + str(bid))
