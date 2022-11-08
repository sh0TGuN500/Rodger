from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate

from .forms import CommentForm, AddQuestionForm, text_validator
from .models import Question, Choice, Tag, Comment
from .tasks import send_task, admin_send_task
from djbook_test.settings import DEBUG


########################################################################################################################
################################################ CORE SECTION ##########################################################
########################################################################################################################


def home(request):
    return render(request, 'polls/home_page.html')


@login_required()
def personal_page(request):
    return render(request, 'polls/personal_page.html')


def info_for_customers(request):
    return render(request, 'polls/info_for_customers_page.html')


def lang_switcher(request, lang):
    user_language = lang
    activate(user_language)
    print(request.session.items())
    return render(request, 'polls/home_page.html')


########################################################################################################################
################################################ QUESTION CRUD #########################################################
########################################################################################################################


class QuestionIndexView(generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'

    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return Question.objects.all().order_by('-pub_date')


# ajax
class QuestionDetailMixinView(generic.edit.FormMixin, generic.detail.DetailView):
    model = Question
    template_name = 'polls/polls_detail.html'
    form_class = CommentForm


class QuestionSearchView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        valid_search = self.request.GET['search']
        if valid_search:
            return Question.objects.filter(question_title__icontains=valid_search).order_by('-pub_date')
        else:
            return HttpResponseRedirect(reverse('polls:home'))


@login_required()
def question_delete(request, question_id):
    user = request.user
    try:
        deleting_question = Question.objects.get(id=question_id, author_name=user)
    except Question.DoesNotExist:
        error_message = _('Question does not exist')
    else:
        deleting_question.delete()
        error_message = _(f'Question "{deleting_question}" has been deleted')
    my_question_list = Question.objects.filter(author_name=user).order_by('-pub_date')
    context = {
        'my_question_list': my_question_list,
        'error_message': error_message
    }
    return render(request, 'polls/polls_list.html', context=context)


class MyQuestionsView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'
    context_object_name = 'my_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(author_name=self.request.user).order_by('-pub_date')


@login_required()
def question_create_update_form(request, question_id=None):
    if question_id:
        question = Question.objects.get(id=question_id)
        if question.author_name == request.user.username:
            form = AddQuestionForm(instance=question)
            return render(request, 'polls/add_question.html', {
                'title': question.question_title,
                'choices': question.choice_set.all(),
                'tags': question.tag.all(),
                'question_id': question_id,
                'form': form

            })
        else:
            return HttpResponseRedirect(reverse('polls:create_question'))
    else:
        return render(request, 'polls/add_question.html', {
            'form': AddQuestionForm
        })


@login_required()
def question_db_save(request, question_id=None):
    if question_id:
        try:
            question_model = Question.objects.get(id=question_id)
            edit = True
        except Question.DoesNotExist:
            edit = False
            question_model = Question(author_name=request.user)
        else:
            question_model.up_date = timezone.now()
    else:
        edit = False
        question_model = Question(author_name=request.user)
    user_ok = question_model.author_name == request.user.username if edit else True

    # request validation
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    data = AddQuestionForm(request.POST, instance=question_model) if request.POST else None
    if not data or not is_ajax or not user_ok:
        return HttpResponseRedirect(reverse('polls:create_question'))

    # constants
    errors = False
    response_dict = {'title_info': _(' • Title: ✔️'),
                     'text_info': _(' • Text: ✔️')}

    # tags data validation
    tag_list, tag_status = add_question_list_validation(request, 'tag')
    if tag_list:
        if 'error' in tag_status:
            response_dict.update({'tag_info': _(' • Tag should be the length between 2 and 200')})
            errors = True
        else:
            response_dict.update({'tag_info': ' ✔️'})

    # choices data validation
    choice_list, choice_status = add_question_list_validation(request, 'choice')
    if choice_list:
        if 'error' in choice_status:
            response_dict.update({'choice_info': _(' • Choice should be the length between 2 and 200')})
            errors = True
        else:
            response_dict.update({'choice_info': ' ✔️'})

    # save data into DB
    for error in data.errors:
        if error == 'question_text':
            key = 'text_info'
            msg = 'Text: '
        elif error == 'question_title':
            key = 'title_info'
            msg = 'Title: '
        response_dict.update({key: ' • ' + msg + list(data.errors[error].data[0])[0]})
    if not errors:
        if edit:
            question_model.choice_set.all().delete()
        if data.is_valid():
            data.save()
        else:
            return JsonResponse(response_dict)

        '''title = data.data['question_title']
            response_dict.update({'title_info': f' • Title "{escape(title)}" already exist'})'''
        # if question exist
        '''if not get_question:
            get_question = Question(author_name=request.user)'''
        '''if get_question:
            form_data = AddQuestionForm(request.POST, instance=get_question)
            # get_question.choice_set.all().delete()
            # get_question.tag.all().delete()
        else:
            form_data = AddQuestionForm(request.POST)
            get_question = Question(author_name=request.user)'''

        # save tags if exist
        if tag_list:
            for tag in tag_list:

                # get tag or create new
                try:
                    add_tag = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    add_tag = Tag(name=tag)
                    add_tag.save()

                # create connection tag-question
                question_model.tag.add(add_tag)

        # save choices if exist
        if choice_list:
            for choice in choice_list:
                create_choice = Choice(question_id=question_model.id,
                                       choice_text=choice)
                create_choice.save()

        # Success jsonResponse
        # return HttpResponseRedirect(reverse('polls:detail', args=(get_question.id,)))
        question_url = reverse('polls:detail', args=(question_model.id,))
        question_href = f'"<a href="{question_url}">{escape(question_model.question_title)}</a>"'
        # email_template = render(request, 'account/email/email_confirmation_message.txt')
        question_url_message = _(f' • Question {question_href} successfully posted')
        if not DEBUG:
            question_absolute_url = 'rodger-dj.herokuapp.com' + question_url
            html_content = strip_tags(render_to_string(
                'polls/email_template.html',
                {'question_url': question_absolute_url,
                 'question_title': escape(question_model.question_title),
                 'user': request.user.username}))
            admin_send_task.delay('New question',
                                  html_content)
        response_dict.update({
            'success': question_url_message
        })
    return JsonResponse(response_dict)


########################################################################################################################
################################################ COMMENT CRUD ##########################################################
########################################################################################################################


class CommentCreate(LoginRequiredMixin, View):
    @staticmethod
    def get(request, question_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author_name=request.user)
        except Comment.DoesNotExist:
            return JsonResponse({'error': _(' • Comment does not exist')})
        else:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'error': _(' • Question does not exist')})
            form = CommentForm(instance=comment)
            return render(request, 'polls/polls_detail.html', {
                'question': question,
                'comment': comment,
                'editing_comment': comment_id,
                'form': form
            })

    @staticmethod
    # is ugly
    def post(request, question_id, comment_id=None):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseRedirect(reverse('polls:home'))
        else:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'error': _(' • Question does not exist')})
            if comment_id:
                try:
                    comment = Comment.objects.get(id=comment_id)
                except Comment.DoesNotExist:
                    return JsonResponse({'error': _(' • Comment does not exist')})
                else:
                    form = CommentForm(request.POST, instance=comment)
                    if form.is_valid():
                        form.save()
                    else:
                        return JsonResponse({'error': _(' • Symbols length less than 3')})

            else:
                form = CommentForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.author_name = request.user
                    form.question = question
                    form.save()
                else:
                    return JsonResponse({'error': _(' • Symbols length less than 3')})
            user = User.objects.get(username=question.author_name)
            if not DEBUG:
                send_task.delay(
                    _(f'New comment for {question.question_title}'),
                    _(f'''User {request.user.username} commented on your question!
                    \nYou can\'t get rid of the mailing because I have not implemented it.'''),
                    user_email=user.email,
                )
            return JsonResponse({'success': _(' • Comment successful posted')})
            # return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


