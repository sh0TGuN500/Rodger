from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required

from .forms import CommentForm, AddQuestionForm, text_validator
from .models import Question, Choice, Tag


########################################################################################################################
################################################ CORE SECTION ##########################################################
########################################################################################################################


def home(request):
    return render(request, 'polls/home_page.html')


@login_required()
def personal_page(request):
    return render(request, 'polls/personal_page.html')


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


class QuestionSearchView(generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'

    @login_required()
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
    my_question_list = Question.objects.filter(author_name=user).order_by('-pub_date')
    deleting_question = Question.objects.get(id=question_id)
    if user.username != deleting_question.author_name:
        error_message = 'U can delete only your questions'
    else:
        deleting_question.delete()
        error_message = f'Question "{deleting_question}" has been deleted'
    context = {
        'my_question_list': my_question_list,
        'error_message': error_message
    }
    return render(request, 'polls/polls_list.html', context=context)


class MyQuestionsView(generic.ListView):
    paginate_by = 16
    template_name = 'polls/polls_list.html'
    context_object_name = 'my_question_list'

    @login_required()
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
            return render(request, 'polls/add_question.html', {
                'title': question.question_title,
                'text': question.question_text,
                'choices': question.choice_set.all(),
                'question_id': question_id
            })
        else:
            return HttpResponseRedirect(reverse('polls:create_question'))
    else:
        return render(request, 'polls/add_question.html', {
            'form': AddQuestionForm
        })


# INJECT AJAX
@login_required()
def question_db_save(request, question_id=None):
    print(question_id)
    get_question = get_object_or_404(Question, id=question_id) if question_id else None
    print(get_question)
    # request validation
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    data = request.POST if request.POST else None
    if not data or not is_ajax or (get_question.author_name != request.user.username if get_question else False):
        return HttpResponseRedirect(reverse('polls:create_question'))
    # question data validation
    title = text_validator(data['question_title'])
    text = text_validator(data['question_text'])
    if title and text:
        # if question exist
        if get_question:
            get_question.question_title = title
            get_question.question_text = text
            get_question.up_date = timezone.now()
            get_question.choice_set.all().delete()
        else:
            get_question = Question(question_title=title,
                                    question_text=data['question_text'],
                                    author_name=request.user,
                                    pub_date=timezone.now())
        # save question in db
        try:
            get_question.save()
        except IntegrityError:
            # Error jsonRequest
            '''return render(request, 'polls/add_question.html', {
                            'error_message': f'Title "{title}" already exist'
                        })'''
            return JsonResponse({'error': f' • Title "{title}" already exist'})

        # tags data validation
        tag_list: list = add_question_list_validation(request, data, 'tag')
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
        # choices data validation
        choice_list: list = add_question_list_validation(request, data, 'choice')
        # save choices if exist
        if choice_list:
            for choice in choice_list:
                create_choice = Choice(question_id=get_question.id,
                                       choice_text=choice)
                create_choice.save()

        # Success jsonResponse
        # return HttpResponseRedirect(reverse('polls:detail', args=(get_question.id,)))
        return JsonResponse({'success': f' • Question "{get_question.question_title}" successfully posted',
                             'question': get_question.id})

    else:
        # Error jsonResponse
        '''return render(request, 'polls/add_question.html', {
            'error_message': 'You input invalid text'
        })'''
        return JsonResponse({'error': ' • You input invalid text'})


########################################################################################################################
################################################ COMMENT SECTION #######################################################
########################################################################################################################


# AJAX
class CommentCreate(View):
    @staticmethod
    @login_required()
    def get(*args, **kwargs):
        return HttpResponseRedirect(reverse('polls:home'))

    @staticmethod
    @login_required()
    def post(request, question):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            question = get_object_or_404(Question, id=question)
            form = CommentForm(request.POST)
            comment_text = text_validator(form['comment_text'].value())
            if form.is_valid() and len(comment_text) > 4:
                form = form.save(commit=False)
                form.question = question
                form.author_name = request.user
                form.save()
                return JsonResponse({'success': ' • Comment successful posted'})
                # return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
            else:
                '''print('error')
                return render(request, 'polls/polls_detail.html', {
                    'question': question,
                    'form': form
                })'''
                return JsonResponse({'error': ' • Symbols less than 3'})
        else:
            return HttpResponseRedirect(reverse('polls:home'))

########################################################################################################################
################################################ VOTE SECTION ##########################################################
########################################################################################################################


# ajax
class VoteResultView(generic.DetailView):
    model = Question
    template_name = 'polls/votes_results.html'


# ajax
@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/polls_detail.html', {
            'question': question,
            'form': CommentForm(),
            'error_message': 'You didn\'t select a choice'
        })
    else:
        if question.vote_set.filter(user=request.user.id):
            return render(request, 'polls/polls_detail.html', {
                'question': question,
                'form': CommentForm(),
                'error_message': 'You have already voted'
            })
        add_vote = question.vote_set.create(choice_id=request.POST['choice'],
                                            user=request.user.id)
        add_vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


########################################################################################################################
################################################ PROCESSORS SECTION ####################################################
########################################################################################################################


# AJAX
def add_question_list_validation(request, data, element_name: str):
    if data.get(element_name):
        request_list = dict(data.lists())[element_name]
        count = 0
        for element in request_list:
            text = text_validator(element)
            if text:
                request_list[count] = text
                count += 1
            else:
                # jsonResponse
                return render(request, 'polls/add_question.html', {
                    'error_message': 'You input invalid text'
                })
        return request_list
    else:
        return []


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
