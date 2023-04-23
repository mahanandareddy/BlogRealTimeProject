from django.shortcuts import render,get_object_or_404
from BlogApp.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from BlogApp.forms import CommentForm,Comment
from taggit.models import Tag
from django.db.models import Count

def Post_List_view(request,tag_slug = None):
    Post_List = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        Post_List = Post_List.filter(tags__in=[tag])
    paginator = Paginator(Post_List,2)
    page_number = request.GET.get('page')
    try:
        Post_List = paginator.page(page_number)
    except PageNotAnInteger:
        Post_List = paginator.page(1)
    except EmptyPage:
        Post_List = paginator.page(paginator.num_pages)
    return render(request,'BlogApp/post_list.html',{'Post_List': Post_List,'tag':tag})

def post_detail_view(request, year,month,day,post):
    post= get_object_or_404(Post,slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    post_tags_ids = post.tags.values_list('id',flat =True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags =Count('tags')).order_by('-same_tags','publish')[:4]

    comments  = post.comments.filter(active = True)
    Csubmit = False
    if request.method == 'POST':
        form  = CommentForm(data = request.POST)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment_post = post
            new_comment.save()
            Csubmit = True
    else:
        form = CommentForm()
    return render(request, "BlogApp/post_detail.html",{'post':post,'comments':comments,'csubmit':Csubmit,'form':form,'similar_posts': similar_posts})
from django.core.mail import send_mail
#send_mail('Hello', 'Very imp msg....','mahananda@gmail.com',['mahanandareddyb@gmail.com','mahanandareddybhumireddy@gmail.com'])



from BlogApp.forms import EmailSendFrom

def mail_send_view(request,id):
    post = get_object_or_404(Post, id=id, status = 'published')
    sent = False
    if request.method == 'POST':
        form = EmailSendFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'], post.title)
            message = "Read Post At: \n{}\n\n{} 'Comments:\n{}".format(post_url, cd['name'], cd['comments'])
            send_mail(subject,message,'mahanandareddyb@gmail.com', [cd['to']])
            sent =True
    else:
            form = EmailSendFrom()
    return render(request,'BlogApp/sharebymail.html', {'post':post,'form':form,'sent':sent})


