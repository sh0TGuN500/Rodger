from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.base import View

from .forms import CommentForm, ArticleEditForm, text_validator, cleanhtml
from .models import Article, Choice, Tag, Comment
# from .tasks import send_task, admin_send_task


########################################################################################################################
################################################ ARTICLE CRUD #########################################################
########################################################################################################################


@login_required()
def personal_page(request):
    return render(request, 'articles/personal_page.html')


@login_required()
def publish_article(request, article_id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse_lazy('home:home'))
    article = get_object_or_404(Article, id=article_id)
    article.publish()
    # HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))
    return redirect(request.META.get('HTTP_REFERER'))


class ArticleIndexView(generic.ListView):
    paginate_by = 16
    template_name = 'articles/article_list.html'

    # context_object_name = 'latest_article_list'
    def get_queryset(self):
        """
        Return the last published articles (not including those set to be
        published in the future).
        """
        if self.request.user.is_superuser:
            return Article.objects.only('title', 'is_published').all().order_by('-pub_date')
        else:
            return Article.objects.only('title').filter(is_published=True).order_by('-pub_date')


# ajax
class ArticleDetailView(generic.DetailView, generic.edit.FormView):
    model = Article
    template_name = 'articles/article_detail.html'
    form_class = CommentForm
    http_method_names = ['get']

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        comments = Comment.objects.filter(article_id=pk).select_related('user').order_by('-pub_date')
        return get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set__vote_set__user', Prefetch('comment_set', queryset=comments)
        ), id=pk)


class ArticleSearchView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'articles/article_list.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        """
        Return the last published articles (not including those set to be
        published in the future).
        """
        valid_search = self.request.GET['search']
        if valid_search:
            return Article.objects.filter(title__icontains=valid_search, is_published=True).order_by('-pub_date')
        else:
            return HttpResponseRedirect(reverse_lazy('articles:home'))


@login_required()
def article_delete(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id, user=user)
    article_title = article.title
    article.delete()
    my_article_list = Article.objects.filter(user=user).only('title').order_by('-pub_date')
    messages.success(request, _(f'Article "{article_title}" has been deleted'))
    return render(request, 'articles/article_list.html', {'my_article_list': my_article_list})


class MyArticlesView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'articles/article_list.html'
    context_object_name = 'my_article_list'

    def get_queryset(self):
        """
        Return the last published articles (not including those set to be
        published in the future).
        """
        return Article.objects.filter(user=self.request.user).only('title').order_by('-pub_date')


@login_required()
def article_create_update_form(request, article_id=None):
    if article_id:
        article = get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set'
        ), id=article_id)
        if article.user != request.user:
            return HttpResponseRedirect(reverse_lazy('articles:article_create'))
        form = ArticleEditForm(instance=article)
        return render(request, 'articles/article_edit.html', {
            'title': article.title,
            'choices': article.choice_set.all(),
            'tags': article.tag.all(),
            'article_id': article_id,
            'form': form
        })
    else:
        form = ArticleEditForm()
        return render(request, 'articles/article_edit.html', {
            'form': form,
            'article_id': article_id,
        })


@login_required
def article_db_save(request, article_id=None):
    """
    Request to save an article and its associated tags and voting from the form to the database
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseRedirect(reverse_lazy('articles:article_create'))
    if article_id:
        article_model = get_object_or_404(Article, id=article_id, user=request.user)
        article_model.up_date = timezone.now()
        article_model.choice_set.all().delete()
    else:
        article_model = Article(user=request.user, up_date=None)
    data = ArticleEditForm(request.POST, instance=article_model)
    if not data.is_valid():
        return JsonResponse({'error': data.errors})
    data.save()

    tag_list, tag_status = add_article_list_validation(request, 'tag')
    choice_list, choice_status = add_article_list_validation(request, 'choice')

    if tag_status == 'error':
        return JsonResponse({'error': _(' • Tag should be the length between 2 and 200')})
    if choice_status == 'error':
        return JsonResponse({'error': _(' • Choice should be the length between 2 and 200')})
    if tag_list:
        existing_tags = set(Tag.objects.filter(name__in=tag_list))
        # existing_tag_names = set(tag.name for tag in existing_tags)

        new_tags_to_create = [Tag(name=tag) for tag in tag_list if tag not in existing_tags]

        # Save the new tags to the database
        Tag.objects.bulk_create(new_tags_to_create)

        # Fetch all tags again to include the newly created ones with primary keys
        all_tags = Tag.objects.filter(name__in=tag_list)
        # tags_to_add = list(existing_tags) + list(all_tags)
        article_model.tag.add(*all_tags)

    if choice_list:
        choices_to_create = [Choice(article_id=article_model.id, text=choice) for choice in choice_list]
        Choice.objects.bulk_create(choices_to_create)

    article_url = reverse_lazy('articles:detail', args=(article_model.id,))
    article_href = f'"<a href="{article_url}">{escape(article_model.title)}</a>"'
    article_url_message = _(f' • Article {article_href} successfully posted')

    #if not DEBUG:
    article_absolute_url = 'rodger-dj.herokuapp.com' + article_url
    html_content = render_to_string(
        'articles/email_template.html',
        {'article_url': article_absolute_url,
         'user': request.user.username,
         'article_title': article_model.title})
    # admin_send_task.delay(
    #     _(f'New article posted: {article_model.title}'),
    #     html_content,
    #     # article_model.user.email
    # )
    return JsonResponse({'success': article_url_message})


