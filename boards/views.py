from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import paginator
from django.core.checks import messages
from django.db.models import Count
from django.db.models.deletion import PROTECT
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import UpdateView
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request,template_name='home.html',context={'boards':boards})

@login_required
def board_topic(request,pk):
    board = get_object_or_404(Board,id = pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
    page = request.GET.get('page',1)

    paginator = Paginator(queryset,6)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request,template_name='topics.html',context={'board':board,'topics': topics})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=board.pk , topic_pk = topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

@login_required
def topic_posts(request,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk = pk,pk=topic_pk)
    topic.views += 1
    topic.save()
    queryset = topic.posts.order_by('created_at').annotate(messages=Count('message')-1)
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,6)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    #<---Pagination------------------>#

    return render(request,template_name='topic_posts.html',context={'topic':topic,'topics': topics})

@login_required
def reply_topic(request,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk = pk,pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit= False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts',pk=pk,topic_pk = topic_pk)
    else:
        form = PostForm()
    return render(request,template_name='reply_topic.html',context={'topic':topic,'form':form})

class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self,form):
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts',pk = post.topic.board.pk, topic_pk = post.topic.pk)