from django.shortcuts import render,redirect
from blog.models import Post
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from blog.forms import EmailSendForm,CommentForm,PostForm
from taggit.models import Tag
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        if request.user.is_authenticated:
            form=CommentForm(data=request.POST)
            if form.is_valid():
                  new_comment=form.save(commit=False)
                  new_comment.post=post
                  new_comment.save()
                  csubmit=True
        else:
            messages.warning(request, "First You have to login!")
            return redirect('login')
    form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'comments':comments,'csubmit':csubmit})
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=Post.objects.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tags':tag})

@login_required(login_url='/login/')
def mail_send_view(request,my_id):
    post=get_object_or_404(Post,my_id=my_id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({})recommendes you to read"{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post At: \n{}\n\n{}\'Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'1857harshitgupta@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'post':post,'form':form,'sent':sent})

@login_required(login_url='/login/')
def home_view(request):
    s=User.objects.filter(pk=1)
    star=False
    if request.method=='POST':
       form = PostForm(request.POST)
       if form.is_valid():
            newpost=form.save(commit=False)
            newpost.slug = slugify(newpost.title)
            newpost.author=User.objects.get(id=2)
            newpost.status="published"
            star=True
            form.save()
    return render(request, 'blog/post_write.html',{'star':star})



