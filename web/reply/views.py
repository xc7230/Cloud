import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from board.models import Post
from reply.forms import ReplyForm
from reply.models import Reply


@login_required(login_url='/user/login')
def create(request, bid):
    if request.method == "POST":
        reply = Reply()
        data = json.loads(request.body)
        reply.contents = data['contents']
        reply.writer = request.user
        post = Post()
        post.id = bid
        reply.post = post
        reply.save()


    return JsonResponse({'message': 'created', 'rid':reply.id})

@login_required(login_url='/user/login')
def create_plain(request, bid):
    if request.method == "POST":
        replyForm = ReplyForm(request.POST)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.writer = request.user
            post = Post()
            post.id = bid
            reply.post = post
            reply.save()

    return redirect('/board/read/'+str(bid))


@login_required(login_url='/user/login')
def update(request, bid, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return JsonResponse({'message': 'error'})

    elif request.method == "POST":
        data = json.loads(request.body)
        reply.contents = data['contents']
        reply.save()
        return JsonResponse({'message': 'updated'})

@login_required(login_url='/user/login')
def update_plain(request, bid, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return redirect('/board/read/' + str(bid))

    elif request.method == "POST":
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.save()
        return redirect('/board/read/' + str(bid))

@login_required(login_url='/accounts/login')
def delete(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return JsonResponse({'message': 'error'})
    else :
        reply.delete()
        return JsonResponse({'message': 'deleted'})
