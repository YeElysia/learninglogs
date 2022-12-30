from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """学习笔记的主页。"""
    return render(request, 'learning_logs/index.html')

def check_topic_owner(topic,request):
    """核实主题关联到的用户为当前登录的用户"""
    if topic.owner != request.user:
        raise Http404
@login_required #login_required() 的代码检查用户是否已登录，仅当用户已登录时，Django才运行topics() 的代码。如果用户未登录，就重定向到登录页面。
def topics(request):
    """显示所有的主题。"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')#查询数据库
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目。"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户。
    check_topic_owner(topic,request)

    entries = topic.entry_set.order_by('-date_added')#date_added 前面的减号指定按降序排列，即先显示最近的条目。
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题。"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单。
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
            #导入了函数redirect ，用户提交主题后将使用这个函数重定向到页面topics 。函数redirect 将视图名作为参数，并将用户重定向到这个视图。

    # 显示空表单或指出表单数据无效。
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目。"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)# 确认请求的主题属于当前用户。

    if request.method != 'POST':
        # 未提交数据：创建一个空表单。
        form = EntryForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) #调用save() 时，传递实参commit=False （见❺），让Django创建一个新的条目对象，并将其赋给new_entry ，但不保存到数据库中。
            new_entry.topic = topic #将new_entry 的属性topic 设置为在这个函数开头从数据库中获取的主题
            new_entry.save() #再调用save() 且不指定任何实参。这将把条目保存到数据库，并将其与正确的主题相关联。
            return redirect('learning_logs:topic', topic_id=topic_id)
    # 显示空表单或指出表单数据无效。
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目。"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题属于当前用户。
    check_topic_owner(topic,request)

    if request.method != 'POST':
        # 初次请求：使用当前条目填充表单。
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(instance=entry, data=request.POST)#让Django根据既有条目对象创建一个表单实例，并根据request.POST 中的相关数据对其进行修改。
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html',context)


