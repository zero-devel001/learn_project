from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponseNotFound
# Create your views here.
from .models import Topic,Entry
from .forms import TopicForm,EntryForm

def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):

    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)  

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)  

@login_required
def new_topic(request):
    #Add new topic
    if request.method !="POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request,'learning_logs/new_topic.html',context) 

@login_required
def new_entry(request,topic_id):
    #Add new topic
    topic = Topic.objects.get(id=topic_id)
    if request.method !="POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id)

    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def delete_topic(request,topic_id):
    
    try:
        if request.method  =="POST":
            topic = Topic.objects.get(id=topic_id)
            topic.delete()
            return redirect('learning_logs:topics')   


    except  Topic.DoesNotExist:
        print("delete Error")   
        
    return redirect('learning_logs:topics')   


def delete_entry(request,entry_id):
    try:
        if  request.method=="POST":
            entry = Entry.objects.get(id=entry_id)
            topic = entry.topic
            entry.delete()
            return redirect('learning_logs:topic',topic_id=topic.id)

    except  Entry.DoesNotExist:
        return redirect('learning_logs:topics')   
