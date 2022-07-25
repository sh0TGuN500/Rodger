from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.base import View

from .forms import CommentForm, AddQuestionForm, text_validator
from .models import Question, Choice


class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'polls/polls_list.html'
    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return Question.objects.all().order_by('-pub_date')


class DetailMixinView(generic.edit.FormMixin, generic.detail.DetailView):
    model = Question
    template_name = 'polls/polls_detail.html'
    form_class = CommentForm

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/votes_results.html'


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
        add_vote = question.vote_set.create(question_id=question_id,
                                            choice_id=request.POST['choice'],
                                            user=request.user.id)
        add_vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


'''def search(request):
    valid_text = text_validator(request.POST['search'])
    if valid_text:
        latest_question_list = Question.objects.filter(question_title__icontains=valid_text)
        context = {'latest_question_list': latest_question_list}
    else:
        search_message = 'You input invalid text'
        context = {'search_message': search_message}
    return render(request, 'polls/polls_list.html', context=context)'''


class SearchView(generic.ListView):
    paginate_by = 10
    template_name = 'polls/polls_list.html'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        valid_search = self.request.GET['search']
        if valid_search:
            return Question.objects.filter(question_title__icontains=valid_search).order_by('-pub_date')
        else:
            return []


def delete_question(request, question_id):
    user = request.user
    if not user.is_authenticated:
        my_question_list = []
        error_message = '4 do this u must be '
    else:
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
    paginate_by = 10
    template_name = 'polls/polls_list.html'
    context_object_name = 'my_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        if self.request.user.is_authenticated:
            return Question.objects.filter(author_name=self.request.user).order_by('-pub_date')
        else:
            return []


def home(request):
    return render(request, 'polls/home_page.html')


def personal_page(request):
    if request.user.is_authenticated:
        return render(request, 'polls/personal_page.html')
    else:
        return HttpResponseRedirect(reverse('polls:home'))


def add_question(request, question_id=None):
    if request.user.is_authenticated:
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
                return HttpResponseRedirect(reverse('polls:add_question'))
        else:
            return render(request, 'polls/add_question.html', {
                'form': AddQuestionForm
            })
    else:
        return HttpResponseRedirect(reverse('polls:home'))


def leave_question(request, question_id=None):
    get_question = get_object_or_404(Question, id=question_id) if question_id else None
    data = request.POST if request.POST else None
    if not data or (get_question.author_name != request.user.username if get_question else False):
        return HttpResponseRedirect(reverse('polls:home'))
    form = AddQuestionForm if not question_id else None
    title = text_validator(data['question_title'])
    text = text_validator(data['question_text'])
    if title and text:
        if question_id:
            get_question.question_title = title
            get_question.question_text = text
            get_question.up_date = timezone.now()
            get_question.choice_set.all().delete()
        else:
            get_question = Question(question_title=title,
                                    question_text=text,
                                    author_name=request.user,
                                    pub_date=timezone.now())
        if data.get('choice'):
            choice_list = dict(data.lists())['choice']
            count = 0
            for choice in choice_list:
                if text_validator(choice):
                    choice_list[count] = text_validator(choice)
                    count += 1
                else:
                    return render(request, 'polls/add_question.html', {
                        'error_message': 'You input invalid text'
                    })
            try:
                get_question.save()
            except IntegrityError:
                return render(request, 'polls/add_question.html', {
                    'error_message': f'Title "{title}" already exist',
                    'form': form,
                })
            for choice in choice_list:
                create_choice = Choice(question_id=get_question.id,
                                       choice_text=choice)
                create_choice.save()
        else:
            try:
                get_question.save()
            except IntegrityError:
                return render(request, 'polls/add_question.html', {
                    'error_message': f'Title "{title}" already exist',
                    'form': form,
                })
        return HttpResponseRedirect(reverse('polls:detail', args=(get_question.id,)))

    else:
        return render(request, 'polls/add_question.html', {
            'error_message': 'You input invalid text',
            'form': form,
        })


class AddComment(View):
    def get(self, request, question):
        return HttpResponseRedirect(reverse('polls:home'))

    def post(self, request, question):
        question = get_object_or_404(Question, id=question)
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.question = question
            form.author_name = request.user
            form.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
        else:
            return render(request, 'polls/polls_detail.html', {
                'question': question,
                'form': form
            })