@login_required()
def comment_delete(request, question_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, author_name=request.user)
    except Comment.DoesNotExist:
        comment_message = _(' • Comment does not exist')
    else:
        comment.delete()
        comment_message = _(' • Comment has been deleted')
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return HttpResponseRedirect(reverse('polls:index'))
    form = CommentForm()
    context = {
        'question': question,
        'form': form,
        'comment_message': comment_message
    }
    return render(request, 'polls/polls_detail.html', context=context)


########################################################################################################################
################################################ TAGS SECTION ##########################################################
########################################################################################################################


class TagListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'
    context_object_name = 'tags_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        tag = self.kwargs['tag_id']
        # tag_name = Tag.objects.get(id=tag).name
        if tag:
            return Question.objects.filter(tag=tag).order_by('-pub_date')
        else:
            return HttpResponseRedirect(reverse('polls:home'))


########################################################################################################################
################################################ VOTE SECTION ##########################################################
########################################################################################################################


# ajax
class VoteResultView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/votes_results.html'


# ajax
@login_required()
def vote(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return JsonResponse({'error': _(' • Question does not exist')})
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return JsonResponse({'error': _(' • You didn\'t select a choice')})
    else:
        results_url = reverse('polls:results', args=(question_id,))
        if question.vote_set.filter(user=request.user.id):
            return JsonResponse({'error': _(f' • You have already voted. <a href="{results_url}">Results</a>')})
        add_vote = question.vote_set.create(choice_id=request.POST['choice'],
                                            user=request.user.id)
        add_vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        return JsonResponse({'success': _(f' • Voting was successful. <a href="{results_url}">Results</a>')})


########################################################################################################################
################################################ PROCESSORS SECTION ####################################################
########################################################################################################################


# AJAX
def add_question_list_validation(request, element_name: str):
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
################################################ TESTING SECTION #######################################################
########################################################################################################################


# froala test form page
'''def froala_form(request):
    return render(request, 'polls/froala template.html', {
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
        return HttpResponseRedirect(reverse('polls:froala_index'))
    else:
        return render(request, 'polls/froala template.html', {
            'form': form
        })


# froala test list view
class FroalaIndexView(generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'

    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return FroalaModel.objects.all().order_by('-pub_date')


# froala test detail view
class FroalaDetailMixinView(generic.edit.FormMixin, generic.detail.DetailView):
    model = FroalaModel
    template_name = 'polls/polls_detail.html'''

# test0 ajax handler
'''class AjaxHandlerView(View):
    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            t = time()
            return JsonResponse({'seconds': t}, status=200)
        return render(request, 'polls/ajax_template.html')

    def post(self, request):
        card_text = request.POST.get('text')

        result = f'i\'ve got: {card_text}'
        return JsonResponse({'data': result}, status=200)'''

'''
# test1 ajax page
def ajax_page(request):
    return render(request, 'polls/ajax_page.html')


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

        return render(request, 'polls/ajax_page.html')
'''
