from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from .forms import CommentForm, AddQuestionForm, text_validator
from .models import Question, Choice, Tag, Comment
from .tasks import send_task, admin_send_task


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
        error_message = 'Question does not exist'
    else:
        deleting_question.delete()
        error_message = f'Question "{deleting_question}" has been deleted'
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
            get_question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            get_question = Question(author_name=request.user)
        else:
            get_question.up_date = timezone.now()
    else:
        get_question = Question(author_name=request.user)
    user_ok = get_question.author_name == request.user.username if question_id else True

    # request validation
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    data = AddQuestionForm(request.POST, instance=get_question) if request.POST else None
    if not data or not is_ajax or not user_ok:
        return HttpResponseRedirect(reverse('polls:create_question'))

    # constants
    no_errors = True
    response_dict = {'title_info': ' • Title ✔️',
                     'text_info': ' • Text ✔️'}

    # title data validation
    title = data['question_title']
    if not get_question:
        try:
            Question.objects.get(question_title=title)
        except Question.DoesNotExist:
            pass
        else:
            response_dict.update({'title_info': f' • Title "{escape(title)}" already exist'})
            no_errors = False
    try:
        data.clean_question_title()
    except ValidationError:
        response_dict.update({'title_info': ' • Title should be the length between 5 and 200'})
        no_errors = False

    # text data validation
    try:
        data.clean_question_text()
    except ValidationError:
        response_dict.update({'text_info': ' • Text should be the length between 10 and 9000'})
        no_errors = False

    # tags data validation
    tag_list, tag_status = add_question_list_validation(request, 'tag')
    if tag_list:
        if 'error' in tag_status:
            response_dict.update({'tag_info': ' • Tag should be the length between 2 and 200'})
            no_errors = False
        else:
            response_dict.update({'tag_info': ' ✔️'})

    # choices data validation
    choice_list, choice_status = add_question_list_validation(request, 'choice')
    if choice_list:
        if 'error' in choice_status:
            response_dict.update({'choice_info': ' • Choice should be the length between 2 and 200'})
            no_errors = False
        else:
            response_dict.update({'choice_info': ' ✔️'})

    # save data into DB
    if no_errors:
        if question_id:
            get_question.choice_set.all().delete()
        try:
            data.save()
        except ValueError:
            return JsonResponse(response_dict)
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
                get_question.tag.add(add_tag)

        # save choices if exist
        if choice_list:
            for choice in choice_list:
                create_choice = Choice(question_id=get_question.id,
                                       choice_text=choice)
                create_choice.save()

        # Success jsonResponse
        # return HttpResponseRedirect(reverse('polls:detail', args=(get_question.id,)))
        question_url = reverse('polls:detail', args=(get_question.id,))
        # email_template = render(request, 'account/email/email_confirmation_message.txt')
        question_url_message = f' • Question "<a href="{question_url}">{escape(get_question.question_title)}</a>" successfully posted'
        admin_send_task.delay('New question',
                              question_url_message)
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
            return JsonResponse({'error': ' • Comment does not exist'})
        else:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'error': ' • Question does not exist'})
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
                return JsonResponse({'error': ' • Question does not exist'})
            if comment_id:
                try:
                    comment = Comment.objects.get(id=comment_id)
                except Comment.DoesNotExist:
                    return JsonResponse({'error': ' • Comment does not exist'})
                else:
                    form = CommentForm(request.POST, instance=comment)
                    if form.is_valid():
                        form.save()
                    else:
                        return JsonResponse({'error': ' • Symbols less than 3'})

            else:
                form = CommentForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.author_name = request.user
                    form.question = question
                    form.save()
                else:
                    return JsonResponse({'error': ' • Symbols less than 3'})
            user = User.objects.get(username=question.author_name)
            send_task.delay(
                f'New comment for {question.question_title}',
                f'''User {request.user.username} commented on your question!
                \nYou can\'t get rid of the mailing because I have not implemented it.''',
                user_email=user.email,
            )
            return JsonResponse({'success': ' • Comment successful posted'})
            # return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


@login_required()
def comment_delete(request, question_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, author_name=request.user)
    except Comment.DoesNotExist:
        comment_message = ' • Comment does not exist'
    else:
        comment.delete()
        comment_message = ' • Comment has been deleted'
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
        return JsonResponse({'error': ' • Question does not exist'})
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return JsonResponse({'error': ' • You didn\'t select a choice'})
    else:
        results_url = reverse('polls:results', args=(question_id,))
        if question.vote_set.filter(user=request.user.id):
            return JsonResponse({'error': f' • You have already voted. <a href="{results_url}">Results</a>'})
        add_vote = question.vote_set.create(choice_id=request.POST['choice'],
                                            user=request.user.id)
        add_vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        return JsonResponse({'success': f' • Voting was successful. <a href="{results_url}">Results</a>'})


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