@login_required()
def article_like(request, article_id, like):
    article = get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set__vote_set', 'comment_set__user'
        ), id=article_id)
    user = request.user
    like = bool(like)
    count = 1 if like else 0
    add_message = _('Liked') if like else _('Disliked')
    delete_message = _('Unliked') if like else _('Undisliked')
    try:
        existing_like = article.articlelike_set.get(user=user)
    except ObjectDoesNotExist:
        # first like/dislike
        message = add_message
        article.like_count += count
        article.articlelike_set.create(user=user, is_like=like)
        article.save()
    else:
        # like/dislike exist
        if existing_like.is_like != like:
            # existing like is different, change is_like value
            existing_like.is_like = like
            existing_like.save()
            article.like_count += count if like else -1
            article.save()
            message = add_message
        else:
            # existing like is same, delete like/dislike raw
            message = delete_message
            existing_like.delete()
            article.like_count -= count
            article.save()
    return JsonResponse({'success': message})


########################################################################################################################
################################################ COMMENT CRUD ##########################################################
########################################################################################################################


class CommentCreate(LoginRequiredMixin, View):
    def get(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment.objects.select_related('user'), id=comment_id, user=request.user)
        article = get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set__vote_set', 'comment_set__user'
        ), id=article_id)
        form = CommentForm(instance=comment)
        return render(request, 'articles/article_detail.html', {
                'article': article,
                'comment': comment,
                'editing_comment': comment_id,
                'form': form
        })

    def post(self, request, article_id, comment_id=None):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseRedirect(reverse_lazy('articles:home'))
        article = get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set__vote_set', 'comment_set__user'
        ), id=article_id)
        if comment_id:
            comment = get_object_or_404(Comment.objects.select_related('user'), id=comment_id)
            comment.up_date = timezone.now()
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
            else:
                error_text = cleanhtml(str(form.errors.get('text')).strip())
                return JsonResponse({'error': f' • {error_text}'})
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.article = article
                form.save()
            else:
                error_text = cleanhtml(str(form.errors.get('text')).strip())
                return JsonResponse({'error': f' • {error_text}'})
        user = article.user
        #if not DEBUG:
        article_absolute_url = 'rodger-dj.herokuapp.com' + reverse_lazy('articles:detail', args=(article_id,))
        # send_task.delay(
        #     _(f'New comment for {article.title}'),
        #     _(f'''User {request.user.username} commented on your article {article_absolute_url}!
        #     \nYou can\'t get rid of the mailing because I haven\'t implemented it.'''),
        #     user_email=user.email,
        # )
        return JsonResponse({'success': _(' • Comment successful posted')})


@login_required()
def comment_delete(request, article_id, comment_id):
    comment = get_object_or_404(Comment.objects.select_related('user'), id=comment_id, user=request.user)
    comment_message = _(' • Comment has been deleted')
    comment.delete()
    article = get_object_or_404(Article.objects.select_related(
            'user'
        ).prefetch_related(
            'tag', 'choice_set__vote_set', 'comment_set__user'
        ), id=article_id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
        'comment_message': comment_message
    }
    return render(request, 'articles/article_detail.html', context=context)


@login_required()
def comment_like(request, comment_id, like):
    comment = get_object_or_404(Comment.objects.select_related('user'), id=comment_id)
    article = get_object_or_404(Article.objects.select_related(
        'user'
    ).prefetch_related(
        'tag', 'choice_set__vote_set', 'comment_set__user'
    ), id=comment.article_id)
    user = request.user
    like = bool(like)
    count = 1 if like else 0
    add_message = _('Comment liked') if like else _('Comment disliked')
    delete_message = _('Comment unliked') if like else _('Comment undisliked')

    try:
        existing_like = comment.commentlike_set.get(user=user)
    except ObjectDoesNotExist:
        message = add_message
        comment.like_count += count
        comment.commentlike_set.create(user=user, is_like=like)
        comment.save()
    else:
        if existing_like.is_like != like:
            existing_like.is_like = like
            existing_like.save()
            comment.like_count += count if like else -1
            comment.save()
            message = add_message
        else:
            existing_like.delete()
            comment.like_count -= count
            comment.save()
            message = delete_message
    return render(request, 'articles/article_detail.html', context={
        'comment_message': message,
        'article': article,
        'form': CommentForm(),
    }
                  )

########################################################################################################################
################################################ TAGS SECTION ##########################################################
########################################################################################################################


class TagListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'articles/article_list.html'
    context_object_name = 'tags_list'

    def get_queryset(self):
        """
        Return articles with chosen tag (not including those set to be
        published in the future).
        """
        tag = self.kwargs['tag_id']
        # tag_name = Tag.objects.get(id=tag).name
        if tag:
            return Article.objects.filter(tag=tag).only('title').order_by('-pub_date')
        else:
            return HttpResponseRedirect(reverse_lazy('articles:home'))


########################################################################################################################
################################################ VOTE SECTION ##########################################################
########################################################################################################################


# ajax
class VoteResultView(LoginRequiredMixin, generic.DetailView):
    model = Article
    template_name = 'articles/votes_results.html'


@login_required()
def vote(request, article_id):
    article = get_object_or_404(Article.objects.prefetch_related('vote_set__choice'), id=article_id)
    user = request.user
    results_url = reverse_lazy('articles:results', args=(article_id,))

    if article.vote_set.filter(user=user).exists():
        return JsonResponse({'error': _(f' • You have already voted. <a href="{results_url}">Results</a>')})

    choice = get_object_or_404(Choice, id=request.POST.get('choice'))
    article.vote_set.create(choice=choice, user=user)
    choice.votes += 1
    choice.save()

    return JsonResponse({'success': _(f' • Voting was successful. <a href="{results_url}">Results</a>')})


########################################################################################################################
################################################ PROCESSORS SECTION ####################################################
########################################################################################################################


# AJAX
def add_article_list_validation(request, element_name: str):
    data = request.POST
    if data.get(element_name):
        request_list = dict(data.lists())[element_name]
        count = 0
        status_list = []
        for element in request_list:
            text = text_validator(element, 2, 200)
            if text:
                request_list[count] = text
                status_list.append('ok')
            else:
                # jsonResponse
                status_list.append('error')
            count += 1
        return request_list, status_list
    else:
        return [], []


########################################################################################################################
################################################ FEATURES SECTION ######################################################
########################################################################################################################


# froala test form page
'''def froala_form(request):
    return render(request, 'articles/froala template.html', {
        'form': FroalaModelForm()
    })


# froala test request post form processor
def post_froala_form(request):
    form = FroalaModelForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.name = request.POST['name']
        form.content = request.POST['content']
        form.save()
        return HttpResponseRedirect(reverse_lazy('articles:froala_index'))
    else:
        return render(request, 'articles/froala template.html', {
            'form': form
        })


# froala test list view
class FroalaIndexView(generic.ListView):
    paginate_by = 16
    template_name = 'articles/article_list.html'

    # context_object_name = 'latest_article_list'

    def get_queryset(self):
        """
        Return the last published articles (not including those set to be
        published in the future).
        """
        return FroalaModel.objects.all().order_by('-pub_date')


# froala test detail view
class FroalaDetailMixinView(generic.edit.FormMixin, generic.detail.DetailView):
    model = FroalaModel
    template_name = 'articles/article_detail.html'''

# test0 ajax handler
'''class AjaxHandlerView(View):
    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            t = time()
            return JsonResponse({'seconds': t}, status=200)
        return render(request, 'articles/ajax_template.html')

    def post(self, request):
        card_text = request.POST.get('text')

        result = f'i\'ve got: {card_text}'
        return JsonResponse({'data': result}, status=200)'''

'''
# test1 ajax page
def ajax_page(request):
    return render(request, 'articles/ajax_page.html')


# test1 ajax request processor
class AjaxDataCheck(View):
    @staticmethod
    def post(request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            post_dict = {
                'name': text_validator(request.POST['name']),
                'email': text_validator(request.POST['email']),
                'bio': text_validator(request.POST['bio'])
            }

            error_dict = {
                'name': '✔️',
                'email': '✔️',
                'bio': '✔️'
            }
            for i in post_dict:
                if len(post_dict[i]) <= 6:
                    error_dict.update({f'{i}': 'not enought symbols'})

            return JsonResponse(error_dict)

        return render(request, 'articles/ajax_page.html')
'''
